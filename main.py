from selenium import webdriver
from time import sleep
import os

class Taaghche:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = 'https://taaghche.com/'
        self.total_pages = 0
        self.current_page_number = 0

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

    def __input_checker(self):
        input_value = input()
        if input_value == 'start':
            return input_value

    def select_book(self, id):
        self.__open_my_lib()
        
        if self.__input_checker() == 'start':
            self.driver.maximize_window()
            self.total_pages = int(self.__get_total_pages())
            print(self.total_pages)
            self.__page_book(id)

    def __page_book(self, id):
        self.page_number = int(self.__get_current_page_number())
        while self.page_number <= self.total_pages:
            self.__screen_shot(id)
            self.__control_reader_page(next=True)
            self.__situation()
            self.page_number += 1

    def __get_total_pages(self):
        totalpages = self.driver.find_element_by_id('totalPages')
        totalpages = totalpages.text
        return totalpages

    def __situation(self):
        print(f'[*]Page {self.page_number} of {self.total_pages}')

    def __get_current_page_number(self):
        current_page = self.driver.find_element_by_id('pageNo')
        current_page = current_page.text
        return current_page

    def __control_reader_page(self, next=False, previous=False):
        if next:
            self.driver.find_element_by_id('___nextPage').click()

        elif previous:
            self.driver.find_element_by_id('___prevPage').click()

    def __screen_shot(self, id):
        self.driver.save_screenshot(f'page{self.page_number}-{id}.jpg')


driver_address = 'chromedriver.exe'
driver = webdriver.Chrome(driver_address)

taaghche = Taaghche(driver=driver)

info = {
    'username': 'a.jalali2005@gmail.com',
    'password': '20052005'
}

taaghche.login(username=info['username'], password=info['password'])

taaghche.select_book(id=39639)