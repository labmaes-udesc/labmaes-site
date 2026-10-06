import test from "node:test";
import assert from "node:assert/strict";
import { CATEGORIAS, categoriaDe } from "./categorias-producao.mjs";
import { loadSchema } from "../validate-content/schema.mjs";

test("tipos derivam a categoria (ADR 0009)", () => {
  assert.equal(categoriaDe("article"), "bibliographic");
  assert.equal(categoriaDe("thesis-dissertation-tcc"), "bibliographic");
  assert.equal(categoriaDe("exhibition"), "artistic");
  assert.equal(categoriaDe("catalog"), "artistic");
  assert.equal(categoriaDe("podcast-audio"), "audiovisual");
  assert.equal(categoriaDe("teaching-material"), "educational");
  assert.equal(categoriaDe("technical-document"), "documentary");
  assert.equal(categoriaDe("software-digital"), "other");
  assert.equal(categoriaDe("other"), "other");
  assert.equal(categoriaDe("inexistente"), null);
});

test("as seis macro categorias públicas têm nome", () => {
  assert.deepEqual(Object.keys(CATEGORIAS), ["bibliographic", "artistic", "audiovisual", "educational", "documentary", "other"]);
  assert.equal(CATEGORIAS.other, "Outros");
});

test("todo Tipo específico do .pages.yml real tem categoria", () => {
  const tipos = loadSchema(".pages.yml").collections.get("productions").fields
    .find((f) => f.name === "productionType").options.values.map((v) => v.name);
  assert.deepEqual(tipos.filter((t) => !categoriaDe(t)), []);
});
