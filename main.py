from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep

class Taaghche:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = 'https://taaghche.com/'
        self.page_number = 1

    def login(self, username, password):
        login_bottun_class = 'profileDropdown_login__1mKoW'
        self.driver.get(self.login_page)
        login_button = self.driver.find_element_by_class_name(login_bottun_class)
        login_button.click()

        sleep(1)

        ########## Fill in the username
        username_name = 'username'
        fill_username = self.driver.find_element_by_name(username_name)
        fill_username.send_keys(username)

        ########## Click on 'Continue'
        continue_xpath = '/html/body/div[2]/div/div/div/div[2]/form/button'
        click_continue = self.driver.find_element_by_xpath(continue_xpath)
        click_continue.click()

        sleep(1)

        ########## Fill in the password
        password_name = 'password'
        fill_password = self.driver.find_element_by_name(password_name)
        fill_password.send_keys(password)

        ########## Click on 'Submit'
        submit_xpath = '/html/body/div[2]/div/div/div/div[2]/form/button'
        click_submit = self.driver.find_element_by_xpath(submit_xpath)
        click_submit.click()

    def __open_my_lib(self):
        self.my_lib_link = 'https://taaghche.com/mylibrary?type=text'
        self.driver.execute_script(f'window.open("{self.my_lib_link}");')
        sleep(10)
        self.driver.switch_to.window(driver.window_handles[1])

    def input_checker(self):
        input_value = input()
        if input_value == 'start':
            return input_value

    def select_book(self):
        self.__open_my_lib()
        #self.driver.execute_script(f'window.open("{self.book_reader_link}","_blank");')
        #return self.book_reader_link
        if self.input_checker() == 'start':
            self.page_book()
    def page_book(self):
        self.driver.maximize_window()
        t = 920
        while t != 0:
            self.__screen_shot(self.driver)
            self.control_reader_page(left=True)
            t += 1


    def control_reader_page(self, left=False, right=False):
        if left:
            self.driver.find_element_by_id('___nextPage').click()

        elif right:
            self.driver.find_element_by_id('___prevPage').click()

    def __screen_shot(self, driver):
        driver.save_screenshot(f'{self.page_number}-book.jpg')
        self.page_number += 1


driver_address = 'chromedriver.exe'
driver = webdriver.Chrome(driver_address)

taaghche = Taaghche(driver=driver)

info = {
    'username': 'a.jalali2005@gmail.com',
    'password': '20052005'
}

taaghche.login(username=info['username'], password=info['password'])

taaghche.select_book()