# Inner modules
import pip, site, importlib, re
import os, requests, sys, time, bs4, urllib3
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pandas as pd
from selenium import webdriver, common
import chromedriver_binary

def login(driver, userid, userpw):
    sci_admin_id = driver.find_element_by_name("act_id")
    sci_admin_pw = driver.find_element_by_name("act_passwd")
    sci_admin_id.send_keys(userid)
    sci_admin_pw.send_keys(userpw)
    sci_admin_login = driver.find_element_by_xpath("/html/body/form/div/input")
    sci_admin_login.click()

def page_edit(driver, data, index=0):
    new_page_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/div[2]/form/input")
    new_page_btn.click()

    time.sleep(0.5)

    new_file = driver.find_element_by_name("cts_filepath")
    new_title = driver.find_element_by_name("cts_title")
    new_inschool = driver.find_element_by_name("cts_inplaceflag")
    new_hidtop = driver.find_element_by_name("cts_hidetoplistflag")
    new_hidtag = driver.find_element_by_name("cts_hidesearchtagflag")
    new_hidtext = driver.find_element_by_name("cts_hideindexflag")
    new_main_src = driver.find_element_by_xpath("//*[@id=\"cke_14\"]")
    new_main_img = driver.find_element_by_xpath("//*[@id=\"cke_51\"]")
    #new_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[1]")
    new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")

    upload_thumb = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[9]/td/input[2]")
    if data['datatype'] == "picture":
        if os.path.getsize(os.getcwd() + f"\\kyu_img\\{data['media'].split('/')[-1]}") > 3000000:
            upload_thumb.send_keys(os.getcwd() + f"/kyu_img/{data['media'].split('/')[-1]}"[:-4] + "_resized.jpg")
            time.sleep(1.0)
        else:
            upload_thumb.send_keys(os.getcwd() + f"/kyu_img/{data['media'].split('/')[-1]}")
            time.sleep(1.0)
    elif data['datatype'] == "movie":
        upload_thumb.send_keys(os.getcwd() + f"/kyu_img/{data['code']}" + ".jpg")
        time.sleep(1.0)
    

    new_file.send_keys(data['code'])

    if len(data['title']) > 100:
        new_title.send_keys(data['title'][:100])
    else:
        new_title.send_keys(data['title'])
    new_inschool.click()
    new_hidtop.click()
    new_hidtag.click()
    new_hidtext.click()
    
    if data['datatype'] == 'picture':
        new_main_img.click()
        time.sleep(0.5)
        new_main_img_upload = driver.find_element_by_id("cke_Upload_136")
        driver.execute_script("arguments[0].click();", new_main_img_upload)
        iframe = driver.find_element_by_xpath('//*[@id="cke_131_fileInput"]')
        driver.switch_to.frame(iframe)
        new_main_img_select = driver.find_element_by_xpath("//*[@id=\"cke_131_fileInput_input\"]")
        new_main_img_select.send_keys(os.getcwd() + f"\\kyu_img\\{data['media'].split('/')[-1]}")
        time.sleep(0.8)
        driver.switch_to.default_content()
        new_main_img_confirm = driver.find_element_by_id("cke_133_label")
        new_main_img_confirm.click()
        if os.path.getsize(os.getcwd() + f"\\kyu_img\\{data['media'].split('/')[-1]}") > 3000000:
            time.sleep(10)
        else:
            time.sleep(5)
        new_main_img_information = driver.find_element_by_id("cke_info_129")
        new_main_img_information.click()
        time.sleep(1.5)
        new_main_img_infotext = driver.find_element_by_id("cke_95_textInput")
        img_link = new_main_img_infotext.get_attribute('value')
        new_main_img_back = driver.find_element_by_id("cke_140_label")
        new_main_img_back.click()
        driver.switch_to.alert.accept()
        driver.switch_to.default_content()

    time.sleep(1.0)
    index = 1
    tag_options = []
    tag_1 = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li/select")
    select_tag_1 = webdriver.support.select.Select(tag_1)
    select_tag_1.select_by_visible_text('Misc')
    time.sleep(0.5)
    tag_2 = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li[1]/select[2]")
    select_tag_2 = webdriver.support.select.Select(tag_2)
    select_tag_2.select_by_visible_text('Kyu Tube Bio')
    time.sleep(1.0)
    
    if data['datatype'] == 'picture':
        tag_3 = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li[1]/select[3]")
        select_tag_3 = webdriver.support.select.Select(tag_3)
        all_available_options = select_tag_3.options
        for item in all_available_options:
            tag_options.append(item.text)
        select_tag_3.select_by_visible_text('Medium Picture')
    else:
        tag_3 = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li[1]/select[3]")
        select_tag_3 = webdriver.support.select.Select(tag_3)
        all_available_options = select_tag_3.options
        for item in all_available_options:
            tag_options.append(item.text)
        select_tag_3.select_by_visible_text('Medium Movie')
    
    try:
        index += 1
        set_tag(driver, data, 'group1', tag_options, index)
    except:
        pass
    try:
        index += 1
        set_tag(driver, data, 'group2', tag_options, index)
    except:
        pass
    try:
        index += 1
        set_tag(driver, data, 'loc', tag_options, index)
    except:
        pass
    try:
        index += 1
        set_tag(driver, data, 'tag', tag_options, index)
    except:
        pass
    try:
        index += 1
        set_tag(driver, data, 'name', tag_options, index)
    except:
        pass
    try:
        index += 1
        set_tag(driver, data, 'copy', tag_options, index)
    except:
        pass
    try:
        if data['en name'] != '---':
            index += 1
            set_tag(driver, data, 'Division', tag_options, index)
            index += 1
            set_tag(driver, data, 'Class', tag_options, index)
    except:
        pass

    new_main_src.click()
    time.sleep(0.5)
    new_main_textbox = driver.find_element_by_xpath("//*[@id=\"cke_1_contents\"]/textarea")

    if index != 0:
        page = index

    try:
        comment = data['comment']
    except:
        comment = "" 

    if data['datatype'] == 'picture':
        if data['en name'] != '---':
            if is_japan(data['loc']):
                new_main_textbox.send_keys(f"<h2>{data['group1']} {data['group2']} {str.upper(data['code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p> \
                <h3>{data['en name']}</h3><p><strong>Phylum</strong><br />{data['Division']}<br /><strong>Class</strong><br />{data['Class']}</p><br />&nbsp;<table align=\"center\"> \
                <tbody><tr><th>Prefecture</th><td>{data['loc']}</td><th>Use of Microscope</th><td>{data['microscope']}</td></tr> \
                <tr><th>Region</th><td>{data['region']}</td><th>Use of Automatic Shooting Devices</th><td>{data['automatic']}</td></tr> \
                <tr><th>Shooting Date</th><td>{data['date']}</td><th>Use of Fluorescent Probe</th><td>{data['ultraviolet']}</td></tr> \
                <tr><th>Shooting Time</th><td>{data['time']}</td><th>Use of Infrared</th><td>{data['probe']}</td></tr> \
                <tr><th>Photographer</th><td>{data['name']}</td><th>Shooting Interval (Sec.)</th><td>{data['interval']}</td></tr> \
                <tr><th>Copyright Holder</th><td>{data['copy']}</td><th>Shooting Speed</th><td>{data['speed']}</td></tr></tbody></table><br /> \
                <a href=\"http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{page}/{data['code']}.html\">In Japanese</a>")
            else:
                new_main_textbox.send_keys(f"<h2>{data['group1']} {data['group2']} {str.upper(data['code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p> \
                <h3>{data['en name']}</h3><p><strong>Phylum</strong><br />{data['Division']}<br /><strong>Class</strong><br />{data['Class']}</p><br />&nbsp;<table align=\"center\"> \
                <tbody><tr><th>Country</th><td>{data['loc']}</td><th>Use of Microscope</th><td>{data['microscope']}</td></tr> \
                <tr><th>Region</th><td>{data['region']}</td><th>Use of Automatic Shooting Devices</th><td>{data['automatic']}</td></tr> \
                <tr><th>Shooting Date</th><td>{data['date']}</td><th>Use of Fluorescent Probe</th><td>{data['ultraviolet']}</td></tr> \
                <tr><th>Shooting Time</th><td>{data['time']}</td><th>Use of Infrared</th><td>{data['probe']}</td></tr> \
                <tr><th>Photographer</th><td>{data['name']}</td><th>Shooting Interval (Sec.)</th><td>{data['interval']}</td></tr> \
                <tr><th>Copyright Holder</th><td>{data['copy']}</td><th>Shooting Speed</th><td>{data['speed']}</td></tr></tbody></table><br /> \
                <a href=\"http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{page}/{data['code']}.html\">In Japanese</a>")
        else:
            if is_japan(data['loc']):
                new_main_textbox.send_keys(f"<h2>{data['group1']} {data['group2']} {str.upper(data['code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                <tbody><tr><th>Prefecture</th><td>{data['loc']}</td><th>Use of Microscope</th><td>{data['microscope']}</td></tr> \
                <tr><th>Region</th><td>{data['region']}</td><th>Use of Automatic Shooting Devices</th><td>{data['automatic']}</td></tr> \
                <tr><th>Shooting Date</th><td>{data['date']}</td><th>Use of Fluorescent Probe</th><td>{data['ultraviolet']}</td></tr> \
                <tr><th>Shooting Time</th><td>{data['time']}</td><th>Use of Infrared</th><td>{data['probe']}</td></tr> \
                <tr><th>Photographer</th><td>{data['name']}</td><th>Shooting Interval (Sec.)</th><td>{data['interval']}</td></tr> \
                <tr><th>Copyright Holder</th><td>{data['copy']}</td><th>Shooting Speed</th><td>{data['speed']}</td></tr></tbody></table><br /> \
                <a href=\"http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{page}/{data['code']}.html\">In Japanese</a>")
            else:
                new_main_textbox.send_keys(f"<h2>{data['group1']} {data['group2']} {str.upper(data['code'])}</h2><img alt=\"\" src=\"{img_link}\" /> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                <tbody><tr><th>Country</th><td>{data['loc']}</td><th>Use of Microscope</th><td>{data['microscope']}</td></tr> \
                <tr><th>Region</th><td>{data['region']}</td><th>Use of Automatic Shooting Devices</th><td>{data['automatic']}</td></tr> \
                <tr><th>Shooting Date</th><td>{data['date']}</td><th>Use of Fluorescent Probe</th><td>{data['ultraviolet']}</td></tr> \
                <tr><th>Shooting Time</th><td>{data['time']}</td><th>Use of Infrared</th><td>{data['probe']}</td></tr> \
                <tr><th>Photographer</th><td>{data['name']}</td><th>Shooting Interval (Sec.)</th><td>{data['interval']}</td></tr> \
                <tr><th>Copyright Holder</th><td>{data['copy']}</td><th>Shooting Speed</th><td>{data['speed']}</td></tr></tbody></table><br /> \
                <a href=\"http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{page}/{data['code']}.html\">In Japanese</a>")                   
    elif data['datatype'] == 'movie':
        if data['en name'] != '---':
            if is_japan(data['loc']):
                new_main_textbox.send_keys(f"<h2>{data['group1']} {data['group2']} {str.upper(data['code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                src=\"{data['media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p> \
                <h3>{data['en name']}</h3><p><strong>Phylum</strong><br />{data['Division']}<br /><strong>Class</strong><br />{data['Class']}</p><br />&nbsp;<table align=\"center\"> \
                <tbody><tr><th>Prefecture</th><td>{data['loc']}</td><th>Use of Microscope</th><td>{data['microscope']}</td></tr> \
                <tr><th>Region</th><td>{data['region']}</td><th>Use of Automatic Shooting Devices</th><td>{data['automatic']}</td></tr> \
                <tr><th>Shooting Date</th><td>{data['date']}</td><th>Use of Fluorescent Probe</th><td>{data['ultraviolet']}</td></tr> \
                <tr><th>Shooting Time</th><td>{data['time']}</td><th>Use of Infrared</th><td>{data['probe']}</td></tr> \
                <tr><th>Photographer</th><td>{data['name']}</td><th>Shooting Interval (Sec.)</th><td>{data['interval']}</td></tr> \
                <tr><th>Copyright Holder</th><td>{data['copy']}</td><th>Shooting Speed</th><td>{data['speed']}</td></tr></tbody></table><br /> \
                <a href=\"http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{page}/{data['code']}.html\">In Japanese</a>")
            else:
                new_main_textbox.send_keys(f"<h2>{data['group1']} {data['group2']} {str.upper(data['code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                src=\"{data['media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p> \
                <h3>{data['en name']}</h3><p><strong>Phylum</strong><br />{data['Division']}<br /><strong>Class</strong><br />{data['Class']}</p><br />&nbsp;<table align=\"center\"> \
                <tbody><tr><th>Country</th><td>{data['loc']}</td><th>Use of Microscope</th><td>{data['microscope']}</td></tr> \
                <tr><th>Region</th><td>{data['region']}</td><th>Use of Automatic Shooting Devices</th><td>{data['automatic']}</td></tr> \
                <tr><th>Shooting Date</th><td>{data['date']}</td><th>Use of Fluorescent Probe</th><td>{data['ultraviolet']}</td></tr> \
                <tr><th>Shooting Time</th><td>{data['time']}</td><th>Use of Infrared</th><td>{data['probe']}</td></tr> \
                <tr><th>Photographer</th><td>{data['name']}</td><th>Shooting Interval (Sec.)</th><td>{data['interval']}</td></tr> \
                <tr><th>Copyright Holder</th><td>{data['copy']}</td><th>Shooting Speed</th><td>{data['speed']}</td></tr></tbody></table><br /> \
                <a href=\"http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{page}/{data['code']}.html\">In Japanese</a>")
        else:
            if is_japan(data['loc']):
                new_main_textbox.send_keys(f"<h2>{data['group1']} {data['group2']} {str.upper(data['code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                src=\"{data['media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                <tbody><tr><th>Prefecture</th><td>{data['loc']}</td><th>Use of Microscope</th><td>{data['microscope']}</td></tr> \
                <tr><th>Region</th><td>{data['region']}</td><th>Use of Automatic Shooting Devices</th><td>{data['automatic']}</td></tr> \
                <tr><th>Shooting Date</th><td>{data['date']}</td><th>Use of Fluorescent Probe</th><td>{data['ultraviolet']}</td></tr> \
                <tr><th>Shooting Time</th><td>{data['time']}</td><th>Use of Infrared</th><td>{data['probe']}</td></tr> \
                <tr><th>Photographer</th><td>{data['name']}</td><th>Shooting Interval (Sec.)</th><td>{data['interval']}</td></tr> \
                <tr><th>Copyright Holder</th><td>{data['copy']}</td><th>Shooting Speed</th><td>{data['speed']}</td></tr></tbody></table><br /> \
                <a href=\"http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{page}/{data['code']}.html\">In Japanese</a>")                  
            else:
                new_main_textbox.send_keys(f"<h2>{data['group1']} {data['group2']} {str.upper(data['code'])}</h2><div class=\"kaltura\"><iframe frameborder=\"0\" height=\"544\" id=\"kaltura_player\" \
                src=\"{data['media']}\" title=\"Kaltura Player\" width=\"912\"></iframe></div> &nbsp;<p>{comment}</p><br /><table align=\"center\"> \
                <tbody><tr><th>Country</th><td>{data['loc']}</td><th>Use of Microscope</th><td>{data['microscope']}</td></tr> \
                <tr><th>Region</th><td>{data['region']}</td><th>Use of Automatic Shooting Devices</th><td>{data['automatic']}</td></tr> \
                <tr><th>Shooting Date</th><td>{data['date']}</td><th>Use of Fluorescent Probe</th><td>{data['ultraviolet']}</td></tr> \
                <tr><th>Shooting Time</th><td>{data['time']}</td><th>Use of Infrared</th><td>{data['probe']}</td></tr> \
                <tr><th>Photographer</th><td>{data['name']}</td><th>Shooting Interval (Sec.)</th><td>{data['interval']}</td></tr> \
                <tr><th>Copyright Holder</th><td>{data['copy']}</td><th>Shooting Speed</th><td>{data['speed']}</td></tr></tbody></table><br /> \
                <a href=\"http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{page}/{data['code']}.html\">In Japanese</a>")

    new_main_src.click()
    time.sleep(1.0)

    try:
        new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[3]")
        new_confirm.click()
        time.sleep(1.0)
        new_confirm_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
        new_confirm_confirm.click()
        time.sleep(2.0)
        new_confirm_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input")
        new_confirm_back.click()
        time.sleep(1.0)

    except:
        new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
        new_confirm.click()
        time.sleep(1.0)
        new_confirm_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
        new_confirm_confirm.click()
        time.sleep(2.0)
        new_confirm_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input")
        new_confirm_back.click()
        time.sleep(1.0)

