from src.pinfluencer_response import PinfluencerResponse


class ProcessOkResponse:

    def do_process(self, event):
        return PinfluencerResponse(200, f'Ok')
