from src.networkdata import NetworkData
import sumolib
import xml.etree.ElementTree as ET
import random
import numpy as np

net_fp = "networks/grid2/net.net.xml"
cfg_fp = "networks/grid2/my.my.sumocfg"
route_xml = "networks/grid2/random.rou.xml"


def incident_occur_time(last_departure):
    # define the incident occurance time
    incident_occur_interval = last_departure/3
    # print(int(incident_occur_interval))
    incident_time = round(random.choice(np.arange(incident_occur_interval, 2 * incident_occur_interval, 1)), 2)
    ret = str(round(incident_time, 2))
    ret = ret[:-2] + "00"
    print(f"incident_time is {ret}")

    return ret

# tree is the parsed rou.xml
def find_veh_element(tree, incident_time):
    vehs = tree.findall("vehicle")
    for x in vehs:
        if x.attrib["depart"] == incident_time:
            return x

def get_veh_edges(veh):
    # find vehicle id with incident_time
    
    print(veh.attrib["id"])

    # get the edges from the veh element in string format
    veh_edges = veh.findall('route')[0].attrib["edges"]
    veh_edges = veh_edges.split()
    return veh_edges

def get_potential_incident_edges(veh_edges, incident_edges):
    l = []
    for e in veh_edges:
        if e in incident_edges:
            l.append(e)
    return l

if __name__ == "__main__":
    # get the next edge of an edge
    net = sumolib.net.readNet(net_fp)
    edge_id = "C1B1"
    # https://sumo.dlr.de/daily/pydoc/sumolib.net.edge.html
    end_node = net.getEdge(edge_id).getToNode()
    print(end_node.getID())
    
    # test how to get a route from an edge to a node
    origin_edge = "right1C1"
    
    
    # print(nextEdges.keys())
    # temp = []
    # for key in nextEdges.keys():
    #     temp = key
    # print(temp.getToNode().getID())


    # nd = NetworkData(net_fp)
    # origin_edges = nd.find_origin_edges()
    # destination_edges = nd.find_destination_edges()
    # # print(origin_edges)
    # # print(destination_edges)
    # incident_edges = nd.incidentEdges
    # print(f"incident_edges = {incident_edges}")

    # # read the last vehicle route information for the last departure time 
    # tree = ET.parse(route_xml)
    # veh_last = tree.findall("vehicle")[-1]
    # last_departure = float(veh_last.attrib["depart"])
    # # print(last_departure)



    # # incident parameters
    # durations = [900, 1200, 1500, 1800]
    # edge_length = 100
    # length = random.choice(np.arange(10, edge_length, 5))
    # duration = random.choice(durations)


    # incident_time = incident_occur_time(last_departure)

    # veh = find_veh_element(tree, incident_time)
    # veh_edges = get_veh_edges(veh)
    # print(veh_edges)
    
    # test_incident_edges = get_potential_incident_edges(veh_edges, incident_edges)

    # print(test_incident_edges)

    # if len(test_incident_edges) >= 1:
    #     target_e = random.choice(test_incident_edges)
    #     n_lanes = nd.edge_data[target_e]["nlanes"]
    #     lane = random.choice(np.arange(0, n_lanes, 1))
    #     print(target_e, lane)

    #     # generate stop string for inserting 
    #     s = '<stop lane="{}_{}" duration="{}" endPos="{}" parking="false" />'.format(target_e, lane,duration, length)

    #     if s is not None:
    #         print(s)
    #         stop_element = ET.fromstring(s)
    #         veh.append(stop_element)
    #         veh.set("color", "1,0,0")
    #         tree.write("code.rou.xml")

    

    
