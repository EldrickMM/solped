# import pandas as pd

# def leer_y_formatear_excel(nombre_archivo):
#     # Leer el archivo Excel
#     df = pd.read_excel(nombre_archivo)

#     # Seleccionar las columnas deseadas
#     columnas_deseadas = ['Grupo de compras', 'Solicitud de pedido', 'Pos.solicitud pedido']
#     df_seleccionado = df[columnas_deseadas]

#     # Convertir los datos a un diccionario JSON
#     json_resultante = df_seleccionado.to_dict(orient='records')

#     return json_resultante

# # Nombre del archivo Excel en la misma carpeta
# nombre_archivo_excel = 'EXPORT.xlsx'

# # Obtener los datos formateados
# json_resultante = leer_y_formatear_excel(nombre_archivo_excel)

# # Imprimir los resultados
# print("JSON resultante:")
# print(json_resultante)

#test con cantidad de registro: 
import pandas as pd

def leer_y_formatear_csv(nombre_archivo, num_registros=10):
    # Leer el archivo CSV con encoding 'latin-1' y delimitador ';'
    df = pd.read_csv(nombre_archivo, encoding='latin-1', delimiter=';')

    # Seleccionar las columnas deseadas
    columnas_deseadas = ['Grupo de compras', 'Solicitud de pedido', 'Pos.solicitud pedido']
    df_seleccionado = df[columnas_deseadas]

    # Limitar a los primeros 10 registros
    df_seleccionado = df_seleccionado.head(num_registros)

    # Convertir los datos a un diccionario JSON
    json_resultante = df_seleccionado.to_dict(orient='records')

    return json_resultante

# Nombre del archivo CSV en la misma carpeta
nombre_archivo_csv = 'EXPORT.csv'

# Obtener los primeros 10 registros formateados
json_resultante = leer_y_formatear_csv(nombre_archivo_csv, num_registros=10)

# Imprimir los resultados
print("JSON resultante:")
print(json_resultante)

#resultado de funcion:
# [
#   {
#     "Grupo de compras": "JB2",
#     "Solicitud de pedido": 1000000022,
#     "Pos.solicitud pedido": 30
#   },
#   {
#     "Grupo de compras": "C01",
#     "Solicitud de pedido": 1000000023,
#     "Pos.solicitud pedido": 20
#   },
#   {
#     "Grupo de compras": "C01",
#     "Solicitud de pedido": 1000000023,
#     "Pos.solicitud pedido": 30
#   },
#   {
#     "Grupo de compras": "JB2",
#     "Solicitud de pedido": 1000000023,
#     "Pos.solicitud pedido": 40
#   },
#   {
#     "Grupo de compras": "C02",
#     "Solicitud de pedido": 1000000023,
#     "Pos.solicitud pedido": 70
#   },
#   {
#     "Grupo de compras": "C01",
#     "Solicitud de pedido": 1000000023,
#     "Pos.solicitud pedido": 90
#   },
#   {
#     "Grupo de compras": "C02",
#     "Solicitud de pedido": 1000000023,
#     "Pos.solicitud pedido": 100
#   },
#   {
#     "Grupo de compras": "C01",
#     "Solicitud de pedido": 1000000023,
#     "Pos.solicitud pedido": 140
#   },
#   {
#     "Grupo de compras": "C01",
#     "Solicitud de pedido": 1000000023,
#     "Pos.solicitud pedido": 150
#   },
#   {
#     "Grupo de compras": "JB2",
#     "Solicitud de pedido": 1000000023,
#     "Pos.solicitud pedido": 160
#   }
# ]