from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import os
import boto3

class DataManager:
    __session: Session
    def __init__(self):
        rds_host = os.environ.get("RDS_HOST")
        rds_port = os.environ.get("RDS_PORT")
        rds_username = os.environ.get("RDS_USER")
        temp_passwd = boto3.client('rds').generate_db_auth_token(
            DBHostname=rds_host,
            Port=rds_port,
            DBUsername=rds_username
        )
        rds_credentials = {'user': rds_username, 'passwd': temp_passwd}
        conn_str = f"postgres://pinfluencer-2.cluster-czqff0jhbhz3.eu-west-2.rds.amazonaws.com:5432/pinfluencer-1"
        kw = dict()
        kw.update(rds_credentials)
        engine = create_engine(conn_str, connect_args=kw)
        Session = sessionmaker(bind=engine)
        self.__session = Session()

    @property
    def session(self):
        return self.__session