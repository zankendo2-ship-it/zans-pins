# Merchant Centre plan for the full ZANS catalogue (24 Nov 2026)

This is a plan only. Nothing has been submitted and nothing has been spent.

## 1. Why the 6 products are "Not approved"
I have no Merchant Centre access, so I could not read the claimed domain or the source fields. The facts below come from the live site and Google's rules.

- **No product markup on the guide pages.** The Ascot and Breeders' Cup guide pages have no Product data. That means Google auto-detected the 6 items and guessed the £16.99 price itself.
- **Every buy button leaves the site.** Each one goes to etsy.com, so the product link domain doesn't match the claimed zanshorseracing.co.uk. That causes "Mismatched online store URL". Google says shoppers must "buy directly from your website without the need to redirect" (answer 12160471), and you must not redirect outside the claimed domain (answer 4752265).
- **PDF guides are limited.** Google doesn't allow ebooks and PDFs in Shopping ADS. They can appear in FREE listings only (answer 6150006).
- **Alex should check one thing in Merchant Centre > Business info > Online store:** that the claimed domain is https://www.zanshorseracing.co.uk, with www.

## 2. Catalogue to match Etsy (the upload thread holds the final list)
| Group | Count | Listing ids |
|---|---|---|
| Guides, each with 3 levels (Beginner, Advanced, Pro) | 21 | Ascot Flat, Ascot Jumps, Cheltenham, Kempton Jumps, Kempton AW, Sandown Jumps, Aintree Jumps |
| Mugs | 3 | 4608193933, 4609859882, 4612435420 |
| Baubles | 2 | 4611232428, 4611213915 |
| Breeders' Cup guide | ? | Merchant Centre shows 3; the upload thread to confirm |

That makes about 29 products in total.

## 3. Landing pages (one per product, as Google requires)
- **Guides:** one page per guide level, for example /ascot-racecourse-guide/beginner/. That's 21 new small pages, each carrying:
  - Product JSON-LD with sku = the Etsy id, the price, GBP, InStock and the image
  - a description of what's inside
  - the policy links
- **Mugs and baubles:** one page each, or the designer page with that variant. 5 pages.
- **Feed:** a Google Sheet or a docs/feed.xml with id, title, description, link, image_link, price, availability, condition, brand ZANS Racing, google_product_category, identifier_exists=no and shipping (free UK, as Alex confirmed).

Even with all of this in place, the products still fail while the buy button goes to Etsy. The pages only become eligible once checkout happens on our own site (section 4).

## 4. Own-site checkout options (Alex to approve before any spend)
| Option | Monthly | Per-sale fee | Works on our GitHub Pages site? | Notes |
|---|---|---|---|---|
| A. Stripe Payment Links | £0 | 1.5% + 20p UK cards; 2.5% + 20p EEA; 3.15% + 20p other (stripe.com/gb/pricing) | Yes: a "Buy now" button per product | Up to 3 custom fields per link can collect silks details. There is no automatic PDF delivery and no Printify link, so orders are fulfilled by hand. Checkout opens on buy.stripe.com, and it's NOT confirmed that Google counts this as on-site. Needs a Stripe account (Alex's bank and ID). |
| B. Shopify Starter | Not shown on Shopify's UK pricing page; needs checking in Shopify signup | Not checked | Link or button only | Not a full online store; it can't be confirmed from Shopify's own page. |
| C. Shopify Basic (store on a subdomain, for example shop.zanshorseracing.co.uk) | £25 a month, or £19 a month paid yearly (shopify.com/uk/pricing; first 3 months £1) | 2% + 25p UK cards | Yes, through a subdomain | It's a full store. Google's own Shopify app feeds Merchant Centre, and the Printify and Printful apps plus digital download apps fulfil orders automatically. |

- **Recommendation:** if Alex wants Google Shopping, choose C. It's the only option that is certainly eligible and automatic. If he wants the cheapest test first, choose A, for mugs and baubles only.
- **Either way:** keep Etsy as well. Selling the same item on our own site is allowed.
- **Free alternative with no site checkout:** Etsy Offsite Ads already puts Etsy listings on Google Shopping. Etsy takes 15% only when an ad leads to a sale.
- **Until Alex decides:** turn off "auto-detected products" in Merchant Centre and don't approve the £16.99 guesses.
