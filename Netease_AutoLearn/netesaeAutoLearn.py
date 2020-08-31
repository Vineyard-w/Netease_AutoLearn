import pandas as pd
import csv
import cv2
import time
import random
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# from contextlib import contextmanager


class netease_Auto_Learn:

    def __init__(self, email, password, writer, comment_list):
        self.email = email
        self.password = password
        self.writer = writer
        self.comment_list = comment_list
        self.time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def open_Chrome(self):  # 打开浏览器
        netEase_url = 'https://study.163.com/member/login.htm?returnUrl=aHR0cHM6Ly9zdHVkeS4xNjMuY29tL215'
        try:
            # 设置浏览器禁止通知弹窗
            chrome_options = Options()  # 实例化Options对象
            prefs = {
                'profile.default_content_setting_values':
                    {
                        'notifications': 2
                    }
            }
            chrome_options.add_experimental_option('prefs', prefs)
            # self.driver.maximize_window()  # 最大化浏览器
            # 打开方式二选一
            # 静默启动浏览器
            # chrome_options = Options()  # 实例化Options对象
            # chrome_options.add_argument('--headless')  # 设置为静默启动浏览器模式
            self.driver = webdriver.Chrome(options=chrome_options)  # 后台运行浏览器
            self.wait = WebDriverWait(self.driver, 10) # 设置等待
        except:
            print('\n' * 3 + '*' * 30 + '找不到浏览器驱动！' + '*' * 30 + '\n' * 3)
        else:
            self.driver.get(netEase_url)
            # time.sleep(8)   # 网页加载

    def close(self):  # 关闭浏览器
        print('\n' * 3 + '*' * 28 + '浏览器将在十秒后自动关闭' + '*' * 28 + '\n' * 3)
        time.sleep(10)
        self.driver.quit()

    def enter_AP(self):
        self.driver.implicitly_wait(20)  # 隐性等待，最长等20秒
        try:
            # 点击同意登录
            self.driver.find_element_by_class_name("ux-btn").click()  # 点击同意按钮
            time.sleep(2)
        except:
            print('\n' * 3 + '*' * 32 + '网络加载超时！' + '*' * 32 + '\n' * 3)
        else:
            self.driver.implicitly_wait(10)  # 隐性等待，最长等20秒
            # 选择邮箱登录
            self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div/div[2]/div/div[2]/div/div[1]/div[1]/ul/li[2]').click()

            # 进入iframe内嵌网页
            iframe = self.driver.find_element_by_xpath(
                '/html/body/div[4]/div/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/iframe')
            iframe_url = iframe.get_attribute('src')  # 获取内嵌页网址
            # print(iframe_url)
            to_iframe = self.driver.find_element_by_xpath("//iframe[contains(@src,'%s')]" % iframe_url)
            self.driver.switch_to.frame(to_iframe)

            # 输入账密
            email_in = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form/div/div[1]/div[2]/input')
            email_in.send_keys(self.email)  # 输入邮箱地址
            psw_in = self.driver.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div[2]/form/div/div[3]/div[2]/input[2]')
            psw_in.send_keys(self.password)  # 输入登录密码

    def login(self):
        con = True
        while con == True:
            try:
                self.driver.find_element_by_id('dologin').click()  # 点击登录
                time.sleep(3)  # 等待页面加载
                # 退出iframe内嵌页
                self.driver.switch_to.default_content()
                # 点击下次再说
                self.driver.find_element_by_class_name('th-bk-main-gh').click()
                print('\n' + "登录成功" + '\n')
                con = False
                learn_or_not = True
            except:
                try:
                    # 进入iframe内嵌网页
                    iframe = self.driver.find_element_by_xpath(
                        '/html/body/div[4]/div/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/iframe')
                    iframe_url = iframe.get_attribute('src')  # 获取内嵌页网址
                    # print(iframe_url)
                    to_iframe = self.driver.find_element_by_xpath("//iframe[contains(@src,'%s')]" % iframe_url)
                    self.driver.switch_to.frame(to_iframe)
                    # 点击继续登录
                    error_mes = "无法正常登录"
                    continue_btn = self.driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div[3]/a[1]')
                    time.sleep(2)
                    if continue_btn.text == "继续登录":
                        continue_btn.click()
                        self.driver.switch_to.default_content()
                        time.sleep(3)  # 等待页面加载
                        # 点击下次再说
                        self.driver.find_element_by_class_name('th-bk-main-gh').click()
                        print('\n' + "登录成功" + '\n')
                        con = False
                        learn_or_not = True
                    elif continue_btn.text == "取消":
                        error_mes = "存在风险，需要进行验证"
                        con = False
                        learn_or_not = False
                        print(error_mes)
                        # self.writer.writerow([self.email,"需要进行手机号验证"," ",self.time])
                        raise Exception(error_mes)
                    else:
                        error_mes = "其他错误111"
                        con = False
                        learn_or_not = False
                        print(error_mes)
                        # self.writer.writerow([self.email,error_mes," ",self.time])
                        raise Exception(error_mes)
                except:
                    if error_mes == "无法正常登录":
                        try:
                            message = self.driver.find_element_by_xpath(
                                '/html/body/div[2]/div[2]/div[2]/form/div/div[7]/div[2]')
                            self.driver.implicitly_wait(5)
                            if message.text[0:7] == "该帐号已被锁定":
                                error_mes = "账号已被锁定"
                                con = False
                                learn_or_not = False
                                print(error_mes)
                                # self.writer.writerow([self.email,"账号被锁定"," ",self.time])
                                raise Exception(error_mes)
                            elif message.text == "请先拖动滑块进行安全验证":
                                # 进行滑块验证操作
                                # verify_count = 6
                                print('*' * 32 + "正在进行滑块验证！" + '*' * 32)
                                ver_num = 1
                                while ver_num <= 5:
                                    self.slider_va()
                                    try:
                                        self.driver.find_element_by_css_selector("[class='m-nerror err_slide f-dn']")
                                        ver_num = 7
                                        con = True
                                        learn_or_not = True
                                        print("验证成功")
                                    except:
                                        con = False
                                        learn_or_not = False
                                        print("第{}次验证失败".format(ver_num))
                                        ver_num += 1
                                if ver_num == 6:
                                    con = False
                                    learn_or_not = False
                                    error_mes = "滑块验证失败"
                                    print(error_mes)
                                    # self.writer.writerow([self.email,error_mes," ",self.time])
                                    raise Exception(error_mes)
                                elif ver_num == 7:
                                    con = True
                                    learn_or_not = True
                                else:
                                    con = False
                                    learn_or_not = False
                            else:
                                error_mes = "其他错误222"
                                con = False
                                learn_or_not = False
                                print(error_mes)
                                # self.writer.writerow([self.email,error_mes," ",self.time])
                                raise Exception(error_mes)
                        except:
                            con = False
                            learn_or_not = False
                            print('\n' * 5 + '账号' + self.email + error_mes + '\n' * 5)
                            self.writer.writerow([self.email, error_mes, " ", self.time])
                    else:
                        con = False
                        learn_or_not = False
                        print('\n' * 5 + '账号' + self.email + error_mes + '\n' * 5)
                        self.writer.writerow([self.email, error_mes, " ", self.time])
        # print(learn_or_not)
        return learn_or_not

    def slider_va(self):
        # 获取背景图并保存
        background = self.wait.until(
            lambda x: x.find_element_by_xpath('//img[@class="yidun_bg-img"]')
        ).get_attribute('src')
        with open('background.png', 'wb') as f:
            resp = requests.get(background)
            f.write(resp.content)

        # 获取滑块图并保存
        slider = self.wait.until(
            lambda x: x.find_element_by_xpath('//img[@class="yidun_jigsaw"]')
        ).get_attribute('src')
        with open('slider.png', 'wb') as f:
            resp = requests.get(slider)
            f.write(resp.content)

        # 计算距离
        distance = self.findfic(target='background.png', template='slider.png')
        # 初始滑块距离边缘 4 px
        trajectory = self.get_tracks(distance + 4)

        # 等待按钮可以点击
        slider_element = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[5]/div/div/div[2]/div[2]'))
        )
        # 添加行动链
        ActionChains(self.driver).click_and_hold(slider_element).perform()
        for track in trajectory['plus']:
            ActionChains(self.driver).move_by_offset(
                xoffset=track,
                yoffset=round(random.uniform(1.0, 3.0), 1)
            ).perform()
        time.sleep(0.5)

        for back_tracks in trajectory['reduce']:
            ActionChains(self.driver).move_by_offset(
                xoffset=back_tracks,
                yoffset=round(random.uniform(1.0, 3.0), 1)
            ).perform()
        #
        for i in [-4, 4]:
            ActionChains(self.driver).move_by_offset(
                xoffset=i,
                yoffset=0
            ).perform()
        time.sleep(0.1)
        ActionChains(self.driver).release().perform()
        time.sleep(2)

    def start_lean(self):
        # self.driver.implicitly_wait(10)  # 隐性等待，最长等10秒
        # class_num = 0
        learn_or_not = self.login()
        print(learn_or_not)
        time.sleep(5)
        while learn_or_not:
            print("开始学习课程")
            self.driver.switch_to.window(self.driver.window_handles[0])  # 定位操作柄到当前标签页
            # 进入“我的学习”页
            # 加载课程列表
            class_list = self.driver.find_elements_by_class_name('uc-ykt-course-card_title')  # 根据标题来选择课程
            # 单账号开始循环学习
            for course_num in range(len(class_list)):
                self.driver.implicitly_wait(10)  # 隐性等待，最长等10秒
                self.driver.switch_to.window(self.driver.window_handles[0])  # 定位操作柄到当前标签页
                # 开始学习课程
                self.driver.execute_script("arguments[0].click();", class_list[course_num])  # 点击课程，跳入课程页面
                self.driver.switch_to.window(self.driver.window_handles[1])  # 定位操作柄到当前标签页
                # 判断是否开始学习
                begin_button = self.driver.find_element_by_xpath(
                    '/html/body/div[5]/div[4]/div[1]/div/div/div[1]/div[2]/a/span')
                begin_or_not = begin_button.text
                while begin_or_not != "":   # 如果内容不为空，则开始学习
                    class_num = len(self.driver.find_elements_by_class_name("section"))  # 课程数
                    if class_num <= 5:
                        start_num = class_num - 1
                        stop_num = class_num
                    elif 5 < class_num <= 10:
                        start_num = 5
                        stop_num = class_num - 1
                    else:
                        start_num = 6
                        stop_num = 9
                    # 点击开始学习 进入课程视频播放页面
                    # begin_button.click()
                    self.driver.find_element_by_class_name("section").click()
                    # 等待页面加载完成
                    self.driver.implicitly_wait(20)  # 隐性等待，最长等20秒
                    time.sleep(2)
                    # 关闭广告
                    try:
                        self.driver.find_element_by_xpath("/html/body/div[16]/div/div[1]/a/i").click()
                    except:
                        pass
                    print("本次课程共{}个课时\n".format(class_num))
                    for i in range(random.randint(start_num, stop_num)):  # 随机学习次数
                        ran_time_num = random.randint(5, 10)  # 生成随机学习时长
                        print("正在学习第{}课时".format(i + 1))
                        time.sleep(ran_time_num)
                        time.sleep(1)
                        learned = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]/div/div/div[2]/em')
                        if learned.get_attribute('title') == '你已经学完该课时了':
                            learned.click()
                            time.sleep(0.5)
                            learned.click()  # 点击学过了
                        else:
                            learned.click()
                        time.sleep(ran_time_num)
                        learn_next = self.driver.find_element_by_xpath(
                            '/html/body/div[2]/div[1]/div[3]/div/div/div[1]/div[2]/div[2]/div/div[4]/a/span')
                        learn_next.click()  # 学习下一课时
                        time.sleep(2)
                    print("已完成{}个课时的学习，即将返回课程首页进行课程评价".format(i+1))
                    # 退出课程学习页面
                    begin_or_not = ""
                    # 返回课程主页
                    time.sleep(0.5)
                    class_home = self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/a[1]')
                    class_home.click()
                # 执行课程评价操作
                self.estimate(course_num)
            time.sleep(2)
            print('\n' * 3 + "账号" + self.email + "已完成{}门课程的学习".format(len(class_list)) + '\n' * 3)
            learn_or_not = False
            self.writer.writerow([self.email, '完成学习', len(class_list), self.time])
            print('*' * 30 + "即将关闭浏览器" + '*' * 30)

    def estimate(self, course_num):     # 评价操作
        # 等待页面加载
        self.driver.implicitly_wait(10)  # 隐性等待，最长等10秒
        time.sleep(1)
        try:
            # 重新编辑评论
            edit_com = self.driver.find_element_by_xpath(
                '/html/body/div[5]/div[5]/div[1]/div[8]/div/div/div[1]/a')
            edit_com.click()
            time.sleep(2)
            # 发表评论
            com = self.driver.find_element_by_xpath(
                '/html/body/div[5]/div[5]/div[1]/div[8]/div/div/div[2]/div[3]/a[1]/span')
            com.click()
            time.sleep(2)  # 等待2秒后关闭当前标签页，回到课程列表页
            self.driver.close()
            print("第{}门课程已重新编辑评论".format(course_num + 1))
        except:
            try:
                # 需要新编辑并打星
                star_cli = self.driver.find_element_by_xpath(
                    '/html/body/div[5]/div[5]/div[1]/div[8]/div/div/div[1]/div/div/div[5]')
                star_cli.click()  # 打5星
                time.sleep(2)
                # 从评论列表里随机选出一句评论
                comment = random.choice(self.comment_list)
                in_com = self.driver.find_element_by_xpath(
                    '/html/body/div[5]/div[5]/div[1]/div[8]/div/div/div[2]/div[1]/div/div[3]/div/textarea')
                in_com.send_keys(comment)  # 输入评论文字（可以设计成从好评栏里随机选择）
                time.sleep(3)
                com = self.driver.find_element_by_xpath(
                    '/html/body/div[5]/div[5]/div[1]/div[8]/div/div/div[2]/div[3]/a[1]/span')
                com.click()  # 发表评论
                time.sleep(2)  # 等待2秒后关闭当前标签页，回到课程列表页
                self.driver.close()
                print("第{}门课程已进行新的评论".format(course_num + 1))
            except:
                # 找不到编辑按钮，即不用重新编辑
                print("第{}门课程没有找到编辑评价按钮，不用重新评价".format(course_num + 1))
                time.sleep(2)
                self.driver.close()  # 关闭当前标签页，回到课程列表页

    def findfic(self, target='background.png', template='slider.png'):
        """
        :param target: 滑块背景图
        :param template: 滑块图片路径
        :return: 模板匹配距离
        """
        target_rgb = cv2.imread(target)
        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
        template_rgb = cv2.imread(template, 0)
        # 使用相关性系数匹配， 结果越接近1 表示越匹配
        # https://www.cnblogs.com/ssyfj/p/9271883.html
        res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
        # opencv 的函数 minMaxLoc：在给定的矩阵中寻找最大和最小值，并给出它们的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # 因为滑块只需要 x 坐标的距离，放回坐标元组的 [0] 即可
        if abs(1 - min_val) <= abs(1 - max_val):
            distance = min_loc[0]
        else:
            distance = max_loc[0]
        distance *= 0.75
        return int(distance)

    def get_tracks(self, distance):
        """

        :param distance: 缺口距离
        :return: 轨迹
        """
        # 分割加减速路径的阀值
        value = round(random.uniform(0.55, 0.75), 2)
        # 划过缺口 20 px
        distance += 15
        # 初始速度，初始计算周期， 累计滑动总距
        v, t, sum = 0, 0.3, 0
        # 轨迹记录
        plus = []
        # 将滑动记录分段，一段加速度，一段减速度
        mid = distance * value
        while sum < distance:
            if sum < mid:
                # 指定范围随机产生一个加速度
                a = round(random.uniform(7, 8), 1)
            else:
                # 指定范围随机产生一个减速的加速度
                a = -round(random.uniform(4.0, 5.0), 1)
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            sum += s
            plus.append(round(s))

        # end_s = sum - distance
        # plus.append(round(-end_s))

        # 手动制造回滑的轨迹累积20px
        # reduce = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
        reduce = [-3, -2, -3, -2]
        return {'plus': plus, 'reduce': reduce}

    def learn(self):
        self.open_Chrome()
        # print("执行步骤1")
        self.enter_AP()
        # print("执行步骤2")
        self.start_lean()
        # print("执行步骤3")
        try:
            self.close()
        except:
            pass


if __name__ == "__main__":
    # 打开评论文件生成列表
    nc = pd.read_excel("./netease_Comment.xlsx")
    comment_list = nc["comments"]
    # 打开账号信息文件
    af = pd.read_excel("./netease_Account.xlsx")
    with open('账号操作记录.csv', 'a', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for a in range(len(af)):
            email = str(af["account"][a])
            password = str(af["password"][a])
            # print("正在执行第{}个账号".format(a+1))
            print('\n' * 3 + "正在执行第{}个账号：".format(a + 1) + email + '\n' * 3)
            learnning = netease_Auto_Learn(email, password, writer, comment_list)
            learnning.learn()
            time.sleep(2)
        csv_file.close()
        print('\n' * 3 + '*' * 30 + '程序将在十秒后自动退出' + '*' * 30 + '\n')
        time.sleep(10)
