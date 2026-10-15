"""Genera los gráficos SVG del README con el sistema visual de Inzomio.

Tokens de la guía de estilos v2: crema, tinta y amarillo acento; Bricolage
Grotesque 800 para títulos y DM Sans para el resto. Las fuentes se embeben
(subset) para que GitHub las muestre dentro de <img>.

Uso: python3 tools/build_assets.py
"""
import base64
import html
import io
import re
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets"
FONTS = Path(__file__).resolve().parent / "fonts"

BG, INK, CARD, MUTED = "#f8f9e9", "#0a0a0a", "#ffffff", "#efefe2"
MUTED_INK, BORDER, ACCENT, ACCENT_DARK = "#7a7a6e", "#e3e3d4", "#fab200", "#7a5200"
SUCCESS, WORDMARK = "#2e7d32", "#c7c7c7"


def font_b64(path, text):
    font = TTFont(path)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    sub = subset.Subsetter(opts)
    sub.populate(text=text + " ")
    sub.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def svg(w, h, body, bg=BG):
    text = html.unescape(re.sub(r"<[^>]+>", "", body))
    style = (
        "@font-face{font-family:'Bricolage Grotesque';font-weight:800;"
        f"src:url(data:font/woff2;base64,{font_b64(FONTS / 'BricolageGrotesque-800-latin.woff2', text)}) format('woff2')}}"
        "@font-face{font-family:'DM Sans';font-weight:100 1000;"
        f"src:url(data:font/woff2;base64,{font_b64(FONTS / 'DMSans-latin.woff2', text)}) format('woff2')}}"
        ".h{font-family:'Bricolage Grotesque',Arial,sans-serif;font-weight:800}"
        ".b{font-family:'DM Sans',Arial,sans-serif;font-weight:400}"
        ".m{font-family:'DM Sans',Arial,sans-serif;font-weight:500}"
        ".s{font-family:'DM Sans',Arial,sans-serif;font-weight:700}"
        f".k{{font-family:'DM Sans',Arial,sans-serif;font-weight:500;font-size:11px;letter-spacing:.12em;fill:{MUTED_INK}}}"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f"<style>{style}</style>"
        f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0 0L10 5L0 10z" fill="{INK}"/></marker></defs>'
        f'<rect width="{w}" height="{h}" rx="10" fill="{bg}"/>{body}</svg>'
    )


def card(x, y, w, h, selected=False, fill=CARD):
    stroke = f'stroke="{ACCENT}" stroke-width="2"' if selected else f'stroke="{BORDER}"'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" {stroke}/>'


def t(x, y, s, cls="b", size=13, fill=INK, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{s}</text>')


def kicker(x, y, s, anchor="start"):
    return f'<text x="{x}" y="{y}" class="k" text-anchor="{anchor}">{s.upper()}</text>'


def badge(x, y, s, on=True):
    w = 26 + len(s) * 7
    bg = "#fef3d6" if on else MUTED
    dot = ACCENT if on else MUTED_INK
    col = ACCENT_DARK if on else MUTED_INK
    return (f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="6" fill="{bg}" stroke="{BORDER}"/>'
            f'<circle cx="{x + 12}" cy="{y + 12}" r="3" fill="{dot}"/>' + t(x + 21, y + 16, s, "m", 12, col))


SYMBOL = (ROOT / "docs" / "brand" / "inzomio-symbol.svg").read_text()


def favicon(x, y, size=44):
    """Símbolo de marca (mascota sobre naranja), anidado como SVG."""
    body = SYMBOL[SYMBOL.index("<svg"):]
    body = body.replace("<svg ", f'<svg x="{x}" y="{y}" width="{size}" height="{size}" ', 1)
    body = re.sub(r"<defs>.*?</defs>", "", body, flags=re.S)
    body = body.replace('class="cls-2"', f'fill="{ACCENT}" rx="200"').replace('class="cls-1"', f'fill="{WORDMARK}"')
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * 0.22}" fill="{ACCENT}"/>'
            f'<g>{body}</g>')


