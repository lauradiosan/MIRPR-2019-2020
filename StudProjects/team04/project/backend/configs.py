from dependency_injector import containers
import yaml


class Configs(containers.DeclarativeContainer):
    # Loading yaml file
    config_file = open('properties.yaml')
    loader = yaml.load(config_file, Loader=yaml.FullLoader)

    # Getting properties from yaml file
    server_ip = loader.get('server-ip')
    port = loader.get('server-port')
    db_file_name = loader.get('db-file-name')
