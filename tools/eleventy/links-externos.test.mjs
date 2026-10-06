import test from "node:test";
import assert from "node:assert/strict";
import { marcarLinksNovaAba } from "./links-externos.mjs";

const AVISO = '<span class="visually-hidden"> (abre em nova aba)</span>';

test("link sem aria-label ganha aviso para leitor de tela", () => {
  assert.equal(
    marcarLinksNovaAba('<a href="https://x.org" target="_blank" rel="noopener">Site</a>'),
    `<a href="https://x.org" target="_blank" rel="noopener">Site${AVISO}</a>`,
  );
});

test("setas decorativas ficam ocultas do leitor de tela", () => {
  assert.equal(
    marcarLinksNovaAba('<a href="/e.pdf" target="_blank">↓ Edital — PDF</a> <a target="_blank" href="x">Inscrições ↗</a>'),
    `<a href="/e.pdf" target="_blank"><span aria-hidden="true">↓</span> Edital — PDF${AVISO}</a> <a target="_blank" href="x">Inscrições <span aria-hidden="true">↗</span>${AVISO}</a>`,
  );
});

test("aria-label recebe o aviso no próprio rótulo, uma vez só", () => {
  assert.equal(
    marcarLinksNovaAba('<a target="_blank" aria-label="Instagram do LabMAES" href="x"><svg aria-hidden="true"></svg></a>'),
    '<a target="_blank" aria-label="Instagram do LabMAES (abre em nova aba)" href="x"><svg aria-hidden="true"></svg></a>',
  );
  const jaAvisa = '<a target="_blank" aria-label="Anais 2024 (abre em nova aba)" href="x">Acessar anais <span aria-hidden="true">↗</span></a>';
  assert.equal(marcarLinksNovaAba(jaAvisa), jaAvisa);
});

test("links na mesma aba e setas fora de links não mudam", () => {
  const html = '<p>Veja ↗</p><a href="/sobre/">Sobre ↗</a>';
  assert.equal(marcarLinksNovaAba(html), html);
});

test("atributos em várias linhas e aspas simples", () => {
  assert.equal(
    marcarLinksNovaAba("<a\n  href='x'\n  target='_blank'>\n  Acessar Even3 ↗\n</a>"),
    `<a\n  href='x'\n  target='_blank'>\n  Acessar Even3 <span aria-hidden="true">↗</span>\n${AVISO}</a>`,
  );
});

test("é idempotente", () => {
  const uma = marcarLinksNovaAba('<a target="_blank" href="x">Ir ↗</a>');
  assert.equal(marcarLinksNovaAba(uma), uma);
});
