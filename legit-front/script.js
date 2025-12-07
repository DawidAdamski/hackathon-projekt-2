window.addEventListener("load", () => {
  const root = document.getElementById("moby-verify");
  if (!root) return;

  const btn = document.getElementById("moby-verify-btn");
  const modal = document.getElementById("verification-modal");
  const modalCloseBtn = document.getElementById("modal-close-btn");
  const modalQrContainer = document.getElementById("modal-qr-container");
  const modalTokenContainer = document.getElementById("modal-token-container");
  const modalStatus = document.getElementById("modal-status");

  const API_URL = root.dataset.apiUrl || ""; // empty = same origin
  const SERVICE_ID = root.dataset.serviceId || "UNKNOWN";

  let currentPollInterval = null;
  let currentNonce = null;

  // Open modal function
  function openModal() {
    modal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
  }

  // Close modal function
  function closeModal() {
    modal.classList.add("hidden");
    document.body.style.overflow = "";

    // Stop polling when modal is closed
    if (currentPollInterval) {
      clearInterval(currentPollInterval);
      currentPollInterval = null;
    }

    // Reset button
    btn.disabled = false;
    currentNonce = null;
  }

  // Close modal handlers
  modalCloseBtn.addEventListener("click", closeModal);
  modal.addEventListener("click", (e) => {
    if (e.target === modal || e.target.classList.contains("modal-overlay")) {
      closeModal();
    }
  });

  // Escape key to close modal
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !modal.classList.contains("hidden")) {
      closeModal();
    }
  });

  btn.addEventListener("click", async () => {
    btn.disabled = true;

    // Clear previous content
    modalQrContainer.innerHTML = "";
    modalTokenContainer.innerHTML = "";
    modalStatus.innerHTML = "";
    modalStatus.className = "modal-status";

    // Show loading state
    modalStatus.innerHTML =
      '<div class="status-loading">Generuję sesję weryfikacyjną...</div>';
    openModal();

    try {
      const res = await fetch(`${API_URL}/verify/session`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: window.location.href,
          service_id: SERVICE_ID,
        }),
      });

      if (!res.ok) {
        let errorMessage = `Błąd HTTP: ${res.status}`;
        if (res.status === 502) {
          errorMessage = "Nie można połączyć się z serwerem weryfikacji. Sprawdź czy backend jest uruchomiony.";
        } else if (res.status === 503) {
          errorMessage = "Serwer weryfikacji jest tymczasowo niedostępny.";
        } else if (res.status === 404) {
          errorMessage = "Endpoint weryfikacji nie został znaleziony.";
        }
        throw new Error(errorMessage);
      }

      const data = await res.json();
      currentNonce = data.nonce;

      // Create QR code
      const qrContainer = document.createElement("div");
      qrContainer.className = "qr-code-wrapper";
      new QRCode(qrContainer, {
        text: data.qr_payload,
        width: 200,
        height: 200,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H,
      });

      const qrLabel = document.createElement("div");
      qrLabel.className = "qr-label";
      qrLabel.textContent = "Zeskanuj ten kod aplikacją mObywatel";

      modalQrContainer.appendChild(qrContainer);
      modalQrContainer.appendChild(qrLabel);

      // Create token display
      const tokenWrapper = document.createElement("div");
      tokenWrapper.className = "token-wrapper";

      const tokenLabel = document.createElement("div");
      tokenLabel.className = "token-label";
      tokenLabel.textContent = "Token (do skopiowania):";

      const tokenValueContainer = document.createElement("div");
      tokenValueContainer.className = "token-value-container";

      const tokenValue = document.createElement("div");
      tokenValue.className = "token-value";
      tokenValue.textContent = data.nonce;

      const copyBtn = document.createElement("button");
      copyBtn.className = "copy-btn";
      copyBtn.textContent = "📋 Kopiuj";
      copyBtn.onclick = () => {
        navigator.clipboard
          .writeText(data.nonce)
          .then(() => {
            copyBtn.textContent = "✓ Skopiowano!";
            copyBtn.classList.add("copied");
            setTimeout(() => {
              copyBtn.textContent = "📋 Kopiuj";
              copyBtn.classList.remove("copied");
            }, 2000);
          })
          .catch(() => {
            // Fallback
            const textArea = document.createElement("textarea");
            textArea.value = data.nonce;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand("copy");
            document.body.removeChild(textArea);
            copyBtn.textContent = "✓ Skopiowano!";
            setTimeout(() => {
              copyBtn.textContent = "📋 Kopiuj";
            }, 2000);
          });
      };

      tokenValueContainer.appendChild(tokenValue);
      tokenValueContainer.appendChild(copyBtn);
      tokenWrapper.appendChild(tokenLabel);
      tokenWrapper.appendChild(tokenValueContainer);
      modalTokenContainer.appendChild(tokenWrapper);

      // Update status
      modalStatus.innerHTML =
        '<div class="status-waiting">Oczekiwanie na zeskanowanie kodu QR...</div>';

      // Start polling
      if (currentPollInterval) {
        clearInterval(currentPollInterval);
      }
      currentPollInterval = startPolling(API_URL, data.nonce, modalStatus);
    } catch (err) {
      console.error(err);
      modalStatus.className = "modal-status status-error";
      modalStatus.innerHTML =
        '<div class="status-error-text">Nie udało się rozpocząć weryfikacji. Spróbuj ponownie później.</div>';
      btn.disabled = false;
    }
  });

  function startPolling(apiUrl, nonce, statusElement) {
    const pollInterval = setInterval(async () => {
      try {
        const res = await fetch(
          `${apiUrl}/verify/result?nonce=${encodeURIComponent(nonce)}`,
        );

        if (!res.ok) {
          console.warn("Błąd podczas pollingu", res.status);
          return;
        }

        const data = await res.json();

        // Continue polling if waiting for scan
        if (data.status === "waiting for scan") {
          statusElement.innerHTML =
            '<div class="status-waiting">Oczekiwanie na zeskanowanie kodu QR...</div>';
          return;
        }

        // Stop polling for final statuses (trusted or untrusted)
        if (data.status === "trusted" || data.status === "untrusted") {
          clearInterval(pollInterval);
          currentPollInterval = null;

          if (data.status === "trusted") {
            statusElement.className = "modal-status status-success";
            statusElement.innerHTML = `
              <div class="status-icon">✅</div>
              <div class="status-text">
                <strong>Weryfikacja zakończona pomyślnie</strong>
                <p>Strona jest zaufana. Możesz bezpiecznie kontynuować.</p>
              </div>
            `;
          } else if (data.status === "untrusted") {
            statusElement.className = "modal-status status-error";
            statusElement.innerHTML = `
              <div class="status-icon">❌</div>
              <div class="status-text">
                <strong>Weryfikacja nie powiodła się</strong>
                <p>Ta strona nie przeszła weryfikacji.</p>
              </div>
            `;
          }
        } else {
          // Unknown status - stop polling and show error
          clearInterval(pollInterval);
          currentPollInterval = null;
          statusElement.className = "modal-status status-error";
          statusElement.innerHTML =
            '<div class="status-error-text">Wystąpił błąd podczas weryfikacji. Spróbuj ponownie później.</div>';
        }
      } catch (err) {
        console.error(err);
        // On error, continue polling (might be temporary network issue)
      }
    }, 2000);

    return pollInterval;
  }
});
