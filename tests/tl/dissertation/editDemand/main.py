import xml.etree.ElementTree as ET
import random
import numpy as np

duration = [900, 1200, 1500, 1800]
edge_length = 100
length = random.choice(np.arange(10, edge_length, 5))
d = random.choice(duration)
edges = ["C2C1", "C1C0"]
# root = ET.Element('Summary')
# sub = ET.SubElement(root, 'TextSummary')
# sub.set('Status', 'Completed')
data="random.rou.xml"
tree = ET.parse(data)
root = tree.getroot()
# vehs = tree.findall("vehicle")
# find the vehicle with id=2
id = random.choice(np.arange(0, 4, 1))
id = 2
veh = root.find(".//vehicle[@id='{}']".format(id))
# add color to vehicle
veh.set("color", "1,0,0")
# add stop element from string
s = '<stop lane="{}_1" duration="{}" endPos="{}" parking="false" />'.format(edges[0], d, length)
print(s)
stop_element = ET.fromstring(s)
veh.append(stop_element)
tree.write("test.rou.xml")


