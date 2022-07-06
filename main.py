# 下载操作浏览器驱动的第三方模块  selenium  pip install selenium

from selenium import webdriver
import time  # 时间模块, 可以用于程序的延迟
import random  # 随机数模块
from constants import TAO_USERNAME1, TAO_PASSWORD1
import csv  # 数据保存的模块

def search_product(keyword):
    driver.find_element_by_xpath('//*[@id="q"]').send_keys(keyword)
    time.sleep(random.randint(1, 3))  # 尽量避免人机检测  随机延迟

    driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()
    time.sleep(random.randint(1, 3))  # 尽量避免人机检测  随机延迟

    driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(TAO_USERNAME1)
    time.sleep(random.randint(1, 3))  # 尽量避免人机检测  随机延迟

    driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(TAO_PASSWORD1)
    time.sleep(random.randint(1, 3))  # 尽量避免人机检测  随机延迟

    driver.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
    time.sleep(random.randint(1, 3))  # 尽量避免人机检测  随机延迟

def parse_data():
    divs = driver.find_elements_by_xpath('//div[@class="grid g-clearfix"]/div/div')  #  所有的div标签

    for div in divs:
        try:
            info = div.find_element_by_xpath('.//div[@class="row row-2 title"]/a').text
            price = div.find_element_by_xpath('.//strong').text + '元'
            deal = div.find_element_by_xpath('.//div[@class="deal-cnt"]').text
            name = div.find_element_by_xpath('.//div[@class="shop"]/a/span[2]').text
            location = div.find_element_by_xpath('.//div[@class="location"]').text
            detail_url = div.find_element_by_xpath('.//div[@class="pic"]/a').get_attribute('href')

            print(info, price, deal, name, location, detail_url)
            with open('某宝.csv', mode='a', encoding='utf-8', newline='') as f:
                csv_write = csv.writer(f)
                csv_write.writerow([info, price, deal, name, location, detail_url])
        except:
            continue
word = input('请输入你要搜索商品的关键字:')
driver = webdriver.Chrome(executable_path='../chromedriver.exe')

# selenium操作的浏览器被识别了, 无法登录
# 修改浏览器的部分属性, 绕过检测
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
            {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => false})"""})
driver.get('https://www.taobao.com/')
driver.implicitly_wait(10)  # 设置浏览器的等待,加载数据
driver.maximize_window()  # 最大化浏览器
search_product(word)

for page in range(100): # 012
    print(f'\n==================正在抓取第{page + 1}页数据====================')
    url = f'https://s.taobao.com/search?q=%E5%B7%B4%E9%BB%8E%E4%B8%96%E5%AE%B6&s={page * 44}'
    # 解析商品数据
    parse_data()
    time.sleep(random.randint(1, 3))  # 尽量避免人机检测  随机延迟
