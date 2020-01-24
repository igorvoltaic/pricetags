#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import csv
from weasyprint import CSS, HTML
from weasyprint.fonts import FontConfiguration
import time
from datetime import date


if len(sys.argv) != 3:
    sys.exit("Usage: ./pricetags.py INPUT.csv OUTPUT.pdf")

infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile, "r") as file:
    reader = csv.reader(file, delimiter=';')
    products = list(reader)

today = date.today()
today = today.strftime("%d.%m.%Y")

properties = '@page{ margin: 3mm; size: A4 portrait; } '
properties += 'ul{  list-style: none; margin: 1.5em auto auto 0.3em; padding: 0; margin-top: 5px;} '
properties += '.box{ display: inline-block; margin: 1px; width: 65mm; height: 95mm; border: 1px solid black; position: relative; font-family: "Roboto Condensed"; } '
properties += 'ul li{ margin-left: 5px; margin-right: 5px;} '
properties += 'ul li span.fabric{ display: flex; font-size: 2em; height: 40px !important; margin-bottom: 9px !important; text-transform: uppercase; margin: 8px auto 0.5em 20px; font-weight: 700; } '
properties += '.desc{ margin-bottom: 0.5em; } '
properties += '.underline{ text-decoration:underline; } '
properties += 'ul li span.price{ position:absolute; font-size: 4.2em; margin: 25px 0.1em 0.5em 0px; right: 0.3em; font-weight: 700; } '
properties += '.date{ position:absolute; bottom:3px; left:0px; font-size: 0.7em; } '
properties += '#rur{ font-size: 0.4em; } '
properties += '.org{  position:absolute; bottom:3px; right:3px; font-size: 0.7em; }'

font_config = FontConfiguration()
css = CSS(string=properties, font_config=font_config)
pricetag = ""

# create pricetags and populate them with data
for product in products:
    if not product[5]:  # print only 1 tag if number of tags to print is not set
        product[5] = 1
    for tag in range(int(product[5].strip())):
        pricetag += '<div class="box">'
        pricetag += '<ul>'
        if len(product[0].strip()) > 9:
            pricetag += '<li class="desc">наименование:<br><span style="font-size: 1.2em" class="fabric">{}</span></li>'.format(product[0].strip())
        else:
            pricetag += '<li class="desc">наименование:<br><span class="fabric">{}</span></li>'.format(product[0].strip())
        pricetag += '<li class="desc">ширина: <span class="underline">{} метра</span></li>'.format(product[1].strip())
        pricetag += '<li class="desc">производитель: <span class="underline">{}</span></li>'.format(product[2].strip())
        if len(product[3]) < 1:
            pricetag += '<li class="desc">артикул: <span class="underline">{}</span></li>'.format('&nbsp;' * 25)
        else:
            pricetag += '<li class="desc">артикул: <span class="underline">{}</span></li>'.format(product[3].strip().rjust(6, '0'))
        pricetag += '<li class="desc">ед. изм.: <span class="underline">пог. метр</span></li>'
        pricetag += '<li class="desc">цена:<span class="price">{}<span id="rur"> &#x20bd;</span></span></li>'.format(product[4].strip())
        pricetag += '<li class="org">Магазин "{}"<br>ИП {}</li>'.format(product[7].strip(), product[6].strip())
        pricetag += '<li class="date">{}</li>'.format(today)
        pricetag += '</ul>'
        pricetag += '</div>'

# create an html body and add prototype
html = '<!DOCTYPE>'
html += '<html>'
html += '<head>'
html += '<style></style>'
html += '</head>'
html += '<body>'
html = html + pricetag
html += '</body>'
html += '</html>'

# compilte html file, set css and write the output to PDF file
doc = HTML(string=html)
doc.write_pdf(outfile, stylesheets=[css], font_config=font_config)

