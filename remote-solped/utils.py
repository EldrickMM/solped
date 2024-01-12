import os
import re
import boto3

import random
import time
import traceback
from os import path
from datetime import datetime

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium.common import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def save_page_html(driver, file_path):
    # Get the HTML source code of the current page
    html = driver.page_source

    # Save the HTML code to a file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html)


def cargar_envs():
    BASE_DIR = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(BASE_DIR, ".env"))


def save_screenshot(driver, file_path):
    # Take a screenshot of the current page
    driver.save_screenshot(file_path)


def check_and_click_button(driver, button_id):
    try:
        button = driver.find_element(By.CSS_SELECTOR, button_id)
        # Find the button element
        button = WebDriverWait(driver, timeout=3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, button_id)))
        # Click the button
        button.click()
        # print(f"Clicked the button with ID: {button_id}")
        return True
    except NoSuchElementException:
        # print(f"Button with ID {button_id} not found")
        return False

def check_and_click_button_by_class(driver, button_id):
    try:
        button = driver.find_element(By.CLASS_NAME, button_id)
        # Find the button element
        button = WebDriverWait(driver, timeout=3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, button_id)))
        # Click the button
        button.click()
        # print(f"Clicked the button with ID: {button_id}")
        return True
    except NoSuchElementException:
        # print(f"Button with ID {button_id} not found")
        return False

def check_and_click_button_by_id(driver, button_id):
    try:
        button = driver.find_element(By.ID, button_id)
        # Find the button element
        button = WebDriverWait(driver, timeout=3).until(
            EC.element_to_be_clickable((By.ID, button_id)))
        # Click the button
        button.click()
        # print(f"Clicked the button with ID: {button_id}")
        return True
    except NoSuchElementException:
        # print(f"Button with ID {button_id} not found")
        return False


def press_key(driver,area,key):
    campo_input = driver.find_element(By.CSS_SELECTOR, area)
    campo_input.send_keys(key)

def enter_value_and_wait(driver, value, element_id, timeout=3):
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_id)))
    element.clear()
    element.send_keys(value)
    time.sleep(2)


def enter_values_and_wait(driver, value, element_id, timeout=3):
    elements = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, element_id)))
    for element in elements:
        try:
            element.clear()
            element.send_keys(value)
            time.sleep(2)
        except ElementNotInteractableException:
            print("Elemento no interactivo")


def get_buttons_and_click(driver, element_id, timeout=3):
    elements = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, element_id)))
    for element in elements:
        try:
            element.click()
        except ElementNotInteractableException:
            print("Elemento no interactivo")


def click_first_inner_div(driver):
    # Find the first outer div
    outer_div = driver.find_element(By.CSS_SELECTOR, 'div.row.tile')

    # Find the first inner div within the outer div
    inner_div = WebDriverWait(outer_div, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.table'))
    )

    # Click the first inner div
    inner_div.click()


def guardar_pantalla(driver, nombre):
    time.sleep(3)
    save_page_html(driver, nombre + ".html")
    save_screenshot(driver, nombre + ".png")


def get_2fa_value(driver, div_id="idRichContext_DisplaySign"):
    # Find the div element by ID
    div_element = driver.find_element(By.ID, div_id)

    # Get the text value of the div element
    div_value = div_element.text

    return div_value


def get_items(driver, class_name="ant-menu-item"):
    # Find the div element by ID
    items = driver.find_elements(By.CLASS_NAME, class_name)

    return items


def combine_lists(keys, values):
    combined_dict = dict(zip(keys, values))
    return combined_dict


def extract_texts(driver):
    texts = []
    parent_divs = driver.find_elements(By.CSS_SELECTOR,
                                       '.ant-col.ant-col-xs-24.ant-col-sm-12.ant-col-md-12.ant-col-lg-8.ant-col-xl-6')

    for div in parent_divs:
        meta_title_div = div.find_element(By.CSS_SELECTOR, '.ant-card-meta-title')
        texts.append(meta_title_div.text)

    return texts


def log_values_to_file(values, title, formato=".log", mode="a"):
    filename = f"{title}{formato}"
    with open(filename, mode) as file:
        for value in values:
            file.write(str(value) + "\n")


def bajar_pantalla(driver, n_scrolls=2):
    import time
    for j in range(0, n_scrolls):
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, 800);")
        # Esperar a que cargue la página
        print(f"Bajando {j + 1} pantalla(s)")
        time.sleep(2)


