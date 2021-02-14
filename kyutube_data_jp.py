# Inner modules
import pip, site, importlib
import os, csv
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import time

# Downloaded modules
print("\nChecking modules requirments. It will install module not exists automatically.")
try:
    import requests
    print("Module [requests] found")
except ImportError:
    print("Module [requests] not found")
    pip.main(['install', 'requests'])
    importlib.reload(site)
    import requests
try:
    import pandas as pd
    print("Module [pandas] found")
except ImportError:
    print("Module [pandas] not found")
    pip.main(['install', 'pandas'])
    importlib.reload(site)
    import pandas as pd
try:
    import bs4
    print("Module [beautifulsoup4] found")
except ImportError:
    print("Module [beautifulsoup4] not found")
    pip.main(['install', 'beautifulsoup4'])
    importlib.reload(site)
    import bs4
try:
    import urllib3
    print("Module [urllib3] found")
    from urllib3.exceptions import InsecureRequestWarning
    urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    print("Module [urllib3] not found")
    pip.main(['install', 'urllib3'])
    importlib.reload(site)
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning
    urllib3.disable_warnings(InsecureRequestWarning)
print("All modules are ready.\n")

def pick_data(url, datatype):
    data = []
    resp = requests.get(url, verify=False)
    try:
        soup = bs4.BeautifulSoup(resp.content, 'lxml')
    except:
        pip.main(['install', 'lxml'])
        importlib.reload(site)
        soup = bs4.BeautifulSoup(resp.content, 'lxml')
    cnts = soup.select_one("[class='row']")
    code = str.lower(cnts.find("div", class_="inline-block delimiter").text.strip())
    title = cnts.find("h1", class_="page-header").find("span").text.strip()
    group1 = cnts.find("div", class_="label font-md bg-head margin-right-xs link-white").text.strip()
    group2 = cnts.find("div", class_="label font-md bg-head link-white").find("a").text.strip()

    data.append(title)
    data.append(code)
    data.append(datatype)
    data.append(group1)
    data.append(group2)

    try:
        try:
            contents = cnts.find("div", class_="row clearfix").find_all("div", class_="col-xs-12")
        except:
            contents = cnts.find("div", class_="clearfix").find("div", class_="row clearfix").find_all("div", class_="col-xs-12")
        if datatype == "picture":
            for i, content in enumerate(contents):
                if i == 0:
                    media = content.find("div", class_="inline-block").find("img").get("src")
                    data.append(media)
                else:
                    try:
                        comment = content.find("div", class_="margin-top-sm").text.strip()
                        data.append(comment)
                    except:
                        data.append("---")
        elif datatype == "movie":
            for i, content in enumerate(contents):
                if i == 0:
                    media = content.find("div", class_="kaltura").find("iframe").get("src")
                    data.append(media)
                else:
                    try:
                        comment = content.find("div", class_="margin-top-sm").text.strip()
                        data.append(comment)
                    except:
                        data.append("---")
    except AttributeError:
        contents = cnts.find("div", class_="carousel-inner").find_all("div", class_="item")
        for content in contents:
            media = content.find("img").get("src")
            data.append(media)
            data.append("---")
    tables = cnts.find_all("table", class_="table table-striped")

    try:
        t = cnts.find("div", class_="bg-secondary bd-secondary padding-xs padding-left-sm padding-right-sm font-black taxonomy-term taxonomy-term--type-object taxonomy-term--view-mode-default ds-1col clearfix")
        try:
            namejp = t.find("div", class_="font-sm font-asbestos en-hide").text.strip()
            data.append(namejp)
        except:
            data.append("---")
        try:
            namereal = t.find("h3", class_="head-lg head-margin-xs").text.strip()
            data.append(namereal)
        except:
            data.append("---")
        names = t.find_all("div", class_="field field--name-taxonomy-term-title field--type-ds field--label-hidden field--item")
        for i, name in enumerate(names):
            if i == 0:
                data.append(name.find("a").text.strip())
            elif i == 1:
                data.append(name.find("a").text.strip())
    except:
        pass

    for table_0 in tables:
        table = table_0.find_all("tr")
        if len(table) == 5:
            for i, row in enumerate(table):
                if i == 0:
                    col2 = row.find("td").text.strip()
                    data.append(col2)
                    data.append("---")
                else:
                    col2 = row.find("td").text.strip()
                    data.append(col2)
        elif len(table) == 6:
            for row in table:
                col2 = row.find("td").text.strip()
                data.append(col2)
    return data

