from pathlib import Path
from io import BytesIO
import json
import re
import sys

import pdfplumber
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import ContentStream, Fit, FloatObject, NameObject
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding="utf-8")
SOURCE = Path("C:/Users/Iago Rossan/Downloads/Estudo_Caso_Real_Data_Mining_Telecom_14Out2026-v2 - Resolução Completa (1).pdf")
DEST = Path("C:/6Semestre/output/pdf/Estudo_Caso_Telecom_Sumario_Detalhado.pdf")
DEST.parent.mkdir(parents=True, exist_ok=True)
W, H = 612, 792
SHIFT = 166.5

pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("ArialBold", "C:/Windows/Fonts/arialbd.ttf"))

# Each source page and heading position was checked in the original PDF.
# Source page numbers below are one-based. The final PDF removes one TOC page.
entries = [
    ("1.", "INTRODUÇÃO", 5, 240.9),
    ("2.", "ARQUITETURA DE DATA MINING", 5, 656.4),
    ("2.1", "Camada de Ingestão e Streaming", 6, 135.6),
    ("2.2", "Camada de Armazenamento Multicloud", 6, 428.1),
    ("2.3", "Camada de Processamento e Análise", 7, 113.8),
    ("2.4", "Camada de Governança e MLOps", 7, 406.3),
    ("3.", "ARQUITETURA MULTICLOUD", 7, 612.2),
    ("3.1", "Kubernetes como Plataforma Unificada", 7, 655.3),
    ("3.2", "Virtualização e Contentores", 8, 200.8),
    ("3.3", "Rede e Conectividade", 8, 378.6),
    ("4.", "PIPELINE DE MACHINE LEARNING", 8, 540.9),
    ("4.1", "Fluxograma Lógico do Pipeline", 8, 584.1),
    ("4.2", "Churn Prediction (Predição de Cancelamento)", 9, 157.3),
    ("4.3", "Deteção de Anomalias de Rede", 9, 378.6),
    ("4.4", "Propensão a Upsell", 9, 534.6),
    ("4.5", "Processamento Batch vs. Real-Time (Lambda Architecture)", 9, 690.6),
    ("5.", "CASO REAL: OPERADORAS GLOBAIS", 10, 228.9),
    ("5.1", "Vodafone: Transformação AIOps Multicloud", 10, 315.6),
    ("5.2", "Operadora Asiática: Churn Prediction em Escala", 10, 430.3),
    ("5.3", "Ericsson Cloud Native Infrastructure", 10, 523.3),
    ("5.4", "Comparativo de Implementações", 11, 80.5),
    ("6.", "FERRAMENTAS OPEN SOURCE", 11, 387.9),
    ("7.", "AUTOMAÇÃO E ADMINISTRAÇÃO", 12, 120.2),
    ("7.1", "Infrastructure as Code (IaC)", 12, 157.3),
    ("7.2", "GitOps e CI/CD", 12, 250.3),
    ("7.3", "Automação de Rede SDN/NFV", 12, 343.3),
    ("7.4", "Monitorização Unificada", 12, 414.6),
    ("8.", "QUESTÕES DE PERFORMANCE, OTIMIZAÇÃO E CONTROLO (1 A 18)", 12, 525.9),
]

# Include all 18 question headings in the visible TOC. Determine the ending
# page from the content preceding the next question, rather than assuming
# that a question finishes on the page where it starts.
page_extents = {}
question_records = []
with pdfplumber.open(SOURCE) as original:
    source_lines = [pg.extract_text_lines() for pg in original.pages]
    for source_index, lines in enumerate(source_lines[11:], start=11):
        for line in lines:
            match = re.match(r"^Questão (\d+): (.+)$", line["text"])
            if match:
                question_records.append((int(match[1]), match[2], source_index + 1, line["top"]))
    assert [record[0] for record in question_records] == list(range(1, 19))
    page_extents["8."] = f"{entries[-1][2] - 1}-{len(original.pages) - 1}"
    for i, (number, title, start_page, top) in enumerate(question_records):
        if i + 1 < len(question_records):
            _, _, next_page, next_top = question_records[i + 1]
            preceding = [line for line in source_lines[next_page - 1] if line["top"] < next_top - 1]
            end_page = next_page if preceding else next_page - 1
            end_page = max(start_page, end_page)
        else:
            end_page = len(original.pages)
        label = f"Questão {number}:"
        entries.append((label, title, start_page, top))
        final_start, final_end = start_page - 1, end_page - 1
        page_extents[label] = str(final_start) if final_start == final_end else f"{final_start}-{final_end}"
