"""Build text cards from shared design tokens.

python scripts/build_assets.py
All assets are self-contained SVG text cards.
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
TOKENS = json.loads((ROOT / "design/tokens.json").read_text())
FONT = '-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif'


def txt(x, y, text, size=16, color=None, weight=400):
    return f'<text x="{x}" y="{y}" fill="{color or C["ink"]}" font-size="{size}" font-weight="{weight}">{escape(text)}</text>'


def rect(x, y, w, h, fill, radius=0, stroke="none"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def save(name, w, h, content, alt):
    (ASSETS / f"ce12-{name}-{THEME}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(alt, quote=True)}">'
        f'<g font-family="{FONT}">' + content + '</g></svg>\n')


def shell(w, h):
    return rect(.5, .5, w-1, h-1, C['surface'], 16, C['line'])


for THEME in ("light", "dark"):
    C = dict(TOKENS['color'])
    if THEME == 'dark':
        C.update(C['dark'])
    # Compact name, with Stip's soft ambient sage and warm neutral tones.
    content = '<defs><radialGradient id="wash"><stop stop-color="' + C['sage'] + '"/><stop offset="1" stop-color="'+C['surface']+'"/></radialGradient></defs>'
    content += rect(0, 0, 960, 148, C['surface'], 16)
    content += '<ellipse cx="125" cy="48" rx="300" ry="115" fill="url(#wash)"/>'
    content += txt(36, 91, 'Can Erturk', 62, weight=500)
    content += f'<circle cx="350" cy="79" r="7" fill="{C["olive"]}"/>'
    content += f'<path d="M36 127H924" stroke="{C["line"]}"/>'
    save('name', 960, 148, content, 'Can Erturk')

    for slug, title, role, lines, result in (
        ('asml', 'ASML', 'Software Engineering Intern', ['Diagnostics software for semiconductor', 'equipment. Working with legacy systems', 'and modern software interfaces.'], 'September 2026–present'),
        ('stellantis', 'TOFAŞ / Stellantis', 'Digital Transformation Intern', ['Built real-time fault detection for', 'an automotive assembly line using', 'Python, YOLO and OpenCV.'], '30+ FPS in production'),
    ):
        content = shell(400, 242)
        content += '<defs><clipPath id="card"><rect width="400" height="242" rx="16"/></clipPath></defs>'
        content += f'<g clip-path="url(#card)">{rect(0,0,400,88,TOKENS["color"]["olive"])}</g>'
        content += txt(24, 39, title, 25, '#FFFFFF', 600) + txt(24, 66, role, 16, '#F1F3ED')
        for y,line in zip((119,143,167),lines): content += txt(24,y,line,16,C['muted'])
        content += f'<path d="M24 190H376" stroke="{C["line"]}"/>' + txt(24,220,result,18,C['olive'],600)
        save(slug,400,242,content,f'{title} · {role}. '+ ' '.join(lines)+' '+result)

    for age,title,lines,result,tail in (
        ('13','3D printing',['Built a 3D printer.','Then, during COVID:'],'50,000+',['mask holders','produced and sold.']),
        ('16','Parmestore',['Founded a China–','Europe business.'],'Self-funded',['my education','through the business.']),
        ('17','TOFAŞ',['Built assembly-line','fault detection.'],'30+ FPS',['Python, YOLO','and OpenCV.']),
        ('19','ASML',['Software engineering','internship.'],'Diagnostics',['for semiconductor','equipment.']),
    ):
        content=shell(150,236)+txt(12,40,age,30,C['olive'],500)
        content+=f'<path d="M12 57H138" stroke="{C["line"]}"/>'+txt(12,82,title,16,weight=600)
        for y,line in zip((107,126),lines):content+=txt(12,y,line,12.5,C['muted'])
        content+=txt(12,165,result,21 if age in ('13','17') else 16,C['olive'],600)
        for y,line in zip((190,209),tail):content+=txt(12,y,line,12.5,C['muted'])
        save('age-'+age,150,236,content,f'At {age}: {title}. '+' '.join(lines)+' '+result+' '+' '.join(tail))

    projects=(
        ('geometry','Polygon intersections','28 verification cases',[
            'Intersection bounds for regular polygons.',
            'Paper plus Python checks of selected',
            'arrangements, crossing points and regions.'],
            'Python · geometry · numerical verification'),
        ('vision','Computer vision','Training → validation → inference',[
            'YOLO training and evaluation scripts.',
            'OpenCV video and webcam inference,',
            'annotated recordings and detection logs.'],
            'Python · YOLO · OpenCV'),
        ('systems','Computer systems','5 labs · C and ARM Assembly',[
            'Calling conventions, pointers and lists.',
            'Matrix multiplication, file I/O and processes.',
            'Boundary checks, Make and QEMU.'],
            'C · ARM Assembly · Linux'),
        ('commerce','Parmestore tools','Margins · prices · marketplaces',[
            'VAT, commission and shipping calculations.',
            'SQLite price history and threshold alerts.',
            'Listing comparisons across marketplaces.'],
            'Python · pandas · SQLite'),
        ('ml','Melanoma classifier','Cross-validation · 8-view augmentation',[
            'PyTorch image-classification experiments.',
            'Weighted sampling and AUC-based selection.',
            'Training, evaluation and inference code.'],
            'PyTorch · timm · scikit-learn'),
        ('simulation','Supply chain experiments','4 reproducible notebooks',[
            'Lead times, ordering, backlog and queues.',
            'Seeded synthetic data and M/M/c simulation.',
            'Separate CSV download and merge tools.'],
            'Python · pandas · NumPy'),
    )
    for slug,title,result,lines,stack in projects:
        content=shell(400,254)+txt(24,39,title,22,weight=600)
        content+=txt(24,73,result,16,C['olive'],600)
        content+=f'<path d="M24 93H376" stroke="{C["line"]}"/>'
        for y,line in zip((122,147,172),lines):content+=txt(24,y,line,16,C['muted'])
        content+=txt(24,218,stack,14,C['olive'])
        save(slug,400,254,content,title+'. '+result+'. '+' '.join(lines))

print('Built detailed text cards for both themes.')
