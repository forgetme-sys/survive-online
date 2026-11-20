const button = document.getElementById('actionButton');
const creationArea = document.getElementById('creationArea');
const projectForm = document.getElementById('projectForm');
const projectName = document.getElementById('projectName');
const projectDescription = document.getElementById('projectDescription');
const message = document.getElementById('message');
const projectsSection = document.getElementById('projectsSection');
const projectsList = document.getElementById('projectsList');
const workspace = document.getElementById('workspace');
const workspaceTitle = document.getElementById('workspaceTitle');
const workspaceMessage = document.getElementById('workspaceMessage');
const htmlCode = document.getElementById('htmlCode');
const cssCode = document.getElementById('cssCode');
const jsCode = document.getElementById('jsCode');
const preview = document.getElementById('preview');
const aiForm = document.getElementById('aiForm');
const aiPrompt = document.getElementById('aiPrompt');
const aiSubmit = document.getElementById('aiSubmit');
const aiStatus = document.getElementById('aiStatus');

const starterCode = {
  html: '<h1>Bonjour !</h1>\n<p>Modifie ce code pour créer ta page.</p>\n<button id="helloButton">Clique ici</button>',
  css: 'body {\n  font-family: Arial, sans-serif;\n  padding: 24px;\n  color: #1f2937;\n}\n\nbutton {\n  padding: 10px 16px;\n  background: #4f46e5;\n  color: white;\n  border: 0;\n  border-radius: 8px;\n  cursor: pointer;\n}',
  js: "document.getElementById('helloButton').addEventListener('click', () => {\n  alert('Bravo, ton JavaScript fonctionne !');\n});"
};

let projects = [];
let activeProjectId = null;

function showProjects() {
  workspace.hidden = true;
  projectsSection.hidden = projects.length === 0;
  document.querySelector('.container > section:first-child').hidden = false;
  creationArea.hidden = true;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function saveProjects() {
  try {
    localStorage.setItem('scratch-projects', JSON.stringify(projects));
    return true;
  } catch (error) {
    const target = workspace.hidden ? message : workspaceMessage;
    target.textContent = `Impossible d'enregistrer les projets : ${error.message}`;
    return false;
  }
}

function renderProjects() {
  projectsList.replaceChildren();
  for (const project of projects) {
    const card = document.createElement('article');
    card.className = 'project-card';

    const openButton = document.createElement('button');
    openButton.className = 'project-open-button';
    openButton.type = 'button';
    openButton.dataset.projectId = project.id;
    openButton.setAttribute('aria-label', `Ouvrir ${project.name}`);

    const title = document.createElement('h3');
    title.textContent = project.name;
    openButton.prepend(title);
    card.append(openButton);

    if (project.description) {
      const detail = document.createElement('p');
      detail.textContent = project.description;
      card.append(detail);
    }
    projectsList.append(card);
  }
  projectsSection.hidden = projects.length === 0;
}

function runProject() {
  const project = projects.find((item) => item.id === activeProjectId);
  if (!project) {
    workspaceMessage.textContent = 'Projet introuvable. Retourne à la liste et ouvre un projet.';
    return false;
  }

  project.html = htmlCode.value;
  project.css = cssCode.value;
  project.js = jsCode.value;

  const safeCss = project.css.replace(/<\/style/gi, '<\\/style');
  const safeJs = project.js.replace(/<\/script/gi, '<\\/script');
  preview.srcdoc = `<!doctype html><html><head><meta charset="utf-8"><style>${safeCss}</style></head><body>${project.html}<script>${safeJs}<\/script></body></html>`;
  if (saveProjects()) {
    workspaceMessage.textContent = 'Code enregistré et aperçu actualisé.';
    return true;
  }
  return false;
}

function openProject(projectId) {
  const project = projects.find((item) => item.id === projectId);
  if (!project) return;

  activeProjectId = project.id;
  workspaceTitle.textContent = project.name;
  htmlCode.value = project.html;
  cssCode.value = project.css;
  jsCode.value = project.js;
  document.querySelector('.container > section:first-child').hidden = true;
  creationArea.hidden = true;
  projectsSection.hidden = true;
  workspace.hidden = false;
  if (runProject()) {
    workspaceMessage.textContent = 'Modifie le code puis clique sur « Enregistrer et exécuter ».';
  }
  workspace.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

try {
  const savedProjects = localStorage.getItem('scratch-projects');
  if (savedProjects) {
    const parsedProjects = JSON.parse(savedProjects);
    if (Array.isArray(parsedProjects)) projects = parsedProjects;
  }
} catch (error) {
  message.textContent = `Impossible de charger les projets enregistrés : ${error.message}`;
}
renderProjects();

button.addEventListener('click', () => {
  creationArea.hidden = false;
  projectName.focus();
  creationArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
});

projectForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const name = projectName.value.trim();
  if (!name) {
    projectName.focus();
    return;
  }

  const project = {
    id: crypto.randomUUID(),
    name,
    description: projectDescription.value.trim(),
    ...starterCode
  };
  projects.unshift(project);
  renderProjects();
  const saved = saveProjects();
  projectForm.reset();
  if (saved) message.textContent = 'Ton projet a été créé !';
});

projectsList.addEventListener('click', (event) => {
  const openButton = event.target.closest('.project-open-button');
  if (openButton) openProject(openButton.dataset.projectId);
});

document.getElementById('backButton').addEventListener('click', showProjects);
document.getElementById('runButton').addEventListener('click', runProject);

aiForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const prompt = aiPrompt.value.trim();
  if (!prompt) {
    aiPrompt.focus();
    return;
  }

  aiSubmit.disabled = true;
  aiStatus.textContent = 'L’assistant réfléchit…';
  try {
    const response = await fetch('/api/assistant', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt,
        html: htmlCode.value,
        css: cssCode.value,
        javascript: jsCode.value
      })
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || `Erreur du serveur (${response.status}).`);
    }
    if (
      typeof result.reply !== 'string' ||
      typeof result.html !== 'string' ||
      typeof result.css !== 'string' ||
      typeof result.javascript !== 'string'
    ) {
      throw new Error('La réponse de l’assistant est incomplète.');
    }

    htmlCode.value = result.html;
    cssCode.value = result.css;
    jsCode.value = result.javascript;
    if (runProject()) {
      aiStatus.textContent = result.reply;
      aiPrompt.value = '';
    } else {
      aiStatus.textContent = workspaceMessage.textContent;
    }
  } catch (error) {
    aiStatus.textContent = `L’assistant n’a pas pu répondre : ${error.message}`;
  } finally {
    aiSubmit.disabled = false;
  }
});
