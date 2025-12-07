window.addEventListener("load", () => {
  const root = document.getElementById("moby-verify");
  if (!root) return;

  const btn = document.getElementById("moby-verify-btn");
  const qrBox = document.getElementById("moby-verify-qr");
  const statusBox = document.getElementById("moby-verify-status");

  const API_URL = root.dataset.apiUrl || ""; // empty = same origin
  const SERVICE_ID = root.dataset.serviceId || "UNKNOWN";

  let currentPollInterval = null;

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    statusBox.className = "hint";
    statusBox.textContent = "Generuję sesję weryfikacyjną...";

    qrBox.innerHTML = "";

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
        throw new Error("Błąd HTTP: " + res.status);
      }

      const data = await res.json();

      const qrContainer = document.createElement("div");
      new QRCode(qrContainer, {
        text: data.qr_payload,
        width: 128,
        height: 128,
      });

      const label = document.createElement("div");
      label.className = "hint";
      label.textContent = "Zeskanuj ten kod aplikacją mObywatel (symulacja).";

      qrBox.appendChild(qrContainer);
      qrBox.appendChild(label);

      statusBox.textContent = "Oczekiwanie na zeskanowanie kodu QR...";

      if (currentPollInterval) {
        clearInterval(currentPollInterval);
      }
      currentPollInterval = startPolling(API_URL, data.nonce, statusBox, btn);
    } catch (err) {
      console.error(err);
      statusBox.className = "status-warn";
      statusBox.textContent =
        "Nie udało się rozpocząć weryfikacji. Spróbuj ponownie później.";
      btn.disabled = false;
    }
  });
});

function startPolling(apiUrl, nonce, statusBox, btn) {
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
        statusBox.className = "hint";
        statusBox.textContent = "Oczekiwanie na zeskanowanie kodu QR...";
        return;
      }

      // Stop polling for final statuses (trusted or untrusted)
      if (data.status === "trusted" || data.status === "untrusted") {
        clearInterval(pollInterval);
        btn.disabled = false;

        if (data.status === "trusted") {
          statusBox.className = "status-ok";
          statusBox.textContent =
            "✅ Strona jest zaufana. Możesz bezpiecznie kontynuować.";
        } else if (data.status === "untrusted") {
          statusBox.className = "status-warn";
          statusBox.textContent =
            "❌ Uwaga! Ta strona nie przeszła weryfikacji. Przerwij korzystanie i zgłoś podejrzenie oszustwa.";
        }
      } else {
        // Unknown status - stop polling and show error
        clearInterval(pollInterval);
        btn.disabled = false;
        statusBox.className = "status-warn";
        statusBox.textContent =
          "Wystąpił błąd podczas weryfikacji. Spróbuj ponownie później.";
      }
    } catch (err) {
      console.error(err);
      // On error, continue polling (might be temporary network issue)
    }
  }, 2000);

  return pollInterval;
}
