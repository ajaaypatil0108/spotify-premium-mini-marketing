# Builds docs/index.html (GitHub Pages) and the case-study PDF from one source.
from model import BUDGET, alloc, working, CPM, scen, out, rev, weekly, monthly, passes, upg, months

def L(x):  # rupees -> "₹x.x L"
    return f"₹{x/1e5:.1f}L"
def n(x):
    return f"{round(x):,}"

G = "#1DB954"
LOGO = f'''<svg viewBox="0 0 40 40" width="40" height="40" aria-hidden="true"><rect width="40" height="40" rx="10" fill="{G}"/>
<rect x="9" y="17" width="4" height="14" rx="2" fill="#121212"/><rect x="15.5" y="10" width="4" height="21" rx="2" fill="#121212"/>
<rect x="22" y="14" width="4" height="17" rx="2" fill="#121212"/><rect x="28.5" y="20" width="4" height="11" rx="2" fill="#121212"/></svg>'''

# ---------- charts (inline SVG) ----------
def budget_chart():
    W, rowh, lw = 640, 34, 270
    h = rowh*len(alloc)+10
    mx = max(s for _, s, _ in alloc)
    rows = []
    for i, (name, s, _) in enumerate(alloc):
        y = i*rowh+6
        bw = (W-lw-90)*s/mx
        col = G if i < 4 else "#535353"
        rows.append(f'<text x="0" y="{y+17}" class="lbl">{name}</text>'
                    f'<rect x="{lw}" y="{y+4}" width="{bw:.1f}" height="18" rx="3" fill="{col}"/>'
                    f'<text x="{lw+bw+8:.1f}" y="{y+17}" class="val">{L(BUDGET*s)} · {s:.0%}</text>')
    return f'<div class="cw"><svg viewBox="0 0 {W} {h}" class="chart" role="img" aria-label="Budget allocation by channel">{"".join(rows)}</svg></div>'

def price_chart():
    items = [("Premium Mini, daily (₹7)", 7.0), ("Premium Individual, monthly (₹119)", monthly/30), ("Premium Mini, weekly (₹25)", weekly/7)]
    W, rowh, lw = 640, 34, 270
    rows = []
    for i, (name, v) in enumerate(items):
        y = i*rowh+6
        bw = (W-lw-90)*v/7
        rows.append(f'<text x="0" y="{y+17}" class="lbl">{name}</text>'
                    f'<rect x="{lw}" y="{y+4}" width="{bw:.1f}" height="18" rx="3" fill="{G if i!=1 else "#b3b3b3"}"/>'
                    f'<text x="{lw+bw+8:.1f}" y="{y+17}" class="val">₹{v:.2f}/day</text>')
    return f'<div class="cw"><svg viewBox="0 0 {W} {rowh*3+10}" class="chart" role="img" aria-label="Cost per day by plan">{"".join(rows)}</svg></div>'

def timeline_chart():
    phases = [("1 · Pre-launch prep", 0, 4, "#535353"), ("2 · Launch & awareness", 4, 6, G),
              ("3 · Consideration", 6, 10, G), ("4 · Conversion", 10, 14, G), ("Optimize (monthly reviews)", 4, 14, "#2e77d0")]
    W, lw, rowh, wk = 640, 200, 32, (640-200-10)/14
    rows = [f'<text x="{lw+i*wk:.1f}" y="12" class="tick">W{i+1}</text>' for i in range(0, 14, 2)]
    for i, (name, a, b, c) in enumerate(phases):
        y = 22+i*rowh
        rows.append(f'<text x="0" y="{y+15}" class="lbl">{name}</text><rect x="{lw+a*wk:.1f}" y="{y+2}" width="{(b-a)*wk-3:.1f}" height="18" rx="3" fill="{c}"/>')
    return f'<div class="cw"><svg viewBox="0 0 {W} {22+rowh*len(phases)}" class="chart" role="img" aria-label="14-week campaign timeline">{"".join(rows)}</svg></div>'

# ---------- content ----------
b = out["Base"]
breakeven_buyers = working/rev
be_rate = breakeven_buyers/b["views"]

