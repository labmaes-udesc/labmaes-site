// Sinaliza que JS está disponível (habilita animações de entrada via CSS)
document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", () => {
  // ── Scroll reveal: cards de atuação ────────────────────────
  const cards = document.querySelectorAll(".event-card");
  if (cards.length && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.setAttribute("data-visible", "");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    cards.forEach((card) => observer.observe(card));
  } else {
    // Fallback: sem IntersectionObserver, mostra tudo imediatamente
    cards.forEach((card) => card.setAttribute("data-visible", ""));
  }

  // ── Menu mobile ─────────────────────────────────────────────
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
