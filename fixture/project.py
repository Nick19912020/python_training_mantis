from model.project import Project


class ProjectHelper:

    project_cache = None

    def __init__(self, app):
        self.app = app

    def open_project_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php") and len(
                wd.find_elements_by_xpath("//button[@type='submit']")) > 0):
            wd.find_element_by_css_selector("i.menu-icon.fa.fa-gears").click()
            wd.find_element_by_link_text(u"Управление проектами").click()

    def create(self, project):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_xpath("//button[@type='submit']").click()
        self.fill_project_form(project)
        wd.find_element_by_xpath(u"//input[@value='Добавить проект']").click()
        self.return_to_project_page()
        self.project_cache = None

    def fill_project_form(self, project):
        self.change_field_value("name", project.name)
        self.change_field_value("description", project.description)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def return_to_project_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php") and len(
                wd.find_elements_by_by_xpath("//button[@type='submit']")) > 0):
            wd.find_element_by_css_selector("i.menu-icon.fa.fa-gears").click()
            wd.find_element_by_link_text(u"Управление проектами").click()

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_project_page()
            self.project_cache = []
            for element in wd.find_elements_by_xpath("//div[@id='main-container']/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/table/tbody/tr"):
                name = element.find_element_by_css_selector("td:nth-child(1)").text
                id_not_fetched = element.find_element_by_css_selector(
                    'a[href ^= "manage_proj_edit_page.php?project_id="]').get_attribute("href")
                identifier = id_not_fetched.replace("http://localhost/mantisbt-2.24.4/manage_proj_edit_page.php?project_id=", "")
                description = element.find_element_by_css_selector("td:nth-child(5)").text
                self.project_cache.append(Project(name=name, description=description, identifier=identifier))
        return list(self.project_cache)

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_project_page()
        self.select_project_by_id(id)
        wd.find_element_by_xpath(u"//input[@value='Удалить проект']").click()
        wd.find_element_by_xpath(u"//input[@value='Удалить проект']").click()
        self.project_cache = None

    def select_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_css_selector('a[href ^= "manage_proj_edit_page.php?project_id=' + str(id) + '"]').click()