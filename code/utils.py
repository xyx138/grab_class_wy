import requests
from selenium import webdriver
import qrcode
from PIL import Image
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException

# 获取二维码的src
def getImgSrc() -> str:


    driver = webdriver.Chrome()

    # 打开包含 iframe 的网页
    driver.get("https://jwgl.ustb.edu.cn/")

    # 等待页面加载完成
    # driver.implicitly_wait(10)

    # 获取页面中的所有 iframe
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"Found {len(iframes)} iframes")

    # 切换到特定的 iframe (这里假设第一个 iframe)
    driver.switch_to.frame(iframes[0])

    # 在 iframe 内抓取网页内容
    iframe_content = driver.page_source
    # print(iframe_content)

    img_element = driver.find_element(By.ID, 'qrimg')

    img_src = img_element.get_attribute('src')

    print("img src:" + img_src)


    # 如果需要进一步操作，例如查找特定的元素，可以继续在 iframe 内进行
    # element = driver.find_element_by_xpath("//some_xpath")

    # 切换回主页面
    driver.switch_to.default_content()

    # 关闭浏览器
    driver.quit()


    return img_src


# 下载图片
def load_img(url):
    qrcode_res = requests.get(url)

    
def generate_qr_code(data):
    # 生成二维码对象
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    # 
    qr.add_data(data)
    img = qr.make(fit=True)

    # 创建图像
    img = qr.make_image(fill='black', back_color='white')
    img.save('qr_img.png')
    # img.show()
    return img

def qrcode_img(url):
    # 初始化浏览器 (以Chrome为例)
    driver = webdriver.Chrome()


    # 打开登录页面
    driver.get(url)

    # 等待二维码加载
    time.sleep(3)  # 视具体情况而定

    # 获取页面中的所有 iframe
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"Found {len(iframes)} iframes")

    # 切换到特定的 iframe (这里假设第一个 iframe)
    driver.switch_to.frame(iframes[0])
    
    # 在 iframe 内抓取网页内容
    iframe_content = driver.page_source
    # print(iframe_content)

    img_element = driver.find_element(By.ID, 'qrimg')
    
    img_src = img_element.get_attribute('src')

    print('img_element:  ', img_element)

    # 获取二维码的位置和尺寸
    location = img_element.location
    size = img_element.size

    # 对整个页面截图

    # 切回主内容页面
    driver.switch_to.default_content()

    return img_src, driver

def show_qr(img):
    img.show()


# 获取课程号和通知号
def getID(str:str) -> tuple: # class_id, inform_id_list

    str = str.strip('qhkc').strip('\n').strip(';')

    str = str.strip('(').strip(')') # 去括号

    split_ls = str.split(',')

    split_ls = list( s.strip("'") for s in split_ls)

    
    return (split_ls[1], split_ls[2:])
    



# 产生选课的url
def get_urls(class_id, inform_id_list, zbid)->list:

    res = []

    for inform_id in inform_id_list:

        url = f"https://jwgl.ustb.edu.cn/xsxk/xsxkoper?jx0404id={inform_id}&dqjx0502zbid={zbid}&yjx02id={class_id}&xdlx=1&jx02id={class_id}&type=gxk&kcfalx=zx&xsid=&opener=gxk&sfzybxk=&qzxkkz=0&glyxk="

        res.append(url)

    return res


# 获取cookies
def getCookies(url):

    img_src, driver = qrcode_img(url)

    # 询问响应
    query_url = img_src.replace('qrimg', 'state')

    print(query_url)

    cookies = []


    # img.show()

    # 不断询问当前状态
    while 1:

        res = requests.get(query_url)

        res_dict = res.json()
        print(driver.get_cookies())
        if res_dict['state'] == 200:
            print("登录成功")
        
            time.sleep(20)

            print("等待cookies获取")

            cookies = driver.get_cookies()

            print(type(cookies), "获取到的cookies:", cookies)

            # 对整个页面截图

            # img.close()
            break
        elif res_dict['state'] == 102:
            print("扫码成功，请确认登录！")

        sleep(0.3)
    
    new_cookies = {}
    
    for obj in cookies:
        key, value = "", ""
        for k, v in obj.items():
            if k == "name":
                key = v
            
            if k == 'value':
                value = v
        
        new_cookies[key] = value 

    # print(new_cookies, type(new_cookies))
    return new_cookies, driver


