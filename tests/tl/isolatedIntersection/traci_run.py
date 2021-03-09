import os, sys, optparse

NOGUI = True
CONFIG_FILE_NAME = "my.sumocfg"

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=NOGUI, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

def run():
    step = 0
    # while there is vehicle in the network
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        # det_vehs = traci.inductionloop.getLastStepVehicleIDs("det_0")
        # for veh in det_vehs:
        #     print(f"veh: {veh}")
        step += 1

    traci.close()
    sys.stdout.flush()

if __name__ == "__main__":
    options = get_options()
    print(options)
    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    data_dir = os.path.join(os.getcwd(), "data")
    # sumoBinary = 'sumo'
    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", os.path.join(data_dir, CONFIG_FILE_NAME),
                             "--tripinfo-output", os.path.join(data_dir, "tripinfo.xml")])
    run()
    
print("Done!")