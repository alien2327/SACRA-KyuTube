import pandas as pd

col =  ['title', 'code', 'datatype', 'group1', 'group2', 'media', 'comment', 'jp name', 'en name', 'Division', 'Class', 'loc', 'region', 'date', 'time', 'name', 'copy', 'microscope', 'automatic', 'ultraviolet', 'probe', 'interval', 'speed', 'link', 'tag']
d0 = pd.read_csv("./data_en_final.csv", names=col, encoding='utf-8')
d1 = pd.read_csv("./data_jp_final.csv", names=col, encoding='utf-8')
d2 = d1[['code','link']]
d = pd.merge(d0, d2, on='code')
d = d.rename(columns={'link_y':'link'})
print(d)