from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import chromedriver_binary
import urllib3, time
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

def page_edit(driver, page_num):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "form1")))
    new_main_src = driver.find_element_by_id("cke_14")
    new_main_src.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"cke_1_contents\"]/textarea")))
    new_main_textbox = driver.find_element_by_xpath("//*[@id=\"cke_1_contents\"]/textarea")

    article = new_main_textbox.get_attribute('value')

    edit_part = article[-40:].split("/")
    if len(edit_part[1]) == 4:
        driver.back()
        return
    else:
        edit_part[1] = page_num
        edit_part = '/'.join(edit_part)
        article = article.replace(article[-40:], edit_part)
        article = re.sub(r"[\r\n]", "", article)
        article = re.sub(r"[\u3000\t]", "", article)
        new_main_textbox.clear()
        new_main_textbox.send_keys(article)
        new_main_src.click()
        try:
            new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[3]")
            new_confirm.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "preview")))
            new_confirm_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
            new_confirm_confirm.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "message")))
            new_confirm_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input")
            new_confirm_back.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ctlr-list")))
        except:
            new_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
            new_confirm.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "preview")))
            new_confirm_confirm = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input[2]")
            new_confirm_confirm.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "message")))
            new_confirm_back = driver.find_element_by_xpath("//*[@id=\"container\"]/form/div/input")
            new_confirm_back.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ctlr-list")))

def login(driver, userid, userpw):
    sci_admin_id = driver.find_element_by_name("act_id")
    sci_admin_pw = driver.find_element_by_name("act_passwd")
    sci_admin_id.send_keys(userid)
    sci_admin_pw.send_keys(userpw)
    sci_admin_login = driver.find_element_by_xpath("/html/body/form/div/input")
    sci_admin_login.click()

if __name__ == "__main__":
    userid = "lee"
    userpw = "Mv3qKTUH"

    driver = webdriver.Chrome()
    driver.get("https://www.sci.kyoto-u.ac.jp/en/admin/")
    login(driver, userid, userpw)
    time.sleep(0.3)
    research_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/table/tbody/tr[4]/td[7]/input[2]")
    research_btn.click()
    time.sleep(0.3)
    kyutube_btn = driver.find_element_by_xpath("//*[@id=\"container\"]/table/tbody/tr[10]/td[7]/input[2]")
    kyutube_btn.click()
    time.sleep(0.3)
    pageNum = 0

    for i in range(18):
        if i < 8:
            continue
        viewPath = f"//*[@id=\"container\"]/table/tbody/tr[{3+i}]/td[7]/input[2]"
        viewBtn = driver.find_element_by_xpath(viewPath)
        page_num = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{3+i}]/td[4]").text.split('/')[0]
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
                        page_edit(driver, page_num)

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
                        page_edit(driver, page_num)
        except:
            print(f"Index {i} Total page: 1")
            lineIndex = driver.find_elements_by_css_selector("#container > table > tbody > tr")
            print(f"Line number: {len(lineIndex)-1}")
            for k in range(len(lineIndex)):
                if k == 0:
                    continue
                edit_btn = driver.find_element_by_xpath(f"//*[@id=\"container\"]/table/tbody/tr[{k+1}]/td[7]/input[1]")
                edit_btn.click()
                page_edit(driver, page_num)
        back = driver.find_element_by_xpath("//*[@id=\"container\"]/div[1]/span[3]/a")
        back.click()
    driver.quit()