def procesar_tabla(tabla):
    datos_tabla = []
    filas = tabla.find_elements(By.CSS_SELECTOR, "tr")
    if len(filas) == 0:
        return []
    for fila in filas:
        dato_tabla = ""
        # Se elimina el último dato porque es el de expansión
        datos_fila = fila.find_elements(By.CSS_SELECTOR, "td")[0:-1]
        if len(datos_fila) == 0:
            return []

        # print(f"La tabla tiene {len(datos_fila)} datos.")

        # Primer dato
        dato_tabla += datos_fila[0].find_element(By.CSS_SELECTOR, "span").text
        dato_tabla += ","

        # Segundo dato
        dato_tabla += validar_estado(datos_fila[1].find_elements(By.CSS_SELECTOR, "span")[1].text)
        dato_tabla += ","

        # Tercer dato
        dato_tabla += datos_fila[2].find_element(By.CSS_SELECTOR, "div").text
        dato_tabla += ","

        # Cuarto dato
        dato_tabla += datos_fila[3].find_element(By.CSS_SELECTOR, "div").text
        dato_tabla += ","

        # Quinto dato
        dato_tabla += datos_fila[4].find_element(By.CSS_SELECTOR, "div").text

        datos_tabla.append(dato_tabla)
    return datos_tabla


def validar_estado(texto):
    posibles_estados = ["APROBADO", "EN REVISIÓN", "RECHAZADO"]
    if str(texto).upper() in posibles_estados:
        return texto
    else:
        return ""


def click_element(driver, element, retries=3, delay=1):
    # Scroll to the top of the page to ensure the element is visible
    driver.execute_script("window.scrollTo(0, 0)")

    for _ in range(retries):
        try:
            element.click()
            return
        except Exception:
            time.sleep(delay)
    raise Exception("Failed to click the element after multiple attempts")


def select_random_elements(lst, n):
    if n >= len(lst):
        return lst
    else:
        return random.sample(lst, n)


def delete_blank_lines(text):
    """
    Deletes new blank lines from a text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with new blank lines removed.
    """
    lines = text.splitlines()
    non_blank_lines = [line for line in lines if line.strip()]
    result = '\n'.join(non_blank_lines)
    return result


def extract_text_from_html(html):
    """
    Extracts the text content from an HTML element.

    Args:
        html (str): The HTML element as a string.

    Returns:
        str: The extracted text content.
    """
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=' ')
    return text.strip()


def keep_first_n_lines(text, n):
    """
    Keeps only the first "n" lines of a text.

    Args:
        text (str): The input text.
        n (int): The number of lines to keep.

    Returns:
        str: The text with only the first "n" lines.
    """
    lines = text.splitlines()
    first_n_lines = lines[:n]
    result = '\n'.join(first_n_lines)
    return result


def select_random_elements_dict(dictionary, n):
    """
    Randomly selects "n" elements from a dictionary and returns a new dictionary.

    Args:
        dictionary (dict): The input dictionary.
        n (int): The number of elements to select.

    Returns:
        dict: A new dictionary with randomly selected elements.
    """
    keys = random.sample(list(dictionary.keys()), n)
    selected_elements = {key: dictionary[key] for key in keys}
    return selected_elements


def flatten_list(nested_list):
    flattened = []
    for sublist in nested_list:
        flattened.extend(sublist)
    return flattened


def find_element_with_timeout(driver, css_selector, timeout, fallback):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        return True, element
    except NoSuchElementException:
        return False, fallback
    except TimeoutError:
        return False, fallback
    except TimeoutException:
        return False, fallback
    except Exception:
        return False, fallback


def open_link_in_new_tab(driver, element, retries=3, delay=1):
    # Create an instance of ActionChains
    actions = ActionChains(driver)

    for _ in range(retries):
        try:
            # Perform key press action to open link in a new tab
            print("Haciendo ctrl + click")
            actions.key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL).perform()

            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[-1])
            return
        except Exception:
            time.sleep(delay)
    raise Exception("Failed to click the element after multiple attempts")


from selenium.common.exceptions import NoSuchWindowException


