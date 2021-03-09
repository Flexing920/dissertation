import configparser
from sumolib import checkBinary
import os
import sys

def import_train_configuration(config_file):
    """
        Read training settings from the ini file
    """
    readings = configparser.ConfigParser()
    readings.read(config_file)
    settings = {}
    settings['gui'] = readings['simulation'].getboolean('gui')
    settings['episodes'] = readings['simulation'].getin('episodes')
    settings['max_steps'] = readings['simulation'].getin('max_steps')
    settings['max_steps'] = readings['simulation'].getint('max_steps')
    settings['green_duration'] = readings['simulation'].getint('green_duration')
    settings['yellow_duration'] = readings['simulation'].getint('yellow_duration')
    settings['red_duration'] = readings['simulation'].getint('red_duration')

    settings['num_layers'] = readings['model'].getint('num_layers')
    settings['num_nodes'] = readings['model'].getint('num_nodes')
    settings['batch_size'] = readings['model'].getint('batch_size')
    settings['batch_size'] = readings['model'].getint('batch_size')
    settings['learning_rate'] = readings['model'].getfloat('learning_rate')
    settings['training_epochs'] = readings['model'].getint('training_epochs')

    settings['mem_size_min'] = readings['memory'].getint('mem_size_min')
    settings['mem_size_max'] = readings['memory'].getint('mem_size_max')

    settings['num_states'] = readings['agent'].getint('num_states')
    settings['num_actions'] = readings['agent'].getint('num_actions')
    settings['gamma'] = readings['agent'].getfloat('gamma')

    settings['models_path_name'] = readings['dir']['models_path_name']
    settings['sumocfg_file_name'] = readings['dir']['sumocfg_file_name'] # careful about the path

    return settings

def set_sumo(gui, sumocfg_file_name, max_steps):
    """ Set up SUMO simulation """

    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
    else:
        sys.exit("please declare environment variable 'SUMO_HOME'")

    # setting the cmd mode or the visual mode    
    if gui == False:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
 
    # setting the cmd command to run sumo at simulation time
    data_dir = os.path.join(os.getcwd(), "data")
    sumo_cmd = [sumoBinary, "-c", os.path.join(data_dir, sumocfg_file_name), "--no-step-log", "true", "--waiting-time-memory", str(max_steps)]

    return sumo_cmd

def set_train_path(models_path_name):
    """
    Create a new model path with an incremental integer, also considering previously created model paths (copied)
    """
    models_path = os.path.join(os.getcwd(), models_path_name, '')
    os.makedirs(os.path.dirname(models_path), exist_ok=True)

    dir_content = os.listdir(models_path)
    if dir_content:
        previous_versions = [int(name.split("_")[1]) for name in dir_content]
        new_version = str(max(previous_versions) + 1)
    else:
        new_version = '1'

    data_path = os.path.join(models_path, 'model_'+new_version, '')
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    return data_path 





    






    