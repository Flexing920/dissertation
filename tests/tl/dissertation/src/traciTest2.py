import os, sys, optparse

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    print(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

def sendEmergency():
    targetEdge = "B1B0"
    startEdge = "top0A2"
    stage = traci.simulation.findRoute(startEdge, targetEdge)
    route = stage.edges
    traci.route.add("Savingtrip", route)
    traci.vehicle.add("99999999", "Savingtrip")
    traci.vehicle.setStop("99999999", "B1B0", 45, 0, 1800)

def run():
    step = 0
    vid = "768"
    # stopPos = 42
    stopLaneID = "B1B0_1"
    stopTime = 0
    stopPos = None
    stopDict = {}
    emerVehScheduled = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        if vid in traci.vehicle.getIDList():
            pos = traci.vehicle.getPosition(vid)
            if stopPos is None:
                stopPos = pos     
            elif stopPos and stopPos == pos:
                stopTime += 1
                stopDict[stopPos] = stopTime
                if stopTime >= 300 and emerVehScheduled == 0:
                    print(traci.vehicle.getLaneID(vid))
                    print("emergency vehicle is needed")
                    sendEmergency()
                    emerVehScheduled = 1
            else:
                stopTime = 0
                stopPos = pos

            
            
        traci.simulationStep()

        step += 1
    print(stopDict)
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

    sumoBinary = 'sumo-gui'
    # traci starts sumo as a subprocess and then this script connects and runs
    cfg = "../networks/grid2/my.sumocfg"
    traci.start([sumoBinary, "-c", cfg,
                             "--tripinfo-output", "tripinfo.xml"])
    run()
    
print("Done!")