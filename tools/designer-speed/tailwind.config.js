// Same as the Tailwind Play CDN default config. Blocklist = plain words in the page's JavaScript
// (e.g. "if(!ring)", "hidden" attribute, comments) that are not classes on any element.
module.exports = { content: ['../../docs/mug-designer/index.html'], theme: { extend: {} }, plugins: [],
  blocklist: ['ring', '!ring', 'filter', 'transform', 'hidden', 'sticky'] }
