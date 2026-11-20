import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const projectDirectory = resolve(fileURLToPath(new URL(".", import.meta.url)));
const port = Number(process.env.PORT || 3000);
const apiKey = process.env.GEMINI_API_KEY;
const model = process.env.GEMINI_MODEL || "gemini-2.5-flash";
const maxBodyBytes = 24_000;
const allowedFiles = new Set(["index.html", "styles.css", "script.js"]);
const mimeTypes = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
};

function sendJson(response, statusCode, body) {
  response.writeHead(statusCode, {
    "Cache-Control": "no-store",
    "Content-Type": "application/json; charset=utf-8",
    "X-Content-Type-Options": "nosniff",
  });
  response.end(JSON.stringify(body));
}

async function readJsonBody(request) {
  const chunks = [];
  let bytes = 0;
  for await (const chunk of request) {
    bytes += chunk.length;
    if (bytes > maxBodyBytes) {
      const error = new Error("La demande et le code sont trop longs.");
      error.statusCode = 413;
      throw error;
    }
    chunks.push(chunk);
  }
  try {
    return JSON.parse(Buffer.concat(chunks).toString("utf8"));
  } catch {
    const error = new Error("La demande reçue n’est pas valide.");
    error.statusCode = 400;
    throw error;
  }
}

async function askGemini(input) {
  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-goog-api-key": apiKey,
      },
      body: JSON.stringify({
        systemInstruction: {
          parts: [{
            text: [
              "Tu es un assistant de programmation pédagogique qui répond en français.",
              "Aide à créer ou modifier de petits projets HTML, CSS et JavaScript.",
              "Retourne uniquement un objet JSON avec les clés reply, html, css et javascript, toutes en texte.",
              "reply explique brièvement ce que tu as fait et comment l'essayer.",
              "html, css et javascript doivent contenir les fichiers complets prêts à remplacer les éditeurs.",
              "Respecte la demande et conserve le code existant autant que possible.",
              "Si la demande ne nécessite pas de changement de code, laisse les trois fichiers exactement comme ils sont et réponds dans reply.",
              "N'inclus pas de balises Markdown autour du JSON."
            ].join(" "),
          }],
        },
        contents: [{
          role: "user",
          parts: [{
            text: [
              `Demande : ${input.prompt}`,
              "Code HTML actuel :",
              input.html,
              "Code CSS actuel :",
              input.css,
              "Code JavaScript actuel :",
              input.javascript,
            ].join("\n\n"),
          }],
        }],
        generationConfig: {
          responseMimeType: "application/json",
          responseSchema: {
            type: "OBJECT",
            properties: {
              reply: { type: "STRING" },
              html: { type: "STRING" },
              css: { type: "STRING" },
              javascript: { type: "STRING" },
            },
            required: ["reply", "html", "css", "javascript"],
          },
        },
      }),
      signal: AbortSignal.timeout(60_000),
    },
  );

  if (!response.ok) {
    console.error(`Le service IA a répondu avec le statut HTTP ${response.status}.`);
    throw new Error(
      response.status === 400 || response.status === 403
        ? "Le service IA a refusé la demande. Vérifie ta clé API et son accès au modèle."
        : `Le service IA est momentanément indisponible (HTTP ${response.status}).`,
    );
  }

  const result = await response.json();
  const text = result.candidates?.[0]?.content?.parts
    ?.map((part) => part.text || "")
    .join("");
  if (!text) throw new Error("L’assistant IA n’a pas renvoyé de réponse.");

  let answer;
  try {
    answer = JSON.parse(text);
  } catch {
    throw new Error("La réponse de l’assistant IA n’a pas pu être lue.");
  }

  for (const key of ["reply", "html", "css", "javascript"]) {
    if (typeof answer[key] !== "string") {
      throw new Error("La réponse de l’assistant IA est incomplète.");
    }
  }
  return answer;
}

const server = createServer(async (request, response) => {
  response.setHeader("X-Content-Type-Options", "nosniff");
  response.setHeader("Referrer-Policy", "no-referrer");

  const url = new URL(request.url, "http://127.0.0.1");
  if (url.pathname === "/api/assistant") {
    if (request.method !== "POST") {
      sendJson(response, 405, { error: "Utilise une demande POST pour contacter l’assistant." });
      return;
    }
    if (!apiKey) {
      sendJson(response, 503, {
        error: "L’assistant IA n’est pas configuré. Ajoute GEMINI_API_KEY dans le fichier .env puis redémarre le serveur.",
      });
      return;
    }

    try {
      const input = await readJsonBody(request);
      if (
        !input ||
        typeof input.prompt !== "string" ||
        !input.prompt.trim() ||
        input.prompt.length > 2000 ||
        !["html", "css", "javascript"].every(
          (key) => typeof input[key] === "string" && input[key].length <= 6000,
        )
      ) {
        sendJson(response, 400, { error: "La demande ou le code est vide ou trop long." });
        return;
      }

      sendJson(response, 200, await askGemini({
        prompt: input.prompt.trim(),
        html: input.html,
        css: input.css,
        javascript: input.javascript,
      }));
    } catch (error) {
      const status = error.statusCode || 502;
      if (status === 502) console.error("Échec de la requête à l’assistant IA.", error);
      sendJson(response, status, { error: error.message || "Impossible de contacter l’assistant IA." });
    }
    return;
  }

  if (request.method !== "GET" && request.method !== "HEAD") {
    response.writeHead(405);
    response.end();
    return;
  }

  const requestedFile = url.pathname === "/" ? "index.html" : decodeURIComponent(url.pathname.slice(1));
  if (!allowedFiles.has(requestedFile)) {
    response.writeHead(404);
    response.end("Page introuvable.");
    return;
  }

  try {
    const filePath = resolve(projectDirectory, requestedFile);
    if (!filePath.startsWith(`${projectDirectory}${sep}`)) {
      response.writeHead(404);
      response.end("Page introuvable.");
      return;
    }
    const content = await readFile(filePath);
    response.writeHead(200, {
      "Cache-Control": "no-store",
      "Content-Type": mimeTypes[extname(filePath)],
    });
    response.end(request.method === "HEAD" ? undefined : content);
  } catch (error) {
    if (error.code === "ENOENT") {
      response.writeHead(404);
      response.end("Page introuvable.");
      return;
    }
    console.error("Impossible de lire un fichier du site.", error);
    response.writeHead(500);
    response.end("Erreur interne du serveur.");
  }
});

server.listen(port, "127.0.0.1", () => {
  console.log(`Scratch est prêt : http://127.0.0.1:${port}`);
  if (!apiKey) console.log("Configure GEMINI_API_KEY dans .env pour activer l’assistant IA.");
});
