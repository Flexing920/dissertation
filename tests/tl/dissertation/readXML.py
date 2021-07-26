import xml.etree.ElementTree as ET
f = "random.rou.xml"
tree = ET.parse(f)
root = tree.getroot()
vehs = root.findall("vehicle")
for i in range(5):
    print(root[i].attrib["depart"])

# vtype = root.findall("vType")[0]
# print(vtype.attrib["id"])
# print(vtype.attrib["length"])
# vtype.set("length", 30)
# print(vtype.attrib["length"])

emergencyVtypeEle = ET.fromstring(f'<vType id="emergency" accel="0.8" decel="4.5" length="30" maxSpeed="30" color="0,1,0"/>')
root.insert(0,emergencyVtypeEle)
# veh.append(el_stop)
# vehs.insert(0, emergencyVtypeEle)
tree.write("test.rou.xml")