def arrow(d, dashed=False):
    dash = 'stroke-dasharray="5 5"' if dashed else ""
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.5" {dash} marker-end="url(#a)"/>'


# ---------------------------------------------------------------- banner
def banner():
    b = favicon(80, 62, 64)
    b += kicker(160, 100, "Portfolio · product case study")
    b += t(76, 228, "Inzomio", "h", 110, INK, extra='letter-spacing="-2"')
    b += f'<rect x="82" y="252" width="120" height="6" rx="3" fill="{ACCENT}"/>'
    b += t(80, 306, "Online bookings for independent professionals:", "b", 24)
    b += t(80, 340, "own website, link in bio, bookings and an AI agent.", "b", 24, MUTED_INK)
    # Tarjeta flotante: el agente respondiendo
    b += card(840, 50, 380, 330)
    b += kicker(864, 82, "Business agent")
    b += f'<rect x="1000" y="100" width="196" height="40" rx="10" fill="{ACCENT}"/>'
    b += t(1186, 125, "How much is a massage?", "m", 13, INK, "end")
    b += card(864, 156, 300, 108, fill=MUTED)
    b += t(882, 182, "Relaxing massage: 60 min,", "b", 13) + t(882, 202, "$18.000 with a $5.000 deposit.", "b", 13)
    b += f'<rect x="882" y="218" width="84" height="30" rx="10" fill="{INK}"/>' + t(924, 238, "Book", "m", 13, CARD, "middle")
    b += card(974, 218, 110, 30) + t(1029, 238, "See services", "m", 12, INK, "middle")
    b += f'<rect x="864" y="290" width="332" height="44" rx="22" fill="{CARD}" stroke="{BORDER}"/>'
    b += t(886, 317, "Ask the agent anything…", "b", 13, MUTED_INK)
    b += f'<circle cx="1174" cy="312" r="14" fill="{ACCENT}"/>'
    b += t(864, 362, "Answers 24/7 from the business knowledge base", "b", 12, MUTED_INK)
    b += t(80, 400, "Next.js · React · TypeScript · Supabase · Vercel · Claude Haiku · Built with Claude Code", "m", 14, MUTED_INK)
    return svg(1280, 440, b)


# ---------------------------------------------------------------- process
def process():
    steps = [("01", "Spot", "a problem"), ("02", "Understand", "the need behind it"),
             ("03", "Hypothesize", "a solution"), ("04", "Iterate", "build · test · observe · fix")]
    b = kicker(40, 46, "Method") + t(40, 80, "The same loop, at every stage", "h", 28)
    x = 40
    for i, (n, title, sub) in enumerate(steps):
        w = 190 if i < 3 else 220
        b += card(x, 116, w, 120)
        b += t(x + 20, 146, n, "m", 12, MUTED_INK) + t(x + 20, 182, title, "h", 22) + t(x + 20, 210, sub, "b", 14, MUTED_INK)
        b += arrow(f"M{x + w + 4} 176 L{x + w + 22} 176")
        x += w + 26
    b += card(x, 116, 1200 - 40 - x, 120, True)
    b += t(x + 20, 146, "05", "m", 12, ACCENT_DARK) + t(x + 20, 182, "Production", "h", 22) + t(x + 20, 210, "live product", "b", 14, MUTED_INK)
    b += arrow("M798 240 C798 280 567 280 567 244", True)
    b += t(682, 296, "repeat until it holds", "b", 12, MUTED_INK, "middle")
    return svg(1200, 320, b)


# ---------------------------------------------------------------- modules
def modules():
    mods = [("Own website", ["Hero, services, gallery,", "map and its own colors.", "Indexed by Google."]),
            ("Bookings", ["Confirm on their own", "against the real agenda.", "Transfer or cash."]),
            ("Inzomio Link", ["Link in bio with booking,", "WhatsApp, services and", "FAQ. Free forever."]),
            ("AI agent", ["Answers clients 24/7 and", "briefs the owner on their", "own business data."]),
            ("Admin panel", ["Bookings, clients, services,", "page builder and plan.", "Mobile first."])]
    b = kicker(40, 46, "Product") + t(40, 80, "Everything a service business needs, in one place", "h", 28)
    for i, (name, lines) in enumerate(mods):
        x = 40 + i * 228
        b += card(x, 112, 212, 210, name == "AI agent")
        b += f'<rect x="{x + 18}" y="132" width="40" height="40" rx="10" fill="{ACCENT if name == "AI agent" else MUTED}"/>'
        b += t(x + 38, 159, f"0{i + 1}", "s", 14, INK, "middle")
        b += t(x + 18, 210, name, "h", 19)
        for j, ln in enumerate(lines):
            b += t(x + 18, 240 + j * 20, ln, "b", 13, MUTED_INK)
    return svg(1200, 350, b)


# ---------------------------------------------------------------- agent
def agent():
    b = kicker(40, 46, "AI agent") + t(40, 80, "Two agents: one for clients, one for the owner", "h", 28)
    # Agente de clientes
    b += card(40, 110, 550, 470, True)
    b += kicker(64, 140, "Client agent · public page") + t(64, 172, "Answers whoever visits the business", "h", 19)
    b += card(64, 196, 502, 64, fill=MUTED) + t(82, 222, "Free / Profesional", "s", 14)
    b += t(82, 244, "FAQ matcher over hand-loaded questions. No AI, no API cost.", "b", 13, MUTED_INK)
    b += card(64, 270, 502, 76, fill=MUTED) + t(82, 296, "Empresas", "s", 14)
    b += t(82, 318, "Conversational agent: Claude Haiku 4.5 or TypeSafe (Jev),", "b", 13, MUTED_INK)
    b += t(82, 336, "engine chosen per business from Super Admin.", "b", 13, MUTED_INK)
    b += kicker(64, 368, "Can do")
    for k, c in enumerate(["Look up services", "Search knowledge base"]):
        b += card(64 + k * 190, 378, 178, 32) + t(78 + k * 190, 399, c, "m", 12)
    b += t(64, 436, "Shows shortcut cards (see services, book) inside the chat.", "b", 13)
    b += t(64, 460, "Never books by itself: hands off to the booking page or", "b", 13)
    b += t(64, 480, "WhatsApp, so the AI can't make a booking mistake.", "b", 13)
    b += t(64, 512, "Usage limits keep AI cost under control.", "b", 13, MUTED_INK)
    b += t(64, 552, "Knowledge base: services, policies, aftercare, brand tone.", "b", 13, MUTED_INK)
    # Agente interno
    b += card(610, 110, 550, 470)
    b += kicker(634, 140, "Internal agent · admin panel") + t(634, 172, "Answers the owner with real business data", "h", 19)
    caps = ["Bookings for a day or range", "Unconfirmed bookings", "Pending balances", "Client search",
            "Business summary", "Services and profile", "How-to guide for the panel"]
    for k, c in enumerate(caps):
        b += card(634 + (k % 2) * 254, 196 + (k // 2) * 40, 242, 32, fill=MUTED) + t(648 + (k % 2) * 254, 217 + (k // 2) * 40, c, "m", 12)
    b += t(634, 388, "“Who comes tomorrow?” · “Who still owes me?”", "s", 14)
    b += t(634, 412, "Finds a client and opens their WhatsApp in one tap.", "b", 13)
    b += t(634, 446, "Voice dictation to talk instead of type.", "b", 13)
    b += t(634, 470, "Can't do it yet? “Propose this improvement” sends", "b", 13)
    b += t(634, 490, "the idea as a ticket to the Super Admin.", "b", 13)
    b += t(634, 552, "Same engine switch: Claude Haiku 4.5 or TypeSafe.", "b", 13, MUTED_INK)
    return svg(1200, 610, b)


# ---------------------------------------------------------------- plans
def plans():
    b = kicker(40, 46, "Business model") + t(40, 80, "Three plans, monthly subscription in ARS", "h", 28)
    b += t(40, 106, "15-day free trial, no card · no fee per booking · paid with Mercado Pago", "b", 14, MUTED_INK)
    ps = [("Free", "$0", "forever", ["Inzomio Link", "Service catalog", "Book via WhatsApp", "Automatic FAQ (no AI)"], False),
          ("Profesional", "$14.900", "/ month", ["Own website on Google", "Self-confirming bookings", "Payment at booking", "Visual page builder"], False),
          ("Empresas", "$24.900", "/ month", ["Conversational AI agent", "Full knowledge base", "Export bookings & clients", "Weekly summary, custom font"], True)]
    for i, (n, price, per, feats, sel) in enumerate(ps):
        x = 40 + i * 380
        b += card(x, 136, 360, 300, sel)
        if sel:
            b += badge(x + 254, 156, "AI agent")
        b += t(x + 24, 180, n, "h", 22) + t(x + 24, 232, price, "h", 40, extra='font-variant-numeric="tabular-nums"')
        b += t(x + 30 + len(price) * 22, 232, per, "b", 14, MUTED_INK)
        for j, f in enumerate(feats):
            b += f'<circle cx="{x + 30}" cy="{276 + j * 36}" r="4" fill="{ACCENT}"/>' + t(x + 44, 281 + j * 36, f.replace("&", "&amp;"), "b", 14)
    b += t(40, 466, "Plus a custom plan on request. Features per plan come from a central registry in Super Admin, not hard-coded.", "b", 13, MUTED_INK)
    return svg(1200, 490, b)


# ---------------------------------------------------------------- architecture
def architecture():
    b = kicker(40, 46, "Architecture") + t(40, 80, "One codebase, every business", "h", 28)
    b += f'<rect x="40" y="110" width="360" height="350" rx="10" fill="none" stroke="{MUTED_INK}" stroke-dasharray="5 5"/>'
    b += kicker(60, 136, "Public · multi-tenant")
    for i, (s1, s2) in enumerate([("Marketing site", "pricing and sign-up"), ("Business page", "own website or Inzomio Link"),
                                  ("Booking flow", "validated on the server"), ("Client agent", "chat on every public page")]):
        b += card(60, 150 + i * 76, 320, 64) + t(80, 177 + i * 76, s1, "s", 15) + t(80, 199 + i * 76, s2, "b", 13, MUTED_INK)
    b += card(40, 476, 360, 62) + kicker(60, 502, "Business panel") + t(60, 524, "Bookings, clients, builder, internal agent", "b", 13, MUTED_INK)
    b += card(40, 550, 360, 62) + kicker(60, 576, "Platform panel") + t(60, 598, "Plans, features and support", "b", 13, MUTED_INK)
    b += card(480, 150, 340, 330, True) + t(650, 190, "Supabase", "h", 22, INK, "middle")
    b += card(504, 210, 292, 76, fill=MUTED) + t(650, 242, "Postgres + RLS", "s", 15, INK, "middle") + t(650, 266, "tenant isolation per business", "b", 13, MUTED_INK, "middle")
    b += card(504, 298, 292, 76, fill=MUTED) + t(650, 330, "Auth", "s", 15, INK, "middle") + t(650, 354, "visitor · owner · super admin", "b", 13, MUTED_INK, "middle")
    b += card(504, 386, 292, 76, fill=MUTED) + t(650, 418, "Plans &amp; features", "s", 15, INK, "middle") + t(650, 442, "configurable per plan", "b", 13, MUTED_INK, "middle")
    b += card(900, 110, 260, 150) + t(1030, 146, "Vercel", "h", 22, INK, "middle")
    for i, s1 in enumerate(["Next.js App Router", "Production deploys"]):
        b += t(1030, 182 + i * 26, s1, "b", 13, MUTED_INK, "middle")
    b += card(900, 276, 260, 196) + kicker(920, 304, "Integrations")
    for i, s1 in enumerate(["Claude Haiku 4.5 · TypeSafe", "Mercado Pago subscriptions", "Google Calendar sync", "Bot protection"]):
        b += t(920, 334 + i * 28, s1, "b", 14)
    b += f'<rect x="900" y="490" width="260" height="76" rx="10" fill="{INK}"/>'
    b += t(1030, 522, "Claude Code + GitHub", "s", 15, CARD, "middle") + t(1030, 546, "agent-driven development", "b", 13, WORDMARK, "middle")
    b += arrow("M400 285 C440 285 440 300 476 300")
    b += arrow("M400 507 C450 507 450 420 476 420")
    b += arrow("M400 581 C460 581 460 470 490 470")
    b += arrow("M820 200 L896 190")
    b += arrow("M820 360 L896 360")
    return svg(1200, 640, b)


# ---------------------------------------------------------------- roadmap
def roadmap():
    b = kicker(40, 46, "Roadmap") + t(40, 80, "From a weekend experiment to a product in production", "h", 28)
    items = [("Weekend PoC", "AI-agent build", "Done", True),
             ("Product v1", "bookings, page, agent", "Done", True),
             ("Public launch", "IG, LinkedIn, YouTube", "Sep 2026", None),
             ("Dec 2026 goal", "30 accounts · 8 paid", "Next", False),
             ("Sep 2027 goal", "300 accounts · 80 paid", "Target", False)]
    b += f'<line x1="120" y1="160" x2="1080" y2="160" stroke="{BORDER}" stroke-width="4"/>'
    b += f'<line x1="120" y1="160" x2="600" y2="160" stroke="{INK}" stroke-width="4"/>'
    for i, (title, sub, st, done) in enumerate(items):
        cx = 120 + i * 240
        if done is None:
            b += f'<circle cx="{cx}" cy="160" r="14" fill="{ACCENT}" stroke="{INK}" stroke-width="2"/>'
        else:
            b += f'<circle cx="{cx}" cy="160" r="10" fill="{INK if done else CARD}" stroke="{INK if done else MUTED_INK}" stroke-width="2"/>'
        b += card(cx - 105, 196, 210, 96, done is None)
        b += kicker(cx, 222, st, "middle")
        b += t(cx, 252, title, "h", 17, INK, "middle")
        b += t(cx, 276, sub, "b", 13, MUTED_INK, "middle")
    b += t(40, 326, "Growth channel: agreements with professional associations (Mendoza first). Goals from the internal plan, not results.", "b", 13, MUTED_INK)
    return svg(1200, 350, b)


for name, fn in [("banner", banner), ("process", process), ("modules", modules), ("agent", agent),
                 ("architecture", architecture), ("plans", plans), ("roadmap", roadmap)]:
    (OUT / f"{name}.svg").write_text(fn())
    print(name, (OUT / f"{name}.svg").stat().st_size // 1024, "KB")
