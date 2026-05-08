const navToggle = document.querySelector("[data-nav-toggle]");
const navMenu = document.querySelector("[data-nav-menu]");

if (navToggle && navMenu) {
  navToggle.addEventListener("click", () => {
    const isOpen = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!isOpen));
    navMenu.classList.toggle("is-open", !isOpen);
  });
}

const yearNodes = document.querySelectorAll("[data-year]");
yearNodes.forEach((node) => {
  node.textContent = String(new Date().getFullYear());
});

const contactForm = document.querySelector("[data-contact-form]");

if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const data = new FormData(contactForm);
    const requestType = data.get("request-type") || "Sherlock inquiry";
    const email = data.get("email") || "";
    const company = data.get("company") || "";
    const website = data.get("website") || "";
    const message = data.get("message") || "";

    const body = [
      `Request type: ${requestType}`,
      `Work email: ${email}`,
      `Company: ${company}`,
      `Website or product URL: ${website}`,
      "",
      "Context:",
      String(message),
    ].join("\n");

    const mailto = new URL("mailto:hello@powerdetect.ai");
    mailto.searchParams.set("subject", `PowerDetect Sherlock - ${requestType}`);
    mailto.searchParams.set("body", body);

    const status = contactForm.querySelector("[data-form-status]");
    if (status) {
      status.textContent = "Opening your email client. This static site does not store form data.";
    }

    window.location.href = mailto.toString();
  });
}

const authForms = document.querySelectorAll("[data-auth-form]");

authForms.forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const status = form.querySelector("[data-form-status]");
    if (status) {
      status.textContent =
        form.dataset.authMessage ||
        "This is a demo UI shell. No production auth action was performed.";
    }
  });
});

const setupForms = document.querySelectorAll("[data-setup-form]");

setupForms.forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();

    const status = form.querySelector("[data-form-status]");
    const summaryId = form.dataset.summaryTarget;
    const summary = summaryId ? document.getElementById(summaryId) : null;

    if (!form.checkValidity()) {
      form.reportValidity();
      if (status) {
        status.textContent = "Complete the required setup metadata before reviewing the local preview.";
      }
      return;
    }

    const fields = Array.from(form.querySelectorAll("[data-summary-label]"));
    const items = fields.map((field) => {
      const label = field.dataset.summaryLabel;
      let value = "";

      if (field.type === "checkbox") {
        value = field.checked ? "Acknowledged" : "Not acknowledged";
      } else {
        value = field.value.trim();
      }

      if (!value) {
        value = "Not provided";
      }

      return { label, value };
    });

    if (summary) {
      summary.innerHTML = "";
      items.forEach((item) => {
        const row = document.createElement("div");
        const term = document.createElement("dt");
        const description = document.createElement("dd");

        term.textContent = item.label;
        description.textContent = item.value;
        row.append(term, description);
        summary.append(row);
      });
    }

    if (status) {
      status.textContent =
        form.dataset.setupMessage ||
        "Local setup preview updated. Nothing was submitted, persisted, verified, or scanned.";
    }
  });
});

const dashboardShell = document.querySelector("[data-dashboard-shell]");
const dashboardNavToggle = document.querySelector("[data-dashboard-nav-toggle]");

if (dashboardShell && dashboardNavToggle) {
  dashboardNavToggle.addEventListener("click", () => {
    const isOpen = dashboardNavToggle.getAttribute("aria-expanded") === "true";
    dashboardNavToggle.setAttribute("aria-expanded", String(!isOpen));
    dashboardShell.classList.toggle("is-open", !isOpen);
  });

  const dashboardLinks = dashboardShell.querySelectorAll(".dashboard-nav a");
  dashboardLinks.forEach((link) => {
    link.addEventListener("click", () => {
      dashboardNavToggle.setAttribute("aria-expanded", "false");
      dashboardShell.classList.remove("is-open");
    });
  });
}

const authStatusNodes = document.querySelectorAll("[data-auth-status]");

authStatusNodes.forEach(async (node) => {
  const authUrl = node.dataset.authUrl || "http://localhost:8000/api/v0/auth/status";
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 2200);

  try {
    const response = await fetch(authUrl, {
      headers: { Accept: "application/json" },
      signal: controller.signal,
    });
    if (!response.ok) {
      throw new Error(`Auth status returned HTTP ${response.status}`);
    }
    const payload = await response.json();
    const data = payload.data || {};
    const authEnabled = Boolean(data.authentication_enabled);
    const jwtReady = Boolean(data.token_validation_active);
    const productionReady = Boolean(data.production_ready);

    node.classList.toggle("is-ready", authEnabled && jwtReady && productionReady);
    node.classList.toggle("is-error", !authEnabled || !jwtReady || !productionReady);
    node.textContent = authEnabled && jwtReady && productionReady
      ? "Auth status: configured and production-ready according to the local API."
      : "Auth status: not production-ready. Dashboard remains a demo UI shell with no browser session.";
  } catch (error) {
    node.classList.add("is-error");
    node.textContent =
      "Auth status unavailable. Start the local API on port 8000 to read /api/v0/auth/status.";
  } finally {
    window.clearTimeout(timeout);
  }
});
