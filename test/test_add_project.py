from model.project import Project


def test_add_project(app, json_project, check_ui, config):
    project = json_project
    old_projects = app.soap.get_project_list(username=config['web']["username"], password=config['web']["password"])
    app.project.create(project)
    new_projects = app.soap.get_project_list(username=config['web']["username"], password=config['web']["password"])
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
    if check_ui:
        assert sorted(new_projects, key=Project.id_or_max) == sorted(app.project.get_project_list(), key=Project.id_or_max)

    def clean(cleaning_project):
        return Project(identifier=cleaning_project.identifier, name=cleaning_project.name.strip(),
                       description=cleaning_project.description.strip())
    if check_ui:
        clean_new_projects = map(clean, new_projects)
        assert sorted(clean_new_projects, key=Project.id_or_max) == sorted(app.project.get_project_list(),
                                                                           key=Project.id_or_max)
