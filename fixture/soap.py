from suds.client import Client
from suds import WebFault
from model.project import Project



class SoapHelper:

    def __init__(self, app):
        self.app = app

    def ensure_user_exists(self, username, password):
        soap_config = self.app.config['soap']
        session = SoapHelper.Session(
            soap_config['host'], soap_config['port'], soap_config['username'], soap_config['password'])
        if session.is_users_registered(username):
            session.reset_password(username, password)
        else:
            session.create_user(username, password)
        session.quit()

    def get_project_list(self, username, password):
        client = Client("http://localhost/mantisbt-2.24.4/api/soap/mantisconnect.php?wsdl")

        def convert(project):
            return Project(identifier=str(project.id), name=project.name, description=project.description)
        try:
            list_projects = client.service.mc_projects_get_user_accessible(username, password)
            return list(map(convert, list_projects))
        except WebFault:
            return False