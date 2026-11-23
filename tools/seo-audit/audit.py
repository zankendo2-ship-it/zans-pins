"""Live technical SEO audit of www.zanshorseracing.co.uk.

Runs on GitHub Actions (the Claude sandbox cannot reach the site).
Fetches only our own site, our DNS/TLS, and Google's official PageSpeed API.
It does not scrape any search engine's results pages.
Writes <out>/report.json and <out>/report.md.
"""
import json, os, re, socket, ssl, sys, time, datetime, urllib.parse
import requests
from bs4 import BeautifulSoup
import dns.resolver

BASE = "https://www.zanshorseracing.co.uk"
HOST = "www.zanshorseracing.co.uk"
APEX = "zanshorseracing.co.uk"
UA = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
UA_BOT = "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
S = requests.Session()
S.headers["User-Agent"] = UA
R = {"run_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}


def q(name, rtype):
    try:
        return sorted(r.to_text() for r in dns.resolver.resolve(name, rtype, lifetime=10))
    except Exception as e:
        return "none (%s)" % type(e).__name__


R["dns"] = {}
for n in (APEX, HOST):
    for t in ("A", "AAAA", "CNAME", "TXT", "CAA", "MX"):
        R["dns"]["%s %s" % (n, t)] = q(n, t)
R["dns"]["%s NS" % APEX] = q(APEX, "NS")
R["dns"]["mwww.%s TXT" % APEX] = q("mwww." + APEX, "TXT")


def cert(host):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=15) as s:
            with ctx.wrap_socket(s, server_hostname=host) as ss:
                c = ss.getpeercert()
        return {"ok": True, "notAfter": c["notAfter"], "issuer": dict(x[0] for x in c["issuer"]),
                "san": [v for k, v in c.get("subjectAltName", [])]}
    except Exception as e:
        return {"ok": False, "error": repr(e)[:300]}


R["tls"] = {h: cert(h) for h in (HOST, APEX)}


def chain(url, ua=UA):
    hops = []
    for _ in range(10):
        try:
            r = requests.get(url, allow_redirects=False, headers={"User-Agent": ua}, timeout=25)
        except Exception as e:
            hops.append({"url": url, "error": repr(e)[:200]})
            break
        hops.append({"url": url, "status": r.status_code, "location": r.headers.get("Location")})
        if r.status_code in (301, 302, 303, 307, 308) and r.headers.get("Location"):
            url = urllib.parse.urljoin(url, r.headers["Location"])
        else:
            break
    return hops


R["redirects"] = {}
for u in ["http://%s/" % APEX, "https://%s/" % APEX, "http://%s/" % HOST, BASE + "/",
          "https://zankendo2-ship-it.github.io/zans-pins/", "https://zankendo2-ship-it.github.io/zans-pins/mug-designer/",
          BASE + "/horse-racing-gifts", BASE + "/index.html", BASE + "/mug-designer/index.html",
          "https://%s/mug-designer/" % APEX, BASE + "/this-page-does-not-exist/", BASE + "/favicon.ico",
          BASE + "/robots.txt", BASE + "/sitemap.xml", BASE + "/mug-designer-test/", BASE + "/mug-order-tool/"]:
    R["redirects"][u] = chain(u)

# robots + sitemap
rb = S.get(BASE + "/robots.txt", timeout=25)
R["robots_txt"] = {"status": rb.status_code, "body": rb.text[:2000]}
sm = S.get(BASE + "/sitemap.xml", timeout=25)
sm_urls = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sm.text)
R["sitemap"] = {"status": sm.status_code, "content_type": sm.headers.get("Content-Type"), "count": len(sm_urls), "urls": sm_urls}

# crawl
seen, queue, pages, assets = set(), [BASE + "/"] + sm_urls, {}, {}
ext_links = {}


def norm(u):
    p = urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path or "/", p.query, ""))


