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

  return {
    dir: {
      input: ".",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
  };
}
