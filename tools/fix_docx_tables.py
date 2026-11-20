"""Give pandoc's Word tables fixed column widths sized to their content.

Pandoc writes tables at a percentage width with equal columns, which Google Docs
handles poorly. This sets a fixed table width, per-column widths proportional to
each column's text, and a matching width on every cell.
Usage: python3 -I fix_docx_tables.py file.docx [more.docx ...]
"""
import re, sys, zipfile, shutil, tempfile, os

TOTAL = 9360  # 6.5 inches of text width, in twentieths of a point

def cell_text(tc):
    return "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", tc))

def fix_table(tbl):
    rows = re.findall(r"<w:tr>.*?</w:tr>", tbl, flags=re.S)
    if not rows:
        return tbl
    ncols = max(len(re.findall(r"<w:tc>", r)) for r in rows)
    weight = [0.0] * ncols
    for r in rows:
        for i, tc in enumerate(re.findall(r"<w:tc>.*?</w:tc>", r, flags=re.S)):
            n = len(cell_text(tc))
            weight[i] = max(weight[i], min(n, 60) ** 0.8 + 4)
    s = sum(weight)
    widths = [max(900, int(TOTAL * w / s)) for w in weight]
    widths[-1] += TOTAL - sum(widths)
    tbl = re.sub(r'<w:tblW [^>]*/>', f'<w:tblW w:type="dxa" w:w="{TOTAL}" /><w:tblLayout w:type="fixed" />', tbl, count=1)
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{w}" />' for w in widths) + "</w:tblGrid>"
    tbl = re.sub(r"<w:tblGrid>.*?</w:tblGrid>", grid, tbl, count=1, flags=re.S)

    def fix_row(m):
        i = [-1]
        def fix_cell(c):
            i[0] += 1
            w = widths[min(i[0], ncols - 1)]
            return c.group(0).replace("<w:tcPr />", f'<w:tcPr><w:tcW w:type="dxa" w:w="{w}" /></w:tcPr>', 1)
        return re.sub(r"<w:tc>.*?</w:tc>", fix_cell, m.group(0), flags=re.S)
    return re.sub(r"<w:tr>.*?</w:tr>", fix_row, tbl, flags=re.S)

def fix(path):
    with zipfile.ZipFile(path) as z:
        items = {n: z.read(n) for n in z.namelist()}
    doc = items["word/document.xml"].decode("utf-8")
    doc = re.sub(r"<w:tbl>.*?</w:tbl>", lambda m: fix_table(m.group(0)), doc, flags=re.S)
    items["word/document.xml"] = doc.encode("utf-8")
    fd, tmp = tempfile.mkstemp(suffix=".docx")
    os.close(fd)
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n, b in items.items():
            if not n.endswith("/"):
                z.writestr(n, b)
    shutil.move(tmp, path)

if __name__ == "__main__":
    for p in sys.argv[1:]:
        fix(p)
        print("fixed", p)
