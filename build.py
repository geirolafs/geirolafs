"""Generate the honest GitHub stats card (not-a-dev-stats.svg), styled after geir.is.

Edit STATS / LANGS below, then run: python3 build.py
"""
from html import escape

W, H = 1000, 232
SHIFT = -180  # layout coordinates below were drawn for a taller card; this moves them into view
PAD = 48

THEMES = {
    "light": dict(bg="#ffffff", border="#e4e4e4", fg="#121212", muted="#767676", rule="#ebebeb",
                  shadow="#000000", shadow_op=0.10),
    "dark":  dict(bg="#0d1117", border="#30363d", fg="#e6edf3", muted="#8b949e", rule="#21262d",  # GitHub dark palette
                  shadow="#000000", shadow_op=0.55),
}

STATS = [
    ("Stars", "0", "I\u2019m a giver (212), not a taker"),
    ("Commits", "119", 'git commit -m "fix previous"'),
    ("PRs", "0", "git push -f origin master"),
    ("Issues", "Yes", "no issues on my end"),
    ("Contributed", "11,402", "Figma frames"),
    ("Tests", "0", "ok."),
]

# Blues: #0040ff (B=255) plus 40% and 70% tints of it; warm end sampled from the site's --gradient-stripe
LANGS = [
    ("Move some divs", 38, "#0040ff"),
    ("Approve diffs", 24, "#668cff"),
    ("Ask The AI", 14, "#b3c5ff"),
    ("!important", 11, "#e3d6d2"),
    ("\u2318C & \u2318V", 8, "#f6bfb3"),
    ("Things no one will notice", 5, "#ffe577"),
]

MONO_FONT = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, monospace"
# Labels laid out in fixed cells (glyphs like \u2318 fall back to non-mono fonts)
MONO = {"\u2318C & \u2318V"}

FONT = MONO_FONT  # everything is monospaced


def mono(cls, x, y, s, cell=6.9):
    """Monospace by construction: each character centred in its own fixed-width cell,
    so spacing holds even when a glyph (e.g. \u2318) falls back to another font."""
    cells = "".join(
        f'<text class="{cls}" x="{x + (i + .5) * cell:.1f}" y="{y}" text-anchor="middle">{escape(ch)}</text>'
        for i, ch in enumerate(s) if ch != " ")
    return f'<g>{cells}</g>'


def sphere(cx, cy, r, grain=1.4, delay=0):
    """Soft matte-chrome ball after the one on geir.is: light body, blurred top highlight,
    a soft dark band below the equator, lighter rim at the bottom, film grain over it all."""
    b = r * 0.16  # blur radius scales with the ball
    return f'''<defs>
  <clipPath id="sph"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
  <radialGradient id="sph-body" cx=".5" cy=".36" r=".68">
    <stop offset="0" stop-color="#e4e4e8"/>
    <stop offset=".55" stop-color="#c0c1c7"/>
    <stop offset="1" stop-color="#8f9099"/>
  </radialGradient>
  <radialGradient id="sph-vig" cx=".5" cy=".5" r=".5">
    <stop offset=".6" stop-color="#7d7e88" stop-opacity="0"/>
    <stop offset="1" stop-color="#7d7e88" stop-opacity=".55"/>
  </radialGradient>
  <filter id="sph-soft" filterUnits="userSpaceOnUse" x="{cx - 2*r}" y="{cy - 2*r}" width="{4*r}" height="{4*r}"><feGaussianBlur stdDeviation="{b:.2f}"/></filter>
  <filter id="sph-grain" filterUnits="userSpaceOnUse" x="{cx - r}" y="{cy - r}" width="{2*r}" height="{2*r}">
    <feTurbulence type="fractalNoise" baseFrequency="{grain}" numOctaves="2" stitchTiles="stitch" seed="1" result="n">
      <animate attributeName="seed" values="1;2;3;4;5;6;7;8;9;10;11;12" dur="1.2s" begin="{delay/1000:.2f}s" calcMode="discrete" fill="freeze"/>
    </feTurbulence>
    <feColorMatrix in="n" type="saturate" values="0"/>
  </filter>
</defs>
<g clip-path="url(#sph)">
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#sph-body)"/>
  <ellipse class="band" style="animation-delay:{delay}ms" cx="{cx}" cy="{cy + r*0.30:.2f}" rx="{r*1.18:.2f}" ry="{r*0.38:.2f}" fill="#3c3d4e" filter="url(#sph-soft)"/>
  <ellipse cx="{cx}" cy="{cy + r*1.12:.2f}" rx="{r*0.95:.2f}" ry="{r*0.42:.2f}" fill="#c9cad0" filter="url(#sph-soft)"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#sph-vig)"/>
  <g class="hl" style="animation-delay:{delay}ms">
    <ellipse cx="{cx}" cy="{cy - r*0.58:.2f}" rx="{r*0.36:.2f}" ry="{r*0.24:.2f}" fill="#ffffff" filter="url(#sph-soft)"/>
    <ellipse cx="{cx}" cy="{cy - r*0.58:.2f}" rx="{r*0.22:.2f}" ry="{r*0.13:.2f}" fill="#ffffff" filter="url(#sph-soft)"/>
  </g>
  <rect x="{cx - r}" y="{cy - r}" width="{2*r}" height="{2*r}" filter="url(#sph-grain)" opacity=".4" style="mix-blend-mode:overlay"/>
</g>'''


