from selenium import webdriver
from selenium.webdriver.support.select import Select
from fixture.session import SessionHelper

class Application:
    def __init__(self, browser, base_url):
        if browser =="firefox":
            self.wd = webdriver.Firefox()
        elif browser =="chrome":
            self.wd = webdriver.Chrome()
        elif browser == "Ie":
            self.wd = webdriver.ie()
        else:
            raise ValueError("Unrecignized browser %s " % browser)
        self.session = SessionHelper(self)

        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def is_session_valid(self):
        try:

            self.wd.find_element_by_css_selector("span.user_info").text
            return True
        except:
            return False

    def is_logged_in(self):
        user = self.wd.find_element_by_css_selector("span.user-info").text
        return user


    def open_home_page(self):
        wd = self.wd
        # open home page
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()



