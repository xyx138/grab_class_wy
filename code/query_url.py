import time
import threading

def qk(urls, cookies, headers, session):
    name = threading.current_thread().name

    while 1:
        
        for url in urls:
            req = session.get(url)
            print(name + ' ' + req.text)
            if "成功" in req.text:
                
                file = open('./result.txt', 'a')
                file.write("成功抢到:" + name + "\n")
                file.close()
                break

            time.sleep(0.5)


def run(name_url_list, cookies, headers, session):
    print("开始抢课！")



    for name, urls  in name_url_list:
        threading.Thread(target=qk, args=(urls, cookies, headers, session), name=name).start()
    