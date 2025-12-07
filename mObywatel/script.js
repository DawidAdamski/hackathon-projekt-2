// Configuration
const CONFIG = {
  API_BASE_URL: "http://127.0.0.1:8000",
  API_ENDPOINT: "/verify/scan",
  MOBYWATEL_INFO: "mObywatel-mock-v1.0",
};

// DOM Elements
const elements = {
  nonceInput: document.getElementById("nonce-input"),
  verifyBtn: document.getElementById("verify-btn"),
  resultSection: document.getElementById("result-section"),
  statusIndicator: document.getElementById("status-indicator"),
  resultDetails: document.getElementById("result-details"),
  tokenDisplay: document.getElementById("token-value"),
  copyBtn: document.getElementById("copy-btn"),
  loadingOverlay: document.getElementById("loading-overlay"),
};

// State
let currentToken = null;

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
  updateTokenDisplay();
});

// Event Listeners Setup
function setupEventListeners() {
  elements.verifyBtn.addEventListener("click", handleVerify);
  elements.nonceInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      handleVerify();
    }
  });
  elements.copyBtn.addEventListener("click", handleCopyToken);

  // Update token display when input changes
  elements.nonceInput.addEventListener("input", (e) => {
    currentToken = e.target.value.trim();
    updateTokenDisplay();
  });
}

// Handle Verify Button Click
async function handleVerify() {
  const nonce = elements.nonceInput.value.trim();

  if (!nonce) {
    showError("Proszę wprowadzić kod nonce");
    return;
  }

  currentToken = nonce;
  updateTokenDisplay();

  // Show loading
  showLoading(true);
  hideResult();

  try {
    const response = await sendVerificationRequest(nonce);
    handleVerificationResponse(response);
  } catch (error) {
    handleVerificationError(error);
  } finally {
    showLoading(false);
  }
}

// Send Verification Request
async function sendVerificationRequest(nonce) {
  const url = `${CONFIG.API_BASE_URL}${CONFIG.API_ENDPOINT}`;

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      nonce: nonce,
      mobywatel: CONFIG.MOBYWATEL_INFO,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP Error: ${response.status}`);
  }

  return await response.json();
}

// Handle Verification Response
function handleVerificationResponse(data) {
  const { status, details, origin } = data;

  // Show result section
  showResult();

  // Update status indicator
  if (status === "trusted" || status === "verified") {
    showSuccessStatus(details, origin);
  } else if (status === "untrusted" || status === "failed") {
    showErrorStatus(details, origin);
  } else {
    showPendingStatus(details, origin);
  }
}

// Handle Verification Error
function handleVerificationError(error) {
  console.error("Verification error:", error);

  showResult();
  showErrorStatus(
    "Weryfikacja nie powiodła się",
    error.message || "Nieznany błąd",
  );
}

// Show Success Status
function showSuccessStatus(details, origin) {
  elements.statusIndicator.className = "status-indicator success";
  elements.statusIndicator.textContent = "✓";

  elements.resultDetails.innerHTML = `
        <h3>Weryfikacja zakończona pomyślnie</h3>
        <p><strong>Status:</strong> Strona jest zaufana</p>
        ${origin ? `<p><strong>Domena:</strong> <span class="domain">${escapeHtml(origin)}</span></p>` : ""}
        ${details ? `<p><strong>Szczegóły:</strong> ${escapeHtml(details)}</p>` : ""}
    `;
}

// Show Error Status
function showErrorStatus(details, origin) {
  elements.statusIndicator.className = "status-indicator error";
  elements.statusIndicator.textContent = "✗";

  elements.resultDetails.innerHTML = `
        <h3>Weryfikacja nie powiodła się</h3>
        <p class="error-message">⚠️ Uwaga! Ta strona nie przeszła weryfikacji.</p>
        ${origin ? `<p><strong>Domena:</strong> <span class="domain">${escapeHtml(origin)}</span></p>` : ""}
        ${details ? `<p><strong>Szczegóły:</strong> ${escapeHtml(details)}</p>` : ""}
        <p class="error-message">Przerwij korzystanie i zgłoś podejrzenie oszustwa.</p>
    `;
}

// Show Pending Status
function showPendingStatus(details, origin) {
  elements.statusIndicator.className = "status-indicator pending";
  elements.statusIndicator.textContent = "⏳";

  elements.resultDetails.innerHTML = `
        <h3>Weryfikacja w toku</h3>
        ${details ? `<p>${escapeHtml(details)}</p>` : "<p>Oczekiwanie na wynik...</p>"}
    `;
}

// Show Error Message
function showError(message) {
  alert(message);
}

// Show/Hide Result
function showResult() {
  elements.resultSection.classList.remove("hidden");
}

function hideResult() {
  elements.resultSection.classList.add("hidden");
}

// Show/Hide Loading
function showLoading(show) {
  if (show) {
    elements.loadingOverlay.classList.remove("hidden");
    elements.verifyBtn.disabled = true;
  } else {
    elements.loadingOverlay.classList.add("hidden");
    elements.verifyBtn.disabled = false;
  }
}

// Update Token Display
function updateTokenDisplay() {
  elements.tokenDisplay.textContent = currentToken || "-";
}

// Handle Copy Token
function handleCopyToken() {
  if (!currentToken) {
    return;
  }

  navigator.clipboard
    .writeText(currentToken)
    .then(() => {
      // Visual feedback
      const originalText = elements.copyBtn.textContent;
      elements.copyBtn.textContent = "✓";
      elements.copyBtn.style.color = "#28a745";

      setTimeout(() => {
        elements.copyBtn.textContent = originalText;
        elements.copyBtn.style.color = "";
      }, 1000);
    })
    .catch((err) => {
      console.error("Failed to copy:", err);
      // Fallback for older browsers
      const textArea = document.createElement("textarea");
      textArea.value = currentToken;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand("copy");
      document.body.removeChild(textArea);
    });
}

// Utility: Escape HTML
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
