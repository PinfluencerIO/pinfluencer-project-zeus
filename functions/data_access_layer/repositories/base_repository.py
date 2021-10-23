from sqlalchemy.orm import Session


class BaseRepository:
    _session: Session
    def __init__(self):
        self._session # TODO: Setup session here