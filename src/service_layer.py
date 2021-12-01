from src.interfaces.data_manager_interface import DataManagerInterface


def load_by_id(id_, resource, data_manager: DataManagerInterface):
    try:
        return (data_manager.session
                .query(resource)
                .filter(resource.id == id_)
                .first())
    finally:
        data_manager.session.commit()
