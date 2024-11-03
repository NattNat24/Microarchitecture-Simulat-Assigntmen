#!/usr/bin/env python3

import os
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define las rutas para cada simulación utilizando rutas absolutas
HOME_DIR = os.path.expanduser("~")
simulation_paths = {
    "mp3_enc": os.path.join(HOME_DIR, "mySimTools/gem5/resources_assignment/workloads/mp3_enc"),
    "mp3_dec": os.path.join(HOME_DIR, "mySimTools/gem5/resources_assignment/workloads/mp3_dec"),
    "jpg2k_enc": os.path.join(HOME_DIR, "mySimTools/gem5/resources_assignment/workloads/jpeg2k_enc"),
    "jpg2k_dec": os.path.join(HOME_DIR, "mySimTools/gem5/resources_assignment/workloads/jpeg2k_dec"),
    "h264_dec": os.path.join(HOME_DIR, "mySimTools/gem5/resources_assignment/workloads/h264_dec"),
    "h264_enc": os.path.join(HOME_DIR, "mySimTools/gem5/resources_assignment/workloads/h264_enc")
}

# Define las rutas para los archivos stats.txt y config.json utilizando rutas absolutas
stats_paths = {
    "mp3_enc": os.path.join(simulation_paths["mp3_enc"], "m5out/stats.txt"),
    "mp3_dec": os.path.join(simulation_paths["mp3_dec"], "m5out/stats.txt"),
    "jpg2k_enc": os.path.join(simulation_paths["jpg2k_enc"], "m5out/stats.txt"),
    "jpg2k_dec": os.path.join(simulation_paths["jpg2k_dec"], "m5out/stats.txt"),
    "h264_dec": os.path.join(simulation_paths["h264_dec"], "m5out/stats.txt"),
    "h264_enc": os.path.join(simulation_paths["h264_enc"], "m5out/stats.txt")
}

config_paths = {
    "mp3_enc": os.path.join(simulation_paths["mp3_enc"], "m5out/config.json"),
    "mp3_dec": os.path.join(simulation_paths["mp3_dec"], "m5out/config.json"),
    "jpg2k_enc": os.path.join(simulation_paths["jpg2k_enc"], "m5out/config.json"),
    "jpg2k_dec": os.path.join(simulation_paths["jpg2k_dec"], "m5out/config.json"),
    "h264_dec": os.path.join(simulation_paths["h264_dec"], "m5out/config.json"),
    "h264_enc": os.path.join(simulation_paths["h264_enc"], "m5out/config.json")
}

# Define el comando de simulación para cada tipo
commands = {
    "mp3_enc": 'CortexA76.py --cmd=mp3_enc --options="mp3enc_testfile.wav mp3enc_outfile.mp3"',
    "mp3_dec": 'CortexA76.py --cmd=mp3_dec --options="-w mp3dec_outfile.wav mp3dec_testfile.mp3"',
    "jpg2k_enc": 'CortexA76.py --cmd=jpg2k_enc --options="-i jpg2kenc_testfile.bmp -o jpg2kenc_outfile.j2k"',
    "jpg2k_dec": 'CortexA76.py --cmd=jpg2k_dec --options="-i jpg2kdec_testfile.j2k -o jpg2kdec_outfile.bmp"',
    "h264_dec": 'CortexA76.py --cmd=h264_dec --options="h264dec_testfile.264 h264dec_outfile.yuv"',
    "h264_enc": 'CortexA76.py --cmd=h264_enc --options="h264enc_configfile.cfg"'
}



# Define los parámetros para la simulación
new_values_array1 = ['16kB', '64kB', '256kB', '512kB']
new_values_array2 = ['64', '32', '16']
new_values_array3 = ['4', '8', '2', '16']

# Directorio base para resultados de simulaciones
output_base_dir = os.path.join(HOME_DIR, "mySimTools/gem5/resources_assignment/simulation_results")
os.makedirs(output_base_dir, exist_ok=True)

# Ruta al ejecutable de gem5 y script de configuración
GEM5PATH = os.path.join(HOME_DIR, "mySimTools/gem5/build/ARM/gem5.fast")
SCRIPTDIR = os.path.join(HOME_DIR, "mySimTools/gem5/resources_assignment/scripts/CortexA76_scripts_gem5/CortexA76.py")

