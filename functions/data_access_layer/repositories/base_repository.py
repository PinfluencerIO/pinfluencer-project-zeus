from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self):
        self.session: Session