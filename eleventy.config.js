import { marcarLinksNovaAba } from "./tools/eleventy/links-externos.mjs";

export default function (eleventyConfig) {
  // Ignorar pasta de documentação interna e README (não fazem parte do site publicado)
  eleventyConfig.ignores.add("docs/**");
  eleventyConfig.ignores.add("README.md");
  // Arquivos de comunidade do repositório (lidos no GitHub, não no site)
  eleventyConfig.ignores.add("CONTRIBUTING.md");
  eleventyConfig.ignores.add("CODE_OF_CONDUCT.md");
  eleventyConfig.ignores.add("SECURITY.md");
  eleventyConfig.ignores.add(".github/**");
  eleventyConfig.ignores.add("tools/**");
  // Fundação de conteúdo do Pages CMS (Fase 1) — ainda não integrada ao build do Eleventy
  eleventyConfig.ignores.add("src/**");

  // Links com target="_blank": aviso de nova aba para leitor de tela e setas decorativas ocultas
  eleventyConfig.addTransform("links-nova-aba", function (content) {
    return (this.page.outputPath || "").endsWith(".html") ? marcarLinksNovaAba(content) : content;
  });

  // Versão do build: sufixo ?v= nos CSS/JS, para que uma atualização não fique presa no cache do navegador
  eleventyConfig.addGlobalData("buildId", () => Date.now().toString(36));

  // Copiar assets estáticos para _site/ sem processar
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("css");
  eleventyConfig.addPassthroughCopy("js");
  eleventyConfig.addPassthroughCopy("_headers");
  eleventyConfig.addPassthroughCopy("_redirects");

  // Iniciais para o fallback de avatar (remove titulação, pega 1ª+última palavra)
  eleventyConfig.addFilter("iniciais", (nome) => {
    if (!nome) return "?";
    const limpo = nome.replace(
      /\b(prof\.?a?|prof|dra?\.?|dr|me\.?|ma\.?|phd\.?|candidate)\b/gi,
      ""
    );
    const palavras = limpo
      .replace(/[.'']/g, "")
      .replace(/[ªº]/g, "")
      .split(/\s+/)
      .filter(Boolean);
    if (palavras.length === 0) return "?";
    const primeira = palavras[0][0] || "";
    const ultima = palavras.length > 1 ? palavras[palavras.length - 1][0] : "";
    return (primeira + ultima).toUpperCase();
  });

  // Ordena participantes de um card colocando mediadores/mediadoras por último
  eleventyConfig.addFilter("ordenarParticipantes", (participantes) => {
    if (!Array.isArray(participantes)) return participantes;
    const ehMediador = (p) =>
      typeof p.papel === "string" && /media/i.test(p.papel);
    return [
      ...participantes.filter((p) => !ehMediador(p)),
      ...participantes.filter((p) => ehMediador(p)),
    ];
  });

  // Índice de cor 1..6 derivado de forma estável do slug
  eleventyConfig.addFilter("corAvatar", (slug) => {
    if (!slug) return 1;
    let h = 0;
    for (let i = 0; i < slug.length; i++) h = (h * 31 + slug.charCodeAt(i)) % 997;
    return (h % 6) + 1;
  });

  return {
    dir: {
      input: ".",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
  };
}
