// Sinaliza que JS está disponível (habilita animações de entrada via CSS)
document.documentElement.classList.add("js");

// Programação: com JS, inicia colapsada (sem JS, <details open> mostra tudo)
window.addEventListener("DOMContentLoaded", () => {
  document
    .querySelectorAll(".prog-card[open]")
    .forEach((d) => d.removeAttribute("open"));
});

document.addEventListener("DOMContentLoaded", () => {
  // ── Scroll reveal: cards de atuação ────────────────────────
  const cards = document.querySelectorAll(".event-card");
  if (cards.length && "IntersectionObserver" in window) {
    const revealCard = (card) => card.setAttribute("data-visible", "");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            revealCard(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      // threshold:0 dispara ao primeiro pixel visível;
      // rootMargin positivo na base aciona cards ainda 80px abaixo do viewport
      { threshold: 0, rootMargin: "0px 0px 80px 0px" }
    );
    cards.forEach((card) => observer.observe(card));

    // Segurança: após 1,5 s revela qualquer card que ainda não foi observado
    setTimeout(() => {
      cards.forEach((card) => {
        if (!card.hasAttribute("data-visible")) revealCard(card);
      });
    }, 1500);
  } else {
    // Fallback: sem IntersectionObserver, mostra tudo imediatamente
    cards.forEach((card) => card.setAttribute("data-visible", ""));
  }

  // ── Scroll reveal: itens da programação ─────────────────
  const scheduleItems = document.querySelectorAll(".schedule-item, .schedule-parallel");
  if (scheduleItems.length && "IntersectionObserver" in window) {
    const revealItem = (el) => el.setAttribute("data-visible", "");
    const scheduleObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            revealItem(entry.target);
            scheduleObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0, rootMargin: "0px 0px 80px 0px" }
    );
    scheduleItems.forEach((item) => scheduleObserver.observe(item));
    setTimeout(() => {
      scheduleItems.forEach((item) => {
        if (!item.hasAttribute("data-visible")) revealItem(item);
      });
    }, 1500);
  } else {
    scheduleItems.forEach((item) => item.setAttribute("data-visible", ""));
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
