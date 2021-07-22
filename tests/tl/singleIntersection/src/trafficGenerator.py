import random
import numpy as np

class TrafficGenerator:

    def __init__(self, base_demand, turning_ratio_filename, 
            distribution_lookup_table,load_turning_ratio, 
            time_interval, random_seed):

        self.base_demand = base_demand
        self.distribution_table = distribution_lookup_table
        self.time_interval = time_interval
        self.random_seed = random_seed
        self.n_intervals = len(distribution_lookup_table)
        if load_turning_ratio:
            self.turning_ratio = \
                            self._load_turning_ratio(turning_ratio_filename)
        else:
            self.turning_ratio = self._generate_turning_ratio()

        self.timings = self._generate_timings()
        # self.demand = self._get_demand()

    def generate_routefile(self, output_dir):
        interval_counter = 0
        with open(output_dir, "w") as routes:
            # define the route info
            print("""<routes>
                <vType accel="1.0" decel="4.5" id="standard_car" length="5.0" minGap="2.5" maxSpeed="25" sigma="0.5" />
                <route id="W_N" edges="W2TL TL2N"/>
                <route id="W_E" edges="W2TL TL2E"/>
                <route id="W_S" edges="W2TL TL2S"/>
                <route id="N_W" edges="N2TL TL2W"/>
                <route id="N_E" edges="N2TL TL2E"/>
                <route id="N_S" edges="N2TL TL2S"/>
                <route id="E_W" edges="E2TL TL2W"/>
                <route id="E_N" edges="E2TL TL2N"/>
                <route id="E_S" edges="E2TL TL2S"/>
                <route id="S_W" edges="S2TL TL2W"/>
                <route id="S_N" edges="S2TL TL2N"/>
                <route id="S_E" edges="S2TL TL2E"/>""", file=routes)
            
            # iterate timings to generate demand
            for car_counter, step in enumerate(self.timings):
                if step != 0 and step % self.time_interval == 0:
                    interval_counter += 1

                # randomly choose an approach
                approach = random.choice(["north","east","south","west"])

                # update the movement ratio for each approach
                movement_ratio_north = self.turning_ratio[interval_counter][0]
                movement_ratio_east = self.turning_ratio[interval_counter][1]
                movement_ratio_south = self.turning_ratio[interval_counter][2]
                movement_ratio_west = self.turning_ratio[interval_counter][3]

                if approach == "north":
                    movement = np.random.choice(["left", "thru", "right"],1,p=movement_ratio_north)[0]
                    if movement == "left":
                        print('    <vehicle id="N_E_%i" type="standard_car" route="N_E" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    elif movement == "thru":
                        print('    <vehicle id="N_S_%i" type="standard_car" route="N_S" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    else:
                        print('    <vehicle id="N_W_%i" type="standard_car" route="N_W" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)


                    
                elif approach == "east":
                    movement = np.random.choice(["left", "thru", "right"],1,p=movement_ratio_east)[0]
                    if movement == "left":
                        print('    <vehicle id="E_S_%i" type="standard_car" route="E_S" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    elif movement == "thru":
                        print('    <vehicle id="E_W_%i" type="standard_car" route="E_W" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    else:
                        print('    <vehicle id="E_N_%i" type="standard_car" route="E_N" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                
                elif approach == "south":
                    movement = np.random.choice(["left", "thru", "right"],1,p=movement_ratio_south)[0]
                    if movement == "left":
                        print('    <vehicle id="S_W_%i" type="standard_car" route="S_W" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    elif movement == "thru":
                        print('    <vehicle id="S_N_%i" type="standard_car" route="S_N" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    else:
                        print('    <vehicle id="S_E_%i" type="standard_car" route="S_E" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                
                else:
                    movement = np.random.choice(["left", "thru", "right"],1,p=movement_ratio_west)[0]
                    if movement == "left":
                        print('    <vehicle id="W_N_%i" type="standard_car" route="W_N" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    elif movement == "thru":
                        print('    <vehicle id="W_E_%i" type="standard_car" route="W_E" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    else:
                        print('    <vehicle id="W_S_%i" type="standard_car" route="W_S" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
            print("</routes>", file=routes)

    # implement after determing the data source
    def _load_turning_ratio(self, filename):
        pass

    # normalize a 3-item array: left, thru, right    
    def _normalize_array(self, turning_ratio_array):
        sum = np.sum(turning_ratio_array)
        turning_ratio_array = np.round(turning_ratio_array/sum, 2)
        temp_max = np.max(turning_ratio_array)
        temp_min = np.min(turning_ratio_array)
        turning_ratio_array[0] = 1 - temp_max - temp_min
        turning_ratio_array[1] = temp_max
        turning_ratio_array[2] = temp_min
        return turning_ratio_array

    # def _generate_random_seeds(n):
    #     seeds = []
    #     for _ in range(n):
    #         seeds.append(random.randint(1, 10000))
    #     return seeds

    def _generate_turning_ratio(self):
        np.random.seed(self.random_seed)
        turningRatio = np.random.rand(self.n_intervals, 4, 3)
        for i in range(turningRatio.shape[0]):
            for j in range(turningRatio.shape[1]):
                turningRatio[i][j] = \
                        self._normalize_array(turningRatio[i][j])
        return turningRatio

    # randomly generate timestep for demand
    def _generate_timings(self):
        random.seed(self.random_seed)
        demand_interval = [int(x*self.base_demand) \
                            for x in self.distribution_table]
        demand = []
        counter = 0
        for i in demand_interval:
            for _ in range(i):
                demand.append(random.randint(counter*self.time_interval + 1, \
                    (counter+1)*self.time_interval))
            counter += 1

        demand.sort()
        return np.array(demand)

