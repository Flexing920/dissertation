import xml.etree.ElementTree as ET

f = "code.rou.xml"
vtype = '<vType id="emergency" length="20.00" vClass="emergency"/>'
s = '<vehicle depart="1" id="17999" type="emergency" color="0,0,1"><route edges="right2C2 right2C2.100.00 C2top2" /></vehicle>'
tree = ET.parse(f)
root = tree.getroot()
# 
e_vtype = ET.fromstring(vtype)
e_veh = ET.fromstring(s)

root.insert(0, e_vtype)
# root.insert(0, e_vtype)
# root.insert(e, 0)
# tree.write("t.xml")
vehs = root.findall("vehicle")
print(len(vehs))
j = -1
for i in range(len(vehs)):
    if vehs[i].attrib["id"] == "2" and vehs[i].attrib["depart"]=="1.00":
        j = i
        break
root.insert(j, e_veh)

tree.write("t.xml")
    
