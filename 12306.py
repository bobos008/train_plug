# coding=utf-8

import time
import ele_utils
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TrainTicket(object):
    """12306抢票模块"""

    def __init__(self, username, password):
        self.init_url =  'https://www.12306.cn/index/'
        self.driver = self.back_driver()
        self._username = username
        self._password = password

    def back_driver(self):
        """加载首页"""
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(chrome_options=option)
        # driver.maximize_window()
        driver.set_window_size(1366,788)
        driver.get(self.init_url)
        return driver

    def open_login_page(self):
        """在首页打开登录页面"""
        open_login_page_btn_xpath = '//li[@id="J-header-login"]/a[1]'
        open_login_page_btn = ele_utils.get_element_for_wait(
            self.driver,
            By.XPATH,
            open_login_page_btn_xpath,
            timeout=25
        )
        if not open_login_page_btn:
            return False
        time.sleep(3)
        open_login_page_btn.click()
        return True

    def login(self):
        """开始登录"""
        # 点击账号登录
        change_hd_account_xpath = '//li[@class="login-hd-account"]/a'
        change_hd_account = ele_utils.get_element_for_wait(
            self.driver,
            By.XPATH,
            change_hd_account_xpath
        )
        if not change_hd_account:
            return False
        time.sleep(2)
        change_hd_account.click()

        # 输入账号
        username_xpath = '//input[@id="J-userName"]'
        username_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            username_xpath
        )
        if not username_ele:
            return False
        username_ele.click()
        username_ele.send_keys(self._username)

        # 输入密码
        password_xpath = '//input[@id="J-password"]'
        password_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            password_xpath
        )
        if not password_ele:
            return False
        password_ele.click()
        password_ele.send_keys(self._password)
        return True

    def send_from_city(self, from_city):
        """输入出发城市"""
        from_city_xpath = '//input[@id="fromStationText"]'
        from_city_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            from_city_xpath
        )
        if not from_city_ele:
            return False
        time.sleep(3)
        from_city_ele.click()
        from_city_ele.send_keys(from_city)
        from_city_ele.send_keys(Keys.ENTER)
        return True

    def send_to_city(self, to_city):
        """输入到达城市"""
        to_city_xpath = '//input[@id="toStationText"]'
        to_city_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            to_city_xpath
        )
        if not to_city_ele:
            return False
        time.sleep(3)
        to_city_ele.click()
        to_city_ele.send_keys(to_city)
        to_city_ele.send_keys(Keys.ENTER)
        return True

    def choose_date(self, day):
        """只能选择右边的日期"""
        train_date_xpath = '//input[@id="train_date"]'
        train_date = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            train_date_xpath
        )
        if not train_date:
            return False
        time.sleep(2)
        train_date.click()

        dates_xpath = '//div[@class="cal cal-right"]/div[2]/div[@class="cell"]/div'
        # dates_xpath = '//div[@class="cal"]/div[2]/div[@class="cell"]/div'
        date_ele_list = ele_utils.get_include_hide_elements_for_wait(
            self.driver,
            By.XPATH,
            dates_xpath
        )
        if not date_ele_list:
            return False
        time.sleep(2)
        for date_ele in date_ele_list:
            print(date_ele.text)
            if date_ele.text == day:
                date_ele.click()
                break
        return True

    def index_search(self):
        """在index页面点击查询"""
        search_xpath = '//a[@id="search_one"]'
        search_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            search_xpath
        )
        if not search_ele:
            return False
        time.sleep(2)
        search_ele.click()

    def is_have_ticket(self, train_list):
        """是否有票"""

        # 二等座剩余数
        have_ticket_xpath = '//tbody[@id="queryLeftTable"]/tr/td[4]'
        have_ticket_list = ele_utils.get_include_hide_elements_for_wait(
            self.driver,
            By.XPATH,
            have_ticket_xpath
        )
        if not have_ticket_list:
            return False

        # 所有预订的按钮
        book_list_xpath = '//tbody[@id="queryLeftTable"]/tr/td[13]/a'
        book_list = ele_utils.get_include_hide_elements_for_wait(
            self.driver,
            By.XPATH,
            book_list_xpath
        )
        if not book_list:
            return False

        # 获取所有的车次号
        train_num_list_xpath = '//tbody[@id="queryLeftTable"]/tr/td/div/div/div/a'
        train_num_list = ele_utils.get_include_hide_elements_for_wait(
            self.driver,
            By.XPATH,
            train_num_list_xpath
        )
        if not train_num_list:
            return False

        total_train = len(train_num_list)
        if (total_train != len(have_ticket_list)) and (total_train != len(book_list)):
            return False
        for t in range(total_train):
            train_name = train_num_list[t].text
            if train_name in train_list:
                remainder_ticket = have_ticket_list[t].text
                print(remainder_ticket)
                if remainder_ticket == u'有':
                    book_list[t].click()
                    break
                if isinstance(remainder_ticket, int):
                    if int(remainder_ticket) > 0:
                        book_list[t].click()
                        break

    def query_ticket(self):
        """进入到火车票详情查询"""
        query_ticket_xpath = '//a[@id="query_ticket"]'
        query_ticket_ele = ele_utils.get_include_hide_element_for_wait(
            self.driver,
            By.XPATH,
            query_ticket_xpath,
            timeout=60
        )
        if not query_ticket_ele:
            return False
        time.sleep(2)
        while 1:
            try:
                query_ticket_ele.click()
            except:
                time.sleep(1)
                continue
            break
        return True

    def main(self, tfrom_city, tto_city, tday, ttrain_num_list):
        """入口"""
        if not self.open_login_page():
            return False
        if not self.login():
            return False
        login_result_url = 'https://kyfw.12306.cn/otn/view/index.html'
        while 1:
            cur_url = self.driver.current_url
            print(cur_url)
            if cur_url == login_result_url:
                self.driver.get(self.init_url)
                break
            continue
        self.send_from_city(tfrom_city)
        self.send_to_city(tto_city)
        self.choose_date(tday)
        self.index_search()

        # 切换页面
        windows = self.driver.window_handles
        self.driver.switch_to_window(windows[-1])
        while 1:
            self.query_ticket()
            time.sleep(0.5)
            if not self.is_have_ticket(ttrain_num_list):
                continue
            break
        return True


if __name__ == "__main__":
    user = ""
    pwd = ""
    to_city = u"湛江"
    from_city = u"广州"
    # day = "30"
    day = u"国庆"
    train_num_list = ['D7191', 'D7459', 'D7461']
    tt = TrainTicket(user, pwd)
    print("----------main:",tt.main(from_city, to_city, day, train_num_list))
