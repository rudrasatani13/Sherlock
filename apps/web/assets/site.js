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
