"use strict";

const status = document.getElementById("status");
const detail = document.getElementById("detail");
const phase = document.getElementById("phase");
const version = document.getElementById("version");
const refresh = document.getElementById("refresh");

async function checkStatus() {
  refresh.disabled = true;
  status.dataset.state = "pending";
  status.textContent = "Checking system";
  detail.textContent = "Connecting to the platform and checking its liveness.";
  phase.textContent = "—";
  version.textContent = "—";

  try {
    const options = { cache: "no-store", signal: AbortSignal.timeout(5000) };
    const [health, metadata] = await Promise.all([
      fetch("/health/live", options),
      fetch("/api/v1/platform", options),
    ]);
    if (!health.ok || !metadata.ok) {
      throw new Error("System check failed");
    }

    const platform = await metadata.json();
    if (typeof platform.phase !== "string" || typeof platform.version !== "string") {
      throw new Error("Platform metadata is incomplete");
    }

    phase.textContent = platform.phase;
    version.textContent = platform.version;
    status.dataset.state = "ready";
    status.textContent = "Foundation online";
    detail.textContent = "The application responded to both checks.";
  } catch {
    status.dataset.state = "error";
    status.textContent = "Status unavailable";
    detail.textContent = "The application could not complete both checks. Refresh status to try again.";
  } finally {
    refresh.disabled = false;
  }
}

refresh.addEventListener("click", checkStatus);
checkStatus();
