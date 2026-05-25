export default function (eleventyConfig) {
  // Ignorar pasta de documentação interna (não faz parte do site)
  eleventyConfig.ignores.add("docs/**");

  // Copiar assets estáticos para _site/ sem processar
  eleventyConfig.addPassthroughCopy("assets");
  eleventyConfig.addPassthroughCopy("css");
  eleventyConfig.addPassthroughCopy("js");
  eleventyConfig.addPassthroughCopy("_headers");
  eleventyConfig.addPassthroughCopy("_redirects");

  return {
    dir: {
      input: ".",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
  };
}