def scen_table():
    hdr = "<tr><th></th>" + "".join(f"<th>{k}</th>" for k in scen) + "</tr>"
    def row(label, f):
        return f"<tr><td>{label}</td>" + "".join(f"<td>{f(k)}</td>" for k in scen) + "</tr>"
    rows = [
        row("Click-through rate", lambda k: f"{scen[k][0]:.1%}"),
        row("Click → plan page view", lambda k: f"{scen[k][1]:.0%}"),
        row("Plan page → first Mini purchase", lambda k: f"{scen[k][2]:.0%}"),
        row("Impressions", lambda k: n(out[k]["imp"])),
        row("Clicks", lambda k: n(out[k]["clicks"])),
        row("<b>New paying users</b>", lambda k: f"<b>{n(out[k]['buyers'])}</b>"),
        row("Cost per new payer (CPA)", lambda k: f"₹{out[k]['cpa']:,.0f}"),
        row("Expected gross revenue", lambda k: L(out[k]["rev"])),
        row("Revenue ÷ working media", lambda k: f"{out[k]['rev']/working:.2f}x"),
    ]
    return f'<div class="tw"><table>{hdr}{"".join(rows)}</table></div>'

def budget_table():
    rows = "".join(f"<tr><td>{nm}</td><td>{s:.0%}</td><td>{L(BUDGET*s)}</td><td>{role}</td></tr>" for nm, s, role in alloc)
    return (f'<div class="tw"><table><tr><th>Channel</th><th>Share</th><th>Budget</th><th>Job in the funnel</th></tr>{rows}'
            f'<tr class="tot"><td>Total</td><td>100%</td><td>{L(BUDGET)}</td><td>Paid media: {L(working)} (first four rows)</td></tr></table></div>')

SECTIONS = []
def sec(id_, title, body):
    SECTIONS.append((id_, title, body))

sec("product", "1 · The product", f"""
<p>Premium Mini is Spotify's short-term pass for India. At launch it cost <b>₹7 for a day</b> or <b>₹25 for a week</b>.<sup>1</sup> It gives ad-free listening, but it works on mobile only, and offline downloads are capped at <b>30 songs on one device</b>.<sup>2</sup> The full Premium Individual plan cost <b>₹119 a month</b> at the time of this project.<sup>3</sup></p>
{price_chart()}
<p class="note"><b>The insight that shapes the plan:</b> the weekly pass is cheaper per day than the monthly plan (₹3.57 vs ₹3.97). Four weeks of passes cost ₹100, or about ₹107 for 30 days. So the upgrade from Mini to monthly cannot be sold on price. It has to be sold on what Mini lacks: desktop and web access, unlimited downloads, and not having to renew every week.</p>
""")

sec("audience", "2 · Who we target", """
<div class="grid4">
<div class="card"><h4>Students</h4><p>18–24, on a tight budget, already stream daily. Want ad-free listening during exams and commutes.</p></div>
<div class="card"><h4>Occasion listeners</h4><p>Want Premium for a road trip, a wedding, or a house party, not every month.</p></div>
<div class="card"><h4>Casual free users</h4><p>Tolerate ads today. A ₹7 day pass shows them what ad-free feels like.</p></div>
<div class="card"><h4>Mobile-first, Tier 2–3 cities</h4><p>Pay with UPI, prefer small prepaid amounts, and have no reason to want desktop access.</p></div>
</div>
<p>All four groups share three traits: they are price-sensitive, they dislike ads, and they live on their phones. Mini's mobile-only limit doesn't hurt them.</p>
""")

sec("goals", "3 · Goals and KPIs", f"""
<div class="tw"><table>
<tr><th>Goal</th><th>Target</th><th>By</th><th>KPIs</th></tr>
<tr><td>Awareness</td><td>+20% branded searches for "Premium Mini" vs. pre-campaign baseline</td><td>End of week 8 (first month after launch)</td><td>Branded search volume, impressions, reach, video views</td></tr>
<tr><td>First purchase</td><td>+15% relative lift in the free → first-Mini-purchase rate vs. baseline</td><td>End of week 14</td><td>Purchase rate, new paying users, CPA</td></tr>
<tr><td>Repeat</td><td>Average {passes} weekly passes per new payer in the first 90 days</td><td>90 days after first purchase</td><td>Repeat purchase rate, passes per payer</td></tr>
<tr><td>Upgrade</td><td>{upg:.0%} of new payers move to monthly Premium</td><td>90 days after first purchase</td><td>Mini → monthly upgrade rate</td></tr>
</table></div>
<p class="note">Mini is a paid pass, not a free trial, so conversion is measured in two steps: free user → first Mini purchase, then Mini buyer → monthly subscriber.</p>
""")

