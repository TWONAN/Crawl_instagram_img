import requests
import time
import os
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json

# 因为采用shadowsocks代理ip，需要把requests更新到支持socks，然后ip和端口需要填本地和ss的端口
# 推荐采用socks5h，避免有SOCKSSSL报错
proxies = {
    'http': 'socks5h://127.0.0.1:1080',
    'https': 'socks5h://127.0.0.1:1080'
}
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('lang=zh_CN.UTF-8')
driver = webdriver.Chrome(chrome_options=options)
url = 'https://www.instagram.com/nanaouyang/'
log_url = 'https://www.instagram.com/accounts/login/'
url_set = set([])
requests.adapters.DEFAULT_RETRIES = 5
# s = requests.session()
# s.keep_alive = False
# ua反爬检测
UserAgent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
headers = {'User-Agent': UserAgent}
filename = './imgp/'
if not os.path.exists(filename):
    os.mkdir(filename)

def getImgList():
    driver.get(log_url)
    url_set_size = 0
    while True:
        if driver.current_url != url:
            print('Please goto nana')
            time.sleep(3)
            continue
        print('开始')
        divs = driver.find_elements_by_class_name('v1Nh3')
        if divs:
            for i in divs:
                url_set.add(i.find_element_by_tag_name('img').get_attribute('src'))
            if len(url_set) == url_set_size:  # 如果本次页面更新没有加入新的URL则可视为到达页面底端，跳出
                break
            elif len(url_set) > 100:
                break
            url_set_size = len(url_set)
            for i in range(5):
                ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()  # 三次滑动，保证页面更新足够
                time.sleep(2)
        continue
    print(url_set, len(url_set))


def get_Cookies(log_url):
    driver.get(log_url)
    while True:
        print('Please login in ins!!!')
        time.sleep(3)
        while driver.current_url != log_url:
            ins_Cookies = driver.get_cookies()
            driver.quit()
            return ins_Cookies


def download(num, img_url):
    p = requests.get(url=img_url, headers=headers, proxies=proxies, verify=False).content
    # tree = etree.HTML(p)
    # img_src = tree.xpath('//div[@class="KL4Bh"/img/@src')
    # img_list.append(tree)
    imgName = num
    with open('%s/%s.jpg' % (filename,imgName), 'wb') as f:
        f.write(p)
        print('%s.jpg 已经下载' % imgName)


if __name__ == '__main__':
    getImgList()
    for num, img_url in enumerate(url_set):
        download(num, img_url)