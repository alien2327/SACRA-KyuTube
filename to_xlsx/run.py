from bs4 import BeautifulSoup as bs
import requests
from tqdm import tqdm

from pages import *
from update import update
from chk_page import kyutube_page

num_childs = {
    2892: 1, 2893: 1, 2894: 1, 2895: 1, 2896: 2,
    2897: 1, 2898: 1, 2899: 1, 2900: 1, 2901: 1,
    2902: 21, 2903: 9, 2904: 2, 2905: 2, 2906: 1,
    2907: 2, 2908: 3, 2909: 8
}

def read_content(url: str):
    page = kyutube_page(url)
    page.requests_page()
    page.read_title()
    page.read_classroom()
    page.check_media()
    page.read_bio()
    page.check_bio_tag()
    page.read_capture_info()
    page.read_table_info()
    page.read_ja_comment()
    page.read_en_comment()
    page.to_pickle()

def main():
    print('Start searching')
    for idx in tqdm(range(2892, 2910, 1), desc="parent page"):
        for p in tqdm(range(1, num_childs[idx]+1), leave=False, desc="child page"):
            mask_url = f'http://www.sci.kyoto-u.ac.jp'
            target_jp = f'http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{idx}/?page={p}'
            r = requests.get(target_jp)
            soup = bs(r.text, 'lxml')
            cards = soup.find_all('li', attrs={'line': 'order_line'})
            for a in cards:
                link = a.find('a').get('href')
                url = mask_url + link
                read_content(url)
    print('End searching')
    update('./kyutube.xlsx')

if __name__ == "__main__":
    main()