def folder_edit(driver, data):
    new_page_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/div[2]/form/input")
    new_page_btn.click()
    codes = data['link'].split('/')[-1].upper().replace('-',',')
    time.sleep(0.5)

    isfolder = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[1]/td/label[2]/input")
    isfolder.click()

    new_file = driver.find_element_by_name("cts_filepath")
    new_title = driver.find_element_by_name("cts_title")
    new_inschool = driver.find_element_by_name("cts_inplaceflag")
    new_hidtop = driver.find_element_by_name("cts_hidetoplistflag")
    new_hidtag = driver.find_element_by_name("cts_hidesearchtagflag")
    new_hidtext = driver.find_element_by_name("cts_hideindexflag")
    new_main_src = driver.find_element_by_xpath("//*[@id=\"cke_14\"]")
    new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")

    new_file.send_keys(data['link'].split('/')[-1].split('-')[0]+'-'+data['link'].split('/')[-1].split('-')[-1])
    new_title.send_keys(data['title'])
    new_inschool.click()
    new_hidtop.click()
    new_hidtag.click()
    new_hidtext.click()

    index = 1
    tag_options = []
    tag_1 = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li/select")
    select_tag_1 = webdriver.support.select.Select(tag_1)
    select_tag_1.select_by_visible_text('Misc')
    time.sleep(0.5)
    tag_2 = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li[1]/select[2]")
    select_tag_2 = webdriver.support.select.Select(tag_2)
    select_tag_2.select_by_visible_text('Kyu Tube Bio')
    time.sleep(0.5)
    if data['datatype'] == 'picture':
        tag_3 = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li[1]/select[3]")
        select_tag_3 = webdriver.support.select.Select(tag_3)
        all_available_options = select_tag_3.options
        for item in all_available_options:
            tag_options.append(item.text)
        select_tag_3.select_by_visible_text('Medium Picture')
    else:
        tag_3 = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li[1]/select[3]")
        select_tag_3 = webdriver.support.select.Select(tag_3)
        all_available_options = select_tag_3.options
        for item in all_available_options:
            tag_options.append(item.text)
        select_tag_3.select_by_visible_text('Medium Movie')

    try:
        index += 1
        set_tag(driver, data, 'group1', tag_options, index)
    except:
        pass
    try:
        index += 1
        set_tag(driver, data, 'group2', tag_options, index)
    except:
        pass
    try:
        index += 1
        set_tag(driver, data, 'loc', tag_options, index)
    except:
        pass
    try:
        index += 1
        set_tag(driver, data, 'tag', tag_options, index)
    except:
        pass
    try:
        index += 1
        set_tag(driver, data, 'name', tag_options, index)
    except:
        pass
    try:
        index += 1
        set_tag(driver, data, 'copy', tag_options, index)
    except:
        pass
    try:
        if data['jp name'] != '---':
            index += 1
            set_tag(driver, data, 'Division', tag_options, index)
            index += 1
            set_tag(driver, data, 'Class', tag_options, index)
    except:
        pass

    new_main_src.click()
    time.sleep(0.5)
    new_main_textbox = driver.find_element_by_xpath("//*[@id=\"cke_1_contents\"]/textarea")

    try:
        comment = data['comment']
    except:
        comment = "" 

    codes = data['link'].split('/')[-1].upper()

    if data['en name'] != '---':
        if is_japan(data['loc']):
            new_main_textbox.send_keys(f"<h2>{data['group1']} {data['group2']} {codes}</h2>&nbsp;<p>{comment}</p>&nbsp;<h4>{data['jp name']}</h4> \
            <h3>{data['en name']}</h3><p><strong>Phylum</strong><br />{data['Division']}<br /><strong>Class</strong><br />{data['Class']}</p><br />&nbsp;<table align=\"center\"> \
            <tbody><tr><th>Prefecture</th><td>{data['loc']}</td><th>Use of Microscope</th><td>{data['microscope']}</td></tr> \
            <tr><th>Region</th><td>{data['region']}</td><th>Use of Automatic Shooting Devices</th><td>{data['automatic']}</td></tr> \
            <tr><th>Shooting Date</th><td>{data['date']}</td><th>Use of Fluorescent Probe</th><td>{data['ultraviolet']}</td></tr> \
            <tr><th>Shooting Time</th><td>{data['time']}</td><th>Use of Infrared</th><td>{data['probe']}</td></tr> \
            <tr><th>Photographer</th><td>{data['name']}</td><th>Shooting Interval (Sec.)</th><td>{data['interval']}</td></tr> \
            <tr><th>Copyright Holder</th><td>{data['copy']}</td><th>Shooting Speed</th><td>{data['speed']}</td></tr></tbody></table><br />\
            <a href=\"http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{page_index}/{data['code']}.html\">in English</a>")
        else:
            new_main_textbox.send_keys(f"<h2>{data['group1']} {data['group2']} {codes}</h2>&nbsp;<p>{comment}</p>&nbsp;<h4>{data['jp name']}</h4> \
            <h3>{data['en name']}</h3><p><strong>Phylum</strong><br />{data['Division']}<br /><strong>Class</strong><br />{data['Class']}</p><br />&nbsp;<table align=\"center\"> \
            <tbody><tr><th>Country</th><td>{data['loc']}</td><th>Use of Microscope</th><td>{data['microscope']}</td></tr> \
            <tr><th>Region</th><td>{data['region']}</td><th>Use of Automatic Shooting Devices</th><td>{data['automatic']}</td></tr> \
            <tr><th>Shooting Date</th><td>{data['date']}</td><th>Use of Fluorescent Probe</th><td>{data['ultraviolet']}</td></tr> \
            <tr><th>Shooting Time</th><td>{data['time']}</td><th>Use of Infrared</th><td>{data['probe']}</td></tr> \
            <tr><th>Photographer</th><td>{data['name']}</td><th>Shooting Interval (Sec.)</th><td>{data['interval']}</td></tr> \
            <tr><th>Copyright Holder</th><td>{data['copy']}</td><th>Shooting Speed</th><td>{data['speed']}</td></tr></tbody></table><br />\
            <a href=\"http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{page_index}/{data['code']}.html\">in English</a>")

    else:
        if is_japan(data['loc']):
            new_main_textbox.send_keys(f"<h2>{data['group1']} {data['group2']} {codes}</h2>&nbsp;<p>{comment}</p>&nbsp;<br /><table align=\"center\"> \
            <tbody><tr><th>Prefecture</th><td>{data['loc']}</td><th>Use of Microscope</th><td>{data['microscope']}</td></tr> \
            <tr><th>Region</th><td>{data['region']}</td><th>Use of Automatic Shooting Devices</th><td>{data['automatic']}</td></tr> \
            <tr><th>Shooting Date</th><td>{data['date']}</td><th>Use of Fluorescent Probe</th><td>{data['ultraviolet']}</td></tr> \
            <tr><th>Shooting Time</th><td>{data['time']}</td><th>Use of Infrared</th><td>{data['probe']}</td></tr> \
            <tr><th>Photographer</th><td>{data['name']}</td><th>Shooting Interval (Sec.)</th><td>{data['interval']}</td></tr> \
            <tr><th>Copyright Holder</th><td>{data['copy']}</td><th>Shooting Speed</th><td>{data['speed']}</td></tr></tbody></table><br />\
            <a href=\"http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{page_index}/{data['code']}.html\">in English</a>")
        else:
            new_main_textbox.send_keys(f"<h2>{data['group1']} {data['group2']} {codes}</h2>&nbsp;<p>{comment}</p>&nbsp;<br /><table align=\"center\"> \
            <tbody><tr><th>Country</th><td>{data['loc']}</td><th>Use of Microscope</th><td>{data['microscope']}</td></tr> \
            <tr><th>Region</th><td>{data['region']}</td><th>Use of Automatic Shooting Devices</th><td>{data['automatic']}</td></tr> \
            <tr><th>Shooting Date</th><td>{data['date']}</td><th>Use of Fluorescent Probe</th><td>{data['ultraviolet']}</td></tr> \
            <tr><th>Shooting Time</th><td>{data['time']}</td><th>Use of Infrared</th><td>{data['probe']}</td></tr> \
            <tr><th>Photographer</th><td>{data['name']}</td><th>Shooting Interval (Sec.)</th><td>{data['interval']}</td></tr> \
            <tr><th>Copyright Holder</th><td>{data['copy']}</td><th>Shooting Speed</th><td>{data['speed']}</td></tr></tbody></table><br />\
            <a href=\"http://www.sci.kyoto-u.ac.jp/ja/research/kyutubebio/{page_index}/{data['code']}.html\">in English</a>")

    new_main_src.click()
    time.sleep(1.0)

    try:
        new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[3]")
        new_confirm.click()
        time.sleep(1.0)
        new_confirm_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
        new_confirm_confirm.click()
        time.sleep(2.0)
        new_confirm_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input")
        new_confirm_back.click()
        time.sleep(1.0)

    except:
        new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
        new_confirm.click()
        time.sleep(1.0)
        new_confirm_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
        new_confirm_confirm.click()
        time.sleep(2.0)
        new_confirm_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input")
        new_confirm_back.click()
        time.sleep(1.0)

