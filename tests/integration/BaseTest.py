import os, boto3, requests
from unittest import TestCase

class BaseTest(TestCase):
    api_endpoint: str

    def stack(self): 
        pass

    def endpoint(self):
        pass

    def setUp(self) -> None:
        """
        Based on the provided env variable AWS_SAM_STACK_NAME,
        here we use cloudformation API to find out what the HelloWorldApi URL is
        """
        
        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=self.stack())
        except Exception as e:
            raise Exception(
                f"Cannot find stack {self.stack()}. \n" f'Please make sure stack with the name "{self.stack()}" exists.'
            ) from e

        stacks = response["Stacks"]

        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == self.endpoint()]
        self.assertTrue(api_outputs, f"Cannot find output APi in stack {self.stack()}")

        self.api_endpoint = api_outputs[0]["OutputValue"]
    