sec("budget", "4 · Channels and budget", f"""
<p class="assume">Assumption: a total budget of <b>₹50 lakh</b> (₹5,000,000). This is an illustrative figure for planning, not a Spotify number.</p>
{budget_chart()}
{budget_table()}
<ul>
<li><b>Instagram and YouTube get half the budget</b> because short video is where students and occasion listeners spend their time. Retargeting reaches people who visited the plan page but didn't buy.</li>
<li><b>Creators get 20%</b> because peer recommendation drives app choice for this audience. Creators show the product in a real moment, like a road-trip playlist.</li>
<li><b>Search gets 15%</b> to capture people already looking for "cheap Spotify Premium" or "Spotify ad-free".</li>
<li><b>CRM and in-app get only 5%</b> because they cost almost nothing per message. Existing free users are the cheapest audience to convert, and push, email and in-app banners reach them without buying media.</li>
</ul>
""")

sec("timeline", "5 · Timeline (14 weeks)", f"""
{timeline_chart()}
<div class="tw"><table>
<tr><th>Phase</th><th>Weeks</th><th>What happens</th><th>Spend</th></tr>
<tr><td>1 · Pre-launch prep</td><td>1–4</td><td>Final audience and messaging, produce creatives, sign creators, set up tracking, A/B test headlines</td><td>Production only</td></tr>
<tr><td>2 · Launch &amp; awareness</td><td>5–6</td><td>Reels, Shorts and pre-roll go live; creator posts drop; watch reach and CTR daily</td><td>~30% of paid media</td></tr>
<tr><td>3 · Consideration</td><td>7–10</td><td>Feature-led ads (ad-free, offline); retarget plan-page visitors; in-app banners to free users</td><td>~35%</td></tr>
<tr><td>4 · Conversion</td><td>11–14</td><td>Time-limited offers, push reminders when a pass expires, upgrade prompts to monthly</td><td>~35%</td></tr>
</table></div>
<p><b>Moments to plan around:</b> Holi, the IPL season, wedding season, and summer travel. Each is a short window when an occasion listener wants Premium for a few days, which is exactly what Mini sells. The 5% reserve funds bursts around these moments.</p>
""")

sec("creative", "6 · Campaign assets", """
<div class="grid2">
<div class="card"><h4>Social ad copy</h4><p>"Road trip this weekend? ₹25 covers the whole week. No ads, no interruptions."</p><p>"Exam week. Your playlist, without the ads. Try Premium Mini from ₹7."</p></div>
<div class="card"><h4>Display &amp; search copy</h4><p>"Ad-free Spotify from ₹7 a day. Pay with UPI. No subscription."</p><p>"Going offline? Save up to 30 songs with Premium Mini."</p></div>
<div class="card"><h4>Visuals</h4><p>Phone screen showing an ad-free queue; a 6-second Reel cutting from an ad break to uninterrupted music; carousel of "moments" (trip, wedding, exam).</p></div>
<div class="card"><h4>Upgrade messages (to Mini buyers)</h4><p>"Your pass ends tonight. Keep listening on every device with Premium."</p><p>"Bought 3 weeks in a row? Go monthly and stop renewing."</p></div>
</div>
<p class="note">Every claim in the copy matches what Mini actually includes. The copy never promises desktop access or unlimited downloads.</p>
""")

