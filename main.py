from selenium import webdriver
from time import sleep
from PIL import Image
import pytesseract
import shutil
import hazm
import os


class Taaghche:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = 'https://taaghche.com/'
        self.total_pages = 0
        self.current_page_number = 0
        self.images_path = './images'
        self.texts_path = './text'
        self.images_address = []
        self.crop_info = {
            'left': 130,
            'right': 1800,
            'top': 65,
            'bottom': 790
        }
        self.texts = []
        self.normalizer = hazm.Normalizer()

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

        sleep(1.5)

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
        self.id = id
        self.__open_my_lib()
        #id = self.__get_book_id()
        if self.__input_checker() == 'start':
            self.driver.maximize_window()
            self.total_pages = int(self.__get_total_pages())
            print(self.total_pages)
            self.__reset_page_number()

            ## Create Images Dir
            try:
                os.mkdir(self.images_path)
            except OSError:
                shutil.rmtree(self.images_path)
                os.mkdir(self.images_path)

            ## Create Texts Dir
            try:
                os.mkdir(self.texts_path)
            except OSError:
                shutil.rmtree(self.texts_path)
                os.mkdir(self.texts_path)

            self.__page_book()
        return self.texts

    def __page_book(self):
        self.page_number = int(self.__get_current_page_number())
        while self.page_number <= self.total_pages:
            self.__situation('save-screenshot')
            self.__screen_shot()
            self.__image_to_text()
            self.__control_reader_page(next=True)
            self.__situation(status='page-number')
            self.page_number += 1


    def __reset_page_number(self, reset=True):
        if reset:
            page_now = self.driver.find_element_by_id('pageNo')
            page_now = int(page_now.text)
            self.__situation(status='page-reset')
            while page_now != 1:
                self.__control_reader_page(previous=True)
                page_now = self.driver.find_element_by_id('pageNo')
                page_now = int(page_now.text)
            self.__situation(status='page-reseted')

    def __get_total_pages(self):
        totalpages = self.driver.find_element_by_id('totalPages')
        totalpages = totalpages.text
        return totalpages

    def __get_book_id(self):
        url = str(self.driver.current_url)
        url = url.split('/')
        for i in range(len(url)):
            if isinstance(url[i], int):
                return int(url[i])

    def __situation(self, status, image_name = ''):
        if status == 'page-number':
            print(f'[*]Page {self.page_number} of {self.total_pages}')
        elif status == 'save-screenshot':
            print(f'[Page {self.page_number}]Screenshot is saving...')
        elif status == 'screenshot-saved':
            print(f'[Page {self.page_number}]Screenshot Saved!')
        elif status == 'page-reset':
            print('Page number is being reset ...')
        elif status == 'page-reseted':
            print('Page number reset!')
        elif status == 'image-cropped':
            print(f'[{image_name}] cropped!')

    def __get_current_page_number(self):
        current_page = self.driver.find_element_by_id('pageNo')
        current_page = current_page.text
        return current_page

    def __control_reader_page(self, next=False, previous=False):
        if next:
            self.driver.find_element_by_id('___nextPage').click()

        elif previous:
            self.driver.find_element_by_id('___prevPage').click()

    def __save_images_address(self, address):
        self.images_address.append(address)
        print(self.images_address[-1])

    def __image_to_text(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        extracted_text = pytesseract.image_to_string(self.images_address[-1], lang='fas')
        extracted_text = self.normalizer.normalize(extracted_text)
        self.texts.append(extracted_text)

    def __crop_images(self, address):
        image = Image.open(address)
        image = image.crop((self.crop_info['left'], self.crop_info['top'], self.crop_info['right'], self.crop_info['bottom']))
        image = image.convert('RGB')
        image.save(address)
        self.__situation(status='image-cropped', image_name=address)

    def __screen_shot(self):
        image_address = f'{self.images_path}/page{self.page_number}-{self.id}.jpg'
        self.__save_images_address(image_address)
        self.driver.save_screenshot(self.images_address[-1])
        self.__crop_images(self.images_address[-1])
        self.__situation(status='screenshot-saved')

driver_address = 'chromedriver.exe'
driver = webdriver.Chrome(driver_address)

taaghche = Taaghche(driver=driver)

info = {
    'username': 'a.jalali2005@gmail.com',
    'password': '20052005'
}

taaghche.login(username=info['username'], password=info['password'])

texts = taaghche.select_book(id=39639)
print(texts)

text = ''

replace_character = [
    [r'\u200c', 'ی'],
    [r'\n', '']
]

for i in range(len(texts)):
    for j in range(len(replace_character)):
        text += texts[i].replace(replace_character[j][0], replace_character[j][1])

normalizer = hazm.Normalizer()
text = normalizer.normalize(text)

print(text)