from sumolib import checkBinary
import os, sys, configparser


def set_sumo(gui, sumocfg_filename):
    if "SUMO_HOME" in os.environ:
        tools = os.path.join(os.environ["SUMO_HOME"], "tools")
        sys.path.append(tools)
    else:
        sys.exit("Please declare environment variable 'SUMO_HOME'")
    
    if gui == False:
        sumoBinary = checkBinary("sumo")
    else:
        sumoBinary = checkBinary("sumo-gui")
    file_dir = f"{sumocfg_filename}"
    sumo_cmd = [sumoBinary, "-c", file_dir, "--no-step-log", "true"]
    return sumo_cmd

def import_train_settings(file):
    settings = configparser.ConfigParser()
    settings.read(file)
    config = {}
    config["gui"] = settings["simulation"].getboolean("gui")
    config["sumocfg_filename"] = settings["simulation"]["sumocfg_filename"]
    return config
