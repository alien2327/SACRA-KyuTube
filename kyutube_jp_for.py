import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pandas as pd
import pyperclip

def read_data():
    col =  ['title', 'code', 'datatype', 'group1', 'group2', 'media', 'comment', 'jp name', 'en name', 'Division', 'Class', 'loc', 'region', 'date', 'time', 'name', 'copy', 'microscope', 'automatic', 'ultraviolet', 'probe', 'interval', 'speed', 'link', 'tag']
    d = pd.read_csv("./data_jp_final.csv", names=col, encoding='utf-8')
    return d

data = read_data()
while True:
    code = input("Enter the code of page: ")
    data_mask = data['code'] == code
    filtered_data = data[data_mask]
    for i, (j, d) in enumerate(filtered_data.iterrows()):
        if d['jp name'] == '---':
            html = f"<h3>{d['en name']}</h3><p><strong>門</strong><br />{d['Division']}<br /><strong>綱</strong><br />{d['Class']}</p><br />&nbsp;"
            print(html)
            pyperclip.copy(html)
        else:
            html = f"<h4>{d['jp name']}</h4><h3>{d['en name']}</h3><p><strong>門</strong><br />{d['Division']}<br /><strong>綱</strong><br />{d['Class']}</p><br />&nbsp;"
            print(html)
            pyperclip.copy(html)
    if code == 'n':
        break