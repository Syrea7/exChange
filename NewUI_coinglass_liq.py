import time
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import liq_tools
import liq_tools

# 创建Chrome浏览器的Service对象
service = Service(r"D:\software\chromedriver\chromedriver.exe")

# 创建ChromeOptions对象，并指定以无头模式运行浏览器
options = Options()
# options.add_argument("--headless")
# 创建Chrome浏览器实例，并将Service对象和Options对象传递给它
options.add_experimental_option("excludeSwitches", ['enable-automation'])
browser = webdriver.Chrome(service=service, options=options)

# 使用Chrome浏览器打开目标页面
browser.set_window_size(1320, 620)
browser.set_window_position(210, 128)

browser.get("https://www.coinglass.com/zh/LiquidationData")
# 滚动屏幕, 以便元素能合适显示
browser.execute_script("window.scrollBy(0, 540)")
time.sleep(3.6)
actions = ActionChains(browser)
# ----------------------------------------------------------------------------------------
# 交易对 .  全部(0)  BTC(1)  ETH(2)  XRP(3)  BNB(4)  LTC(5)  DOGE(6)  SOL(7)
instID = browser.find_element(By.ID, ":Rd9laj9lqm:")
liq_tools.change_iterm(actions, instID, 2)
# ----------------------------------------------------------------------------------------
# 交易所 .  全部(0)  币安(1)  Bybit(2)  Huobi(3)  OKX(4)
exchange = browser.find_element(By.CSS_SELECTOR, '[aria-controls=":Rl9laj9lqm:"]')
liq_tools.change_iterm(actions, exchange, 0)
# ----------------------------------------------------------------------------------------
# 数量金额.  全部(0)  10k(1)   100k(2)  1M(3)
amount = browser.find_element(By.CSS_SELECTOR, '.MuiSelect-root:nth-child(3)')
liq_tools.change_iterm(actions, amount, 1)
# ----------------------------------------------------------------------------------------
# 获取 liq-live-table 数据, 父级数据
scrollable_div = browser.find_element(By.CLASS_NAME, "orderbook")
list_all = []
# 初始化后第一次获取, 采用外部方法, 传入参数
time.sleep(1.2)
childs = scrollable_div.find_elements(By.CLASS_NAME, "liq-live-table")
list_all.extend(liq_tools.new_glass_to_data(childs))

# 循环获取
for i in range(7):
    try:
        browser.execute_script("arguments[0].scrollTop += 663", scrollable_div)  # 条目间隔51px , 一次可获取 13X , 遂移动 510px
        childs = scrollable_div.find_elements(By.CLASS_NAME, "liq-live-table")
        time.sleep(0.6)
        list_all.extend(liq_tools.new_glass_to_data(childs))
        time.sleep(0.6)
    except Exception:
        print("数据已枯竭.")
print("列表已载入!")

time.sleep(1.2)
# 保存临时工作表
liq_tools.glass_to_excel(list_all)
