from src.data_access_layer.brand import Brand
from src.interfaces.data_manager_interface import DataManagerInterface


def load_by_id(id_, resource, data_manager: DataManagerInterface):
    try:
        return (data_manager.session
                .query(resource)
                .filter(resource.id == id_)
                .first())
    finally:
        data_manager.session.commit()


def load_brand_by_auth_id(id_, data_manager: DataManagerInterface):
    try:
        return (data_manager.session
                .query(Brand)
                .filter(Brand.auth_user_id == id_)
                .first())
    finally:
        data_manager.session.commit()
