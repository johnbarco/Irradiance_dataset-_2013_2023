import pandas as pd
import numpy as np

def fill_missing_irradiance_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Completa los datos perdidos (NaN) en las columnas de irradiancia
    utilizando el promedio de los valores existentes para el mismo intervalo
    de tiempo en los años anteriores y siguientes.

    Args:
        df (pd.DataFrame): DataFrame de entrada con columnas de 'Date', 'Day'
                          y columnas de años (ej., 2013, 2014, ...).
                          Se asume que los valores de irradiancia están en las
                          columnas de los años.

    Returns:
        pd.DataFrame: Un nuevo DataFrame con los valores NaN en las columnas
                      de irradiancia completados.
    """
    # Crear una copia del DataFrame para no modificar el original
    df_filled = df.copy()

    # Identificar las columnas que contienen los datos de irradiancia (los años)
    # Asumimos que las columnas de irradiancia comienzan desde la tercera columna (índice 2)
    # y que sus nombres son los años.
    irradiance_cols = df_filled.columns[2:]

    print(f"Columnas de irradiancia identificadas: {list(irradiance_cols)}")
    print(f"Número inicial de valores NaN en las columnas de irradiancia: {df_filled[irradiance_cols].isnull().sum().sum()}")

    # Iterar sobre cada fila (intervalo de tiempo de 5 minutos en un día)
    # Para cada fila, calculamos el promedio de los valores existentes en esa fila
    # a través de los diferentes años, y usamos ese promedio para llenar los NaN
    # en esa misma fila.
    for index, row in df_filled.iterrows():
        # Seleccionar solo los valores de irradiancia para la fila actual
        irradiance_values_in_row = row[irradiance_cols]

        # Calcular el promedio de los valores no NaN en esa fila (intervalo de tiempo)
        # np.nanmean ignora los NaN al calcular el promedio
        row_mean = np.nanmean(irradiance_values_in_row)

        # Si el promedio es NaN (lo que significa que todos los valores para ese
        # intervalo de tiempo en todos los años están perdidos), no podemos imputar.
        # En ese caso, el NaN permanecerá.
        if not np.isnan(row_mean):
            # Llenar los NaN en la fila actual con el promedio calculado
            df_filled.loc[index, irradiance_cols] = row[irradiance_cols].fillna(row_mean)
        # else:
            # print(f"Advertencia: Todos los datos para el intervalo de tiempo en la fila {index} son NaN. No se pudo imputar.")

    print(f"Número final de valores NaN en las columnas de irradiancia: {df_filled[irradiance_cols].isnull().sum().sum()}")
    return df_filled

# --- Ejemplo de Uso ---
if __name__ == "__main__":
    # --- 1. Crear un DataFrame de ejemplo con datos perdidos ---
    # Simula la estructura de tu archivo Excel para una hoja mensual
    data = {
        'Date': pd.to_datetime(['2023-01-01 00:00:00', '2023-01-01 00:05:00', '2023-01-01 00:10:00',
                                '2023-01-01 00:15:00', '2023-01-01 00:20:00']),
        'Day': [1, 1, 1, 1, 1],
        2013: [0.1, 0.2, np.nan, 0.4, 0.5],
        2014: [0.15, np.nan, 0.35, 0.45, 0.55],
        2015: [np.nan, 0.22, 0.32, np.nan, 0.52],
        2016: [0.12, 0.23, 0.33, 0.43, np.nan]
    }
    sample_df = pd.DataFrame(data)
    print("--- DataFrame de Ejemplo Original ---")
    print(sample_df)
    print("\nValores NaN antes de la imputación:\n", sample_df.isnull().sum())

    # --- 2. Aplicar la función para completar los datos ---
    filled_df = fill_missing_irradiance_data(sample_df)

    print("\n--- DataFrame de Ejemplo Después de la Imputación ---")
    print(filled_df)
    print("\nValores NaN después de la imputación:\n", filled_df.isnull().sum())

    # --- Notas importantes para tu caso real ---
    # 1. Carga de tus datos:
    #    Asegúrate de cargar tu DataFrame real como se hizo en tu código de visualización.
    #    file_path = "Proccess_irradiance_data_2013_2023.xlsx"
    #    sheet_name = "Enero" # O la hoja mensual que quieras procesar
    #    your_df = pd.read_excel(file_path, sheet_name=sheet_name)
    #
    # 2. Aplicar la función:
    #    df_irradiancia_limpio = fill_missing_irradiance_data(your_df)
    #
    # 3. Manejo de casos sin datos:
    #    Si una fila completa de datos de irradiancia (para un intervalo de tiempo específico)
    #    está en NaN en todos los años, la función no podrá imputar y esos NaN permanecerán.
    #    Considera si quieres un método de respaldo para estos casos (ej., interpolación temporal
    #    si hay datos faltantes consecutivos en una columna de año, o rellenar con 0 si es de noche).
    #
    # 4. Columnas de irradiancia:
    #    El código asume que las columnas de irradiancia son todas las columnas a partir del índice 2.
    #    Asegúrate de que esto sea correcto para la estructura de tu DataFrame.
