import requests
from tests.integration.BaseTest import BaseTest

AWS_SAM_STACK_NAME = "pinflencer-backend-stack"
API_ENDPOINT_OUTPUT_NAME = "ApiGetBrands"


class TestApiGateway(BaseTest):
    def stack(self):
        return AWS_SAM_STACK_NAME

    def endpoint(self):
        return API_ENDPOINT_OUTPUT_NAME

    def test_api_gateway(self):
        """
        Call the API Gateway endpoint and check the response
        """
        response = requests.get(self.api_endpoint)
        # self.assertDictEqual(response.json(), {"message": "hello brand get"})
        # no test at this stage, this is a placehold test
