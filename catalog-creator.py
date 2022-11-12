from jinja2 import Template, Environment, FileSystemLoader
import os, shutil
import logging
import glob
import pathlib


class Collection:
    def __init__(self, name:str):
        self.name = name

class Role:
    def __init__(self, name:str):
        self.name = name

#path where collections are
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
COLECTIONS_PATH=f'{BASE_DIR}/test'
TARGET_PATH=f'{BASE_DIR}/target'

#list of collections 
COLLECTIONS:list[Collection]=[
        Collection("core"), 
        Collection("networking"),
        Collection("security"),
        Collection("web")
    ]

#location of templates
FILE_LOADER = FileSystemLoader(BASE_DIR + '/catalog-templates')
ENV = Environment(loader=FILE_LOADER)

def main():
    logging.basicConfig(level=logging.INFO)


    clean_target_folder()
    create_users()
    create_groups()
    create_domain()

    logging.info('---------')
    logging.info('Create System catalog files')
    for col in COLLECTIONS:
        create_systems(col)

def clean_target_folder():
    logging.info('---------')
    logging.info('Cleaning target/ folder')
    for files in os.listdir(TARGET_PATH):
        path = os.path.join(TARGET_PATH, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

def create_domain():
    logging.info('---------')
    logging.info('Create Domain catalog file')
    os.system('cp catalog-templates/azurefactory-domain.yml ' + TARGET_PATH + '/azurefactory-domain.yml')

def create_groups():
    logging.info('---------')
    logging.info('Create Groups catalog file')
    os.system('cp catalog-templates/azurefactory-groups.yml ' + TARGET_PATH + '/azurefactory-groups.yml')

def create_users():
    logging.info('---------')
    logging.info('Create Users catalog file')
    os.system('cp catalog-templates/azurefactory-users.yml ' + TARGET_PATH + '/azurefactory-users.yml')

def create_systems(col:Collection):
    logging.info(f'Create System catalog file: {col.name}')
    template = ENV.get_template('system-catalog.j2')
    output = template.render(collection=col)

    f = open(f"{TARGET_PATH}/system-catalog-{col.name}.yml", "a")
    f.write(output)
    f.close()

    create_components(col)

def create_components(col:Collection):
    #find roles
    for role_full_path in get_roles_list(f'{COLECTIONS_PATH}/ubs-azurefactory-{col.name}/azurefactory/{col.name}/roles'):
        create_component_role(col, role_full_path)

def get_roles_list(roles_path:str) -> list[str]:
    roles:list[str]=[]
    for path in glob.glob(f'{roles_path}/*/'):
        roles.append(path)
    return roles

def create_component_role(col:Collection, role_full_path:str):
    role_dir = pathlib.PurePath(role_full_path)
    logging.info(f' - Create Role catalog file: {role_dir.name}')
    template = ENV.get_template('role-catalog.j2')
    output = template.render(collection=col, role=Role(role_dir.name))

    #TODO: this is not needed when playing with real roles
    create_folder_structure(f'{TARGET_PATH}/{role_dir}')

    f = open(f'{TARGET_PATH}/{role_dir}/catalog-info.yml', 'a')
    f.write(output)
    f.close()

def create_folder_structure(path:str): 
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(path)
main()