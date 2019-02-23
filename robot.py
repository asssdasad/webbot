#coding=utf-8
import time,re,requests,sys,random
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from multiprocessing import Process, Pool
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# 一直等待某元素可见，默认超时10秒
def is_visible(locator, timeout=10,type="select"):
    if type == "xpath":
        try:
            ui.WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False
    else:
        try:
            ui.WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, locator)))
            return True
        except TimeoutException:
            return False

# 一直等待某个元素消失，默认超时10秒
def is_not_visible(locator, timeout=10):
    try:
        ui.WebDriverWait(driver, timeout).until_not(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

#图灵机器人
def get_response(msg):
    KEY = '342aecd770b64e37a72ddf8b00b7db48'
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'   : KEY,
        'info'   : msg,   # 这是要发送出去的信息
        'userid'  : 'wechat-rebot',  #这里随意写点什么都行
    }
    try:
        # 发送一个post请求
        r = requests.post(apiUrl, data =data).json()
        # 获取文本信息，若没有‘Text’ 值，将返回Nonoe
        return r.get('text')
    except:
        return


#the  thing start
def sendmessage(msg):
    if msg is not None:
        if msg.replace(" ","") != "":
            if is_visible('[id="message"]', t + 10):
                driver.find_element_by_id("message").send_keys(msg)
            if is_visible('[id="sbutton"]', t + 10):
                driver.find_element_by_id("sbutton").click()

def start():
    print("new start 1111")
    global driver, t, a
    starttime = time.time()
    a = 0
    t = 5
    # 不带界面写法
    driver = selenium.webdriver.PhantomJS(executable_path=r"phantomjs-2.1.1-windows\bin\phantomjs.exe")
    # 使用谷歌浏览器
    #driver = webdriver.Chrome(r"chromedriver.exe")
    driver.get('http://www.suiliao520.com/')
    time.sleep(4)

    #开始匹配
    if is_visible('[id="enterroom"]', t + 10):
        driver.find_element_by_id("enterroom").click()
        #driver.execute('''  document.getElementById('enterroom').click() ''')

    # 查看是否匹配成功
    while True:
        #循环必须注意的一点
        if time.time() - starttime >= 120:
            break
        else:
            print(time.time() - starttime)
        if u"对方进入了房间(enter the room)" in driver.page_source:
            # 发消息
            if random.randint(1,2) == 1:
                sendmessage(u"hi")
            else:
                sendmessage(u"hello")
            time.sleep(3)
            break
        else:
            print("didnt find person wait")
            time.sleep(8)

    #开始回复
    msgglist = []
    while True:
        time.sleep(5)
        if time.time() - starttime >= 120:
            break
        else:
            print(time.time() - starttime)
            pass

        msgg = str(driver.execute_script(
            '''return document.getElementsByClassName("duihu left")[document.getElementsByClassName("duihu left").length-1].innerText '''))
        if msgg is None:
            print("null")
        else:
            if msgg.replace(" ","") != "":
                msgglist.append(msgg)
                if len(msgglist) > 1:
                    if msgglist[len(msgglist)-2]  == msgglist[len(msgglist)-1]:
                        print("no respond")
                        continue
                    else:
                        pass
                else:
                    pass
                print(msgg)
                sendmessage(get_response(msgg))
            else:
                print("fakeee")

    try:
        driver.close()
        print("close sucsss")
    except:
        print("close failed maybe already?")


def newme():
    try:
        while True:
            start()
    except:
        print("unknow error")
        newme()
        time.sleep(5)

newme()



