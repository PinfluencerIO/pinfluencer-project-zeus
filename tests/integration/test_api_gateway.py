import os
from unittest import TestCase

import boto3
import requests

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test. 
"""


class TestApiGateway(TestCase):
    brands_endpoint: str

    @classmethod
    def get_stack_name(cls) -> str:
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")
        print(f"!!!!!!!{stack_name}")
        if not stack_name:
            raise Exception(
                "Cannot find env var AWS_SAM_STACK_NAME. \n"
                "Please setup this environment variable with the stack name where we are running integration tests."
            )

        return stack_name

    def setUp(self) -> None:
        """
        Based on the provided env variable AWS_SAM_STACK_NAME,
        here we use cloudformation API to find out what the HelloWorldApi URL is
        """
        stack_name = TestApiGateway.get_stack_name()

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name}. \n" f'Please make sure stack with the name "{stack_name}" exists.'
            ) from e

        stacks = response["Stacks"]

        stack_outputs = stacks[0]["Outputs"]
        get_all_brands_output = [output for output in stack_outputs if output["OutputKey"] == "PinfluencerGetAllBrands"]
        self.assertTrue(get_all_brands_output, f"Cannot find output PinfluencerGetAllBrands in stack {stack_name}")

        self.brands_endpoint = get_all_brands_output[0]["OutputValue"]

    def test_get_brands(self):
        response = requests.get(self.brands_endpoint)
        self.assertEquals(response.status_code, 200)

    def test_post_requires_auth(self):
        response = requests.post(self.brands_endpoint,  json={})
        self.assertEquals(response.status_code, 401)