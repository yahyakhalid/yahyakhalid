"""Insert today's 3D contribution city into the profile panel.

Keeps the city, the total contributions and the date range; drops the
language pie, the radar and the star/fork counters.
"""
import re
import sys
import xml.etree.ElementTree as ET

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
city_src, template, dst = sys.argv[1], sys.argv[2], sys.argv[3]

root = ET.parse(city_src).getroot()


def name(el):
    return el.tag.split("}")[-1]


for el in list(root):
    text = "".join(el.itertext())
    if name(el) == "rect" and "fill-bg" in (el.get("class") or ""):
        root.remove(el)  # let the panel background show through
    elif name(el) == "g" and el.get("transform") and ("Commit" in text or "other" in text):
        root.remove(el)  # radar, language pie
    elif name(el) == "style":
        el.text = re.sub(r"\*\s*\{[^}]*\}", ".city text { font-family: 'Alexandria', 'Segoe UI', Arial, sans-serif; }", el.text or "")

for el in root:
    if name(el) == "g" and "contributions" in "".join(el.itertext()):
        drop = False
        for child in list(el):
            if name(child) == "g":  # star / fork icon
                el.remove(child)
                drop = True
            elif name(child) == "text" and drop:
                el.remove(child)
                drop = False

inner = "".join(ET.tostring(c, encoding="unicode") for c in root)
nested = f'<svg class="city" x="40" y="360" width="1200" height="778" viewBox="0 20 1280 830">{inner}</svg>'
out = open(template, encoding="utf-8").read().replace("<!--CITY-->", nested)
open(dst, "w", encoding="utf-8").write(out)
