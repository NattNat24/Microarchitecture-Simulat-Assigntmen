#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt

# Rutas de directorios
simulation_results_dir = os.path.expanduser("~/mySimTools/gem5/resources_assignment/simulation_results")
graphs_output_dir = os.path.expanduser("~/mySimTools/gem5/resources_assignment/ExecutionTime_graphs")

# Crear el directorio de salida para gráficos si no existe
os.makedirs(graphs_output_dir, exist_ok=True)

# Configuraciones posibles
L1d_sizes = [16, 64, 256, 512]
write_sizes = [64, 32, 16]
L2_associativities = [4, 8, 2, 16]

# Recopilación de datos
data_by_config = {}

# Recorrer todos los archivos en el directorio
for file_name in os.listdir(simulation_results_dir):
    # Verificar que el archivo sea .txt
    if file_name.endswith(".txt"):
        # Extraer la configuración del archivo
        parts = file_name.split('_')
        try:
            sim_num = parts[1]
            config_part = "_".join(parts[2:]).split('.')[0]
            
            # Filtrar configuraciones que coincidan con nuestras combinaciones
            for L1d in L1d_sizes:
                for write in write_sizes:
                    for L2 in L2_associativities:
                        config_str = f"L1d{L1d}kB_write{write}_L2asso{L2}"
                        
                        if config_str in config_part:
                            config_files = data_by_config.setdefault(config_str, [])
                            config_files.append(file_name)
                            break  # Si encontramos una coincidencia, no es necesario seguir buscando

        except IndexError:
            print(f"Error al procesar el archivo {file_name}, formato inesperado.")
            continue

# Extraer y graficar tiempo de ejecución para cada configuración
for config_str, files in data_by_config.items():
    exec_times = []
    labels = []

    for file_name in files:
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

    # Crear gráfico de barras para esta configuración
    plt.figure(figsize=(10, 6))
    plt.bar(labels, exec_times, color='skyblue')
    plt.xlabel("Simulación")
    plt.ylabel("Tiempo de Ejecución (segundos)")
    plt.title(f"Tiempo de Ejecución para configuración {config_str}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Guardar gráfico en la carpeta de gráficos
    output_file = os.path.join(graphs_output_dir, f"ExecutionTime_{config_str}.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Gráfico guardado para configuración {config_str} en {output_file}")
