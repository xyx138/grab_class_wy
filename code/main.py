from utils import getCookies, getClassList, getID, get_urls
from time import sleep
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from query_url import run  
from requests import Session
if __name__ == "__main__":
    
    # 登录界面
    index_url = "https://jwgl.ustb.edu.cn"

    cookies, driver = getCookies(index_url)

    with open('./cookies_list.txt', 'a') as f:
        f.write(str(cookies) + '\n')

    sleep(10)
    
    
    # 模拟点击，并爬取所有外语的课程号通知号,课程号

    infos, names, zbid = getClassList(driver)

    # 从 Selenium 中提取请求头
    selenium_headers = driver.execute_script(
        "var req = new XMLHttpRequest();"
        "req.open('GET', document.location, false);"
        "req.send(null);"
        "return req.getAllResponseHeaders()"
    )

    # 将提取的头转换为字典格式
    headers_dict = dict(line.split(": ", 1) for line in selenium_headers.splitlines() if line)

    print("请求头："  , headers_dict)

    session = Session()

    # 从 Selenium 获取 cookies 并添加到 requests 会话中
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])


    driver.quit() # 关闭浏览器
        

    # 过滤信息，合并课程名
    
    name_url_list = []



    for i, s in enumerate(infos):
        cls_id, info_id_ls = getID(s)
        # 拼接url
        urls = get_urls(cls_id, info_id_ls, zbid)
        
        name_url_list.append((names[i], urls))


    # 轮询发送请求
    run(name_url_list, cookies, headers_dict, session=session)