# Define el número máximo de simulaciones concurrentes
MAX_CONCURRENT_SIMULATIONS = 6

def ejecutar_simulacion(simulation_name, param1, param2, param3, sim_id):
    """
    Ejecuta una simulación específica y maneja la copia de archivos stats.txt y config.json.
    """
    # Construir las opciones adicionales basadas en los parámetros
    more_options = f"--l1d_size={param1} --num_fu_write={param2} --l2_assoc={param3}"
    simulation_dir = simulation_paths.get(simulation_name)
    
    if not simulation_dir or not os.path.isdir(simulation_dir):
        return f"Error: El directorio {simulation_dir} para la simulación {simulation_name} no existe."
    
    # Construir el comando completo
    full_command = f'"{GEM5PATH}" "{SCRIPTDIR}" {commands[simulation_name]} {more_options}'
    print(f"Lanzando simulación {sim_id}: {simulation_name} con comando:\n{full_command}\n")
    
    try:
        log_file_path = os.path.join(output_base_dir, f'sim_{sim_id}_log.txt')
        with open(log_file_path, 'w') as log_file:
            process = subprocess.Popen(full_command, shell=True, cwd=simulation_dir, stdout=log_file, stderr=subprocess.STDOUT)
        
        return_code = process.wait()
        
        if return_code != 0:
            return f"Simulación {sim_id} ({simulation_name}) falló con código de salida: {return_code}."
        
        # Archivos de salida stats.txt y config.json
        stats_file = stats_paths.get(simulation_name)
        config_file = config_paths.get(simulation_name)
        safe_param1 = param1.replace('/', '_').replace(' ', '_')
        safe_param2 = param2.replace('/', '_').replace(' ', '_')
        safe_param3 = param3.replace('/', '_').replace(' ', '_')
        
        # Archivos de salida con nombres únicos
        output_stats_file = os.path.join(output_base_dir, f'stats_sim{sim_id}_{simulation_name}_L1d{safe_param1}_write{safe_param2}_L2asso{safe_param3}.txt')
        output_config_file = os.path.join(output_base_dir, f'config_sim{sim_id}_{simulation_name}_L1d{safe_param1}_write{safe_param2}_L2asso{safe_param3}.json')
        
        # Copiar stats.txt y config.json si existen y no están vacíos
        if stats_file and os.path.exists(stats_file) and os.path.getsize(stats_file) > 0:
            shutil.copy(stats_file, output_stats_file)
        
        if config_file and os.path.exists(config_file) and os.path.getsize(config_file) > 0:
            shutil.copy(config_file, output_config_file)
        
        return f"Simulación {sim_id} ({simulation_name}) completada. Archivos guardados."
    
    except Exception as e:
        return f"Simulación {sim_id} ({simulation_name}) falló con error: {e}"

def main():
    # Crear lista de combinaciones de simulaciones
    tareas = []
    simulation_id_counter = 1
    for value1 in new_values_array1:
        for value2 in new_values_array2:
            for value3 in new_values_array3:
                for simulation_name in commands.keys():
                    tareas.append((simulation_name, value1, value2, value3, simulation_id_counter))
                    simulation_id_counter += 1
    
    resultados = []
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_SIMULATIONS) as executor:
        futuros = {
            executor.submit(ejecutar_simulacion, sim[0], sim[1], sim[2], sim[3], sim[4]): sim for sim in tareas
        }
        
        for futuro in as_completed(futuros):
            sim = futuros[futuro]
            try:
                resultado = futuro.result()
                resultados.append(resultado)
                print(resultado + "\n")
            except Exception as e:
                error_msg = f"Simulación {sim[4]} ({sim[0]}) falló con excepción: {e}"
                resultados.append(error_msg)
                print(error_msg + "\n")
    
    # Guardar resultados en archivo resumen
    resumen_path = os.path.join(output_base_dir, "resumen_simulaciones.txt")
    with open(resumen_path, 'w') as resumen_file:
        for linea in resultados:
            resumen_file.write(linea + "\n")
    
    print("Todas las simulaciones han finalizado y los resultados han sido guardados.\n")

if __name__ == "__main__":
    main()
