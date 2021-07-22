import traci
import traci.constants as tc

traci.start(["sumo", "-c", "my.sumocfg"])
traci.vehicle.subscribe(vehID, (tc.VAR_ROAD_ID, tc.VAR_LANEPOSITION))
print(traci.vehicle.getSubscriptionResults(vehID))
for step in range(3):
   print("step", step)
   traci.simulationStep()
   print(traci.vehicle.getSubscriptionResults(vehID))
traci.close()