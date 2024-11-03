#!/usr/bin/env python3

import os
from openpyxl import Workbook

# Rutas de directorios
simulation_results_dir = os.path.expanduser("~/mySimTools/gem5/resources_assignment/simulation_results")
excel_output_path = os.path.expanduser("~/mySimTools/gem5/resources_assignment/ExecutionTime_results.xlsx")

# Configuraciones posibles
L1d_sizes = [16, 64, 256, 512]
write_sizes = [64, 32, 16 ]
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
            config_found = False
            for L1d in L1d_sizes:
                for write in write_sizes:
                    for L2 in L2_associativities:
                        config_str = f"L1d{L1d}kB_write{write}_L2asso{L2}"
                        
                        if config_str in config_part:
                            config_files = data_by_config.setdefault(config_str, [])
                            config_files.append(file_name)
                            config_found = True
                            break  # Si encontramos una coincidencia, no es necesario seguir buscando
                if config_found:
                    break  # Rompe la búsqueda de L1d si ya encontramos la configuración
            
            # Si no se encontró configuración, podrías registrarlo
            if not config_found:
                print(f"No se encontró configuración para el archivo {file_name}")

        except IndexError:
            print(f"Error al procesar el archivo {file_name}, formato inesperado.")
            continue

# Crear un nuevo libro de Excel
workbook = Workbook()
workbook.remove(workbook.active)  # Quitar la hoja por defecto

# Procesar cada configuración y guardar los datos en el Excel
for config_str, files in data_by_config.items():
    # Crear una hoja para cada configuración
    sheet = workbook.create_sheet(title=config_str)
    sheet.append(["Simulación", "Tiempo de Ejecución (segundos)"])

    # Extraer valores de tiempo de ejecución y escribir en la hoja
    for file_name in files:
        file_path = os.path.join(simulation_results_dir, file_name)

        try:
            # Leer la línea 3 y extraer el valor de tiempo de ejecución (simSeconds)
            with open(file_path, 'r') as f:
                lines = f.readlines()
                exec_time_line = lines[2]  # línea 3 es el índice 2
                exec_time_value = float(exec_time_line.split()[1])  # asume que el valor de simSeconds es el segundo elemento

                # Guardar datos en la hoja
                sim_label = file_name.split('_', 2)[2].split('.')[0]
                sheet.append([sim_label, exec_time_value])
                print(f"Datos guardados para {file_name} en la configuración {config_str}")

        except (IndexError, ValueError, FileNotFoundError) as e:
            print(f"Error al leer el archivo {file_name}: {e}")
            continue

# Guardar el archivo Excel
workbook.save(excel_output_path)
print(f"Todos los datos de tiempo de ejecución se han guardado en {excel_output_path}")
