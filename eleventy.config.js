export default function (eleventyConfig) {
  // Ignorar pasta de documentação interna e README (não fazem parte do site publicado)
  eleventyConfig.ignores.add("docs/**");
  eleventyConfig.ignores.add("README.md");

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
