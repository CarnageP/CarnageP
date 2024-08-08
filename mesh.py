from mininet.node import Controller
from mininet.wifi.node import Station, AccessPoint
from mininet.wifi.link import wmediumd
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_mesh_topology(num_nodes):
    net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=wmediumd, build=False)

    print(f"*** Creating a mesh network with {num_nodes} nodes")

    # Create nodes
    nodes = []
    for i in range(1, num_nodes + 1):
        sta = net.addStation(f'sta{i}', ip=f"10.0.0.{i}/8", position=f"{i*10},50,0", range=100, meshID="meshNet")
        nodes.append(sta)

    # Add an Access Point
    ap = net.addAccessPoint('ap', ssid='meshNet', mode='g', channel='1', position='50,50,0')

    # Add a Controller
    c0 = net.addController('c0')

    # Configure nodes and access point
    net.configureWifiNodes()
    net.setMobilityModel(time=0, model='RandomWaypoint', min_x=0, max_x=100, min_y=0, max_y=100, min_v=0.5, max_v=1.0)

    print("*** Starting network")
    net.build()
    c0.start()

    ap.start([c0])

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    num_nodes = 10  # Change to 10, 25, 50, 100 as needed
    create_mesh_topology(num_nodes)
