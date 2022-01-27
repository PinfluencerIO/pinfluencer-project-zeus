from src.pinfluencer_response import PinfluencerResponse


class GetAllMyCampaigns:
    def __init__(self) -> None:
        super().__init__()

    def do_process(self, event):
        return PinfluencerResponse(200, f'Ok')