assert len(entries) == 46


def target(source_page, source_top):
    # Two original TOC pages are replaced by a single TOC page.
    final_page = source_page - 1
    top = source_top - (SHIFT if source_page == 5 else 0)
    return final_page - 1, H - top + 12


toc_stream = BytesIO()
c = canvas.Canvas(toc_stream, pagesize=(W, H))
c.setFillColorRGB(0.067, 0.067, 0.067)
c.setFont("ArialBold", 14)
c.drawCentredString(W / 2, H - 86, "SUMÁRIO")
c.setFont("Arial", 8.5)
c.setFillColorRGB(0.38, 0.38, 0.38)
c.drawRightString(540, H - 105, "PÁGINA(S)")
c.setFillColorRGB(0.067, 0.067, 0.067)
row_links = []
baseline = H - 124
for i, (num, title, source_page, source_top) in enumerate(entries):
    main = num.endswith(".")
    if main and i:
        baseline -= 2.5
    font, size = ("ArialBold", 11) if main else ("Arial", 10.5)
    c.setFont(font, size)
    nx, tx = (72, 93) if main else (87, 114)
    if num.startswith("Questão "):
        tx = 151
    c.drawString(nx, baseline, num)
    c.drawString(tx, baseline, title)
    end_x = tx + pdfmetrics.stringWidth(title, font, size)
    target_page, target_y = target(source_page, source_top)
    page_text = page_extents.get(num, str(target_page + 1))
    c.setFont("Arial", 10.5)
    c.drawRightString(540, baseline, page_text)
    page_left = 540 - pdfmetrics.stringWidth(page_text, "Arial", 10.5)
    leader_start, leader_end = end_x + 8, page_left - 8
    assert leader_end > leader_start, (num, end_x, page_left)
    c.setFont("Arial", 9)
    c.setFillColorRGB(0.38, 0.38, 0.38)
    dot_width = pdfmetrics.stringWidth(".", "Arial", 9)
    dot_count = int((leader_end - leader_start) / dot_width)
    c.drawString(leader_start, baseline, "." * dot_count)
    c.setFillColorRGB(0.067, 0.067, 0.067)
    row_links.append((num + " " + title, (72, baseline - 2, 541, baseline + 10), target_page, target_y, main))
    baseline -= 12.5
assert baseline >= 72
c.setFont("Arial", 8.5)
c.setFillColorRGB(0.38, 0.38, 0.38)
c.drawString(72, 59, "Números indicam páginas de início; intervalos mostram onde a seção ou questão continua.")
c.showPage()
c.save()
toc_stream.seek(0)

reader = PdfReader(SOURCE)
writer = PdfWriter()
writer.add_page(reader.pages[0])
writer.add_page(reader.pages[1])
writer.add_page(PdfReader(toc_stream).pages[0])

# Remove the three TOC paragraph groups from the mixed TOC/introduction page,
# then move its original text blocks to the normal top margin. No body text is
# rasterized or retyped; original fonts and paragraph layout remain in the PDF.
intro = reader.pages[4]
cs = ContentStream(intro.get_contents(), reader)
assert cs.operations[0][1] == b"cm"
cleaned = [cs.operations[0]]
groups = []
current = []
depth = 0
for args, op in cs.operations[1:]:
    if op == b"q":
        depth += 1
    if depth:
        current.append((args, op))
    elif op not in (b"BDC", b"BMC", b"EMC"):
        cleaned.append((args, op))
    if op == b"Q":
        depth -= 1
        if not depth:
            groups.append(current)
            current = []
