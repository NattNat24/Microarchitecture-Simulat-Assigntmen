#!/usr/bin/env python3

import os
import subprocess

# Rutas de directorios
mcpat_executable = os.path.expanduser("~/mySimTools/mcpat/mcpat")
mcpat_results_dir = os.path.expanduser("~/mySimTools/gem5/resources_assignment/McPAT_results")
json_output_dir = os.path.expanduser("~/mySimTools/gem5/resources_assignment/McPAT_json_results_time")

# Crear el directorio de salida si no existe
os.makedirs(json_output_dir, exist_ok=True)

# Ejecutar el comando mcpat para cada archivo XML desde sim1 hasta sim288
for sim_num in range(1, 289):
    # Buscar el archivo XML correspondiente que comienza con "config_sim" seguido del número
    xml_file = next(
        (os.path.join(mcpat_results_dir, file_name) 
         for file_name in os.listdir(mcpat_results_dir)
         if file_name.startswith(f"config_sim{sim_num}_") and file_name.endswith(".xml")), 
        None
    )
    
    # Verificar si el archivo XML existe antes de ejecutar el comando
    if xml_file:
        # Convertir el nombre del archivo XML a formato JSON
        json_file_name = os.path.basename(xml_file).replace(".xml", ".json")
        json_output_file = os.path.join(json_output_dir, json_file_name)

        # Construir el comando
        command = [mcpat_executable, "-infile", xml_file]
        
        # Ejecutar el comando y redirigir la salida al archivo JSON
        with open(json_output_file, 'w') as outfile:
            try:
                print(f"Ejecutando mcpat para sim{sim_num} con archivo XML: {xml_file}\n")
                # Ejecutar el comando y esperar a que termine
                subprocess.run(command, check=True, stdout=outfile, stderr=outfile)
                print(f"Resultado guardado en {json_output_file}\n")
            except subprocess.CalledProcessError as e:
                print(f"Error al ejecutar mcpat para sim{sim_num}: {e}")
    else:
        print(f"Archivo XML para sim{sim_num} no encontrado.")
