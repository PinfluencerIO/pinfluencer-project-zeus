from src.pinfluencer_response import PinfluencerResponse


class ProcessOkResponse:

    def do_process(self):
        return PinfluencerResponse(200, f'Ok')
