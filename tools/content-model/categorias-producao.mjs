/**
 * Macro categoria pública de uma produção, derivada do Tipo específico (ADR 0009).
 * A categoria não é editada no CMS: quem cadastra escolhe só o tipo.
 * Ao acrescentar um tipo em `.pages.yml`, acrescente-o aqui; o validador recusa tipo sem categoria.
 */
export const CATEGORIAS = {
  bibliographic: "Bibliográficas",
  artistic: "Artísticas",
  audiovisual: "Audiovisuais",
  educational: "Educacionais",
  documentary: "Documentais",
  other: "Outros",
};

const CATEGORIA_POR_TIPO = {
  article: "bibliographic",
  book: "bibliographic",
  "book-chapter": "bibliographic",
  "edited-book": "bibliographic",
  "conference-paper": "bibliographic",
  "thesis-dissertation-tcc": "bibliographic",
  artistic: "artistic",
  exhibition: "artistic",
  catalog: "artistic",
  audiovisual: "audiovisual",
  "podcast-audio": "audiovisual",
  "teaching-material": "educational",
  "technical-document": "documentary",
  "software-digital": "other",
  other: "other",
};

export const categoriaDe = (tipo) => CATEGORIA_POR_TIPO[tipo] ?? null;
