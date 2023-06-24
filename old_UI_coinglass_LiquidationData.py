import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import liq_tools
import os

# 创建Chrome浏览器的Service对象
service = Service(r"D:\software\chromedriver\chromedriver.exe")

# 创建ChromeOptions对象 , 设置
options = Options()
# options.add_argument("--headless") # 生效则代表selenium以后台模式运行
# 创建Chrome浏览器实例，并将Service对象和Options对象传递给它
options.add_experimental_option("excludeSwitches", ['enable-automation'])
browser = webdriver.Chrome(service=service, options=options)

# 使用Chrome浏览器打开目标页面
browser.set_window_size(1320, 660)
browser.set_window_position(200, 128)

browser.get("https://www.coinglass.com/zh/LiquidationData")
# 获取旧版网页(模拟点击返回旧版)
element1 = browser.find_element(By.CSS_SELECTOR, '.shou:nth-child(1)')
element1.click()
time.sleep(3)
# 实现向下滑动 2000px
browser.execute_script("window.scrollBy(0, 2000);")
time.sleep(3)
# 创建动作
actions = ActionChains(browser)
# 获得select下拉框的合集, 其中交易对为 index5  交易所[6]  方向[7]  金额[8]
# 下拉框元素,或者说index, 可能会随着时间, 网站会改, 所以发现不能用请用浏览器F12去定位.
select_elements = browser.find_elements(By.CLASS_NAME, "ant-select-selection-search-input")
# --------------------------------------------------------------------------
# 交易对5 .  全部(0)  BTC(1)  ETH(2)  XRP(3)  BNB(4)  LTC(5)  DOGE(6)  SOL(7)
# 交易所6 .  全部(0)  币安(1)  Bybit(2)  Huobi(3)  OKX(4)
# 方向 7 .  全部(0)  做多(1)  做空(2)
# 金额 8 .  全部(0)  50k(1)   100k(2)  1M(3)
liq_tools.change_iterm(actions, select_elements[5], 2)  # 5代表交易对下拉框,2 代表选择ETH
liq_tools.change_iterm(actions, select_elements[8], 0)  #
# 查看更多按钮
element_data_more = browser.find_element(By.CSS_SELECTOR, ".ant-btn-primary > span")
for i in range(4):
    #  循环一次增加20个数据
    try:
        element_data_more.click()
    except:
        print("数据已枯竭!")
    time.sleep(2.2)

elements = browser.find_elements(By.CLASS_NAME, "ant-table-row")
list_ = []
for el in elements:
    list1 = el.text.split("\n")
    time_ = list1[1] + " " + list1[2]
    direct = list1[7].replace("做多", "Long").replace("做空", "Short")
    list_.append([list1[0], list1[3], direct, list1[6], list1[4], list1[5].replace("≈", ""), time_])
print("列表已载入!")
# 关闭进程中的工作表
time.sleep(2.4)
liq_tools.glass_to_excel(list_)

# 打开 Excel 查看文件.
