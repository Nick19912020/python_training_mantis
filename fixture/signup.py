import re


class SignupHelper:

    def __init__(self, app):
        self.app = app

    def new_user(self, username, email, password):
        wd = self.app.wd
        wd.get(self.app.base_URL + "/signup_page.php")
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("email").send_keys(email)
        wd.find_element_by_css_selector("input[type='submit']").click()

        mail = self.app.mail.get_mail(username, password, "=?utf-8?B?W01hbnRpc0JUXSDQoNC10LPQuNGB0YLRgNCw0YbQuNGPINGD0Y"
                                                          "fRkdGC0L0=?\n =?utf-8?B?0L7QuSDQt9Cw0L/QuNGB0Lg=?")
        url = self.extract_confirmation_url(mail)

        wd.get(url)
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_name("password_confirm").send_keys(password)
        wd.find_element_by_css_selector("span[class='bigger-110']").click()

    def extract_confirmation_url(self, text):
        new_text = text.replace("\n", "")
        new_text2 = re.search("http://.*Если", new_text).group(0)
        return new_text2.replace('Если', '')