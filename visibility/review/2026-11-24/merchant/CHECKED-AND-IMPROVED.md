# ZANS website: Merchant Centre + gift page SEO preview (24 Nov 2026)

These changes are a preview only and are not live yet.

- **Preview branch:** zans-pins `claude/project-thread-d6n9z9`, commit `0900f1a`.
- **Live branch:** `claude/project-thread-cbdh5k`.
- **Full diff against live:** `all-changes.diff`, 20 files.
- **Phone previews:**
  1. Returns
  2. Privacy
  3. Terms
  4. Contact
  5. Gifts for racehorse owners
  6. Horse racing gifts

## Checked and already fine
These checks apply to both /horse-racing-gifts/ and /gifts-for-racehorse-owners/.
- Neither page has a noindex tag, and robots.txt allows everything.
- Both canonical URLs are correct.
- Both pages are in the sitemap.
- Both are linked from the home page and from 16 other pages.
- There is no sideways scroll at 390px.
- The live Lighthouse audit on 21 Nov (phone) scored performance 99, accessibility 100 and SEO 100, with LCP about 2.2s.

## Improved
1. **Horse racing gifts page.**
   - The title, meta description, OG tags and H1 now cover both mugs and baubles.
   - A new bauble section near the top has a photo and direct Etsy buttons (listings 4611232428 and 4611213915).
   - Prices shown: mug £14.99, silks bauble £14.99, green and gold bauble £12.99. These are the live Etsy prices, read 24 Nov.
   - Product JSON-LD now covers the 3 items. No ratings or reviews are included.
2. **Gifts for racehorse owners page.**
   - The same title, meta description and H1 change as the gifts page.
   - A bauble section written for owners.
   - Links to the syndicate and gifts pages.
   - Product JSON-LD for the 3 items.
3. **Home page:** the meta description now uses the wording from issue #26.
4. **Gifts, syndicate and owners pages:**
   - Removed "order by Monday 7 December", "3 to 5 working days" and "plus postage". This includes the owners page FAQ JSON-LD.
   - They now say that Etsy shows the delivery estimate at checkout.
5. **New pages:** /returns-policy/, /privacy-policy/, /terms/ and /contact/.
   - All four are added to the sitemap.
   - Every page with the standard footer now links to them. The mug and bauble designers have no footer, so they don't.
   - **Returns policy:**
     - Personalised items are exempt from cancellation under CCR 2013. If one arrives damaged or misprinted, the customer gets a free replacement or a refund and doesn't need to send it back.
     - Non-personalised items can be cancelled within 14 days and returned within 14 days of cancelling. The buyer pays return postage unless the item is faulty. Refunds are made within 14 days. Faulty goods can be rejected within 30 days under the Consumer Rights Act 2015.
     - For digital PDFs, the right to cancel ends once the file is available to download. If a file is faulty, we fix it, replace it or refund it.
   - **Privacy policy:** covers the Metricool tracker, the designers' browser storage (localStorage), Etsy order data, the print partner, UK GDPR rights and the ICO.
   - **Terms:** checkout happens on Etsy; the guides carry a personal-use licence; no winners are promised; buyers must be 18+; the law of England and Wales applies.
6. **Sitemap:** lastmod is set to 2026-11-24 for the changed pages.

## Open questions
- **Contact email:** the pages show a placeholder until Alex gives a real address. Nothing has been invented.
- **Merchant Centre:** Google's rule (answer 12160471) says customers must be able to "buy directly from your website without the need to redirect". Every product here links to Etsy to buy, so the products are likely to be rejected. Alex has been told.
- **Cookie consent:** under PECR, the Metricool tracker may need a cookie consent banner. There isn't one yet.
- **Site-wide banner:** "from £11.99 · Free UK delivery" has not been checked. I've asked Alex whether it's true.
