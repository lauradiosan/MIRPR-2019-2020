from dependency_injector import containers
import yaml


class Configs(containers.DeclarativeContainer):
    # Loading yaml file
    config_file = open('properties.yaml')
    loader = yaml.load(config_file, Loader=yaml.FullLoader)

    # Getting properties from yaml file
    host_ip = loader.get('host-ip')
    host_port = loader.get('host-port')