while queue and len(pages) < 80:
    u = norm(queue.pop(0))
    if u in seen:
        continue
    seen.add(u)
    t0 = time.time()
    try:
        r = S.get(u, timeout=30)
    except Exception as e:
        pages[u] = {"error": repr(e)[:200]}
        continue
    dt = round(time.time() - t0, 2)
    info = {"status": r.status_code, "final_url": r.url, "secs": dt, "bytes": len(r.content),
            "content_type": r.headers.get("Content-Type"), "cache_control": r.headers.get("Cache-Control"),
            "content_encoding": r.headers.get("Content-Encoding"), "x_robots_tag": r.headers.get("X-Robots-Tag"),
            "last_modified": r.headers.get("Last-Modified"), "age": r.headers.get("Age"), "server": r.headers.get("Server")}
    if "text/html" in (r.headers.get("Content-Type") or ""):
        soup = BeautifulSoup(r.text, "lxml")
        meta = {}
        for m in soup.find_all("meta"):
            k = m.get("name") or m.get("property")
            if k:
                meta[k.lower()] = m.get("content")
        info["title"] = (soup.title.string or "").strip() if soup.title else None
        info["description"] = meta.get("description")
        info["robots"] = meta.get("robots")
        info["canonical"] = [l.get("href") for l in soup.find_all("link", rel="canonical")]
        info["h1"] = [" ".join(h.get_text(" ").split()) for h in soup.find_all("h1")]
        info["og_image"] = meta.get("og:image")
        info["icons"] = [l.get("href") for l in soup.find_all("link") if "icon" in " ".join(l.get("rel") or [])]
        lds = []
        for s in soup.find_all("script", type="application/ld+json"):
            try:
                o = json.loads(s.string or "")
                lds.append("ok")
            except Exception as e:
                lds.append("PARSE ERROR " + str(e)[:80])
        info["jsonld"] = lds
        imgs = []
        for im in soup.find_all("img"):
            src = urllib.parse.urljoin(u, im.get("src") or "")
            imgs.append({"src": src, "alt": im.get("alt"), "w": im.get("width"), "h": im.get("height"), "loading": im.get("loading")})
            assets.setdefault(src, set()).add(u)
        info["images"] = imgs
        for sc in soup.find_all("script", src=True):
            assets.setdefault(urllib.parse.urljoin(u, sc["src"]), set()).add(u)
        for ln in soup.find_all("link", href=True):
            if any(x in (ln.get("rel") or []) for x in ("stylesheet", "preload", "icon", "apple-touch-icon", "manifest")):
                assets.setdefault(urllib.parse.urljoin(u, ln["href"]), set()).add(u)
        if info["og_image"]:
            assets.setdefault(urllib.parse.urljoin(u, info["og_image"]), set()).add(u)
        links = []
        for a in soup.find_all("a", href=True):
            h = urllib.parse.urljoin(u, a["href"])
            p = urllib.parse.urlsplit(h)
            if p.scheme not in ("http", "https"):
                continue
            if p.netloc == HOST:
                links.append(norm(h))
                if norm(h) not in seen and len(seen) + len(queue) < 200:
                    queue.append(norm(h))
            else:
                ext_links.setdefault(h, {"rel": a.get("rel"), "pages": set()})["pages"].add(u)
        info["internal_links"] = sorted(set(links))
        info["text_words"] = len(soup.get_text(" ").split())
    pages[u] = info

R["pages"] = pages

# assets: status + size
ares = {}
for a, used in sorted(assets.items()):
    if urllib.parse.urlsplit(a).netloc not in (HOST,):
        ares[a] = {"external": True, "used_on": sorted(used)}
        continue
    try:
        r = S.get(a, timeout=30)
        ares[a] = {"status": r.status_code, "bytes": len(r.content), "type": r.headers.get("Content-Type"),
                   "cache_control": r.headers.get("Cache-Control"), "used_on": sorted(used)}
    except Exception as e:
        ares[a] = {"error": repr(e)[:200], "used_on": sorted(used)}
R["assets"] = ares

# external links (status only; Etsy often blocks robots, so a 403/429 here is not proof of a broken link)
eres = {}
for h, v in sorted(ext_links.items()):
    try:
        r = requests.get(h, headers={"User-Agent": UA, "Accept-Language": "en-GB,en;q=0.9"}, timeout=25, allow_redirects=True)
        eres[h] = {"status": r.status_code, "final": r.url, "rel": v["rel"], "pages": sorted(v["pages"])}
    except Exception as e:
        eres[h] = {"error": repr(e)[:200], "rel": v["rel"], "pages": sorted(v["pages"])}
    time.sleep(1.5)
R["external_links"] = eres

# Googlebot view of the homepage (same bytes as a normal visitor?)
try:
    gb = requests.get(BASE + "/", headers={"User-Agent": UA_BOT}, timeout=25)
    nb = S.get(BASE + "/", timeout=25)
    R["googlebot_same_as_visitor"] = {"googlebot_status": gb.status_code, "same_bytes": gb.content == nb.content}
except Exception as e:
    R["googlebot_same_as_visitor"] = {"error": repr(e)[:200]}

