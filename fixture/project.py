from model.project import Project
from selenium.webdriver.support.select import Select

class ProjectHelper:
    def __init__(self, app):
        self.app = app


    def open_projects_page(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[contains(@href, '/mantisbt-2.20.0/manage_overview_page.php')]").click()

    def manage(self):
        wd = self.app.wd
        wd.find_element_by_xpath(u"//a[contains(text(),'Управление проектами')]").click()

    def add_project_button(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//button[@type='submit']").click()

    def fill_project(self, project):
        wd = self.app.wd
        self.fill_field('name', project.name)
        self.fill_field('status', project.state)
        self.fill_field('inherit_global', project.globaled)
        self.fill_field('view_state', project.visibility)
        self.fill_field('description', project.description)
        wd.find_element_by_xpath("//form[@id='manage-project-create-form']/div/div[3]/input").click()


    def fill_field(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            #wd.find_elements_by_name(field_name).click
            wd.find_element_by_name(field_name).send_keys(text)

    def select_value(self, field_name, value):
        wd = self.app.wd
        wd.find_element_by_name(field_name).selectByValue(value)


    def get_proj_list(self):
        wd = self.app.wd
        proj_list = []
        self.open_projects_page()
        self.manage()
        for element in wd.find_elements_by_xpath(".//div[@id='main-container']/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/table/tbody/tr"):
            id = (str(element.find_element_by_xpath(".//td[1]/a").get_attribute("href"))).partition('=')[2]
            name = element.find_element_by_xpath(".//td[1]").text
            state = element.find_element_by_xpath(".//td[2]").text
            #globaled = element.find_element_by_xpath(".//td[4]").text
            #description = element.find_element_by_xpath(".//td[5]").text
            proj_list.append(Project(id=id, name=name, state=state))

        return proj_list

