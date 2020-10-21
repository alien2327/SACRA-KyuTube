import requests
import bs4
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

def pick(url,data_type):
    resp = requests.get(url, verify=False)
    print("Connecting: ", url)
    soup = bs4.BeautifulSoup(resp.content, 'lxml')
    cnts = soup.select_one("[class='row']")
    title = cnts.find("h1", class_="page-header").find("span").text
    groups = cnts.find("div", class_="col-xs-12 group-header")
    group1 = groups.find("div", class_="label font-md bg-head margin-right-xs link-white").text
    group2 = groups.find("div", class_="label font-md bg-head link-white").text
    number = groups.find("div", class_="inline-block delimiter").text
    if data_type == "picture":
        print("picture")
    elif data_type == "movie":
        print("movie")
    comment = cnts.find("div", class_="col-xs-12").find("div", class_="margin-top-sm").text
    species = [] #[和名, 学名, 門, 綱]
    spcs = cnts.find("div", class_="row clearfix margin-top-sm margin-bottom-sm")
    species.append(spcs.find("div", class_="font-sm font-asbestos en-hide").text)
    species.append(spcs.find("h3", class_="head-lg head-margin-xs").text)
    species.append(spcs.find("div", class_="margin-top-sm").find("a").text)
    species.append(spcs.find("div", class_="margin-top-xs").find("a").text)
    tbl1 = cnts.find("div", class_="col-lg-6 col-md-6 col-sm-6 col-sh-12 col-xs-12 group-left").find("table")
    tbl2 = cnts.find("div", class_="col-lg-6 col-md-6 col-sm-6 col-sh-12 col-xs-12 group-right").find("table")
    footer = cnts.find("div", class_="col-xs-12 group-footer")
    keys = footer.find_all("div", class_="inline-block delimiter")
    key = [item.text for item in keys]
    paper = footer.find("div", class_="margin-top-sm").select_one("[class='inline-block']").text
    author = footer.find("div", class_="margin-top-sm text-right").select_one("[class='inline-block']").text
    print(title)
    print(group1, group2, number)
    print(comment)
    print(species)
    print(tbl1, tbl2)
    print(key)
    print(paper)
    print(author)

if __name__ == '__main__':
    URL_parent = "https://kyutubebio.sci.kyoto-u.ac.jp/"
    URL="https://kyutubebio.sci.kyoto-u.ac.jp/ja/search?branch=All&title=&scientific_name=&name=&phylum=All&class=All&prefecture=All&country=&region=&target=All&keyword=&explanation=&paper=&photographer=All&copyright=All&flag=All&op=Search&page="
    for page in range(57):
        URL += str(page)
        resp = requests.get(URL, verify=False)
        if resp.status_code == 200:
            print("Connected page : ", page)
            soup = bs4.BeautifulSoup(resp.content, 'lxml')
            cards = soup.find_all("div", class_="margin-bottom-lg")
            for card in cards:
                title = card.find("h2", class_="head-xl").find("a").text
                href = card.find("h2", class_="head-xl").find("a").get("href")
                if card.find("i", class_="glyphicon-camera"):
                    print("Picture", title, URL_parent+href)
                else:
                    print("Movie", title, URL_parent+href)
        else:
            print("Connection Failed")