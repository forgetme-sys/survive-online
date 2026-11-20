"use strict";

const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const { randomUUID } = require("node:crypto");
const { WebSocket, WebSocketServer } = require("ws");

const ROOT = __dirname;
const PORT = Number(process.env.PORT || 3000);
const MAX_PLAYERS = 32;
const MAX_WORLD_EDITS = 30000;
const MAX_CHAT_MESSAGES_PER_SECOND = 2;
const BLOCK_TYPES = new Set(["grass", "dirt", "stone", "wood", "sand", "planks", "torch", null]);
const players = new Map();
const worldEdits = new Map();

const server = http.createServer((request, response) => {
  const pathname = new URL(request.url, `http://${request.headers.host || "localhost"}`).pathname;
  const requested = pathname === "/" ? "index.html" : pathname.slice(1);
  if (requested !== "index.html") {
    response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
    response.end("Not found");
    return;
  }

  fs.readFile(path.join(ROOT, "index.html"), (error, content) => {
    if (error) {
      response.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" });
      response.end("Unable to read the game page");
      console.error("Failed to read index.html:", error);
      return;
    }
    response.writeHead(200, {
      "Content-Type": "text/html; charset=utf-8",
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff"
    });
    response.end(content);
  });
});

const sockets = new WebSocketServer({
  server,
  path: "/multiplayer",
  maxPayload: 4096,
  perMessageDeflate: false
});

function send(socket, message) {
  if (socket.readyState === WebSocket.OPEN) socket.send(JSON.stringify(message));
}

function broadcast(message, exceptId) {
  const serialized = JSON.stringify(message);
  for (const peer of sockets.clients) {
    if (peer.playerId === exceptId || peer.readyState !== WebSocket.OPEN || !peer.player) continue;
    peer.send(serialized);
  }
}

function cleanName(value) {
  if (typeof value !== "string") return "Explorateur";
  const name = value.replace(/[\u0000-\u001f\u007f<>]/g, "").trim().slice(0, 18);
  return name || "Explorateur";
}

function validCoordinate(value) {
  return Number.isInteger(value) && Math.abs(value) <= 1_000_000;
}

sockets.on("connection", (socket) => {
  if (players.size >= MAX_PLAYERS) {
    send(socket, { type: "error", message: "Le serveur est complet." });
    socket.close(1013, "Server full");
    return;
  }

  const id = randomUUID();
  socket.playerId = id;
  socket.lastMoveAt = 0;
  socket.chatTimes = [];

  socket.on("message", (data) => {
    let message;
    try {
      message = JSON.parse(data.toString());
    } catch {
      send(socket, { type: "error", message: "Message invalide." });
      return;
    }
    if (!message || typeof message !== "object" || typeof message.type !== "string") return;

    if (message.type === "join" && !socket.player) {
      const player = {
        id,
        name: cleanName(message.name),
        x: validCoordinate(Math.round(message.x)) ? Math.max(-1_000_000, Math.min(1_000_000, message.x)) : 0,
        y: validCoordinate(Math.round(message.y)) ? Math.max(0, Math.min(1_000_000, message.y)) : 0,
        facing: message.facing === -1 ? -1 : 1
      };
      socket.player = player;
      players.set(id, player);
      send(socket, {
        type: "welcome",
        id,
        players: [...players.values()],
        blocks: [...worldEdits.entries()].slice(-MAX_WORLD_EDITS)
      });
      broadcast({ type: "player-joined", player }, id);
      broadcast({ type: "system", text: `${player.name} a rejoint le monde.` }, id);
      return;
    }

    if (!socket.player) return;

    if (message.type === "move") {
      const now = Date.now();
      if (now - socket.lastMoveAt < 40) return;
      if (!Number.isFinite(message.x) || !Number.isFinite(message.y)
        || Math.abs(message.x) > 1_000_000 || message.y < 0 || message.y > 1_000_000) return;
      socket.lastMoveAt = now;
      socket.player.x = message.x;
      socket.player.y = message.y;
      socket.player.facing = message.facing === -1 ? -1 : 1;
      broadcast({ type: "move", player: socket.player }, id);
      return;
    }

    if (message.type === "chat") {
      const now = Date.now();
      socket.chatTimes = socket.chatTimes.filter((timestamp) => now - timestamp < 1000);
      if (socket.chatTimes.length >= MAX_CHAT_MESSAGES_PER_SECOND) return;
      if (typeof message.text !== "string") return;
      const text = message.text.replace(/[\u0000-\u001f\u007f]/g, "").trim().slice(0, 240);
      if (!text) return;
      socket.chatTimes.push(now);
      broadcast({ type: "chat", id, name: socket.player.name, text, at: now });
      return;
    }

    if (message.type === "block") {
      const { x, y, block } = message;
      if (!validCoordinate(x) || !Number.isInteger(y) || y < 0 || y > 512 || !BLOCK_TYPES.has(block)) return;
      const key = `${x},${y}`;
      if (!worldEdits.has(key) && worldEdits.size >= MAX_WORLD_EDITS) {
        send(socket, { type: "error", message: "Le monde a atteint sa limite de modifications." });
        return;
      }
      worldEdits.set(key, block);
      broadcast({ type: "block", x, y, block }, id);
    }
  });

  socket.on("close", () => {
    const player = players.get(id);
    if (!player) return;
    players.delete(id);
    broadcast({ type: "player-left", id });
    broadcast({ type: "system", text: `${player.name} a quitté le monde.` });
  });
  socket.on("error", (error) => console.warn("WebSocket client error:", error.message));
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`Terra 2D multijoueur disponible sur http://localhost:${PORT}`);
});
