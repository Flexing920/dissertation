from trafficGenerator import TrafficGenerator


if __name__=="__main__":
    demand = TrafficGenerator(500, "none", [0.5, 0.8, 1, 0.7], False, 900, 10000)
    demand.generate_routefile("../network/episode_routes.rou.xml")