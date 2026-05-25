document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector("[data-mobile-menu-toggle]");
  const nav = document.querySelector("[data-site-nav]");
  if (!toggle || !nav) return;

  function closeMenu() {
    nav.setAttribute("data-open", "false");
    toggle.setAttribute("aria-expanded", "false");
  }

  function openMenu() {
    nav.setAttribute("data-open", "true");
    toggle.setAttribute("aria-expanded", "true");
  }

  // Abrir/fechar ao clicar no botão
  toggle.addEventListener("click", () => {
    const isOpen = nav.getAttribute("data-open") === "true";
    isOpen ? closeMenu() : openMenu();
  });

  // Fechar ao pressionar Esc
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.getAttribute("data-open") === "true") {
      closeMenu();
      toggle.focus(); // Devolver foco ao botão para acessibilidade
    }
  });

  // Fechar ao clicar fora do menu
  document.addEventListener("click", (e) => {
    if (
      nav.getAttribute("data-open") === "true" &&
      !nav.contains(e.target) &&
      !toggle.contains(e.target)
    ) {
      closeMenu();
    }
  });

  // Fechar ao clicar em qualquer link dentro da nav
  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });
});
