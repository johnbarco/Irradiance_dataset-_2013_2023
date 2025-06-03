import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D # Necesario para gráficos 3D

# --- Configuración global ---
# Ruta del archivo Excel. Considera usar una ruta relativa para GitHub.
# Por ejemplo: 'data/Proccess_irradiance_data_2013_2023.xlsx'
EXCEL_FILE_PATH = "Proccess_irradiance_data_2013_2023.xlsx"
SHEET_NAME = "Enero"
OUTPUT_FILENAME = "irradiance_behaviour_3d.png"
OUTPUT_DPI = 300 # Resolución de la imagen (puntos por pulgada)

# --- Funciones ---

def load_and_preprocess_data(file_path: str, sheet_name: str) -> tuple:
    """
    Carga los datos de irradiancia desde un archivo Excel y realiza un preprocesamiento inicial.

    Args:
        file_path (str): Ruta al archivo Excel.
        sheet_name (str): Nombre de la hoja a leer.

    Returns:
        tuple: Una tupla que contiene:
            - time (pd.Series): Serie de tiempo de la primera cuarta parte de los datos.
            - irradiance_data (pd.DataFrame): DataFrame de irradiancia de la primera cuarta parte.
            - years (pd.Index): Nombres de las columnas de los años.
            - num_time_points (int): Número de puntos de tiempo en la porción seleccionada.
            - num_years (int): Número de años en el dataset.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró. Asegúrate de que la ruta sea correcta.")
        exit()
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        exit()

    # La primera columna es el tiempo, las columnas de irradiancia comienzan desde la tercera.
    time_full = df.iloc[:, 0]
    irradiance_data_full = df.iloc[:, 2:]
    years = irradiance_data_full.columns # Los nombres de las columnas son los años

    # Seleccionar la primera cuarta parte de los datos para visualización
    num_rows = len(df)
    quarter_rows = num_rows // 4
    time = time_full[:quarter_rows]
    irradiance_data = irradiance_data_full.iloc[:quarter_rows, :]

    num_time_points = len(time)
    num_years = len(years)

    return time, irradiance_data, years, num_time_points, num_years

def create_3d_irradiance_plot(time_points: pd.Series, irradiance_df: pd.DataFrame,
                             years_labels: pd.Index, num_time_points: int, num_years: int) -> plt.Figure:
    """
    Crea un gráfico 3D del comportamiento de la irradiancia a lo largo de los años.

    Args:
        time_points (pd.Series): Puntos de tiempo para el eje Y.
        irradiance_df (pd.DataFrame): Datos de irradiancia por año.
        years_labels (pd.Index): Etiquetas de los años para el eje X.
        num_time_points (int): Número de puntos de tiempo.
        num_years (int): Número de años.

    Returns:
        plt.Figure: Objeto Figure de Matplotlib.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # --- Configuración de la estética de los paneles 3D ---
    # Hace los paneles de la caja 3D transparentes
    ax.xaxis.pane.set_facecolor('none')
    ax.yaxis.pane.set_facecolor('none')
    ax.zaxis.pane.set_facecolor('none')

    # Hace los bordes de los paneles transparentes
    ax.xaxis.pane.set_edgecolor('none')
    ax.yaxis.pane.set_edgecolor('none')
    ax.zaxis.pane.set_edgecolor('none')

    # Elimina la cuadrícula del gráfico
    ax.grid(False)

    # Define una paleta de colores para las líneas de los años
    colors = sns.color_palette("inferno", n_colors=num_years)

    # Graficar las líneas para cada año
    # En el gráfico 3D (x, y, z):
    # x: Representa el índice del año (para separar las líneas)
    # y: Representa los puntos de tiempo
    # z: Representa los valores de irradiancia
    x_plot_coords = np.arange(num_time_points) # Coordenadas para el eje 'Time' del plot

    for i, year in enumerate(years_labels):
        z_irradiance = irradiance_df[year].values # Valores de irradiancia para el año actual
        y_year_index = np.full(num_time_points, i) # Índice del año para el eje 'Year' del plot

        # Grafica la línea 3D
        ax.plot(y_year_index, x_plot_coords, z_irradiance,
                linestyle='-', linewidth=0.5, color=colors[i], label=year)

    # --- Personalizar las etiquetas y ticks de los ejes ---
    # Etiqueta del eje X (representa los años)
    ax.set_xlabel("Year", fontsize=10, fontweight='normal', labelpad=20)

    # Configurar los ticks del eje X para mostrar los años
    ax.set_xticks(np.arange(num_years))
    ax.set_xticklabels(years_labels, rotation=45, ha='right', fontsize=8)

    # Etiqueta del eje Y (representa el tiempo)
    ax.set_ylabel("Time", fontsize=10, fontweight='normal')
    # Quitar los ticks del eje Y (tiempo) para una visualización más limpia
    ax.set_yticks([]) # Si deseas mostrar los ticks de tiempo, comenta esta línea

    # Etiqueta del eje Z (irradiancia)
    ax.set_zlabel("Irradiance", fontsize=10, fontweight='normal')
    # Mover la etiqueta del eje Z más abajo para evitar superposición
    zlabel = ax.zaxis.get_label()
    zlabel.set_position((0.5, 0.05)) # (horizontal_relative_pos, vertical_relative_pos)

    # Ajustar el tamaño del texto de los ticks del eje Z
    ax.tick_params(axis='z', labelsize=8)

    # Establecer el límite superior del eje Z (irradiancia)
    ax.set_zlim(0, 5000)

    # Ajustar el ángulo de la vista 3D
    ax.view_init(elev=30, azim=120)

    # Título del gráfico
    ax.set_title(f"Irradiance Behavior Over 8 Days", fontsize=14, fontweight='bold')

    # --- Configuración de la leyenda ---
    # Mover la leyenda al centro superior de la figura
    ax.legend(title="Year", loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=num_years, fontsize=8)

    plt.tight_layout() # Ajusta el diseño para evitar recortes

    return fig

# --- Bloque principal de ejecución ---
if __name__ == "__main__":
    # 1. Cargar y preprocesar los datos
    time_data, irradiance_df_processed, years_labels, num_time_points, num_years = \
        load_and_preprocess_data(EXCEL_FILE_PATH, SHEET_NAME)

    # 2. Crear el gráfico 3D
    fig = create_3d_irradiance_plot(time_data, irradiance_df_processed,
                                    years_labels, num_time_points, num_years)

    # 3. Guardar la imagen con alta resolución y transparencia
    plt.savefig(OUTPUT_FILENAME, dpi=OUTPUT_DPI, bbox_inches='tight', transparent=True)
    print(f"Gráfico guardado como '{OUTPUT_FILENAME}' con {OUTPUT_DPI} DPI.")

    # 4. Mostrar el gráfico
    plt.show()
