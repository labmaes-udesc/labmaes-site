/**
 * Links que abrem em nova aba (target="_blank"), aplicado ao HTML gerado:
 * - as setas ↗ e ↓ dentro do link ficam ocultas do leitor de tela (são decorativas);
 * - quem usa leitor de tela é avisado de que o link abre em nova aba: no aria-label,
 *   quando o link tem um, ou num texto visualmente oculto no fim do link.
 * WCAG 2.2: 2.4.4 (propósito do link) e 3.2.5 (mudança de contexto).
 */
const LINK = /<a\b([^>]*)>([\s\S]*?)<\/a>/g;
const NOVA_ABA = /\btarget\s*=\s*(["'])_blank\1/;
const ARIA_LABEL = /\baria-label\s*=\s*(["'])([\s\S]*?)\1/;
const AVISO = " (abre em nova aba)";
// Seta já oculta (mantém), qualquer tag (mantém, para não mexer em atributos) ou seta solta (oculta).
const SETA = /(<span aria-hidden="true">[↗↓]<\/span>)|(<[^>]*>)|([↗↓])/g;
const ocultarSetas = (html) =>
  html.replace(SETA, (m, jaOculta, tag, seta) => jaOculta ?? tag ?? `<span aria-hidden="true">${seta}</span>`);

export function marcarLinksNovaAba(html) {
  return html.replace(LINK, (link, attrs, conteudo) => {
    if (!NOVA_ABA.test(attrs)) return link;
    const corpo = ocultarSetas(conteudo);
    const rotulo = attrs.match(ARIA_LABEL);
    if (rotulo) {
      const novos = /nova aba/i.test(rotulo[2])
        ? attrs
        : attrs.replace(ARIA_LABEL, (_, q, valor) => `aria-label=${q}${valor}${AVISO}${q}`);
      return `<a${novos}>${corpo}</a>`;
    }
    if (corpo.includes('class="visually-hidden"> (abre em nova aba)')) return `<a${attrs}>${corpo}</a>`;
    return `<a${attrs}>${corpo}<span class="visually-hidden">${AVISO}</span></a>`;
  });
}