# Google's official PageSpeed Insights API (no key; may be rate limited)
psi = {}
for u in [BASE + "/", BASE + "/mug-designer/", BASE + "/horse-racing-gifts/"]:
    for strat in ("mobile", "desktop"):
        api = ("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=%s&strategy=%s"
               "&category=performance&category=seo&category=best-practices&category=accessibility") % (urllib.parse.quote(u, safe=""), strat)
        try:
            r = requests.get(api, timeout=120)
            if r.status_code != 200:
                psi["%s %s" % (u, strat)] = {"status": r.status_code, "body": r.text[:300]}
                continue
            j = r.json()
            lr = j.get("lighthouseResult", {})
            cats = {k: round((v.get("score") or 0) * 100) for k, v in lr.get("categories", {}).items()}
            au = lr.get("audits", {})
            keep = {}
            for k in ("first-contentful-paint", "largest-contentful-paint", "total-blocking-time", "cumulative-layout-shift",
                      "speed-index", "total-byte-weight", "render-blocking-resources", "unused-javascript", "uses-optimized-images",
                      "modern-image-formats", "uses-responsive-images", "server-response-time", "font-display", "unminified-javascript",
                      "uses-text-compression", "dom-size", "bootup-time", "mainthread-work-breakdown", "largest-contentful-paint-element",
                      "is-crawlable", "document-title", "meta-description", "link-text", "crawlable-anchors", "image-alt", "hreflang",
                      "canonical", "robots-txt", "tap-targets", "font-size", "color-contrast"):
                if k in au:
                    a = au[k]
                    keep[k] = {"score": a.get("score"), "display": a.get("displayValue"), "title": a.get("title")}
                    if k in ("render-blocking-resources", "unused-javascript", "largest-contentful-paint-element", "total-byte-weight", "modern-image-formats", "uses-optimized-images"):
                        items = (a.get("details") or {}).get("items") or []
                        keep[k]["items"] = [{kk: it.get(kk) for kk in ("url", "totalBytes", "wastedBytes", "wastedMs", "node") if kk in it} for it in items[:8]]
            fld = j.get("loadingExperience", {}).get("overall_category")
            psi["%s %s" % (u, strat)] = {"categories": cats, "audits": keep, "field_data": fld}
        except Exception as e:
            psi["%s %s" % (u, strat)] = {"error": repr(e)[:200]}
        time.sleep(3)
R["pagespeed"] = psi


def dflt(o):
    if isinstance(o, set):
        return sorted(o)
    return str(o)


json.dump(R, open(os.path.join(out, "report.json"), "w"), indent=1, default=dflt)

# short markdown summary
L = ["# Live SEO audit %s" % R["run_utc"], ""]
L.append("## DNS"); [L.append("- %s: %s" % (k, v)) for k, v in R["dns"].items()]
L.append("\n## TLS"); [L.append("- %s: %s" % (k, v)) for k, v in R["tls"].items()]
L.append("\n## Redirects")
for k, v in R["redirects"].items():
    L.append("- %s -> %s" % (k, " -> ".join("%s %s" % (h.get("status", h.get("error")), h.get("location") or "") for h in v)))
L.append("\n## Pages")
for u, p in R["pages"].items():
    L.append("- %s: %s %s bytes %ss | %s | robots=%s | canon=%s | h1=%s | jsonld=%s | words=%s" % (
        u, p.get("status"), p.get("bytes"), p.get("secs"), p.get("title"), p.get("robots"), p.get("canonical"), p.get("h1"), p.get("jsonld"), p.get("text_words")))
L.append("\n## Broken or odd assets")
for a, v in R["assets"].items():
    if v.get("external"):
        continue
    if v.get("status") != 200 or (v.get("bytes") or 0) > 300000:
        L.append("- %s: %s %s bytes (used on %d pages)" % (a, v.get("status", v.get("error")), v.get("bytes"), len(v.get("used_on", []))))
L.append("\n## External links")
for h, v in R["external_links"].items():
    L.append("- %s: %s (rel=%s, on %d pages)" % (h, v.get("status", v.get("error")), v.get("rel"), len(v.get("pages", []))))
L.append("\n## PageSpeed (Google API)")
for k, v in R["pagespeed"].items():
    L.append("- %s: %s" % (k, v.get("categories") or v.get("status") or v.get("error")))
    for ak in ("largest-contentful-paint", "total-blocking-time", "cumulative-layout-shift", "total-byte-weight"):
        if ak in (v.get("audits") or {}):
            L.append("    - %s: %s" % (ak, v["audits"][ak].get("display")))
open(os.path.join(out, "report.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L))
