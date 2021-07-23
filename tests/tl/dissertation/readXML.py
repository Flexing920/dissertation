import xml.etree.ElementTree as ET
f = "code.rou.xml"
tree = ET.parse(f)
root = tree.getroot()
vehs = root.findall("vehicle")
t = "900.00"
edge_1 = "top2C2"
edge_2 = "C1B1.100.00"
id = "no"
edges = "empty"
for i in range(len(vehs)):
    route = vehs[i].find("route")
    temp = route.attrib["edges"]
    # print(temp)
    l = temp.split()
    # print(l)
    if edge_1 in l and edge_2 in l:
        print("yes")
        id = vehs[i].attrib["id"]
        edges = temp
        print(f"id = {id} and edges = {edges}")
        break