assert depth == 0 and not current
removed = 0
for group in groups:
    matrix = next((args for args, op in group if op == b"cm"), None)
    assert matrix is not None
    y = float(matrix[5])
    if 70 <= y < 230:
        removed += 1
        continue
    if y >= 230:
        matrix[5] = FloatObject(y - SHIFT)
    cleaned.extend((args, op) for args, op in group if op not in (b"BDC", b"BMC", b"EMC"))
assert removed == 3
cs.operations = cleaned
intro[NameObject("/Contents")] = cs
writer.add_page(intro)
for pg in reader.pages[5:]:
    writer.add_page(pg)
assert len(writer.pages) == 22

# Add discreet visible page numbers matching the TOC and the PDF viewer.
for i in range(2, len(writer.pages)):
    footer = BytesIO()
    f = canvas.Canvas(footer, pagesize=(W, H))
    f.setFont("Arial", 10)
    f.setFillColorRGB(0.25, 0.25, 0.25)
    f.drawRightString(540, 36, str(i + 1))
    f.showPage()
    f.save()
    footer.seek(0)
    writer.pages[i].merge_page(PdfReader(footer).pages[0])

writer.add_outline_item("SUMÁRIO", 2, fit=Fit.xyz(left=72, top=720, zoom=0))
section_parent = None
last_main = None
for title, rect, page_index, top, main in row_links:
    fit = Fit.xyz(left=72, top=top, zoom=0)
    annotation = writer.add_annotation(2, Link(rect=rect, target_page_index=page_index, fit=fit))
    annotation["/Dest"][0] = writer.pages[page_index].indirect_reference
    item = writer.add_outline_item(title, page_index, parent=None if main else section_parent, fit=fit, bold=main)
    if main:
        section_parent = item
        last_main = title
assert last_main.startswith("8.")

writer.add_metadata({
    "/Title": "Estudo de Caso: Data Mining em Telecomunicações - Sumário Detalhado",
    "/Subject": "Sumário com 18 questões, páginas de início, intervalos e navegação interna",
    "/Producer": "ReportLab / pypdf",
})
writer.write(DEST)

# Compare every retained body page and cover, excluding the new page numbers.
def compact(text):
    return re.sub(r"\s+", "", text)

with pdfplumber.open(SOURCE) as src, pdfplumber.open(DEST) as out:
    assert len(out.pages) == 22
    for source_index, output_index in [(0, 0), (1, 1)] + [(i, i - 1) for i in range(4, 23)]:
        sp = src.pages[source_index]
        if source_index == 4:
            sp = sp.crop((0, 230, W, H))
        op = out.pages[output_index].crop((0, 0, W, 735))
        assert compact(sp.extract_text() or "") == compact(op.extract_text() or ""), (source_index + 1, output_index + 1)
    toc_lines = out.pages[2].extract_text_lines()
    assert len([line for line in toc_lines if re.match(r"^(?:\d+[.]|Questão \d+:)", line["text"])]) == 46
    for line in toc_lines:
        assert line["x0"] >= 71 and line["x1"] <= 542

check = PdfReader(DEST)
assert len(check.pages[2]["/Annots"]) == 46
for link, (_, _, expected_page, _, _) in zip(check.pages[2]["/Annots"], row_links):
    dest = link.get_object()["/Dest"]
    assert check.get_page_number(dest[0].get_object()) == expected_page
assert page_extents["Questão 18:"] == "21-22"
print(json.dumps({"output": str(DEST), "pages": len(check.pages), "toc_entries": len(row_links), "body_text_preserved": True, "clickable_toc_links": len(check.pages[2]["/Annots"]), "question_pages": page_extents}, ensure_ascii=False))
