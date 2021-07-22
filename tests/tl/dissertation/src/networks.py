import os

base_dir = "networks"

single_intersection = {"net_file": os.path.join(base_dir, 
                                    "single_intersection/single_intersection.net.xml"), 
                        "route_file": os.path.join(base_dir, 
                                    "single_intersection/single_intersection.rou.xml")
                                    ,
                        "sumocfg_file": os.path.join(base_dir, 
                                    "single_intersection/sumo.sumocfg")
                                    }
