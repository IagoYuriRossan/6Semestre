from io import BytesIO
from pathlib import Path
import json
import sys

import pdfplumber
from pypdf import PdfReader, PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding="utf-8")
source = Path("C:/6Semestre/output/pdf/Estudo_Caso_Telecom_Sumario_Detalhado.pdf")
destination = Path("C:/6Semestre/output/pdf/Estudo_Caso_Telecom_Revisado.pdf")
reader = PdfReader(source)
writer = PdfWriter()
writer.clone_document_from_reader(reader)
assert len(writer.pages) == 22

font_name = "ArialBold"
pdfmetrics.registerFont(TTFont(font_name, "C:/Windows/Fonts/arialbd.ttf"))
font_size = 12
face = pdfmetrics.getFont(font_name).face
char_above_baseline = font_size * (1 + face.descent / 1000)
names = ["GUSTAVO LOPES", "FERNANDO RIBEIRO"]

overlay = BytesIO()
c = canvas.Canvas(overlay, pagesize=(612, 792))
c.setFillColorRGB(0.067, 0.067, 0.067)
c.setFont(font_name, font_size)
for i, name in enumerate(names):
    # Continue the original centered author list at the same line spacing.
    top = 418.312968465 + i * 21.75
    c.drawCentredString(306, 792 - top - char_above_baseline, name)
c.showPage()
c.save()
overlay.seek(0)
writer.pages[0].merge_page(PdfReader(overlay).pages[0])
writer.write(destination)

result = PdfReader(destination)
assert len(result.pages) == 22
cover_text = result.pages[0].extract_text()
for name in names:
    assert cover_text.count(name) == 1
for i in range(1, 22):
    assert reader.pages[i].get_contents().get_data() == result.pages[i].get_contents().get_data(), i + 1
assert len(result.pages[2]["/Annots"]) == 46
for old_link, new_link in zip(reader.pages[2]["/Annots"], result.pages[2]["/Annots"]):
    old_target = old_link.get_object()["/Dest"][0].get_object()
    new_target = new_link.get_object()["/Dest"][0].get_object()
    assert reader.get_page_number(old_target) == result.get_page_number(new_target)
with pdfplumber.open(destination) as document:
    author_lines = [line for line in document.pages[0].extract_text_lines() if line["text"] in names]
    assert len(author_lines) == 2
    for i, line in enumerate(author_lines):
        assert abs((line["x0"] + line["x1"]) / 2 - 306) < 0.1
        assert abs(line["top"] - (418.312968465 + i * 21.75)) < 0.1
print(json.dumps({"output": str(destination), "pages": 22, "authors_added": names, "toc_links": 46}, ensure_ascii=False))