sec("funnel", "7 · Expected results", f"""
<p class="assume">Assumptions: paid media of {L(working)}, a blended CPM of ₹{CPM}, and the funnel rates below. These are planning estimates, not industry benchmarks. Revenue per new payer is gross (before royalties and payment fees): {passes} weekly passes (₹{passes*weekly}) plus a {upg:.0%} chance of upgrading to monthly for {months} months (₹{upg*monthly*months:.1f}), which totals <b>₹{rev:.1f}</b>.</p>
{scen_table()}
<p><b>Reading the base case:</b> the campaign brings in about <b>{n(b['buyers'])} new paying users</b> at roughly <b>₹{b['cpa']:,.0f} each</b>. Each payer is worth about ₹{rev:.0f} in gross revenue, so paid media alone does not pay back within six months. To break even, the plan-page purchase rate would need to reach about <b>{be_rate:.0%}</b> instead of the assumed 8%. Only the bull case clears that bar.</p>
<p class="note"><b>Why this replaces the "3X users" claim:</b> the original draft said users would grow up to 3X. That can't be checked without Spotify's current Mini subscriber count, so this version estimates the number of new paying users and shows the math behind it.</p>
""")

sec("recs", "8 · Recommendations", f"""
<ol>
<li><b>Lead with owned channels.</b> In-app banners and push messages to existing free users cost almost nothing, so they lower the blended CPA the most. Scale them first.</li>
<li><b>Treat launch as a test.</b> Use weeks 5–6 to check each channel's CPA against the ₹{rev:.0f} break-even, then move the remaining 70% of paid media to the channels that beat it.</li>
<li><b>Grow repeat purchases.</b> Each extra weekly pass per payer adds ₹{weekly} of revenue. A loyalty nudge (for example, a discount after several passes) is cheaper than buying new users.</li>
<li><b>Sell the upgrade on features, not price.</b> Weekly passes are cheaper per day than monthly, so the upgrade message should stress all-device access, unlimited downloads and not having to renew.</li>
</ol>
""")

sec("risks", "9 · Risks and limits", """
<ul>
<li><b>Cannibalization:</b> some monthly subscribers could switch to weekly passes and pay Spotify less. Track downgrades alongside new payers.</li>
<li><b>Mobile only:</b> Mini cannot reach desktop listeners, so desktop placements are wasted spend.</li>
<li><b>Assumed numbers:</b> the budget, CPM and funnel rates are illustrative. Real campaign data would replace them after the test phase.</li>
<li><b>Prices change:</b> prices shown are launch-era figures. Spotify has since changed its India pricing, so they should be checked before any real use.</li>
</ul>
""")

SOURCES = [
    ("exchange4media — Spotify unveils 2 Premium Mini plans (Feb 2021)", "https://www.exchange4media.com/marketing-news/spotify-unveils-2-premium-mini-plans-for-listeners-to-have-uninterrupted-music-experience-110963.html"),
    ("TechStory — Spotify's new daily and weekly plans are cheaper now (Dec 2020)", "https://techstory.in/?p=325135"),
    ("Music Business Worldwide — Spotify cuts Premium prices in India (notes ₹119 monthly price before the Aug 2025 increase)", "https://www.musicbusinessworldwide.com/spotify-cuts-premium-prices-in-india-by-30-and-scraps-lite-tier-just-six-months-after-launching-it/"),
]