def conn_page():
    data = []
    for page in range(57):
        URL_base = "https://kyutubebio.sci.kyoto-u.ac.jp"
        URL="https://kyutubebio.sci.kyoto-u.ac.jp/jp/search?branch=All&title=&scientific_name=&name=&phylum=All&class=All&prefecture=All&country=&region=&target=All&keyword=&explanation=&paper=&photographer=All&copyright=All&flag=All&op=Search&page="
        URL += str(page)
        resp = requests.get(URL, verify=False)
        if resp.status_code == 200:
            print("Start collecting from KyuTube archive page : ", page)
            soup = bs4.BeautifulSoup(resp.content, 'lxml')
            cards = soup.find_all("div", class_="margin-bottom-lg")
            for card in cards:
                link = card.find("h2", class_="head-xl").find("a").get("href")
                if card.find("i", class_="glyphicon-camera"):
                    d = pick_data(URL_base+link, "picture")
                    data.append(d)
                else:
                    d = pick_data(URL_base+link, "movie")
                    data.append(d)
        else:
            print("Connection Failed")
    return data

def make_csv(data):
    col = ['title', 'code', 'datatype', 'group1', 'group2', 'media', 'comment', 'jp name', 'en name', 'div', 'class', 'loc', 'region', 'date', 'time', 'name', 'copy', 'microscope', 'automatic', 'ultraviolet', 'probe', 'interval', 'speed']
    res = pd.DataFrame(data, columns=col)
    res.to_csv('./data_jp_0.csv', index=False, encoding="cp932")
    return res

if __name__ == "__main__" :
    fp = open("./data_tag_jp_1.csv", 'a', newline="", encoding="utf-8")
    writer = csv.writer(fp)
    data = []
    tag = ['個体','個体群','分子','細胞小器官','細胞','組織','器官','生物群集']
    for tag_name in tag:
        base_url = f"https://kyutubebio.sci.kyoto-u.ac.jp/ja/search?branch=All&title=&scientific_name=&name=&phylum=All&class=All&prefecture=All&country=&region=&target={tag_name}&keyword=&explanation=&paper=&photographer=All&copyright=All&flag=All&op=Search&page="
        resp = requests.get(base_url, verify = False)
        if resp.status_code == 200:
            soup = bs4.BeautifulSoup(resp.content, 'lxml')
            page_amount = int(soup.find("div", class_="view-header").text.strip().split()[0])
            page_amount /= 10
            for page in range(int(page_amount+1)):
                base_url = f"https://kyutubebio.sci.kyoto-u.ac.jp/ja/search?branch=All&title=&scientific_name=&name=&phylum=All&class=All&prefecture=All&country=&region=&target={tag_name}&keyword=&explanation=&paper=&photographer=All&copyright=All&flag=All&op=Search&page=" + str(page)
                resp = requests.get(base_url, verify = False)
                if resp.status_code == 200:
                    soup = bs4.BeautifulSoup(resp.content, 'lxml')
                    cards = soup.find_all("div", class_="margin-bottom-lg")
                    for card in cards:
                        title = card.find("h2", class_="head-xl").find("a").text.strip()
                        code_link = card.find("div", class_="col-xs-12 group-footer").find("div", class_="text-right margin-top-xs").find("a").get("href")
                        code = code_link.split('/')[-1]
                        print(title, code, tag_name)
                        writer.writerow([tag_name, code_link])
                else:
                    print("Connection Failed")
        else:
            print("Connection Failed")