#!/usr/bin/env python3

import os
import subprocess

# Rutas de directorios
simulation_results_dir = os.path.expanduser("~/mySimTools/gem5/resources_assignment/simulation_results")
output_dir = os.path.expanduser("~/mySimTools/gem5/resources_assignment/McPAT_results")
script_path = os.path.expanduser("~/mySimTools/gem5/resources_assignment/scripts/McPAT/gem5toMcPAT_cortexA76.py")
xml_path = os.path.expanduser("~/mySimTools/gem5/resources_assignment/scripts/McPAT/ARM_A76_2.1GHz.xml")

# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Procesar cada archivo desde sim1 hasta sim288
for sim_num in range(1, 289):
    # Buscar los archivos correspondientes a este número de simulación
    stats_file = None
    config_file = None

    for file_name in os.listdir(simulation_results_dir):
        if file_name.startswith(f"stats_sim{sim_num}_"):
            stats_file = os.path.join(simulation_results_dir, file_name)
        elif file_name.startswith(f"config_sim{sim_num}_"):
            config_file = os.path.join(simulation_results_dir, file_name)

    # Ejecutar el comando de Linux solo si ambos archivos existen
    if stats_file and config_file:
        # Mostrar nombres completos de los archivos usados
        print(f"Procesando Simulación {sim_num}")
        print(f"Archivo stats usado: {stats_file}")
        print(f"Archivo config usado: {config_file}")
        
        # Definir el nombre del archivo de salida con extensión .xml
        output_file = os.path.join(output_dir, f"result_sim{sim_num}.xml")
        command = [
            "python3", script_path, stats_file, config_file, xml_path
        ]
        print(command)
        try:
            # Ejecutar el comando y redirigir la salida al archivo .xml
            with open(output_file, 'w') as outfile:
                subprocess.run(command, check=True, stdout=outfile, stderr=outfile)
            print(f"Simulación {sim_num} completada, resultado guardado en {output_file}\n")
        except subprocess.CalledProcessError as e:
            print(f"Error en la simulación {sim_num}: {e}")
    else:
        print(f"Archivos para sim{sim_num} no encontrados.")