def chooseST(driver):
    pass


def getClassList(driver):

    try:
      driver.get("https://jwgl.ustb.edu.cn/xsxk/xsxkzx_index")
    except UnexpectedAlertPresentException:
      # 处理弹窗
      print("弹窗已接受，继续执行后续操作")
      driver.get("https://jwgl.ustb.edu.cn/xsxk/xsxkzx_index") # 进入index页
    
    # 模拟点击选课

    all_tr = driver.find_elements(By.TAG_NAME, 'tr')

    time.sleep(1)

    top_tr = all_tr[1]

    td = top_tr.find_element(By.XPATH, "//*[@onclick]")
    
    zbid = td.get_attribute('onclick')

    zbid = zbid.strip("jrxk('").strip("');") # 去除前后缀


    td.click()

    # 模拟点击'素质拓展课'

    tag_sutuo_a = driver.find_element(By.XPATH,  "//*[text()='素质拓展课']")

    tag_sutuo_a.click()


    # 获取包含选课列表的iframe
    main_iframe = driver.find_element(By.ID, "mainFrame")

    # 切换到特定的frame
    driver.switch_to.frame(main_iframe)

    # 获取table
    table = driver.find_element(By.TAG_NAME, 'table')

    # 获取tr

    all_tr = table.find_elements(By.XPATH, "//*[@onclick]")


    # 筛选外语

    new_tr = []
    names = [] # 课程名字
    for tr in all_tr:
       
        tds = tr.find_elements(By.TAG_NAME, 'td')

        haswy = any(td.text.strip() == '外语' for td in tds)
        
        # 是否是外语
        if haswy:
           
           new_tr.append(tr)
           names.append(tds[2].text) # 第3个td包裹了课程名字

    print(f"查找到的外语课程总数：{len(new_tr)}")

    new_tr[0].click() # 点击行

    target_llist = [] # 课程信息

    with open('./target.txt', 'w') as f:
      for element in new_tr:
       
        s = element.get_attribute('onclick')
        target_llist.append(s)
        f.write(s + "\n")

    print('数据输入完成')

    print('开始打印字符串的值')

    for s in target_llist:
       print(s)

    print("所有值打印完毕")

    print("开始模拟点击选课")


    # 切回主内容页面
    driver.switch_to.default_content()


    

    kcxx_iframe = driver.find_element(By.ID, "kcxxFrame")

    driver.switch_to.frame(kcxx_iframe)

    top_tr = driver.find_elements(By.TAG_NAME, 'tr')[1]

    choose_a = top_tr.find_element(By.XPATH,  "//*[text()='选课']")



    choose_a.click() # 点击选课


    # 选课确定
    try:
        # 等待弹窗出现
        WebDriverWait(driver, 10).until(EC.alert_is_present())

        # 获取并接受弹窗
        alert = driver.switch_to.alert
        print(f"弹窗内容: {alert.text}")  # 可选：打印弹窗内容
        alert.accept()  # 接受弹窗
        print("弹窗已接受，继续执行后续操作")


    except NoAlertPresentException:
        # 如果没有弹窗
        print("没有检测到弹窗，继续执行操作")


    # 回复确定
    try:
        # 等待弹窗出现
        WebDriverWait(driver, 10).until(EC.alert_is_present())

        # 获取并接受弹窗
        alert = driver.switch_to.alert
        print(f"弹窗内容: {alert.text}")  # 可选：打印弹窗内容
        alert.accept()  # 接受弹窗
        print("弹窗已接受，继续执行后续操作")


    except NoAlertPresentException:
        # 如果没有弹窗
        print("没有检测到弹窗，继续执行操作")

    

    return target_llist, names, zbid