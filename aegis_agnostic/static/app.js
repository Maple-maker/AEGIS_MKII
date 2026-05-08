const generateBtn = document.getElementById("generateBtn");
const speakBtn = document.getElementById("speakBtn");
const stopBtn = document.getElementById("stopBtn");
const copyBtn = document.getElementById("copyBtn");
const notesEl = document.getElementById("notes");
const briefEl = document.getElementById("brief");
const providerEl = document.getElementById("provider");
const briefingTypeEl = document.getElementById("briefingType");
const metaEl = document.getElementById("meta");

let latestBrief = "";

function setLoading(isLoading) {
  generateBtn.disabled = isLoading;
  generateBtn.textContent = isLoading ? "Generating..." : "Generate Brief";
}

async function generateBrief() {
  const notes = notesEl.value.trim();
  const provider = providerEl.value;
  const briefing_type = briefingTypeEl.value;

  if (!notes) {
    briefEl.textContent = "Enter notes first.";
    return;
  }

  setLoading(true);
  briefEl.textContent = "AEGIS is thinking...";
  metaEl.textContent = "";

  try {
    const response = await fetch("/api/brief", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ notes, provider, briefing_type }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unknown error");
    }

    latestBrief = data.brief;
    briefEl.textContent = data.brief;
    metaEl.textContent = `${data.provider} · ${data.model} · ${data.briefing_type}`;

    speakBtn.disabled = false;
    copyBtn.disabled = false;
  } catch (error) {
    latestBrief = "";
    briefEl.textContent = `Error: ${error.message}`;
    speakBtn.disabled = true;
    copyBtn.disabled = true;
  } finally {
    setLoading(false);
  }
}

function speakBrief() {
  if (!latestBrief || !("speechSynthesis" in window)) return;

  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(latestBrief);
  utterance.rate = 0.95;
  utterance.pitch = 1;
  utterance.volume = 1;

  window.speechSynthesis.speak(utterance);
  stopBtn.disabled = false;
}

function stopSpeech() {
  window.speechSynthesis.cancel();
  stopBtn.disabled = true;
}

async function copyBrief() {
  if (!latestBrief) return;
  await navigator.clipboard.writeText(latestBrief);
  copyBtn.textContent = "Copied";
  setTimeout(() => {
    copyBtn.textContent = "Copy";
  }, 1200);
}

generateBtn.addEventListener("click", generateBrief);
speakBtn.addEventListener("click", speakBrief);
stopBtn.addEventListener("click", stopSpeech);
copyBtn.addEventListener("click", copyBrief);
