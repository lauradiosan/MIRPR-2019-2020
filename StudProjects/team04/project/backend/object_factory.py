from dependency_injector import providers, containers
from flask import Flask
from flask_socketio import SocketIO
from sqlalchemy import create_engine
from backend.configs import Configs
from backend.db_access import DbAccess
from backend.rest_controller import RestController
from backend.socket_controller import SocketController
from backend.ANN_controller import ANNController


class ObjectFactory(containers.DeclarativeContainer):
    app = providers.Singleton(Flask, import_name=__name__)
    socket_io = providers.Singleton(SocketIO, app=app)
    db_engine = create_engine(f'sqlite:///{Configs.db_file_name}')
    db_access = providers.Singleton(DbAccess, db_engine)
    rest_controller = providers.Singleton(RestController, db_access=db_access)
    socket_controller = providers.Singleton(SocketController, socket_io=socket_io, db_access=db_access)
    ann_controller = providers.Singleton(ANNController, db_access=db_access)
