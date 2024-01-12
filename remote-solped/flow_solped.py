import time
from os import getenv

from flows.authentication.login import login_AD, login_cognito
from flows.pages.recomendaciones import procesar_pantalla_recomendaciones
from flows.pages.tableros import procesar_pantalla_tableros
from utils import *


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def flow_solped(driver, url, remoto=False, idp="AZURE", pantalla=False, timeout_seconds=60):
    

    
    
    #TODO: INGRESO A SAP--------------------------------------------------------------------
    print("INGRESO A SAP")


    driver.get(url)
    driver.maximize_window()

    print("Esperando a que cargue la página")
    time.sleep(5) #! revisar SI tiempo de carga en directo es eficiente
    # check_and_click_button(driver, ".gNO89b")
    check_and_click_button_by_class(driver, "gNO89b") #!clase del boton continuar
    time.sleep(5)




    #TODO: INGRESAR A PAGINA DE TRABAJO PRINCIPAL-------------------------------------------
    print("INGRESAR A PAGINA DE TRABAJO PRINCIPAL")


    # check_and_click_button(driver, "#searchFieldInShell-button-img")
    check_and_click_button_by_id(driver, "#searchFieldInShell-button-img")#!clase del boton lupa
    time.sleep(1)

    enter_value_and_wait(driver, "me52n", "#searchFieldInShell-input-inner") #!data + id de imput   IMPÓRTNATE LOGICA DE DATOS
    press_key(driver,"#searchFieldInShell-input-inner",Keys.ENTER)
    #?en caso no sirva el enter poner ner funcion click en lupa 
    time.sleep(5)

    check_and_click_button_by_id(driver, "#__tile374-subHdr-text")#!clase del card ESTA CON LA DEL TITLE DEL CARD -----FALTAAA xxxxxxxxxxxxxxxx
    time.sleep(5)



    #TODO: SELECCIONAR SOLICITUD DEL PEDIDO ADECUADA----------------------------------------(for)
    print("SELECCIONAR SOLICITUD DEL PEDIDO ADECUADA")

    check_and_click_button_by_id(driver, "#M0:48:::btn[17]-cnt")#?(revision) id o clase del (seleccionar Otra solicitud de pedido) 
    time.sleep(1)
    #aparece pop up
    #seleccionar input box
    enter_value_and_wait(driver, "1300011162", "#M1:46:1::0:21")  #!data + id de imput   IMPÓRTNATE LOGICA DE DATOS
    time.sleep(1)
    #seleccionar OTRO DOCUMENTO
    check_and_click_button_by_id(driver, "#M1:50::btn[0]-cnt")#!id de box

    #TODO: PROCESO ITERACTIVO PARA MOSTRAR LAS POS.----------------------------------------(if)
    print("PROCESO ITERACTIVO PARA MOSTRAR LAS POS.")

    check_and_click_button_by_id(driver, "#")#!id de botton fijar filtro POS -----------FALTAAA xxxxxxxxxxxxxxxx
    time.sleep(1)
    enter_value_and_wait(driver, "10", "#")#!data + id de imput   IMPÓRTNATE LOGICA DE DATOS  -----------FALTAAA xxxxxxxxxxxxxxxx
    time.sleep(1)
    check_and_click_button_by_id(driver, "#")#!id de botton Check -----------FALTAAA xxxxxxxxxxxxxxxx
    time.sleep(1)

    #TODO: ACTUALIZACION DE GCP  Y GURADADO-----------------------------------------------
    

    enter_value_and_wait(driver, "C01", "#")  #!data + id de imput box + Revision si el id cambia    
    time.sleep(1)





    #?--boton grabar general
    check_and_click_button_by_id(driver, "#M0:50::btn[11]-cnt")#!id de boton grabar general


    # #!test---------------------------
    # enter_value_and_wait(driver, "holaaa como estas", "#APjFqb") #---------------test
    # time.sleep(2)
    # campo_input = driver.find_element(By.CSS_SELECTOR, "#APjFqb")
    # campo_input.send_keys(Keys.ENTER)
    # print("paso")
    # time.sleep(2)
    # # Cierra el navegador

    
    driver.quit()





    # enter_value_and_wait(driver, "holaaa como estas", "#APjFqb") #---------------test
    # enter_value_and_wait(driver, "holaaa como estas", "Continuar") 

    return "final"
