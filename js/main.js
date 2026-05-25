document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector("[data-mobile-menu-toggle]");
  const nav = document.querySelector("[data-site-nav]");
  if (!toggle || !nav) return;

  toggle.addEventListener("click", () => {
    const isOpen = nav.getAttribute("data-open") === "true";
    nav.setAttribute("data-open", String(!isOpen));
    toggle.setAttribute("aria-expanded", String(!isOpen));
  });
});
