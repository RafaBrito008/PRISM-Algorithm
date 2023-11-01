import pandas as pd
import random
from colorama import Fore, Style

# Configurar colores
COLOR_SUBTITULO = Fore.YELLOW  # Color para los subtítulos (amarillo)
COLOR_DESTACADO = Fore.CYAN  # Color para los textos destacados (cian)
RESET_COLOR = Style.RESET_ALL

# Función para imprimir subtítulos en amarillo
def imprimir_subtitulo(texto, color=COLOR_SUBTITULO):
    print(color + texto + RESET_COLOR)

# Paso 1: Crear un dataset ficticio
def crear_dataset():
    data = {
        'pañales': [random.choice([True, False]) for _ in range(40)],
        'leche': [random.choice([True, False]) for _ in range(40)],
        'biberones': [random.choice([True, False]) for _ in range(40)],
        'cerveza': [random.choice([True, False]) for _ in range(40)]
    }
    df = pd.DataFrame(data)
    return df

# Paso 3: Calcular reglas
def calcular_reglas(df, columns):
    reglas = []
    
    for col in columns:
        for val in [True, False]:
            condition = df[col] == val
            
            if len(df[condition]) == 0:  # Verificar si el divisor es cero
                continue

            count_condition_and_cerveza = len(df[condition & (df['cerveza'] == True)])
            confianza = count_condition_and_cerveza / len(df[condition])
            soporte = count_condition_and_cerveza / len(df)
            reglas.append(((col, val), confianza, soporte))
            
    return sorted(reglas, key=lambda x: (-x[1], -x[2]))


# Main
df = crear_dataset()
imprimir_subtitulo("DATASET ORIGINAL:")
print(df)

iteration = 0
columns_to_check = list(df.columns[:-1])  # Excluyendo 'cerveza'
reglas_seleccionadas = []

while not df.empty:
    iteration += 1
    imprimir_subtitulo(f"\n\nITERACIÓN {iteration}:")

    reglas = calcular_reglas(df, columns_to_check)
    
    if not reglas:
        break
    
    # Paso 4: Imprimir reglas
    for r in reglas:
        condition = f"{r[0][0]}={r[0][1]}"
        print(f"SI {condition} ENTONCES cerveza=Sí -> Confianza = {r[1]:.2f} | Soporte = {r[2]:.2f}")

    regla_seleccionada = reglas[0]
    reglas_seleccionadas.append(f"{regla_seleccionada[0][0]}={regla_seleccionada[0][1]}")
    columns_to_check.remove(regla_seleccionada[0][0])
    
    imprimir_subtitulo(f"\nRegla seleccionada para la iteración {iteration}:", color=COLOR_DESTACADO)
    condition = f"{regla_seleccionada[0][0]}={regla_seleccionada[0][1]}"
    print(f"SI {condition} ENTONCES cerveza=Sí -> Confianza = {regla_seleccionada[1]:.2f} | Soporte = {regla_seleccionada[2]:.2f}")

    # Paso 5: Reducir el dataset
    condition = df[regla_seleccionada[0][0]] == regla_seleccionada[0][1]
    df = df[condition]
    imprimir_subtitulo("\nDataset reducido:", color=COLOR_DESTACADO)
    print(df)

imprimir_subtitulo("\n\nREGLAS SELECCIONADAS:", color=COLOR_DESTACADO)
print(" AND ".join(reglas_seleccionadas) + " ENTONCES cerveza=true\n")