CSS = f"""
:root{{--bg:#121212;--s1:#181818;--s2:#242424;--line:#2a2a2a;--g:{G};--t:#fff;--m:#b3b3b3;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--t);font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.6;font-size:16px}}
a{{color:var(--g)}}
.wrap{{max-width:900px;margin:0 auto;padding:0 20px}}
header.hero{{background:linear-gradient(180deg,#1f5f3a 0%,#163d27 45%,var(--bg) 100%);padding:56px 0 40px}}
.brand{{display:flex;align-items:center;gap:12px;font-weight:700;letter-spacing:.02em;color:var(--m);font-size:14px;text-transform:uppercase}}
h1{{font-size:clamp(30px,5vw,48px);line-height:1.1;margin:18px 0 12px;letter-spacing:-.02em}}
.sub{{color:var(--m);max-width:640px;margin:0}}
.meta{{margin-top:18px;color:var(--m);font-size:14px}}
.meta b{{color:var(--t)}}
.btns{{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}}
.btn{{display:inline-block;background:var(--g);color:#000;font-weight:700;padding:12px 22px;border-radius:999px;text-decoration:none}}
.btn.alt{{background:transparent;color:var(--t);border:1px solid #727272}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:28px 0 0}}
.kpi{{background:var(--s1);border-radius:10px;padding:16px}}
.kpi .v{{font-size:24px;font-weight:800;color:var(--g)}}
.kpi .k{{font-size:13px;color:var(--m)}}
nav.toc{{display:flex;gap:8px;flex-wrap:wrap;margin:32px 0 0}}
nav.toc a{{background:var(--s2);color:var(--t);text-decoration:none;padding:6px 12px;border-radius:999px;font-size:13px}}
section{{padding:36px 0;border-bottom:1px solid var(--line)}}
h2{{font-size:26px;margin:0 0 16px;letter-spacing:-.01em}}
h4{{margin:0 0 6px;font-size:16px}}
p,li{{color:#e6e6e6}}
.note{{background:var(--s1);border-left:3px solid var(--g);padding:12px 16px;border-radius:6px}}
.assume{{background:#2a2410;border-left:3px solid #f59b23;padding:12px 16px;border-radius:6px}}
.grid4{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}}
.grid2{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:12px}}
.card{{background:var(--s1);border-radius:10px;padding:16px}}
.card p{{margin:6px 0;color:var(--m)}}
.tw{{overflow-x:auto;margin:16px 0}}
table{{border-collapse:collapse;width:100%;font-size:14px}}
th{{text-align:left;color:var(--m);font-weight:600;border-bottom:1px solid #3e3e3e;padding:8px 10px}}
td{{border-bottom:1px solid var(--line);padding:8px 10px;vertical-align:top}}
tr.tot td{{font-weight:700;border-top:1px solid #3e3e3e}}
svg.chart{{width:100%;height:auto;margin:12px 0;display:block}}
.cw{{overflow-x:auto}}
@media (max-width:640px){{svg.chart{{min-width:600px}}}}
svg .lbl{{fill:#e6e6e6;font-size:13px;font-family:Inter,sans-serif}}
svg .val{{fill:#b3b3b3;font-size:12px;font-family:Inter,sans-serif}}
svg .tick{{fill:#727272;font-size:11px;font-family:Inter,sans-serif}}
sup{{color:var(--g)}}
footer{{padding:32px 0 48px;color:var(--m);font-size:13px}}
footer ol{{padding-left:18px}} footer li{{color:var(--m)}}
@media (max-width:640px){{.kpis{{grid-template-columns:repeat(2,1fr)}}.grid4,.grid2{{grid-template-columns:1fr}}}}
"""

PRINT_CSS = """
@page{size:A4;margin:0}
body{font-size:12.5px;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.wrap{max-width:none;padding:0 16mm}
header.hero{padding:10mm 0 8mm}
nav.toc,.btns{display:none}
section{padding:10mm 0 6mm;break-inside:avoid}
h2{font-size:20px;break-after:avoid}
.card,.note,.assume,table,svg.chart,.kpi{break-inside:avoid}
#audience,#budget,#timeline,#creative,#funnel,#recs{break-before:page}
#audience{break-before:auto}
footer{padding:6mm 0 10mm}
"""


