import pandas as pd
import random
from colorama import Fore, Style

# Constantes
NUMERO_DE_DATOS = 30  # Cantidad de filas de datos ficticios que generaremos
COLOR_SUBTITULO = Fore.YELLOW  # Color para imprimir subtítulos
COLOR_DESTACADO = Fore.CYAN  # Color para imprimir texto destacado
REINICIAR_COLOR = Style.RESET_ALL  # Código para reiniciar el color del texto

# Función para imprimir subtítulos con color
def imprimir_subtitulo(texto, color=COLOR_SUBTITULO):
    print(color + texto + REINICIAR_COLOR)  # Imprimimos el texto con el color especificado y luego reseteamos el color

# Función para crear un conjunto de datos ficticio
def crear_conjunto_de_datos(n=NUMERO_DE_DATOS):
    datos = {
        'pañales': [random.choice([True, False]) for _ in range(n)],
        'leche': [random.choice([True, False]) for _ in range(n)],
        'biberones': [random.choice([True, False]) for _ in range(n)],
        'cerveza': [random.choice([True, False]) for _ in range(n)]
    }
    return pd.DataFrame(datos)  # Convertimos el diccionario en un DataFrame de pandas y lo retornamos

# Función para calcular reglas basadas en confianza y soporte
def calcular_reglas(df, columnas):
    reglas = []  # Lista para almacenar las reglas generadas
    for col in columnas:  # Iteramos sobre cada columna especificada
        for val in [True, False]:  # Iteramos sobre los posibles valores booleanos
            condicion = df[col] == val  # Creamos una serie de condiciones booleanas
            if len(df[condicion]) == 0:  # Si no hay filas que cumplan la condición, continuamos con la siguiente iteración
                continue

            # Calculamos la confianza y el soporte de la regla
            cuenta_condicion_y_cerveza = len(df[condicion & (df['cerveza'] == True)])  # Contamos las filas que cumplen la condición y tienen cerveza
            confianza = cuenta_condicion_y_cerveza / len(df[condicion])  # Calculamos la confianza
            soporte = cuenta_condicion_y_cerveza / len(df)  # Calculamos el soporte
            reglas.append(((col, val), confianza, soporte))  # Añadimos la regla a la lista

    # Ordenamos las reglas por confianza y soporte de forma descendente y retornamos la lista
    return sorted(reglas, key=lambda x: (-x[1], -x[2]))

# Función para imprimir las reglas generadas
def imprimir_reglas(reglas):
    for r in reglas:  # Iteramos sobre cada regla
        condicion = f"{r[0][0]}={r[0][1]}"  # Formateamos la condición de la regla
        # Imprimimos la regla con su confianza y soporte
        print(f"SI {condicion} ENTONCES cerveza=Sí -> Confianza = {r[1]:.2f} | Soporte = {r[2]:.2f}")

# Función principal para ejecutar el análisis
def prism(df):
    numero_de_iteracion = 0  # Contador para las iteraciones
    columnas_a_analizar = list(df.columns[:-1])  # Obtenemos las columnas a analizar excluyendo la última ('cerveza')
    reglas_seleccionadas = []  # Lista para almacenar las reglas seleccionadas

    while not df.empty:  # Mientras el conjunto de datos no esté vacío
        numero_de_iteracion += 1  # Aumentamos el contador de iteraciones
        imprimir_subtitulo(f"\n\nITERACIÓN {numero_de_iteracion}:")  # Imprimimos el número de iteración

        reglas = calcular_reglas(df, columnas_a_analizar)  # Calculamos las reglas para las columnas actuales
        if not reglas:  # Si no hay reglas, salimos del bucle
            break

        imprimir_reglas(reglas)  # Imprimimos las reglas generadas

        regla_seleccionada = reglas[0]  # Seleccionamos la primera regla (la de mayor confianza y soporte)
        reglas_seleccionadas.append(f"{regla_seleccionada[0][0]}={regla_seleccionada[0][1]}")  # Añadimos la regla a la lista de seleccionadas
        columnas_a_analizar.remove(regla_seleccionada[0][0])  # Removemos la columna de la regla seleccionada de la lista de columnas a analizar

        # Imprimimos la regla seleccionada con su confianza y soporte
        imprimir_subtitulo(f"\nRegla seleccionada para la iteración {numero_de_iteracion}:", color=COLOR_DESTACADO)
        texto_condicion = f"{regla_seleccionada[0][0]}={regla_seleccionada[0][1]}"
        print(f"SI {texto_condicion} ENTONCES cerveza=Sí -> Confianza = {regla_seleccionada[1]:.2f} | Soporte = {regla_seleccionada[2]:.2f}")

        df = df[df[regla_seleccionada[0][0]] == regla_seleccionada[0][1]]  # Filtramos el conjunto de datos según la regla seleccionada
        imprimir_subtitulo("\nConjunto de datos reducido:", color=COLOR_DESTACADO)  # Imprimimos el conjunto de datos reducido
        print(df)

    # Al finalizar, imprimimos las reglas seleccionadas
    imprimir_subtitulo("\n\nREGLAS SELECCIONADAS:", color=COLOR_DESTACADO)
    print(" Y ".join(reglas_seleccionadas) + " ENTONCES cerveza=true\n")

# Bloque principal de ejecución
# Bloque principal de ejecución
if __name__ == "__main__":
    conjunto_de_datos = crear_conjunto_de_datos()
    imprimir_subtitulo("CONJUNTO DE DATOS ORIGINAL:")
    print(conjunto_de_datos)
    prism(conjunto_de_datos)