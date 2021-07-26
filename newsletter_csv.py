import pandas as pd
from sys import argv

script, csv_file, target = argv

fin = open(target, 'w')

fin.close()

space = '&nbsp;'

first_article = """<br/>
<span style=\"color:#000000\">"""

second_article = """</span><a href=\""""

third_article = """\" target=\"_blank\"><span style=\"color:rgb(0, 0, 255)\">continua</span></a><br/>"""

first_header = """<div style=\"text-align: left;\"><span style=\"font-family:open sans\"><span style=\"font-size:18px\"><font color=\"#000000\"><strong>"""

end_header = """</strong></font><br/>"""

newsletter = pd.read_csv(csv_file)

sections = newsletter['section'].unique()

for section in sections:
    temp_section = newsletter[newsletter['section'] == section]
    articles = first_header + ''.join(temp_section['section'].unique()) + end_header

    for index, row in temp_section.iterrows():
        temp_article = first_article + row['title'] + space + second_article + row['link'] + third_article
        articles = articles + temp_article

    fin = open(target, "a")

    articles = '\n\n' + '## Sezione ' + section + '\n\n' + articles

    fin.write(articles);

    fin.close()
