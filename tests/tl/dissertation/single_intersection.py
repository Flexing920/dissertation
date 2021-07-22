import argparse
import os
import sys
from datetime import datetime

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

import traci
from src.environment import SumoEnvironment
from src.WebstersTSC import WebstersTSC
from src.pretimedTSC import pretimedTSC
from src.networks import single_intersection

# Constants
MODES = ["pretimedTSC", "WebstersTSC", "maxpressureTSC", "dqnTSC"]
network_name = "single_intersection"
if __name__ == '__main__':
    mode = MODES[1]
    if mode == "pretimedTSC":
        print(f"mode: {mode}")
        sumocfg = single_intersection["sumocfg_file"]
        net_file = single_intersection["net_file"]
        route_file = single_intersection["route_file"]
        prs = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                  description="""Pretimed Single-Intersection""")
        prs.add_argument("-a", dest="alpha", type=float, default=0.1, required=False, help="Alpha learning rate.\n")
        prs.add_argument("-g", dest="gamma", type=float, default=0.99, required=False, help="Gamma discount rate.\n")
        prs.add_argument("-e", dest="epsilon", type=float, default=0.05, required=False, help="Epsilon.\n")
        prs.add_argument("-me", dest="min_epsilon", type=float, default=0.005, required=False, help="Minimum epsilon.\n")
        prs.add_argument("-d", dest="decay", type=float, default=1.0, required=False, help="Epsilon decay.\n")
        prs.add_argument("-mingreen", dest="min_green", type=int, default=10, required=False, help="Minimum green time.\n")
        prs.add_argument("-maxgreen", dest="max_green", type=int, default=50, required=False, help="Maximum green time.\n")
        prs.add_argument("-gui", action="store_true", default=False, help="Run with visualization on SUMO.\n")
        prs.add_argument("-fixed", action="store_true", default=True, help="Run with fixed timing traffic signals.\n")
        prs.add_argument("-ns", dest="ns", type=int, default=42, required=False, help="Fixed green time for NS.\n")
        prs.add_argument("-we", dest="we", type=int, default=42, required=False, help="Fixed green time for WE.\n")
        prs.add_argument("-s", dest="seconds", type=int, default=5000, required=False, help="Number of simulation seconds.\n")
        prs.add_argument("-v", action="store_true", default=False, help="Print experience tuple.\n")
        prs.add_argument("-runs", dest="runs", type=int, default=5, help="Number of runs.\n")

        args = prs.parse_args()
        experiment_time = str(datetime.now()).split('.')[0]
        out_csv = f'outputs/single_intersection/{experiment_time}'
        
        env = SumoEnvironment(net_file=net_file,
                          route_file=route_file,
                          out_csv_name=out_csv,
                          use_gui=args.gui,
                          num_seconds=args.seconds,
                          min_green=args.min_green,
                          max_green=args.max_green,
                          max_depart_delay=0)

        for run in range(1, args.runs+1):

            initial_states = env.reset()
            done = {'__all__': False}
            if args.fixed:
                while not done['__all__']:
                    _, _, done, _ = env.step({})
            else:
                pass
            env.save_csv(out_csv, run)
            env.close()
    elif mode == "WebstersTSC":
        pass

    