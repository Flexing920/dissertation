from __future__ import absolute_import
from __future__ import print_function

import os
import datetime
from shutil import copyfile

from training_simulation import SimulationTemplate
from generator import TrafficGenerator
from memory import MemoryBuffer
from model import TrainModel
from visualization import VisualizationTemplate
from utils import import_train_configuration, set_sumo, set_train_path

total_episodes_list = [400]
learning_rate_list = [0.0001]
num_layeys_list = [8]
batch_size_list = [512]
training_epochs_list = [1200]

# total_episodes_list = [200]
# learning_rate_list = [0.001]
# num_layeys_list = [8]
# batch_size_list = [128]
# training_epochs_list = [800]

if __name__ == "__main__":
    for episode_chosen in total_episodes_list:
        for lr_chosen in learning_rate_list:
            for num_layer_chosen in num_layeys_list:
                for batch_chosen in batch_size_list:
                    for training_epochs_chosen in training_epochs_list:
                        config = import_train_configuration(config_file='training_settings.ini')
                        config['total_episodes'] = episode_chosen
                        config['learning_rate'] = lr_chosen
                        config['num_layers'] = num_layer_chosen
                        config['batch_size'] = batch_chosen
                        config['training_epochs'] = training_epochs_chosen


                        sumo_cmd = set_sumo(config['gui'], config['sumocfg_file_name'], config['max_steps'])
                        path = set_train_path(config['models_path_name'])

                        Model = TrainModel(
                            config['num_layers'], 
                            config['width_layers'], 
                            config['batch_size'], 
                            config['learning_rate'], 
                            input_dim=config['num_states'], 
                            output_dim=config['num_actions']
                        )

                        Memory = MemoryBuffer(
                            config['memory_size_max'], 
                            config['memory_size_min']
                        )

                        TrafficGen = TrafficGenerator(
                            config['max_steps'], 
                            config['n_cars_generated_1'],
                            config['n_cars_generated_2'],
                            config['n_cars_generated_3'],
                            config['n_cars_generated_4'],
                            config['n_cars_generated_5'],
                        )

                        Visualization = VisualizationTemplate(
                            path, 
                            dpi=96
                        )
                            
                        Simulation = SimulationTemplate(
                            Model,
                            Memory,
                            TrafficGen,
                            sumo_cmd,
                            config['gamma'],
                            config['max_steps'],
                            config['green_duration'],
                            config['yellow_duration'],
                            config['num_states'],
                            config['num_actions'],
                            config['training_epochs']
                        )
                        
                        episode = 0
                        timestamp_start = datetime.datetime.now()
                        
                        while episode < config['total_episodes']:
                            print('\n----- Episode', str(episode+1), 'of', str(config['total_episodes']))
                            epsilon = 1.0 - (episode / config['total_episodes'])  # set the epsilon for this episode according to epsilon-greedy policy
                            simulation_time, training_time = Simulation.run(episode, epsilon)  # run the simulation
                            print('Simulation time:', simulation_time, 's - Training time:', training_time, 's - Total:', round(simulation_time+training_time, 1), 's')
                            episode += 1

                        print("\n----- Start time:", timestamp_start)
                        print("----- End time:", datetime.datetime.now())
                        print("----- Session info saved at:", path)

                        Model.save_model(path)

                        copyfile(src='training_settings.ini', dst=os.path.join(path, 'training_settings.ini'))
                        write_file_name = f"episodes{episode_chosen}lr{lr_chosen}layers{num_layer_chosen}batch{batch_chosen}epochs{training_epochs_chosen}.txt"
                        with open(os.path.join(path, write_file_name), 'w') as f:
                            f.write("done")
                            

                        Visualization.save_data_and_plot(data=Simulation.reward_store, filename='reward', xlabel='Episode', ylabel='Cumulative negative reward')
                        Visualization.save_data_and_plot(data=Simulation.cumulative_wait_store, filename='delay', xlabel='Episode', ylabel='Cumulative delay (s)')
                        Visualization.save_data_and_plot(data=Simulation.avg_queue_length_store, filename='queue', xlabel='Episode', ylabel='Average queue length (vehicles)')

            