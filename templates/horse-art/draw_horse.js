// ZANS own-drawn racehorse (vector, no AI, no photo). Usage: node draw_horse.js <out.svg> <coat> <points> <silks body> <silks second> <cap> <pattern hoops|spots>
const fs = require('fs');
const [out, coat='#7B4B2A', pts='#1B1410', sb='#0E6B3B', s2='#F5D130', cap='#FFFFFF', pat='hoops'] = process.argv.slice(2);
const leg = (p, w, c) => `<polyline points="${p}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
let jacket = '';
const J = 'M 395 178 C 420 150 470 150 505 178 C 525 196 520 232 498 244 L 408 246 C 385 232 378 200 395 178 Z';
if (pat === 'hoops') {
  jacket = `<clipPath id="jk"><path d="${J}"/></clipPath><path d="${J}" fill="${sb}"/><g clip-path="url(#jk)" fill="${s2}"><rect x="370" y="176" width="170" height="18"/><rect x="370" y="208" width="170" height="18"/></g>`;
} else {
  jacket = `<clipPath id="jk"><path d="${J}"/></clipPath><path d="${J}" fill="${sb}"/><g clip-path="url(#jk)" fill="${s2}"><circle cx="425" cy="190" r="12"/><circle cx="465" cy="186" r="12"/><circle cx="500" cy="200" r="12"/><circle cx="440" cy="224" r="12"/><circle cx="482" cy="228" r="12"/></g>`;
}
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520" width="1600" height="1040">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient></defs>
<g>
<!-- far legs (darker) -->
${leg('510,320 590,372 668,392', 24, pts)}${leg('300,326 220,370 128,372', 24, pts)}
<!-- tail -->
<path d="M 262 238 C 200 228 150 250 96 318 C 130 296 170 290 218 292 C 236 286 252 268 262 238 Z" fill="${pts}"/>
<!-- body, neck, head -->
<path d="M 262 232 C 280 190 360 182 440 192 C 500 196 540 214 558 192 C 574 168 596 134 626 112 L 640 96 L 650 118 C 690 134 724 168 744 206 C 750 220 738 234 722 230 C 700 228 684 220 660 214 C 640 240 604 266 560 282 C 540 318 470 336 400 334 C 340 334 296 324 270 296 C 254 276 254 252 262 232 Z" fill="${coat}"/>
<path d="M 262 232 C 280 190 360 182 440 192 C 500 196 540 214 558 192 C 574 168 596 134 626 112 L 640 96 L 650 118 C 690 134 724 168 744 206 C 750 220 738 234 722 230 C 700 228 684 220 660 214 C 640 240 604 266 560 282 C 540 318 470 336 400 334 C 340 334 296 324 270 296 C 254 276 254 252 262 232 Z" fill="url(#g)"/>
<!-- ear, eye, nostril, mane -->
<path d="M 636 104 L 640 70 L 656 104 Z" fill="${coat}"/>
<circle cx="670" cy="150" r="5" fill="#120d09"/><ellipse cx="740" cy="214" rx="4" ry="6" fill="#120d09"/>
<path d="M 566 188 C 582 150 606 122 628 104 C 618 138 604 168 586 200 Z" fill="${pts}"/>
<!-- near legs -->
${leg('528,306 612,330 690,298', 28, coat)}${leg('690,298 712,286', 20, pts)}
${leg('318,318 244,352 176,326', 28, coat)}${leg('176,326 150,316', 20, pts)}
<!-- bridle and rein -->
<path d="M 722 228 L 650 150 M 672 196 L 560 196" stroke="#2a1c12" stroke-width="3" fill="none"/>
<!-- saddle cloth -->
<path d="M 388 240 L 500 244 L 494 290 L 392 284 Z" fill="#FFFFFF" opacity=".95"/>
<!-- jockey: leg, boot, silks, arm, cap (back of head only, no face) -->
${leg('430,262 470,300 452,318', 20, '#FFFFFF')}<path d="M 440 308 L 484 306 L 478 330 L 442 332 Z" fill="#14100c"/>
${jacket}
${leg('500,190 540,214 566,200', 16, sb)}
<circle cx="470" cy="152" r="26" fill="${cap}"/><path d="M 446 150 C 452 128 490 126 496 150 Z" fill="${cap}"/>
<path d="M 486 154 C 506 154 516 160 520 168" stroke="#14100c" stroke-width="4" fill="none" opacity=".6"/>
</g></svg>`;
fs.writeFileSync(out, svg);
