from selenium import webdriver

from flow import general_flow
from flow_solped import flow_solped
# from flow_w2 import general_flow_w2
from utils import cargar_envs
from os import getenv


def test_local(url, driver_path="C:/Work/Antamina/remote-solped/chromedriver-win64/chromedriver-win64/chromedriver.exe", idp="AZURE"):
    cargar_envs()
    driver = webdriver.Chrome(driver_path)
    # return general_flow_w2(driver, url, idp=idp)
    return general_flow(driver, url, idp=idp)


def test_local_solped():
    driver_path="C:/Work/Antamina/remote-solped/chromedriver-win64/chromedriver-win64/chromedriver.exe"
    cargar_envs()
    driver = webdriver.Chrome(driver_path)
    url="https://www.google.com.pe/?hl=es"
    # return general_flow_w2(driver, url, idp=idp)
    return flow_solped(driver, url)



if __name__ == '__main__':
    cargar_envs()
    # test_local(getenv("AZURE_URL"), idp="COGNITO")
    test_local_solped()
    
    # test_local(getenv("AZURE_URL"), idp="AZURE")