def many_page_edit(driver, data):
    new_page_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/div[2]/form/input")
    new_page_btn.click()

    time.sleep(0.5)

    new_file = driver.find_element_by_name("cts_filepath")
    new_title = driver.find_element_by_name("cts_title")
    new_inschool = driver.find_element_by_name("cts_inplaceflag")
    new_hidtop = driver.find_element_by_name("cts_hidetoplistflag")
    new_hidtag = driver.find_element_by_name("cts_hidesearchtagflag")
    new_hidtext = driver.find_element_by_name("cts_hideindexflag")
    new_main_img = driver.find_element_by_xpath("//*[@id=\"cke_51\"]")
    new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")

    data_path = f"\\kyu_img\\{data.upper()}"+".jpg"
    upload_thumb = driver.find_element_by_xpath("//*[@id=\"container\"]/form/table[1]/tbody/tr[9]/td/input[2]")
    if os.path.getsize(os.getcwd() + data_path) > 3000000:
        upload_thumb.send_keys(os.getcwd() + f"\\kyu_img\\{data.upper()}" + "_resized.jpg")
        time.sleep(10)
    else:
        upload_thumb.send_keys(os.getcwd() + data_path)
        time.sleep(5)

    new_file.send_keys(data)
    new_title.send_keys(data.upper())
    new_inschool.click()
    new_hidtop.click()
    new_hidtag.click()
    new_hidtext.click()
    
    new_main_img.click()
    time.sleep(0.5)
    new_main_img_upload = driver.find_element_by_id("cke_Upload_136")
    driver.execute_script("arguments[0].click();", new_main_img_upload)
    iframe = driver.find_element_by_xpath('//*[@id="cke_131_fileInput"]')
    driver.switch_to.frame(iframe)
    new_main_img_select = driver.find_element_by_xpath("//*[@id=\"cke_131_fileInput_input\"]")
    new_main_img_select.send_keys(os.getcwd() + data_path)
    time.sleep(0.5)
    driver.switch_to.default_content()
    new_main_img_confirm = driver.find_element_by_id("cke_133_label")
    new_main_img_confirm.click()
    if os.path.getsize(os.getcwd() + data_path) > 3000000:
        time.sleep(15)
    else:
        time.sleep(15)
    new_main_img_confirm_confirm = driver.find_element_by_id("cke_138_label")
    new_main_img_confirm_confirm.click()
    time.sleep(1.0)

    try:
        new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[3]")
        new_confirm.click()
        time.sleep(1.0)
        new_confirm_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
        new_confirm_confirm.click()
        time.sleep(2.0)
        new_confirm_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input")
        new_confirm_back.click()
        time.sleep(1.0)

    except:
        new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
        new_confirm.click()
        time.sleep(1.0)
        new_confirm_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
        new_confirm_confirm.click()
        time.sleep(2.0)
        new_confirm_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input")
        new_confirm_back.click()
        time.sleep(1.0)

