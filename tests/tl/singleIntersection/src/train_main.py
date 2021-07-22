import traci
from utils import set_sumo, import_train_settings
from trafficGenerator import TrafficGenerator

training_settings = import_train_settings("train_settings.ini")
gui = training_settings["gui"]
sumocfg_filename = training_settings["sumocfg_filename"]


for i in range(5):
    demand = TrafficGenerator(500, "none", [0.5, 0.8, 1, 0.7], False, 900, i * 100)
    demand.generate_routefile("../network/episode_routes.rou.xml")
    traci.start(set_sumo(gui, sumocfg_filename))

    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step += 1

    traci.close()
    print(f"Simulation {i} is done!!!")