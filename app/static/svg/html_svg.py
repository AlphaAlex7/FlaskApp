import os

svg_template='<img src="{}" width="24" height="24" role="img" title="{}" alt="{}" style="margin: 10px;">'
res_str = ""
for i in os.listdir():
    if ".svg" in i:
        res_str+=svg_template.format(i,i,i)

with open("html_svg.html", "w") as html:
    html.write(res_str)

