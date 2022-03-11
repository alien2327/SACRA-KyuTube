from bs4 import BeautifulSoup as bs
import requests
import pickle
import regex

from pages import *

class kyutube_page(object):
    def __init__(self, url: str) -> None:
        self.url_ja = url
        self.url_en = self.url_ja.replace('ja', 'en')

        self.p_info = page_info()
        self.b_info = bio_info()
        self.c_info = capture_info()
        self.cc_info = condition_info()

    def requests_page(self) -> None:
        r_ja = requests.get(self.url_ja)
        r_en = requests.get(self.url_en)
        self.soup_ja = bs(r_ja.text, 'lxml')
        self.soup_en = bs(r_en.text, 'lxml')
        self.text_wrapper = self.soup_ja.find('div', attrs={'class': 'text-wrapper'})
        self.tag_wrapper = self.soup_ja.find('div', attrs={'class': 'tag-wrapper'})
        self.text_wrapper_en = self.soup_en.find('div', attrs={'class': 'text-wrapper'})
        return

    def read_title(self) -> None:
        """ Read title from japanese and english page """
        self.p_info.title_jp = self.soup_ja.find('div', attrs={'class': 'visBox'}).text.strip()
        self.p_info.title_en = self.soup_en.find('div', attrs={'class': 'visBox'}).text.strip()
        return

    def read_classroom(self) -> None:
        """ Read Classroom, Subject, Index from <h2> tag from page """
        h2_title = self.text_wrapper.find('h2').text.strip().split(' ')
        if type(h2_title[2:]) == list: self.p_info.index = ''.join(h2_title[2:])
        else: self.p_info.index = h2_title[2]
        self.p_info.classroom = h2_title[0].replace('\xa0', '')
        self.p_info.subject = h2_title[1].replace('\xa0', '')
        return

    def check_media(self) -> None:
        """ Check video content """
        div_video = self.text_wrapper.find('div', attrs={'class': 'kaltura'})
        if div_video is not None:
            self.p_info.is_video = True
            self.p_info.data_type = 'MPEG4'
        else:
            self.p_info.is_video = False
            self.p_info.data_type = 'JPEG'
        return

    def read_bio(self) -> None:
        """ Read bio information from page """
        h4 = self.text_wrapper.find('h4')
        h3 = self.text_wrapper.find('h3')
        self.b_info.name_jp = h4.text.strip() if h4 is not None else ''
        self.b_info.name_en = h3.text.strip() if h3 is not None else ''

        txt = self.text_wrapper.text
        pattern_1 = r'門\s*[a-zA-Zあ-んア-ン一-鿐]+\s*綱'
        pattern_2 = r'綱\s*[a-zA-Zα-ωΑ-Ωあ-んア-ン一-鿐]+\s*'

        try:
            self.b_info.phylum = regex.findall(pattern_1, txt)[0][1:-1].strip()
            self.b_info.bio_class = regex.findall(pattern_2, txt)[0][1:].strip()
        except IndexError: # Some page has no bio information
            self.b_info.phylum = ''
            self.b_info.bio_class = ''
        self.p_info.bio.append(self.b_info)
        return

    def check_bio_tag(self) -> None:
        """ Read bio tag from page. \n
        Some page doesn't have tag, so maybe it should be filled manually. """
        txt = self.tag_wrapper.text
        pattern = r'階層段階\s*[a-zA-Zあ-んア-ン一-鿐]+\s*撮'
        try:
            self.p_info.bio_type = regex.findall(pattern, txt)[0][4:-1].strip()
        except IndexError:
            self.p_info.bio_type = ''
        return

    def read_capture_info(self) -> None:
        txt = self.text_wrapper.text
        pattern_local = r'都道府県'
        is_local = True if len(regex.findall(pattern_local, txt)) == 1 else False
        
        self.c_info.place_type = '' # Cannot read from page automatically, so it should be filled manually
        pattern_1 = r'都道府県\s*[a-zA-Zあ-んア-ン一-鿐]+\s*顕' if is_local else r'国\s*[:,!?.A-Za-zあ-んア-ン一-鿐 ]+\s*顕'
        pattern_2 = r'地域\s*[:,!?.A-Za-zあ-んア-ン一-鿐 ]+\s*自'
        self.c_info.is_local = '国内' if is_local else '国外'
        try:
            self.c_info.location_1 = regex.findall(pattern_1, txt)[0][4:-1].strip() if is_local else regex.findall(pattern_1, txt)[0][1:-1].strip()
            self.c_info.location_2 = regex.findall(pattern_2, txt)[0][2:-1].strip()
        except IndexError:
            self.c_info.location_1 = ''
            self.c_info.location_2 = ''
            self.c_info.is_local = ''
        self.p_info.capture_place = self.c_info
        return

    def read_table_info(self) -> None:
        def chk_str(reg, idx):
            try: return reg[0][idx:].strip()
            except IndexError: return ''

        txt = self.text_wrapper.text

        pattern_date = r'撮影日\s*[()0-9a-zA-Zα-ωΑ-Ω０-９あ-んア-ン一-鿐、。／/々ヶヵヴぅぃゥィ～（）　 :：ー・~\-,.?!]+\s*'
        pattern_time = r'撮影時刻\s*[()0-9a-zA-Zα-ωΑ-Ω０-９あ-んア-ン一-鿐、。／/々ヶヵヴぅぃゥィ～（）　 :：ー・~\-,.?!]+\s*'
        pattern_micro = r'顕微鏡の利用\s*[()0-9a-zA-Zα-ωΑ-Ω０-９あ-んア-ン一-鿐、。／/々ヶヵヴぅぃゥィ～（）　 :：ー・~\-,.?!]+\s*'
        pattern_auto = r'自動撮影装置の利用\s*[()0-9a-zA-Zα-ωΑ-Ω０-９あ-んア-ン一-鿐、。／/々ヶヵヴぅぃゥィ～（）　 :：ー・~\-,.?!]+\s*'
        pattern_infra = r'赤外線\s*[()0-9a-zA-Zα-ωΑ-Ω０-９あ-んア-ン一-鿐、。／/々ヶヵヴぅぃゥィ～（）　 :：ー・~\-,.?!]+\s*'
        pattern_photographer = r'撮影者\s*[()0-9a-zA-Zα-ωΑ-Ω０-９あ-んア-ン一-鿐、。／/々ヶヵヴぅぃゥィ～（）　 :：ー・~\-,.?!]+\s*'
        pattern_copyright = r'著作権者\s*[()0-9a-zA-Zα-ωΑ-Ω０-９あ-んア-ン一-鿐、。／/々ヶヵヴぅぃゥィ～（）　 :：ー・~\-,.?!]+\s*'
        pattern_probe = r'蛍光プローブ\s*[()0-9a-zA-Zα-ωΑ-Ω０-９あ-んア-ン一-鿐、。／/々ヶヵヴぅぃゥィ～（）　 :：ー・~\-,.?!]+\s*'
        pattern_interval = r'時間間隔[()一-鿐 ]+\s*[()0-9a-zA-Zα-ωΑ-Ω０-９あ-んア-ン一-鿐、。／/々ヶヵヴぅぃゥィ～（）　 :：ー・~\-,.．，?!]+\s*'
        pattern_speed = r'速度\s*[()0-9a-zA-Zα-ωΑ-Ω０-９あ-んア-ン一-鿐、。／/々ヶヵヴぅぃゥィ～（）　 :：ー・~\-,.?!]+\s*'

        self.p_info.capture_date = chk_str(regex.findall(pattern_date, txt), 3)
        self.p_info.capture_time = chk_str(regex.findall(pattern_time, txt), 4)

        self.cc_info.use_micro = chk_str(regex.findall(pattern_micro, txt), 6)
        self.cc_info.use_auto = chk_str(regex.findall(pattern_auto, txt), 9)
        self.cc_info.use_probe = chk_str(regex.findall(pattern_probe, txt), 6)
        self.cc_info.use_infrared = chk_str(regex.findall(pattern_infra, txt), 3)
        self.cc_info.capture_interval = chk_str(regex.findall(pattern_interval, txt), 8)
        self.cc_info.capture_speed = chk_str(regex.findall(pattern_speed, txt), 2)
        self.cc_info.photographer = chk_str(regex.findall(pattern_photographer, txt), 3)
        self.cc_info.copyright = chk_str(regex.findall(pattern_copyright, txt), 4)

        self.p_info.condition = self.cc_info
        return

    def check_keyword(self):
        txt = self.text_wrapper.text
        pattern_keyword = r'キーワード'
        is_keyword = True if len(regex.findall(pattern_keyword, txt)) == 1 else False
        pattern_keyword = r'キーワード：[-:.,?!0-9a-zA-Zあ-んア-ン一-鿐 ]+\s*'
        self.p_info.keywords = regex.findall(pattern_keyword, txt)[0][6:].strip() if is_keyword else ''
        return

    def read_ja_comment(self):
        h2_title = self.text_wrapper.find('h2').text
        pattern = h2_title + r'\s*[()0-9a-zA-Zα-ωΑ-Ω０-９あ-んア-ン一-鿐、。／/々ヶヵヴぅぃゥィ～（）　 ：ー・~\-,.?!]+\s*'
        txt = self.text_wrapper.text
        comment = regex.findall(pattern, txt)[0]
        comment = regex.sub(h2_title, '', comment).strip()
        comment = regex.sub('---', '', comment)

        h4_title = self.text_wrapper.find('h4')
        
        if h4_title:
            h4_title = h4_title.text.strip()
            h4_title_len = len(h4_title)
            comment_len = len(comment)
            if h4_title_len == comment_len: comment = ''
        else:
            h3_title = self.text_wrapper.find('h3')
            if h3_title:
                h3_title = h3_title.text
                h3_title_len = len(h3_title)
                comment_len = len(comment)
                if h3_title_len == comment_len: comment = ''
            else: pass
        self.p_info.comment_jp = comment
        return

    def read_en_comment(self):
        try:
            h2_title = self.text_wrapper_en.find('h2').text
        except AttributeError:
            self.p_info.comment_en = ''
            return
        pattern = h2_title + r'\s*[()0-9a-zA-Zα-ωΑ-Ω０-９あ-んア-ン一-鿐、。／/々ヶヵヴぅぃゥィ～（）　 ：ー・~\-,.?!]+\s*'
        txt = self.text_wrapper_en.text
        comment = regex.findall(pattern, txt)[0]
        comment = regex.sub(h2_title, '', comment).strip()
        comment = regex.sub('---', '', comment)

        h4_title = self.text_wrapper.find('h4')
        
        if h4_title:
            h4_title = h4_title.text.strip()
            h4_title_len = len(h4_title)
            comment_len = len(comment)
            if h4_title_len == comment_len: comment = ''
        else:
            h3_title = self.text_wrapper.find('h3')
            if h3_title:
                h3_title = h3_title.text
                h3_title_len = len(h3_title)
                comment_len = len(comment)
                if h3_title_len == comment_len: comment = ''
            else: pass
        self.p_info.comment_en = comment
        return

    def __str__(self):
        return f"""
            page url(ja): {self.url_ja}
            page url(en): {self.url_en}
            page source:
            {self.text_wrapper}
        """

    def get_page_info(self) -> page_info:
        return self.p_info

    def to_pickle(self) -> None:
        with open(f'./pkl/{self.p_info.index}.pkl', mode='wb') as f:
            pickle.dump(self.p_info, f)
        return