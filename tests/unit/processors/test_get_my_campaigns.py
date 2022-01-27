import json
import os

from _pytest.fixtures import fixture

from src.processors.campaign.get_all_campaigns import ProcessGetAllMyCampaigns
from tests import StubDataManager

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

my_data_path = os.path.join(THIS_DIR, os.pardir, '../../events/')


@fixture
def event():
    with open(my_data_path + 'get_campaigns_event_with_auth.json') as f:
        data = json.load(f)
    return data


def fake_db_layer(user, data_manager):
    assert user == "google_106146319509880568839"
    return []


def test_processor_calls_db(event):
    processor = ProcessGetAllMyCampaigns(StubDataManager(), fake_db_layer)
    result = processor.do_process(event)
    assert result.status_code == 200
    assert result.body == []