def is_japan(region):
    prefecture = ['Hokkaido', 'Aomori', 'Iwate', 'Miyagi', 'Akita', 'Yamagata', 'Fukushima', 'Ibaraki', 'Tochigi', 'Tokyo', \
                'Chiba', 'Kanagawa', 'Yamanashi', 'Saitama', 'Gunma', 'Nigata', 'Gifu', 'Nagano', 'Toyama', 'Ishikawa', \
                'Fukui', 'Aichi', 'Shizuoka', 'Mie', 'Osaka', 'Hyogo', 'Kyoto', 'Shiga', 'Nara', 'Wakayama', 'Okayama', \
                'Tottori', 'Hiroshima', 'Shimane', 'Yamaguchi', 'Fukuoka', 'Saga', 'Nagasaki', 'Oita', 'Kumamoto', 'Miyazaki', \
                'Kagoshima', 'Okinawa', 'Kagawa', 'Ehime', 'Tokushima', 'Kochi']
    if region in prefecture:
        return True
    else:
        return False

def set_tag(driver, data, tag_name, options, index):
    tag_1 = driver.find_element_by_xpath(f"//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li[{index}]/select")
    select_tag_1 = webdriver.support.select.Select(tag_1)
    select_tag_1.select_by_visible_text('Misc')
    time.sleep(0.5)
    tag_2 = driver.find_element_by_xpath(f"//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li[{index}]/select[2]")
    select_tag_2 = webdriver.support.select.Select(tag_2)
    select_tag_2.select_by_visible_text('Kyu Tube Bio')
    time.sleep(0.5)
    tag_3 = driver.find_element_by_xpath(f"//*[@id=\"container\"]/form/table[1]/tbody/tr[11]/td/ul/li[{index}]/select[3]")
    select_tag_3 = webdriver.support.select.Select(tag_3)
    for tag in options:
        if tag_name == 'name':
            if (data[tag_name] in tag) and ('Photographer' in tag):
                select_tag_3.select_by_visible_text(tag)
        elif tag_name == 'copy':
            if (data[tag_name] in tag) and ('Copyright' in tag):
                select_tag_3.select_by_visible_text(tag)
        else:
            if data[tag_name] in tag:
                select_tag_3.select_by_visible_text(tag)

