from model.project import Project
import random
from random import randint


def test_delete_some_project(app, db, check_ui, config):
    if len(db.get_project_list()) == 0:
        app.group.create(Project(name='Test'+str(randint(1, 10000)), description='description'+str(randint(1, 100000))))
    old_projects = app.soap.get_project_list(username=config['web']["username"], password=config['web']["password"])
    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.identifier)
    new_projects = app.soap.get_project_list(username=config['web']["username"], password=config['web']["password"])
    old_projects.remove(project)
    assert old_projects == new_projects

    def clean(cleaning_project):
        return Project(identifier=cleaning_project.identifier, name=cleaning_project.name.strip(),
                       description=cleaning_project.description.strip())

    if check_ui:
        clean_new_projects = map(clean, new_projects)
        assert sorted(clean_new_projects, key=Project.id_or_max) == sorted(app.project.get_project_list(), key=Project.id_or_max)