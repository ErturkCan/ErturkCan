"""Build the profile artwork from shared tokens and reproducible demo outputs.

python scripts/build_assets.py
Then rasterise vision-{light,dark}.svg to PNG with any SVG renderer.
Other assets stay SVG so type and diagrams remain sharp at every size.
"""
import base64
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
TOKENS = json.loads((ROOT / "design/tokens.json").read_text())
GEOMETRY = json.loads((ASSETS / "geometry-data.json").read_text())
SAMPLE = base64.b64encode((ASSETS / "vision-sample.jpg").read_bytes()).decode()
FONT = '-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif'


def txt(x, y, text, size=16, color=None, weight=400):
    return f'<text x="{x}" y="{y}" fill="{color or C["ink"]}" font-size="{size}" font-weight="{weight}">{escape(text)}</text>'


def rect(x, y, w, h, fill, radius=0, stroke="none"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def save(name, w, h, content, alt):
    (ASSETS / f"{name}-{THEME}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(alt, quote=True)}">'
        f'<g font-family="{FONT}">' + content + '</g></svg>\n')


def shell(w, h):
    return rect(.5, .5, w-1, h-1, C['surface'], 16, C['line'])


for THEME in ("light", "dark"):
    C = dict(TOKENS['color'])
    if THEME == 'dark':
        C.update(C['dark'])
    # Compact name, with Stip's soft ambient sage and the portfolio's blue tint.
    content = '<defs><radialGradient id="wash"><stop stop-color="' + C['sage'] + '"/><stop offset="1" stop-color="'+C['surface']+'"/></radialGradient></defs>'
    content += rect(0, 0, 960, 148, C['surface'], 16)
    content += '<ellipse cx="125" cy="48" rx="300" ry="115" fill="url(#wash)"/>'
    content += txt(36, 91, 'Can Erturk', 62, weight=500)
    content += f'<circle cx="350" cy="79" r="7" fill="{C["olive"]}"/>'
    content += f'<path d="M36 127H924" stroke="{C["line"]}"/>'
    save('name', 960, 148, content, 'Can Erturk')

    for slug, title, role, lines, color in (
        ('asml', 'ASML', 'Software Engineering Intern', ['Diagnostics software for', 'semiconductor equipment.'], C['blue']),
        ('stellantis', 'TOFAŞ / Stellantis', 'Digital Transformation Intern', ['Real-time fault detection.', 'Python · YOLO · OpenCV'], C['clay']),
    ):
        content = shell(400, 188)
        content += f'<defs><clipPath id="card"><rect width="400" height="188" rx="16"/></clipPath></defs>'
        content += f'<g clip-path="url(#card)">{rect(0,0,400,88,color)}</g>'
        content += txt(24, 39, title, 25, '#FFFFFF', 600) + txt(24, 66, role, 16, '#F1F3ED')
        content += txt(24, 126, lines[0], 18) + txt(24, 154, lines[1], 18, C['muted'])
        save(slug, 400, 188, content, f'{title} · {role}. ' + ' '.join(lines))

    for age, title, lines in (
        ('13','3D printing',['Built my first','3D printer.']),
        ('16','Parmestore',['Started my own','e-commerce business.']),
        ('17','TOFAŞ',['Computer vision','on the assembly line.']),
        ('19','ASML',['Software','engineering intern.']),
    ):
        content = shell(150, 157) + txt(14, 43, age, 32, C['olive'], 500)
        content += f'<path d="M14 60H136" stroke="{C["line"]}"/>'
        content += txt(14, 88, title, 16, weight=600)
        content += txt(14, 115, lines[0], 12.5, C['muted']) + txt(14, 134, lines[1], 12.5, C['muted'])
        save(f'age-{age}', 150, 157, content, f'At {age}: {title}. ' + ' '.join(lines))

    # Coordinates and crossing points are exported by the project's demo.py.
    content = shell(400, 430) + rect(12, 12, 376, 225, C['paper'], 12)
    def xy(p): return 200 + 87*p[0], 124 - 87*p[1]
    for polygon, color in zip(GEOMETRY['polygons'], [C['olive'], '#6E91AE', '#B78977']):
        coords=' '.join(f'{x:.3f},{y:.3f}' for x,y in map(xy, polygon))
        content += f'<polygon points="{coords}" fill="none" stroke="{color}" stroke-width="1.6"/>'
    for point in GEOMETRY['crossings']:
        x,y=xy(point)
        content += f'<circle cx="{x:.3f}" cy="{y:.3f}" r="2.1" fill="{C["ink"]}"/>'
    content += txt(28, 38, 'COMPUTED EXAMPLE', 12, C['muted'], 500)
    content += txt(28, 221, '3 pentagons · 30 crossings', 14, C['olive'], 500)
    content += txt(24, 273, 'Polygon intersections', 23, weight=600)
    content += txt(24, 305, 'How many crossings can overlapping', 16, C['muted'])
    content += txt(24, 328, 'regular polygons produce?', 16, C['muted'])
    content += txt(24, 361, 'Paper · Python · numerical checks', 15, C['olive'])
    content += f'<path d="M24 383H376" stroke="{C["line"]}"/>' + txt(24, 411, 'Explore the geometry ↗', 16, C['olive'], 500)
    save('geometry', 400, 430, content, 'Polygon intersections: three pentagons, 30 computed crossings. Paper, Python and numerical checks.')

    content = shell(400, 430) + rect(12,12,376,225,C['paper'],12)
    content += f'<image x="153" y="20" width="135" height="180" href="data:image/jpeg;base64,{SAMPLE}"/>'
    content += txt(28, 38, 'COCO', 12, C['muted'], 500) + txt(28, 56, 'SAMPLE', 12, C['muted'], 500)
    content += txt(28, 221, 'Pretrained YOLO · actual output', 14, C['olive'], 500)
    content += txt(24, 273, 'Computer vision', 23, weight=600)
    content += txt(24, 305, 'Training and video inference tools.', 16, C['muted'])
    content += txt(24, 328, 'Demo uses public COCO weights.', 16, C['muted'])
    content += txt(24, 361, 'Python · YOLO · OpenCV', 15, C['olive'])
    content += f'<path d="M24 383H376" stroke="{C["line"]}"/>' + txt(24,411,'Inspect the code ↗',16,C['olive'],500)
    save('vision',400,430,content,'Computer vision: actual pretrained COCO inference output on an Ultralytics sample. Not a defect model or production benchmark.')

    for slug,title,line1,line2,stack in (
        ('systems','Computer systems','C and ARM Assembly exercises.','Linux, Make and QEMU.','C / ARM / Linux'),
        ('commerce','Parmestore tools','Pricing, sales and shipping scripts.','Tools from my e-commerce business.','Python / pandas / SQLite'),
        ('ml','Melanoma classifier','Image-classification experiments.','Training and evaluation code.','Python / PyTorch'),
        ('simulation','Supply chain experiments','Queues, backlogs and simulation.','Synthetic data, reproducible notebooks.','Python / pandas / NumPy'),
    ):
        content=shell(400,162)+txt(24,40,title,22,weight=600)
        content+=txt(24,76,line1,16,C['muted'])+txt(24,100,line2,16,C['muted'])
        content+=f'<circle cx="28" cy="134" r="4" fill="{C["olive"]}"/>'+txt(40,139,stack,14,C['olive'])
        save(slug,400,162,content,title+'. '+line1+' '+line2)

print('Built profile SVG assets for both themes.')