def check_data_0(title, data):
    for i, data_pd in enumerate(data):
        if title == data_pd['title']:
            del data[i]
            print(f"{title} exists.")
    return data

def check_data(title, data):
    data_mask = data['title'] == title
    data_res = data[~data_mask]
    return data_res

def read_data():
    col =  ['title', 'code', 'datatype', 'group1', 'group2', 'media', 'comment', 'jp name', 'en name', 'Division', 'Class', 'loc', 'region', 'date', 'time', 'name', 'copy', 'microscope', 'automatic', 'ultraviolet', 'probe', 'interval', 'speed', 'link', 'tag']
    d0 = pd.read_csv("./data_en_final.csv", names=col, encoding='utf-8')
    d1 = pd.read_csv("./data_jp_final.csv", names=col, encoding='utf-8')
    d2 = d1[['code','link']]
    d = pd.merge(d0, d2, on='code')
    d = d.rename(columns={'link_y':'link'})
    print(d)
    return d

if __name__ == "__main__":   
    userid = "lee"
    userpw = "Mv3qKTUH"

    data = read_data()

    driver = webdriver.Chrome()
    driver.get("https://www.sci.kyoto-u.ac.jp/en/admin/")
    login(driver, userid, userpw)

    time.sleep(0.5)
    research_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/table/tbody/tr[4]/td[7]/input[2]")
    research_btn.click()

    time.sleep(0.5)
    kyutube_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/table/tbody/tr[10]/td[7]/input[2]")
    kyutube_btn.click()

    time.sleep(0.5)
    total_page = 0

    while True:
        print("KyU Tube Bio List INDEX")
        print("3\tStructural Physiology\t\t4\tMolecular Biology\t5\tNeuroScience")
        print("6\tTheoretical Biophysics\t\t7\tMolecular Physiology\t\t8\tMolecular Developmental Biology")
        print("9\tPlant Physiology\t\t10\tChronobiology\t\t11\tPlant Molecular Cell Biology")
        print("12\tMolecular Genetics\t\t13\tPlant Systematics and Evolutionary Botany\t\t14\tSystematic Zoology")
        print("15\tEthology\t\t16\tAnimal Ecology\t\t17\tDevelopmental Biology and Genome Biology")
        print("18\tStress Response Biology\t19\tPhysical Anthropology\t\t20\tHuman Evolution Studies")
        i = int(input("Choose INDEX number : "))
        global page_index
        page_index = 2889 + i
        title = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{i}]/td[3]")
        title_text = title.text
        data_mask = data['group2'] == title_text
        filtered_data = data[data_mask]
        len_first = len(filtered_data)
        print("Searching element in title : " + title_text)

        title_btn = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{i}]/td[7]/input[2]")
        title_btn.click()
        time.sleep(0.5)

        title_sib_list = driver.find_elements_by_class_name("ctlr-line")

        cur_url = driver.current_url
        title_list = driver.find_elements_by_class_name("ctlr-line")
        for i, (j, d) in enumerate(filtered_data.iterrows()):
            i = i
            if i < 5:
                continue
            link = d['link']
            ty = d['media']
            code = link.split('/')[-1]
            codelen = len(code)
            if len(code) > 6:
                codes = code.split('-')
                folder_edit(driver, d)
                if i > 24:
                    ii = i%25
                    pp = int(i/25)
                    pp_url = f"https://www.sci.kyoto-u.ac.jp/en/admin/contents/?pageno={pp+1}&parentcode=2286"
                    driver.get(pp_url)
                    btn = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{2+ii}]/td[7]/input[2]")
                    btn.click()
                    for c in codes:
                        many_page_edit(driver, c)
                else:
                    btn = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{2+i}]/td[7]/input[2]")
                    btn.click()
                    for c in codes:
                        many_page_edit(driver, c)
            else:
                page_edit(driver, d)
            driver.get(cur_url)

        back = driver.find_element_by_xpath("//*[@id=\"container\"]/div[1]/span[3]/a")
        back.click()
        time.sleep(0.5)

        back = driver.find_element_by_xpath("//*[@id=\"container\"]/div[1]/span[3]/a")
        back.click()
        time.sleep(0.5)

        a = input("Do MORE?(y/n) : ")
        if a == "n":
            driver.quit()
            break
