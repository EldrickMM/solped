import time
from os import getenv

from selenium.common import StaleElementReferenceException

from utils import *


def login_AD(driver, remoto, pantalla=False):
    print("Ingresando el username")
    enter_value_and_wait(driver, getenv('USER'), "#i0116")
    check_and_click_button(driver, "#idSIButton9")

    # Retry if StaleElementReferenceException occurs
    retry_count = 0
    while retry_count < 3:
        try:
            print("Ingresando el password")
            enter_value_and_wait(driver, getenv('PASSWORD'), "#i0118")

            print("Iniciando sesión")
            check_and_click_button(driver, "#idSIButton9")
            break  # Exit the loop if no exception occurs
        except StaleElementReferenceException:
            # Increment the retry count and wait for a short time before trying again
            retry_count += 1
            time.sleep(1)
    else:
        # Handle the case where retries have been exhausted without success
        print("Failed to click the Next button after multiple retries.")

    if pantalla:
        print("Guardando pantalla - ./Pantallas/1-MFA")
        guardar_pantalla(driver, "./Pantallas/1-MFA")

    try:
        time.sleep(2)
        print("Por favor, valide 2FA")
        two_fa_code = get_2fa_value(driver)
        print("Ingresar el siguiente código en Microsoft Authentication App")
        print(two_fa_code)

        # Haciendo click en el "Remember me"
        print('Haciendo click en el "Remember me"')
        check_and_click_button(driver, "#idChkBx_SAOTCAS_TD")
        return True
    except Exception as e:
        print("No se encontró le código, puede que sea un acceso anómalo")

    waiting_time = 20
    if remoto:
        waiting_time = 15
    time.sleep(waiting_time)

    if check_and_click_button(driver, "#idSIButton9"):
        print("Verificando acceso anómalo")
        if pantalla:
            print("Guardando pantalla - ./Pantallas/2-Verificacion")
            guardar_pantalla(driver, "./Pantallas/2-Verificacion")

        click_first_inner_div(driver)

        if pantalla:
            print("Guardando pantalla - ./Pantallas/3-MFA")
            guardar_pantalla(driver, "./Pantallas/3-MFA")

        two_fa_code = get_2fa_value(driver)

        # Haciendo click en el "Remember me"
        check_and_click_button(driver, "#idChkBx_SAOTCAS_TD")

        print("Ingresar el siguiente código en Microsoft Authentication App")
        print(two_fa_code)

        return True

    return False


def login_cognito(driver, url,pantalla=False):
    driver.get(url)
    enter_values_and_wait(driver, getenv('COGNITO_USER'), "#signInFormUsername")
    enter_values_and_wait(driver, getenv('COGNITO_PASSWORD'), "#signInFormPassword")
    if pantalla:
        print("Guardando pantalla - ./Pantallas/1-COGNITO")
        guardar_pantalla(driver, "./Pantallas/1-COGNITO")

    get_buttons_and_click(driver, '[name="signInSubmitButton"]', timeout=3)
    print("Iniciando sesión")
    time.sleep(3)


def set_local_storage(driver, data):
    # Iterate over the key-value pairs in the data dictionary
    for key, value in data.items():
        # Execute JavaScript to insert the key-value pair into localStorage
        script = f"localStorage.setItem('{key}', '{value}');"
        driver.execute_script(script)
