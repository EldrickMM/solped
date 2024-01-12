from os import getenv

from flow import general_flow
from utils import cargar_envs

import boto3

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Remote


# in your tests:
# Set up the Device Farm client, get a driver URL:
class TestSuite:
    def __init__(self):
        self.driver = None

    def setup_method(self):
        devicefarm_client = boto3.client("devicefarm", region_name=getenv("AWS_REGION_DEVICE_FARM"))
        testgrid_url_response = devicefarm_client.create_test_grid_url(
            projectArn=getenv("ARN"),
            expiresInSeconds=1000)
        print(testgrid_url_response)
        self.driver = Remote(testgrid_url_response["url"],
                             DesiredCapabilities.FIREFOX)

    # later, make sure to end your WebDriver session:
    def teardown_method(self):
        self.driver.quit()


def test_remoto(url="https://mldev.antamina.com/mayta/", idp="AZURE"):
    cargar_envs()
    print(url)
    suite = TestSuite()
    suite.setup_method()
    driver = suite.driver
    return general_flow(driver, url, remoto=True, idp=idp)


def init_test_remoto():
    cargar_envs()
    return test_remoto(getenv("AZURE_URL"), idp="COGNITO")


if __name__ == '__main__':
    init_test_remoto()
    # test_remoto(getenv("AZURE_URL"), idp="AZURE")