def click_tablero_and_log_text(driver, numero_tablero, tableros, file):
    funciona_iframe = False
    continue_searching = True
    while continue_searching:
        try:
            tableros_cards = driver.find_elements(By.CSS_SELECTOR, ".ant-card.ant-card-bordered.ant-card-hoverable")
            print(f"Ingresando al tablero: {tableros[numero_tablero]}")
            print(f"Ingresando al tablero: {numero_tablero}")
            print(f"Cantidad de tableros: {len(tableros_cards)}")
            print(f"Cantidad de tableros: {len(tableros)}")

            tableros_cards[numero_tablero].click()
            continue_searching = False
            # Esperando 20 segundos para que cargue
            time.sleep(20)
            text = [f"Tablero: {tableros[numero_tablero]}"]

            # Switch to the iframe by its index (zero-based)
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(iframe)

            # Perform operations inside the iframe
            html_code = driver.find_element(By.ID, "dashboard-spacer").get_attribute("innerHTML")
            for line in keep_first_n_lines(delete_blank_lines(extract_text_from_html(html_code)), 3).splitlines():
                text.append(line)
            print(text)
            funciona_iframe = True

            # Switch back to the default content (outside the iframe)
            driver.switch_to.default_content()
            time.sleep(1)

        except NoSuchWindowException:
            # Handle the NoSuchWindowException by reloading or reinitializing the browser
            print("Browser window was closed or context discarded. Reloading...")
            driver.get(os.getenv("TABLEROS_URL"))
            # Perform necessary setup (e.g., navigate to the desired page, authenticate, etc.)

        except IndexError as e:
            traceback.print_exc()
            print(f"An error occurred: {str(e)}")
            print("Error por index")
            continue
        except Exception as e:
            continue_searching = False
            print(f"An error occurred: {str(e)}")
            text.append("El tablero no cargó")
            funciona_iframe = False

    log_values_to_file(text, file)
    driver.get(os.getenv('TABLEROS_URL'))
    print("Volviendo a la página de tableros")
    time.sleep(10)
    return funciona_iframe


def get_current_timestamp():
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S_%f")[:-3]
    return timestamp


def generate_random_numbers(n, m):
    numbers = []
    for _ in range(n):
        num = random.randint(0, m)
        numbers.append(num)
    return numbers


def upload_file_to_s3(bucket_name, bucket_folder, file_path, object_name, filetype=".log"):
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Upload the file to the S3 bucket
    try:
        folder_path = bucket_folder.strip("/") + "/"
        s3_object_name = folder_path + object_name + filetype
        s3_client.upload_file(f"{file_path}{filetype}", bucket_name, s3_object_name)
        print(f"File uploaded successfully to S3 bucket: {bucket_name}/{s3_object_name}")

        # Delete the local file after successful upload
        os.remove(f"{file_path}{filetype}")
        print(f"Local file deleted: {file_path}{filetype}")
        return s3_object_name
    except Exception as e:
        print(f"Error uploading file to S3 bucket: {e}")
        return "No se pudo subir el archivo generado"


def generate_unique_numbers(n, m):
    if n > m + 1:
        raise ValueError("The range is not large enough to generate unique numbers.")
    numbers = random.sample(range(m + 1), n)
    return numbers


def get_number_from_text(text):
    return text


def get_message(driver, class_name):
    alert_or_info = driver.find_element(By.CLASS_NAME, class_name)
    return alert_or_info.text


def extract_number(string):
    pattern = r'\d+'  # Regular expression pattern to match one or more digits
    matches = re.findall(pattern, string)
    if matches:
        return int(matches[0])  # Convert the first matched number to an integer
    else:
        return None  # Return None if no number is found


def count_boolean_values(array, value):
    count = 0
    for item in array:
        if item == value:
            count += 1
    return count


def compare_options(opcion_recomendaciones, opciones_disponibles, index):
    return str(opcion_recomendaciones).strip().upper() == opciones_disponibles[index]


def read_file_contents(file_path):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
        return contents
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except IOError:
        print(f"An error occurred while reading the file '{file_path}'.")

    return None


def evaluate_and_return(first_param, default_value):
    if first_param and first_param.strip():  # Check if first_param is not empty or None
        return first_param
    else:
        return default_value

def get_peru_timestamp():
    # Get the current UTC time
    utc_now = datetime.utcnow()

    # Set the timezone to "America/Lima" (Peru Time)
    peru_tz = pytz.timezone('America/Lima')
    peru_time = utc_now.replace(tzinfo=pytz.utc).astimezone(peru_tz)

    return peru_time.strftime('%Y-%m-%d %I:%M:%S %p')