def card(t):
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">')
    a('<title id="t">GitHub stats, honest edition</title>')
    a(f'''<style>
  text {{ font-family: {FONT}; fill: {t["fg"]}; }}
  .m {{ fill: {t["muted"]}; }}
  .meta {{ font-size: 12.5px; letter-spacing: .01em; }}
  .h {{ font-size: 26px; letter-spacing: -.02em; }}
  .lbl {{ font-size: 12.5px; letter-spacing: 0; }}
  .num {{ font-size: 16px; font-weight: 500; letter-spacing: -.012em; }}
  .note {{ font-size: 16px; font-weight: 400; letter-spacing: -.012em; }}
  .lang {{ font-size: 11.5px; letter-spacing: 0; }}
  .grade {{ font-size: 26px; letter-spacing: -.02em; }}

  /* Load-in: same easing as geir.is (--ease-out) */
  .in    {{ opacity: 0; animation: rise .7s cubic-bezier(.23,1,.32,1) forwards; }}
  .rule  {{ stroke-dasharray: 432; stroke-dashoffset: 432; animation: draw .9s cubic-bezier(.23,1,.32,1) forwards; }}
  .grow  {{ transform-box: fill-box; transform-origin: 0 50%; transform: scaleX(0); animation: grow 1.1s cubic-bezier(.23,1,.32,1) forwards; }}
  .ball  {{ transform-box: fill-box; transform-origin: 50% 50%; opacity: 0; animation: ball .9s cubic-bezier(.23,1,.32,1) forwards; }}
  .ring  {{ animation: sweep 1.3s cubic-bezier(.65,0,.35,1) forwards; }}
  .shade {{ transform-box: fill-box; transform-origin: 50% 50%; opacity: 0; animation: shade 1.3s cubic-bezier(.23,1,.32,1) forwards; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
  @keyframes grow {{ to {{ transform: scaleX(1); }} }}
  @keyframes sweep {{ to {{ stroke-dashoffset: 0; }} }}
  /* Light moves over the ball as it rises, like it's rolling under a fixed lamp */
  .hl   {{ transform-box: fill-box; transform-origin: 50% 50%; animation: hl 1.5s cubic-bezier(.23,1,.32,1) both; }}
  .band {{ transform-box: fill-box; transform-origin: 50% 50%; animation: band 1.7s cubic-bezier(.23,1,.32,1) both; }}
  @keyframes hl   {{ from {{ opacity: .35; transform: translateY(16px) scale(1.35); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes band {{ from {{ opacity: .5; transform: translateY(-12px) scaleY(.6); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes ball {{ from {{ opacity: 0; transform: translateY(28px) scale(.94); }} to {{ opacity: 1; transform: none; }} }}
  /* Ball starts close to the floor: shadow tight and dark, then spreads and softens as it lifts */
  @keyframes shade {{
    0%   {{ opacity: 0; transform: scale(.45, .6); }}
    35%  {{ opacity: {min(1, t["shadow_op"]*1.8):.2f}; transform: scale(.6, .75); }}
    100% {{ opacity: {t["shadow_op"]}; transform: scale(1); }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .in, .rule, .grow, .ball, .shade, .ring, .hl, .band {{ animation: none; opacity: 1; transform: none; stroke-dashoffset: 0; }}
    .shade {{ opacity: {t["shadow_op"]}; }}
  }}
</style>''')
    a('''<defs>
  <radialGradient id="sh" cx=".5" cy=".5" r=".5">
    <stop offset="0" stop-color="#000" stop-opacity="1"/>
    <stop offset="1" stop-color="#000" stop-opacity="0"/>
  </radialGradient>
</defs>''')
    # Background bleeds far past the viewBox: if the <img> box is taller than the scaled card
    # (fixed height to prevent layout shift), the letterbox strips stay the same dark
    a(f'<rect x="-{W}" y="-{W}" width="{3*W}" height="{H + 2*W}" fill="{t["bg"]}"/>')



    a(f'<g transform="translate(0,{SHIFT})">')
    gap = 56           # space between columns
    top = 229          # first row baseline
    seg_gap = 2.5      # gap between ring segments
    rr = 40 + seg_gap + 2  # ring radius: sphere r + same gap + half the 4px stroke

    # Languages, middle
    lx = PAD + 2 * rr + 4 + gap
    cw = (W - PAD - lx - gap) / 2  # two equal text columns fill the rest
    for i, (name, pct, col) in enumerate(LANGS):
        y = top + i * 26.6
        a(f'<g class="in" style="animation-delay:{300 + i*70}ms">')
        a(f'<circle cx="{lx + 4}" cy="{y - 4.5}" r="4" fill="{col}"/>')
        if name in MONO:
            a(mono("lang", lx + 16, y, name))
        else:
            a(f'<text class="lang" x="{lx + 16}" y="{y}">{escape(name)}</text>')
        a(f'<text class="lang m" x="{lx + cw}" y="{y}" text-anchor="end">{pct}%</text>')
        a('</g>')
        a(f'<line class="rule" style="animation-delay:{350 + i*70}ms" x1="{lx}" x2="{lx + cw}" y1="{y + 9.5}" y2="{y + 9.5}" stroke="{t["rule"]}"/>')

    # Stats, right: label, note, value right-aligned
    sx = lx + cw + gap
    for i, (label, num, note) in enumerate(STATS):
        y = top + i * 26.6
        a(f'<g class="in" style="animation-delay:{450 + i*70}ms">')
        a(f'<text class="lang" x="{sx}" y="{y}">{escape(label)}</text>')
        a(f'<text class="lang m" x="{sx + 89}" y="{y}">{escape(note)}</text>')
        a(f'<text class="lang m" x="{sx + cw}" y="{y}" text-anchor="end">{escape(num)}</text>')
        a('</g>')
        a(f'<line class="rule" style="animation-delay:{500 + i*70}ms" x1="{sx}" x2="{sx + cw}" y1="{y + 9.5}" y2="{y + 9.5}" stroke="{t["rule"]}"/>')

    # The chrome sphere, left, ringed by the language split
    cx, cy, r = PAD + rr + 2, 287, 40
    ball_delay = 150
    a(f'<ellipse class="shade" style="animation-delay:{ball_delay - 50}ms" cx="{cx}" cy="{cy + rr + 14}" rx="{r*0.9}" ry="6" fill="url(#sh)"/>')
    a(f'<g class="ball" style="animation-delay:{ball_delay}ms">')
    a(sphere(cx, cy, r, delay=ball_delay))
    a('</g>')

    # Ring: segments sit in a mask that sweeps round once the sphere has landed
    circ = 2 * 3.141592653589793 * rr
    a(f'<mask id="sweep"><circle class="ring" style="animation-delay:{ball_delay + 800}ms" cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="#fff" stroke-width="8" stroke-dasharray="{circ:.2f} {circ:.2f}" stroke-dashoffset="{circ:.2f}"/></mask>')
    a(f'<g mask="url(#sweep)" transform="rotate(-90 {cx} {cy})">')
    start = 0.0
    for _, pct, col in LANGS:
        seg = circ * pct / 100
        a(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{col}" stroke-width="4" '
          f'stroke-dasharray="{max(seg - seg_gap, 0.5):.2f} {circ:.2f}" stroke-dashoffset="{-start:.2f}"/>')
        start += seg
    a('</g>')

    a('</g>')
    a('</svg>')
    return "\n".join(o)


# Always dark, whatever the viewer's GitHub theme
with open("not-a-dev-stats.svg", "w") as f:
    f.write(card(THEMES["dark"]))
