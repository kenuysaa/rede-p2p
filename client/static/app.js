const messages = document.getElementById("messages");
const filesBody = document.getElementById("filesBody");
const peerList = document.getElementById("peerList");
const downloadFileSelect = document.getElementById("downloadFileSelect");
const downloadIpInput = document.getElementById("downloadIp");
const downloadPortInput = document.getElementById("downloadPort");
const downloadHashInput = document.getElementById("downloadHash");
const downloadFilenameInput = document.getElementById("downloadFilename");

let currentFiles = [];

function log(message) {
  const ts = new Date().toLocaleTimeString();
  messages.textContent += `[${ts}] ${message}\n`;
  messages.scrollTop = messages.scrollHeight;
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.message || "Falha na requisicao.");
  }
  return data;
}

function renderFiles(files) {
  currentFiles = Array.isArray(files) ? files : [];
  filesBody.innerHTML = "";
  for (const file of currentFiles) {
    const row = document.createElement("tr");
    row.addEventListener("click", () => applySelectedFile(file.hash));
    row.innerHTML = `
      <td>${file.name || "-"}</td>
      <td>${file.discipline || "-"}</td>
      <td>${file.author || "-"}</td>
      <td>${file.type || "-"}</td>
      <td>${file.hash || "-"}</td>
    `;
    filesBody.appendChild(row);
  }
  renderDownloadFileOptions(currentFiles);
}

function renderPeers(peers) {
  peerList.innerHTML = "";
  for (const peer of peers) {
    const item = document.createElement("li");
    item.textContent = `${peer.ip}:${peer.port} | reputacao: ${Number(peer.score).toFixed(4)}`;
    peerList.appendChild(item);
  }
}

function renderDownloadFileOptions(files) {
  downloadFileSelect.innerHTML = '<option value="">Selecione um arquivo da lista</option>';
  for (const file of files) {
    const option = document.createElement("option");
    option.value = file.hash || "";
    option.textContent = `${file.name || "-"} (${file.discipline || "-"})`;
    downloadFileSelect.appendChild(option);
  }
}

function applySelectedFile(fileHash) {
  if (!fileHash) {
    return;
  }
  const selected = currentFiles.find((file) => file.hash === fileHash);
  if (!selected) {
    return;
  }

  downloadFileSelect.value = selected.hash || "";
  downloadHashInput.value = selected.hash || "";
  downloadFilenameInput.value = selected.name || "";
}

async function suggestPeerForHash(fileHash) {
  if (!fileHash) {
    return;
  }

  try {
    const data = await requestJson(`/api/lookup/${encodeURIComponent(fileHash)}`);
    renderPeers(data.peers);
    if (data.peers && data.peers.length > 0) {
      downloadIpInput.value = data.peers[0].ip || "";
      downloadPortInput.value = String(data.peers[0].port || "");
      log(`Peer sugerido para download: ${data.peers[0].ip}:${data.peers[0].port}`);
    }
  } catch (error) {
    log(`Nao foi possivel sugerir peer: ${error.message}`);
  }
}

document.getElementById("btnRegister").addEventListener("click", async () => {
  try {
    const data = await requestJson("/api/register", { method: "POST" });
    log(data.message);
  } catch (error) {
    log(`Erro ao registrar: ${error.message}`);
  }
});

document.getElementById("btnList").addEventListener("click", async () => {
  try {
    const data = await requestJson("/api/files");
    renderFiles(data.files);
    log(`Lista atualizada: ${data.files.length} arquivo(s).`);
  } catch (error) {
    log(`Erro ao listar arquivos: ${error.message}`);
  }
});

document.getElementById("btnLookup").addEventListener("click", async () => {
  const hash = document.getElementById("lookupHash").value.trim();
  if (!hash) {
    log("Informe um hash para buscar peers.");
    return;
  }

  try {
    const data = await requestJson(`/api/lookup/${encodeURIComponent(hash)}`);
    renderPeers(data.peers);
    log(`Peers encontrados: ${data.peers.length}.`);
  } catch (error) {
    peerList.innerHTML = "";
    log(`Erro no lookup: ${error.message}`);
  }
});

downloadFileSelect.addEventListener("change", async (event) => {
  const selectedHash = event.target.value;
  applySelectedFile(selectedHash);
  if (selectedHash) {
    await suggestPeerForHash(selectedHash);
  }
});

document.getElementById("btnDownload").addEventListener("click", async () => {
  const peer_ip = downloadIpInput.value.trim();
  const file_hash = downloadHashInput.value.trim();
  const filename = downloadFilenameInput.value.trim();
  const peer_port_input = downloadPortInput.value.trim();

  if (!peer_ip || !file_hash || !filename) {
    log("Preencha IP, hash e nome do arquivo para download.");
    return;
  }

  const body = { peer_ip, file_hash, filename };
  if (peer_port_input) {
    body.peer_port = Number(peer_port_input);
  }

  try {
    const data = await requestJson("/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    log(data.message);
  } catch (error) {
    log(`Erro no download: ${error.message}`);
  }
});

async function loadStatus() {
  try {
    const data = await requestJson("/api/status");
    document.getElementById("myIp").textContent = data.my_ip;
  } catch (error) {
    document.getElementById("myIp").textContent = "nao disponivel";
  }
}

loadStatus();
