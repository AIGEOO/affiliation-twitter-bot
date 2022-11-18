import json, os, random, time, schedule

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

class AccountOperations:
    def __init__(self):
        self.username = os.getenv('TWITTER_USERNAME')
        self.password = os.getenv('TWITTER_PASSWORD')
        self.is_logged_in = False

    # initializing chrome drivers 
    def init_chrome_driver(self):
        """"Initializing chrome drivers"""
        # If there is no instance create one
        try:
            # Creating chrome options
            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "eager"
            chrome_options = webdriver.ChromeOptions()

            prefs = {"profile.managed_default_content_settings.images": 2,
                        "profile.default_content_settings.images": 2}

            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

            chrome_options.add_argument('--incognito')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--silent')
            chrome_options.add_argument('--log-level=OFF')
            chrome_options.add_argument('--disable-extensions')

            # , options=chrome_options
            self.chrome_driver = webdriver.Chrome(executable_path=os.getenv('CHROME_DRIVER_PATH'))
        except Exception as e:
            raise ConnectionError("Couldn't init chrome drivers" + str(e))

    def login(self) -> bool:
        self.chrome_driver.get('https://twitter.com/login')
        time.sleep(5)

        print("Start Log in process...")

        try:
            username = self.chrome_driver.find_element_by_xpath("//input[@name='text']")
            username.clear()
            username.send_keys(self.username)
            username.send_keys(keys.Keys.RETURN)
            time.sleep(2)
            try:
                password = self.chrome_driver.find_element_by_xpath("//input[@name='password']")
                password.clear()
                password.send_keys(self.password)
                password.send_keys(keys.Keys.RETURN)
            except NoSuchElementException as e:
                print("password input field does not exsist!")
        except NoSuchElementException as e:
            print("username input field does not exsist!")
        
        print("Login process done successfully :)")

        self.is_logged_in = True
        time.sleep(5)

        return self.is_logged_in

    def logout(self) -> bool:
        if not self.is_logged_in:
            return 

        print("Start Logout process...")
        
        self.chrome_driver.get('https://twitter.com/logout')

        try:
            logout_btn = WebDriverWait(self.chrome_driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='button'][1]"))
            )

            logout_btn.click()
        except NoSuchElementException as e:
            print("logout button does not exsist!")

        self.is_logged_in = False
        return self.is_logged_in 

    def search(self, query: str = "") -> str:
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        print(f"searching for {query}")

        time.sleep(5)

        search_bar = self.chrome_driver.find_element_by_xpath("//input[@enterkeyhint='search']")
        search_bar.send_keys(query)
        search_bar.send_keys(keys.Keys.RETURN)
        time.sleep(5)

        return "Results listed!" 

    def post_tweet(self, text_content: str, img: str) -> None:
        if not self.is_logged_in:
            raise Exception("You must log in first!")

        print("Start Posting tweet process")

        self.chrome_driver.get('https://twitter.com/compose/tweet')
        
        time.sleep(5) 

        try:
            self.chrome_driver.find_element_by_xpath("//div[@role='textbox']").send_keys(text_content)

            image = self.chrome_driver.find_element_by_xpath("//input[@data-testid='fileInput']")

            image.send_keys(os.getcwd() + img) 

            # This to click on the page to remove the container on the  tweetButton
            self.chrome_driver.find_element_by_xpath("//div[@class='css-1dbjc4n r-1p0dtai r-1d2f490 r-1xcajam r-zchlnj r-ipm5af']").click()

            self.chrome_driver.find_element_by_xpath("//div[@data-testid='tweetButton']").click()

        except NoSuchElementException as e:
            print("Tweet input field does not exsist!")

        time.sleep(5)
    
    def delete_tweets(self, cycles: int = 100) -> None:
        if not self.is_logged_in:
            raise Exception("You must log in first!") 

        self.chrome_driver.get(f'https://twitter.com/{self.username}')

        time.sleep(5)

        for i in range(cycles):
            try:
                self.chrome_driver.find_element_by_xpath(f"//div[@data-testid='cellInnerDiv'][{i}]/div/div/div/article[@data-testid='tweet']//*[@data-testid='caret']").click()
                time.sleep(1)
                self.chrome_driver.find_element_by_xpath(f"//div[@data-testid='Dropdown']/div").click()
                self.chrome_driver.find_element_by_xpath("//div[@data-testid='confirmationSheetConfirm']").click()
            except NoSuchElementException:
                print('Delete buttons does not exsists')
                self.chrome_driver.execute_script(f"window.scrollTo(0, 170)")
                pass
        
        self.refresh()
    
    def retweet_tweets(self, cycles: int = 100) -> None:
        if not self.is_logged_in:
            raise Exception("You must log in first!") 

        for i in range(cycles):
            try:
                self.chrome_driver.find_element_by_xpath(f"//div[@data-testid='cellInnerDiv'][{i}]/div/div/div/article[@data-testid='tweet']//*[@data-testid='retweet']").click()
                time.sleep(5)
                self.chrome_driver.find_element_by_xpath("//div[@data-testid='retweetConfirm']").click()
                time.sleep(3)
            except NoSuchElementException:
                print('Retweet buttons does not exsists')
                pass

        self.refresh()

    def remove_retweets(self, cycles: int = 100) -> None:
        if not self.is_logged_in:
            raise Exception("You must log in first!") 

        for i in range(cycles):
            try:
                self.chrome_driver.find_element_by_xpath(f"//div[@data-testid='cellInnerDiv'][{i}]/div/div/div/article[@data-testid='tweet']//*[@data-testid='unretweet']").click()
                time.sleep(5)
                self.chrome_driver.find_element_by_xpath("//div[@data-testid='unretweetConfirm']").click()
                time.sleep(5)
            except NoSuchElementException:
                print('Unretweet buttons does not exsists')
                pass

        self.refresh()

    def like_tweets(self, cycles: int = 100) -> None:
        if not self.is_logged_in:
            raise Exception("You must log in first!") 

        for i in range(cycles):
            try:
                self.chrome_driver.find_element_by_xpath(f"//div[@data-testid='cellInnerDiv'][{i}]/div/div/div/article[@data-testid='tweet']//*[@data-testid='like']").click()
            except NoSuchElementException:
                print('Like buttons does not exsists')
                pass

        self.refresh()
    
    def unlike_tweets(self, cycles: int = 100) -> None:
        if not self.is_logged_in:
            raise Exception("You must log in first!") 

        for i in range(cycles):
            try:
                self.chrome_driver.find_element_by_xpath(f"//div[@data-testid='cellInnerDiv'][{i}]/div/div/div/article[@data-testid='tweet']//*[@data-testid='unlike']").click()
            except NoSuchElementException:
                print('Unlike buttons does not exsists')
                pass

        self.refresh()

    def refresh(self) -> None:
        self.chrome_driver.refresh()
        time.sleep(5)

    @staticmethod
    def fetch_content(counter: int) -> list:
        with open('assets/content.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        text_content = data[f'{counter}']['txt']
        img = f"\\assets\\images\\{random.randint(1, 2)}.png"

        return [text_content, img]

    def start(self) -> None:
        counter = 0
        self.init_chrome_driver()
        self.login()

        while True:
            counter += 1
            content = self.fetch_content(counter)
            self.post_tweet(content[0], content[1])
            
            # self.search("#my_name_is_aigeo")
            self.chrome_driver.get(f'https://twitter.com/{self.username}')
            self.chrome_driver.refresh()
            time.sleep(5)

            self.retweet_tweets()
            self.like_tweets()

            if counter >= 20:
                self.unlike_tweets()
                self.remove_retweets()
                self.delete_tweets()
                counter = 0

        # self.logout()