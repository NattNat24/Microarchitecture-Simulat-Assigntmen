#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt

# Rutas de directorios
simulation_results_dir = os.path.expanduser("~/mySimTools/gem5/resources_assignment/simulation_results")
graphs_output_dir = os.path.expanduser("~/mySimTools/gem5/resources_assignment/ExecutionTime_graphs")

# Crear el directorio de salida para gráficos si no existe
os.makedirs(graphs_output_dir, exist_ok=True)

# Recopilación de datos
data_by_application = {}

# Recorrer todos los archivos en el directorio
for file_name in os.listdir(simulation_results_dir):
    # Verificar que el archivo sea .txt
    if file_name.endswith(".txt"):
        # Extraer la configuración del archivo
        parts = file_name.split('_')
        try:
            sim_num = parts[1]
            app_type = parts[2]  # tipo de aplicación (jpg2k, h264, mp3, etc.)
            config_part = "_".join(parts[3:]).split('.')[0]  # el resto de la configuración
            
            # Filtrar configuraciones que coincidan con nuestras combinaciones
            key = f"{app_type}_{parts[3]}"  # Usa la parte que indica si es enc o dec
            if key in data_by_application:
                data_by_application[key].append((config_part, file_name))
            else:
                data_by_application[key] = [(config_part, file_name)]

        except IndexError:
            print(f"Error al procesar el archivo {file_name}, formato inesperado.")
            continue

# Extraer y graficar tiempo de ejecución para cada aplicación y su modo
for app_type, config_files in data_by_application.items():
    exec_times = []
    labels = []

    for config_part, file_name in config_files:
        file_path = os.path.join(simulation_results_dir, file_name)

        try:
            # Leer la línea 3 y extraer el valor de tiempo de ejecución (simSeconds)
            with open(file_path, 'r') as f:
                lines = f.readlines()
                exec_time_line = lines[2]  # línea 3 es el índice 2
                exec_time_value = float(exec_time_line.split()[1])  # asume que el valor de simSeconds es el segundo elemento
                exec_times.append(exec_time_value)

                # Agregar etiqueta del archivo
                sim_label = file_name.split('_', 2)[2].split('.')[0]  # Parte posterior del nombre
                labels.append(sim_label)

        except (IndexError, ValueError, FileNotFoundError) as e:
            print(f"Error al leer el archivo {file_name}: {e}")
            continue

    # Crear gráfico de barras para esta aplicación y su modo
    plt.figure(figsize=(12, 6))
    plt.bar(labels, exec_times, color='skyblue')
    plt.xlabel("Configuraciones de Simulación")
    plt.ylabel("Tiempo de Ejecución (segundos)")
    plt.title(f"Tiempo de Ejecución para {app_type}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Guardar gráfico en la carpeta de gráficos
    output_file = os.path.join(graphs_output_dir, f"ExecutionTime_{app_type}.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Gráfico guardado para {app_type} en {output_file}")