# Inner modules
import pip, site, importlib
import os, csv
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import time

# Downloaded modules
print("\nChecking modules requirments. It will install module not exists automatically.")
try:
    from selenium import webdriver
    print("Module [selenium] found")
except ImportError:
    print("Module [selenium] not found")
    pip.main(['install', 'selenium'])
    importlib.reload(site)
    from selenium import webdriver
try:
    import chromedriver_binary
    print("Module [chromedriver_binary] found")
except ImportError:
    print("Module [chromedriver_binary] not found")
    pip.main(['install', 'chromedriver_binary'])
    importlib.reload(site)
    import chromedriver_binary
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
                    download_img(media)
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
                    download_thumb(code, media)
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
            download_img(media)
            data.append(media)
            data.append("---")
            break
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
                try:
                    data.append(name.find("a").text.strip())
                except:
                    data.append("---")
            elif i == 1:
                try:
                    data.append(name.find("a").text.strip())
                except:
                    data.append("---")
    except:
        data.append("---")
        data.append("---")

    for table_0 in tables:
        table = table_0.find_all("tr")
        if len(table) == 4:
            for i, row in enumerate(table):
                if i == 0:
                    data.append("---")
                    data.append("---")
                    col2 = row.find("td").text.strip()
                    data.append(col2)                    
                else:
                    col2 = row.find("td").text.strip()
                    data.append(col2)
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
    fp = open("./data_en.csv", 'a', newline="", encoding="utf-8")
    writer = csv.writer(fp)
    data = []
    for page in range(57):
        URL_base = "https://kyutubebio.sci.kyoto-u.ac.jp"
        URL="https://kyutubebio.sci.kyoto-u.ac.jp/en/search?branch=All&title=&scientific_name=&name=&phylum=All&class=All&prefecture=All&country=&region=&target=All&keyword=&explanation=&paper=&photographer=All&copyright=All&flag=All&op=Search&page="
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
                    d.append(link)
                    writer.writerow(d)
                    data.append(d)
                else:
                    d = pick_data(URL_base+link, "movie")
                    d.append(link)
                    writer.writerow(d)
                    data.append(d)
        else:
            print("Connection Failed")
    return 0

def read_data():
    if not os.path.isfile("./data_en.csv"):
        print("Containing data to csv file.")
        conn_page()
    col = ['title', 'code', 'datatype', 'group1', 'group2', 'media', 'comment', 'jp name', 'en name', 'div', 'class', 'loc', 'region', 'date', 'time', 'name', 'copy', 'microscope', 'automatic', 'ultraviolet', 'probe', 'interval', 'speed', 'link']
    d = pd.read_csv("./data_en.csv", names=col)
    return d

def download_img(link):
    img_path = './kyu_img'
    if 'kyutubebio' not in link:
        link = "https://kyutubebio.sci.kyoto-u.ac.jp" + link
    if not os.path.isdir(img_path):
        os.makedirs(img_path)
    if not os.path.isfile(img_path + '/' + link.split('/')[-1]):
        re = requests.get(link, verify=False)
        with open(img_path + '/' + link.split('/')[-1], 'wb') as f:
            f.write(re.content)

def download_thumb(fname, link):
    img_path = './kyu_img'
    code = link[155:165]
    link = f"https://cfvod.kaltura.com/p/2075011/sp/207501100/thumbnail/entry_id/{code}/version/100022/width/500"
    if not os.path.isdir(img_path):
        os.makedirs(img_path)
    if not os.path.isfile(img_path + '/' + fname + ".jpg"):
        re = requests.get(link, verify=False)
        with open(img_path + '/' + fname + ".jpg", 'wb') as f:
            f.write(re.content)

def check_data(title, data):
    for i, data_pd in enumerate(data):
        if title == data_pd.at[0, 'title']:
            del data[i]
            print(f"{title} exists.")
    return data

def login(driver, userid, userpw):
    sci_admin_id = driver.find_element_by_name("act_id")
    sci_admin_pw = driver.find_element_by_name("act_passwd")
    sci_admin_id.send_keys(userid)
    sci_admin_pw.send_keys(userpw)
    sci_admin_login = driver.find_element_by_xpath("/html/body/form/div/input")
    sci_admin_login.click()

if __name__ == "__main__":
    data = read_data()
    userid = "lee"
    userpw = "Mv3qKTUH"
    #userid = input("Enter your admin id: ")
    #userpw = input("Enter your admin password: ")

    driver = webdriver.Chrome()
    driver.get("https://www.sci.kyoto-u.ac.jp/en/admin/")
    login(driver, userid, userpw)
    time.sleep(0.5)
    new_page_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/div[2]/form/input")
    new_page_btn.click()

    time.sleep(0.5)

    tag_1 = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li/select")
    select_tag_1 = webdriver.support.select.Select(tag_1)
    select_tag_1.select_by_visible_text('Misc')
    time.sleep(0.5)
    tag_2 = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li[1]/select[2]")
    select_tag_2 = webdriver.support.select.Select(tag_2)
    select_tag_2.select_by_visible_text('Kyu Tube Bio')
    tag_1 = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li[2]/select")
    select_tag_1 = webdriver.support.select.Select(tag_1)
    select_tag_1.select_by_visible_text('Misc')
    time.sleep(0.5)
    tag_2 = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li[2]/select[2]")
    select_tag_2 = webdriver.support.select.Select(tag_2)
    select_tag_2.select_by_visible_text('Kyu Tube Bio')



"""
    time.sleep(0.5)
    research_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/table/tbody/tr[4]/td[7]/input[2]")
    research_btn.click()

    time.sleep(0.5)
    kyutube_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/table/tbody/tr[10]/td[7]/input[2]")
    kyutube_btn.click()

    time.sleep(0.5)
    total_page = 0
"""