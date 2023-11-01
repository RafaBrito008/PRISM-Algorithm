import pandas as pd
import random
from colorama import Fore, Style

# Configurar constantes
NUM_DATOS = 30
COLOR_SUBTITULO = Fore.YELLOW
COLOR_DESTACADO = Fore.CYAN
RESET_COLOR = Style.RESET_ALL

def imprimir_subtitulo(texto, color=COLOR_SUBTITULO):
    """Imprime un texto como subtítulo con el color especificado."""
    print(color + texto + RESET_COLOR)

def crear_dataset(n=NUM_DATOS):
    """Crea un dataset ficticio con 'n' filas."""
    data = {
        'pañales': [random.choice([True, False]) for _ in range(n)],
        'leche': [random.choice([True, False]) for _ in range(n)],
        'biberones': [random.choice([True, False]) for _ in range(n)],
        'cerveza': [random.choice([True, False]) for _ in range(n)]
    }
    return pd.DataFrame(data)

def calcular_reglas(df, columns):
    """Calcula las reglas basadas en la confianza y el soporte."""
    reglas = []
    for col in columns:
        for val in [True, False]:
            condition = df[col] == val
            if len(df[condition]) == 0:
                continue

            count_condition_and_cerveza = len(df[condition & (df['cerveza'] == True)])
            confianza = count_condition_and_cerveza / len(df[condition])
            soporte = count_condition_and_cerveza / len(df)
            reglas.append(((col, val), confianza, soporte))
    return sorted(reglas, key=lambda x: (-x[1], -x[2]))

def imprimir_reglas(reglas):
    """Imprime las reglas en el formato deseado."""
    for r in reglas:
        condition = f"{r[0][0]}={r[0][1]}"
        print(f"SI {condition} ENTONCES cerveza=Sí -> Confianza = {r[1]:.2f} | Soporte = {r[2]:.2f}")

def ejecutar_analisis(df):
    iteration_number = 0
    columns_to_analyze = list(df.columns[:-1])
    selected_rules = []

    while not df.empty:
        iteration_number += 1
        imprimir_subtitulo(f"\n\nITERACIÓN {iteration_number}:")

        reglas = calcular_reglas(df, columns_to_analyze)
        if not reglas:
            break

        imprimir_reglas(reglas)

        selected_rule = reglas[0]
        selected_rules.append(f"{selected_rule[0][0]}={selected_rule[0][1]}")
        columns_to_analyze.remove(selected_rule[0][0])

        imprimir_subtitulo(f"\nRegla seleccionada para la iteración {iteration_number}:", color=COLOR_DESTACADO)
        condition_text = f"{selected_rule[0][0]}={selected_rule[0][1]}"
        print(f"SI {condition_text} ENTONCES cerveza=Sí -> Confianza = {selected_rule[1]:.2f} | Soporte = {selected_rule[2]:.2f}")

        df = df[df[selected_rule[0][0]] == selected_rule[0][1]]
        imprimir_subtitulo("\nDataset reducido:", color=COLOR_DESTACADO)
        print(df)

    imprimir_subtitulo("\n\nREGLAS SELECCIONADAS:", color=COLOR_DESTACADO)
    print(" AND ".join(selected_rules) + " ENTONCES cerveza=true\n")

# Main
if __name__ == "__main__":
    data_frame = crear_dataset()
    imprimir_subtitulo("DATASET ORIGINAL:")
    print(data_frame)
    ejecutar_analisis(data_frame)
