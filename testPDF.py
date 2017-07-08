import pdfkit
import os
def save_PDF(htmls):
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
    }
    htmls = []
    for x in os.listdir('.'):
        if os.path.isfile(x):
            htmls.append(x)
    print(htmls)
    # pdfkit.from_file(htmls, "廖雪峰的Python.pdf", options=options)