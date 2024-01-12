# Monitoreo con Selenium y Device Farm

Programa hecho en python con Selenium e integrado con AWS Device Farm para el monitoreo funcional de [Mayta](https://mldev.antamina.com/mayta/). 

## Uso

```shell
pip3 install requirements.txt
python remote_testing.py
```

## Variables de entorno

| **Variable**           | **Definición**                                           |
|------------------------|----------------------------------------------------------|
| AWS_ACCESS_KEY_ID      | Access key de la cuenta de Amazon                        |
| AWS_SECRET_ACCESS_KEY  | Secret key de la cuenta de Amazon                        |
| ARN                    | ARN del proyecto de Device Farm                          |
| AWS_REGION_DEVICE_FARM | Region del proyecto de Device Farm                       |
| BUCKET_NAME            | Nombre del bucket donde se guardaran los logs            |
| BUCKET_FOLDER          | Ruta del folder del Bucket donde se guardaran los logs   |
| AZURE_URL              | Endpoint normalmente usado para Mayta                    |
| COGNITO_URL_DEV        | Endpoint creado especialmente para el usuario de Cognito |
| USER                   | Usuario registrado en AD                                 |
| PASSWORD               | Constraseña del usuario AD                               |
| COGNITO_USER           | Usuario creado en Cognito                                |
| COGNITO_PASSWORD       | Contraseña del usuario de Cognito                        |
| HISTORIAL_URL          | Enlace al historial de mensajes de Mayta.                |
| TABLEROS_URL           | Enlace al historial de tableros de Mayta.                |
| CROSS_ACCOUNT_AWS_ID   | ID de la cuenta que contiene el pipeline crossaccount    |


## PROCEDIMIENTO GLOBAL ------------------------------------------------------------

    #Ingreseo pagina CIA. Minera Antamina
    (click  SAP FIORI)



    --INGRESO A SAP 
    link directo a sap fiori
    espera 5 SEG
    click en boton continuar
    wait 8 seg

    --INGRESAR A PAGINA DE TRABAJO PRINCIPAL
    seleccionar lupita
    espera 2 
    seleccionar imput box
    ingresaar texto imput box (ME52N) y seleccionar O ENTER 
    ESPERA 5 
    Click en modificar solicitud de pedido box
    espera 5 seg


    --SELECCIONAR SOLICITUD DEL PEDIDO ADECUADA
    seleccionar Otra solicitud de pedido
    --se abre pop up
    Imput box ingresar solicitud de pedido numero (1300012545)
    clik en boton: Otro documento
    
    --PROCESO ITERACTIVO PARA MOSTRAR LAS POS.
    filtrar por Pos.solicitud pedido (--------------------procedimiento aparte)

    --ACTUALIZACION DE GCP  Y GURADADO
    seleccionar o buscar el GCP y cambiarlo por el GCP de la data (---------procedimiento aparte)
    seleccionar boton grabar

    --CONDICIONAL--
    IF (EL SIGUIENTE REGISTO TIENE EL MISMO ID): seleccionar nuevo filtro y seguir
    ELSE (): Regresar a paso de seleccion de solicitud y luego a flitrado 

    (CONDICIONAL= PROCESO ITERATIVO HASTA QUE SE ACABEN TODOS LOS REGISTROS)

 ##  --------------------------------------------------------------------------------------

