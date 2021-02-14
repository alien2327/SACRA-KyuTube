# Inner modules
import pip, site, importlib
import os, csv
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import time

# Downloaded modules
print("\nChecking modules requirments. It will install module not exists automatically.")
try:
    from selenium import webdriver, common
    print("Module [selenium] found")
except ImportError:
    print("Module [selenium] not found")
    pip.main(['install', 'selenium'])
    importlib.reload(site)
    from selenium import webdriver, common
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

def page_edit(driver):
    new_inschool = driver.find_element_by_name("cts_inplaceflag")
    new_hidtop = driver.find_element_by_name("cts_hidetoplistflag")
    new_hidtag = driver.find_element_by_name("cts_hidesearchtagflag")
    new_hidtext = driver.find_element_by_name("cts_hideindexflag")

    new_inschool.click()
    new_hidtop.click()
    new_hidtag.click()
    new_hidtext.click()

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

def login(driver, userid, userpw):
    sci_admin_id = driver.find_element_by_name("act_id")
    sci_admin_pw = driver.find_element_by_name("act_passwd")
    sci_admin_id.send_keys(userid)
    sci_admin_pw.send_keys(userpw)
    sci_admin_login = driver.find_element_by_xpath("/html/body/form/div/input")
    sci_admin_login.click()

if __name__ == "__main__":

    userid = input("Enter your admin id: ")
    userpw = input("Enter your admin password: ")

    driver = webdriver.Chrome()
    driver.get("https://www.sci.kyoto-u.ac.jp/ja/admin/")
    login(driver, userid, userpw)
    time.sleep(0.3)
    research_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/table/tbody/tr[4]/td[7]/input[2]")
    research_btn.click()
    time.sleep(0.3)
    kyutube_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/table/tbody/tr[15]/td[7]/input[2]")
    kyutube_btn.click()
    time.sleep(0.3)
    pageNum = 0

    for i in range(18):
        viewPath = f"//*[@id=\"container\"]/table/tbody/tr[{3+i}]/td[7]/input[2]"
        viewBtn = driver.find_element_by_xpath(viewPath)
        viewBtn.click()
        parentUrlCode = int(driver.current_url.split("=")[-1])
        try:
            pageIndex = driver.find_element_by_xpath("//*[@id=\"container\"]/div[3]/span").text.split(":")[1]
            pageIndex = int(pageIndex[:-1].strip())//25 + 1
            print(f"Index {i} Total page: {pageIndex}")
            if pageIndex < 10:
                for j in range(pageIndex):
                    pageBtn = driver.find_element_by_xpath(f"//*[@id=\"container\"]/div[3]/ul/li[{2+j}]")
                    pageBtn.click()
                    time.sleep(0.3)
                    lineIndex = driver.find_elements_by_css_selector("#container > table > tbody > tr")
                    print(f"Page {j+1} Line number: {len(lineIndex)-1}")
                    for k in range(len(lineIndex)):
                        if k == 0:
                            continue
                        edit_btn = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{k+1}]/td[7]/input[1]")
                        edit_btn.click()
                        driver.back()

            else:
                for j in range(pageIndex):
                    if j == 4 or j == 5 or j == 6:
                        j = 4
                    elif j > 6:
                        j = j - 2
                    pageBtn = driver.find_element_by_xpath(f"//*[@id=\"container\"]/div[3]/ul/li[{2+j}]")
                    pageBtn.click()
                    time.sleep(0.3)
                    lineIndex = driver.find_elements_by_css_selector("#container > table > tbody > tr")
                    print(f"Page {j+1} Line number: {len(lineIndex)-1}")
                    for k in range(len(lineIndex)):
                        if k == 0:
                            continue
                        edit_btn = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{k+1}]/td[7]/input[1]")
                        edit_btn.click()
                        driver.back()
        except:
            print(f"Index {i} Total page: 1")
            lineIndex = driver.find_elements_by_css_selector("#container > table > tbody > tr")
            print(f"Line number: {len(lineIndex)-1}")
            for k in range(len(lineIndex)):
                if k == 0:
                    continue
                edit_btn = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{k+1}]/td[7]/input[1]")
                edit_btn.click()
                driver.back()
        back = driver.find_element_by_xpath("//*[@id=\"container\"]/div[1]/span[3]/a")
        back.click()
    driver.quit()