def og_card():
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
body{{margin:0;width:1200px;height:627px;background:linear-gradient(135deg,#1f5f3a 0%,#163d27 40%,#121212 100%);color:#fff;font-family:Inter,sans-serif;display:flex;flex-direction:column;justify-content:center;padding:0 80px;box-sizing:border-box}}
.brand{{display:flex;align-items:center;gap:16px;color:#b3b3b3;font-weight:700;font-size:22px;letter-spacing:.04em;text-transform:uppercase}}
h1{{font-size:68px;line-height:1.05;margin:28px 0 18px;letter-spacing:-.02em}}
p{{font-size:26px;color:#d0d0d0;margin:0 0 40px}}
.k{{display:flex;gap:18px}} .k div{{background:rgba(24,24,24,.85);border-radius:14px;padding:18px 26px}}
.k b{{display:block;color:{G};font-size:36px}} .k span{{color:#b3b3b3;font-size:18px}}
</style></head><body>
<div class="brand">{LOGO.replace('width="40" height="40"','width="56" height="56"')}<span>Case study · Ajay Patil</span></div>
<h1>Growing Spotify Premium Mini in India</h1>
<p>Performance marketing plan: audience, budget, timeline and funnel estimate</p>
<div class="k"><div><b>₹50L</b><span>Illustrative budget</span></div><div><b>14 weeks</b><span>Campaign</span></div><div><b>{n(b['buyers'])}</b><span>New payers, base case</span></div></div>
</body></html>"""

def page(printing=False):
    toc = "".join(f'<a href="#{i}">{t.split(" · ")[1]}</a>' for i, t, _ in SECTIONS)
    body = "".join(f'<section id="{i}"><h2>{t}</h2>{c}</section>' for i, t, c in SECTIONS)
    srcs = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in SOURCES)
    fonts = "" if printing else '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">'
    desc = "A performance marketing plan for Spotify Premium Mini in India: audience, goals, a ₹50 lakh channel budget, a 14-week timeline and a funnel estimate of results."
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Premium Mini Growth Plan — Ajay Patil</title><meta name="description" content="{desc}">
<meta property="og:title" content="Performance Marketing Strategy: Spotify Premium Mini (India)"><meta property="og:description" content="{desc}">
<meta property="og:type" content="website"><meta property="og:url" content="https://ajaaypatil0108.github.io/REPO_NAME/">
<meta property="og:image" content="https://ajaaypatil0108.github.io/REPO_NAME/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="627">
<meta property="og:image:alt" content="Case study cover: Growing Spotify Premium Mini in India, by Ajay Patil">
<meta name="twitter:card" content="summary_large_image"><meta name="author" content="Ajay Patil">
{fonts}<style>{CSS}{PRINT_CSS if printing else ""}</style></head><body>
<header class="hero"><div class="wrap">
<div class="brand">{LOGO}<span>Case study · Performance marketing</span></div>
<h1>Growing Spotify Premium Mini in India</h1>
<p class="sub">A performance marketing plan to turn free listeners into first-time payers, then move them to monthly Premium: audience, goals, a channel budget, a 14-week timeline and an estimate of results.</p>
<p class="meta"><b>Ajay Patil</b> · Personal project · Feb 2024 · Revised Oct 2026</p>
<div class="btns"><a class="btn" href="Spotify_Premium_Mini_Strategy.pdf" download>Download the PDF</a><a class="btn alt" href="https://github.com/ajaaypatil0108/REPO_NAME">View on GitHub</a></div>
<div class="kpis">
<div class="kpi"><div class="v">₹50L</div><div class="k">Illustrative budget</div></div>
<div class="kpi"><div class="v">14 wks</div><div class="k">Campaign length</div></div>
<div class="kpi"><div class="v">{n(b['buyers'])}</div><div class="k">New payers, base case</div></div>
<div class="kpi"><div class="v">₹{b['cpa']:,.0f}</div><div class="k">Cost per new payer, base</div></div>
</div>
<nav class="toc">{toc}</nav>
</div></header>
<main class="wrap">{body}</main>
<footer class="wrap"><p><b>Sources</b></p><ol>{srcs}</ol>
<p>Independent student project. Not affiliated with or endorsed by Spotify. Spotify and Premium Mini are trademarks of Spotify AB. All campaign figures are illustrative assumptions.</p></footer>
</body></html>"""

if __name__ == "__main__":
    import os, sys
    repo = sys.argv[1] if len(sys.argv) > 1 else "REPO_NAME"
    os.makedirs("docs", exist_ok=True)
    open("docs/index.html", "w", encoding="utf-8").write(page().replace("REPO_NAME", repo))
    open("print.html", "w", encoding="utf-8").write(page(True).replace("REPO_NAME", repo))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page()
        pg.goto("file://" + os.path.abspath("print.html")); pg.wait_for_timeout(300)
        pg.pdf(path="Spotify_Premium_Mini_Strategy.pdf", format="A4", print_background=True)
        pg2 = br.new_page(viewport={"width": 1200, "height": 627})
        pg2.set_content(og_card()); pg2.wait_for_timeout(300)
        pg2.screenshot(path="docs/og-image.png")
        br.close()
    print("built")
