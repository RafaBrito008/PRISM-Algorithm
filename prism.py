import pandas as pd
import random
from colorama import Fore, Style

# Configurar constantes
NUMERO_DE_DATOS = 30
COLOR_SUBTITULO = Fore.YELLOW
COLOR_DESTACADO = Fore.CYAN
REINICIAR_COLOR = Style.RESET_ALL

def imprimir_subtitulo(texto, color=COLOR_SUBTITULO):
    """Imprime un texto como subtítulo con el color especificado."""
    print(color + texto + REINICIAR_COLOR)

def crear_conjunto_de_datos(n=NUMERO_DE_DATOS):
    """Crea un conjunto de datos ficticio con 'n' filas."""
    datos = {
        'pañales': [random.choice([True, False]) for _ in range(n)],
        'leche': [random.choice([True, False]) for _ in range(n)],
        'biberones': [random.choice([True, False]) for _ in range(n)],
        'cerveza': [random.choice([True, False]) for _ in range(n)]
    }
    return pd.DataFrame(datos)

def calcular_reglas(df, columnas):
    """Calcula las reglas basadas en la confianza y el soporte."""
    reglas = []
    for col in columnas:
        for val in [True, False]:
            condicion = df[col] == val
            if len(df[condicion]) == 0:
                continue

            cuenta_condicion_y_cerveza = len(df[condicion & (df['cerveza'] == True)])
            confianza = cuenta_condicion_y_cerveza / len(df[condicion])
            soporte = cuenta_condicion_y_cerveza / len(df)
            reglas.append(((col, val), confianza, soporte))
    return sorted(reglas, key=lambda x: (-x[1], -x[2]))

def imprimir_reglas(reglas):
    """Imprime las reglas en el formato deseado."""
    for r in reglas:
        condicion = f"{r[0][0]}={r[0][1]}"
        print(f"SI {condicion} ENTONCES cerveza=Sí -> Confianza = {r[1]:.2f} | Soporte = {r[2]:.2f}")

def ejecutar_analisis(df):
    numero_de_iteracion = 0
    columnas_a_analizar = list(df.columns[:-1])
    reglas_seleccionadas = []

    while not df.empty:
        numero_de_iteracion += 1
        imprimir_subtitulo(f"\n\nITERACIÓN {numero_de_iteracion}:")

        reglas = calcular_reglas(df, columnas_a_analizar)
        if not reglas:
            break

        imprimir_reglas(reglas)

        regla_seleccionada = reglas[0]
        reglas_seleccionadas.append(f"{regla_seleccionada[0][0]}={regla_seleccionada[0][1]}")
        columnas_a_analizar.remove(regla_seleccionada[0][0])

        imprimir_subtitulo(f"\nRegla seleccionada para la iteración {numero_de_iteracion}:", color=COLOR_DESTACADO)
        texto_condicion = f"{regla_seleccionada[0][0]}={regla_seleccionada[0][1]}"
        print(f"SI {texto_condicion} ENTONCES cerveza=Sí -> Confianza = {regla_seleccionada[1]:.2f} | Soporte = {regla_seleccionada[2]:.2f}")

        df = df[df[regla_seleccionada[0][0]] == regla_seleccionada[0][1]]
        imprimir_subtitulo("\nConjunto de datos reducido:", color=COLOR_DESTACADO)
        print(df)

    imprimir_subtitulo("\n\nREGLAS SELECCIONADAS:", color=COLOR_DESTACADO)
    print(" Y ".join(reglas_seleccionadas) + " ENTONCES cerveza=true\n")

# Principal
if __name__ == "__main__":
    conjunto_de_datos = crear_conjunto_de_datos()
    imprimir_subtitulo("CONJUNTO DE DATOS ORIGINAL:")
    print(conjunto_de_datos)
    ejecutar_analisis(conjunto_de_datos)
