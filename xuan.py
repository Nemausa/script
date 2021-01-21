class HuoChe(object):
     
    """docstring for Train"""
    driver_name='Chrome'
    executable_path='D:\爬虫实战\12306\chromedriver_win32'
    #用户名 密码
    username = u"your_username"
    passwd = u"your_password"
 
 
    """网址"""
    # 强智教务系统登录URL
    select_url = "http://............"
    # 强智选课页面URL
    login_url = "http://............."
 
 
    def __init__(self):
        print("Welcome To Use The Tool")
 
#登录函数
    def login(self):
        proxy.new_har()
        self.driver.visit(self.login_url)
        #填充密码
        self.driver.fill("userAccount",self.username)
        #sleep(1)
        self.driver.fill("userPassword",self.passwd)
        print("等待验证码，自行输入....")
        while True:
            if self.driver.url != self.initmy_url:
                sleep(1)
            else :
                break
#抢课成功，利用twilio发送短信的函数
    def send_message():
        account_sid="your_sid"
        auth_token="your_auth_totken"
        client=Client(account_sid,auth_token)
 
        client.messages.create(
        body=u" 抢课成功，请登录查看 ",to="+86你注册twilio时手机号",from_="+twilio分配给你的手机号")
 
#登录进入，开始抢课
    def start(self):
        #选择模拟的浏览器类型
        self.driver = Browser(driver_name='chrome')
        self.driver.driver.set_window_size(1400,1000)
        self.login()
        self.driver.visit(self.select_url)
        #选择你想抢课的种类，名字或教学方式
        self.driver.find_by_text(u'公选课选课').click()
        class_name=u"网络授课"
 
        #利用iframe表格找到想选的课的选课按钮，然后点击
        #循环点击所有要抢的课的选课id，当抢课成功发送短信通知
        if self.driver.find_by_id('mainFrame'):
            with self.driver.get_iframe('mainFrame') as frame:
                b=frame.find_by_name("skls")
                b.fill(class_name)
                frame.find_by_value(u"查询").click()
 
                #要抢课的id列表
                list=[......]
                #循环抢课，提示抢课成功后发送手机短信通知
                A=False
                while A==False:
                    for i in range(len(list)):
                        frame.find_by_id(list[i]).click()
                        with frame.get_alert() as alert:
                            alert.accept()
                            if alert.text=="选课失败：此课堂选课人数已满！":
                                alert.accept()
                                continue
                            elif alert.text=="选课成功":
                                alert.accept()
                                A=True
                                print('抢课成功')
                                #调用发送短信函数
                                self.send_message()
                                break
                            else:
                                alert.accept()
                                continue
 
 
if __name__=="__main__":
    train = HuoChe()
    train.start()