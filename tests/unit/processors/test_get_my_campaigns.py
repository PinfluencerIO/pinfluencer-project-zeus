from src.processors.get_all_campaigns import GetAllMyCampaigns


def test_do_process_get_collection():
    processor = GetAllMyCampaigns()
    response = processor.do_process({})
    assert response.is_ok() is True
    assert response.status_code == 200
