import os
import time
from datetime import datetime

import win32com.client
from openpyxl.styles import GradientFill, Side, Alignment, Border
import openpyxl
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


def column_width(worksheet):
    worksheet.column_dimensions['A'].width = 11
    worksheet.column_dimensions['B'].width = 16.6
    worksheet.column_dimensions['C'].width = 9
    worksheet.column_dimensions['D'].width = 12.2
    worksheet.column_dimensions['E'].width = 15
    worksheet.column_dimensions['F'].width = 15
    worksheet.column_dimensions['G'].width = 16.6


def excel_close():
    excel = win32com.client.Dispatch("Excel.Application")
    # 获取所有打开的工作簿
    workbooks = excel.Workbooks
    # 查找名为 a.xlsx 的工作簿并关闭
    for workbook in workbooks:
        if workbook.Name == "info.xlsx":
            workbook.Close(False)
            break
    excel.Quit()


def color_gradient(worksheet):
    green_fill = GradientFill(stop=("FFFFFF", "B5E3DC"))
    red_fill = GradientFill(stop=("FFFFFF", "E89696"))
    thin = Side(style='thin', color="D4D4D4")
    border = Border(top=thin, bottom=thin, left=thin, right=thin)
    for cell in worksheet['C']:
        value = cell.value
        if value == 'Short':
            cell.fill = red_fill
            cell.border = border
        elif value == 'Long':
            cell.fill = green_fill
            cell.border = border


def glass_to_excel(list_):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'LiquidationData'
    row_1 = ["Exchange", "交易对", "方向", "价格", "总额", "数量", "时间"]
    worksheet.append(row_1)
    # 设置工作页宽度
    column_width(worksheet)
    # 载入列表到工作页
    for x in list_:
        worksheet.append(x)

    # (方向)颜色渐变处理
    color_gradient(worksheet)
    # 设置每个单元格内容, 水平居中显示
    for row in worksheet.iter_rows():
        for cell in row:
            cell.alignment = Alignment(horizontal='center')
    # 保存单元格.
    name_now = set_name()
    workbook.save(name_now)
    workbook.close()
    print("已保存至 !")
    print(name_now)


def new_glass_to_data(elements):
    list_return = []
    for x in elements:
        # 获取交易所名称
        img_element = x.find_element(By.XPATH, ".//img")
        src_ = img_element.get_attribute("src")
        exchange = new_glass_get_exchange(src_)
        list_ = x.text.split("\n")
        amount = new_glass_get_amount(list_[1], list_[2])
        time_ = list_[3] + " " + list_[4]
        list_return.append([exchange, list_[0], new_glass_get_direction(x), list_[1], list_[2], amount, time_])
    return list_return


def new_glass_get_exchange(str_):
    str1 = str_.replace("https://cdn.coinglasscdn.com/static/exchanges/", "")
    if str1 == '270.png':
        return "Binance"
    elif str1 == 'bybit2.png':
        return "bybit2.png"
    elif str1 == '2502.png':
        return "Huobi.png"
    elif str1 == 'okx2.png':
        return "OKX"
    elif str1 == 'bitfinex.jpg':
        return "Bitfinex"
    elif str1 == '157.png':
        return "Bitmexx"
    elif str1 == 'deribit.png':
        return "deribit"
    elif str1 == 'CoinEx.png':
        return "CoinEx"
    else:
        return "ALL"


def new_glass_get_direction(element):
    direction1 = element.get_attribute("class").split(" ")[1]
    if "Short" in direction1:
        return "Short"
    else:
        return "Long"


def new_glass_get_amount(str1, str2):
    n1 = str1.replace("$", "")
    if "万" in str2:
        n2 = str2.replace("$", "").replace("万", "")
        amount = float(n2) * 10000 / float(n1)
        return str(round(amount, 3))
    else:
        n2 = str2.replace("$", "")
        amount = float(n2) / float(n1)
        return str(round(amount, 3))


def change_iterm(actions, element, num):
    if num == 0:
        # 不做修改
        time.sleep(0.3)
    else:
        # 移到目标元素 . 激活点开列表,
        actions.move_to_element(element).click().perform()
        time.sleep(0.8)
        for i in range(num):
            # 选择 Next
            actions.send_keys(Keys.DOWN).perform()
            time.sleep(0.8)

        actions.send_keys(Keys.ENTER).perform()
        time.sleep(0.8)


def time_to_date(time1):
    dt1 = datetime.strptime(time1, "%d %m月%H:%M")
    return dt1


def set_name():
    path = r"C:\Users\Administrator\Desktop"

    # 获取目录下所有文件名
    file_names = os.listdir(path)

    # 获取所有扩展名为.xlsx的文件名
    xlsx_files = [file_name for file_name in file_names if file_name.endswith(".xlsx")]

    # 打印所有.xlsx文件名
    name = "LiquidationData" + str(len(xlsx_files) + 1) + ".xlsx"
    new_file_path = os.path.join(path, name)
    return new_file_path
