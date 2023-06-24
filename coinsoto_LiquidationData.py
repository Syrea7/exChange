import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
browser.set_window_size(1320, 690)
browser.set_window_position(200, 128)

browser.get("https://coinsoto.com/zh/liquidation")
time.sleep(3.2)
browser.execute_script("window.scrollBy(0, 1500)")
#  ant-select-selection-selected-value
actions = ActionChains(browser)
# 获取的都是select元素, 其中爆仓单列表位于
select_elements = browser.find_elements(By.CLASS_NAME, "ant-select-selection-selected-value")
#  ↑  此元素为select集合,   其index[6]=交易所    [7]=交易对   [8]=方向   9=数量
# -------------------------------------------------------------------------------------------------------------------
# 交易所 6   ALL(0)  Binance(1)  Huobi(2)  OKX(3)  Bitget(4)  Bitmex(5)  Bybit(6)
# 交易对 7   ALL(0)  BTC(1)  ETH(2)  XRP(3)  BNB(4)  LTC(5)  DOGE(6)  SOL(7)
# 方向   8   ALL(0)  多单(1)  空单(2)
# 金额   9   ALL(0)  >$1,000(1)  >$1万(2)  >$10万(3)  >$100万(4)  >$1000万(5)
liq_tools.change_iterm(actions, select_elements[7], 2)  # 意思是修改交易所 , 0 , 等于没改,默认是0
liq_tools.change_iterm(actions, select_elements[9], 1)  # 这里是改金额9, 变成 >$1,000
#                                  类别           具体哪个
# -------------------------------------------------------------------------------------------------------------------
# 每循环一次 , 条目 +20
next_page_element = browser.find_element(By.CSS_SELECTOR, ".ant-col > div > .ant-btn")
for i in range(2):  # 这里共计40条
    next_page_element.click()
    time.sleep(0.8)
# -------------------------------------------------------------------------------------------------------------------
# 此类父元素一共有两个, 第二个就是爆仓数据所在位置. 详情请F12, 搜索此类 ant-col-24 结果仅两个.
liq_table = browser.find_elements(By.CLASS_NAME, "ant-col-24")
childs = liq_table[1].find_elements(By.CLASS_NAME, "ant-table-row")
#  分离childs , 由于数据前一半是爆仓数据,后面是每条数据对应的交易所, 顺序没变  k1 k2 k3 k4 k5 // v1 v2 v3 v4 v5
listA = childs[:len(childs)//2]
listB = childs[len(childs)//2:]
for i in range(len(childs)//2):
    exchange = listB[i].text
    list_n = listA[i].text.split("\n")
    list_n.insert(0, exchange)
    print(list_n)
