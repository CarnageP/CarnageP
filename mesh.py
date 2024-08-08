from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_mesh_topology(num_nodes):
    "Create a Mesh network topology with the specified number of nodes."
    net = Mininet(controller=Controller, switch=OVSKernelSwitch)

    print(f"*** Creating a mesh network with {num_nodes} nodes")

    # Add mesh stations
    mesh_stations = []
    for i in range(1, num_nodes + 1):
        sta = net.addStation(f'sta{i}', ip=f"10.0.0.{i}/8", position=f"{i*10},50,0", \
                             range=100, meshID="meshNet")
        mesh_stations.append(sta)

    # Add a controller
    c0 = net.addController('c0')

    # Configure WiFi nodes
    net.configureWifiNodes()

    # Set mobility model (optional)
    net.setMobilityModel(time=0, model='RandomWaypoint', min_x=0, max_x=100, min_y=0, max_y=100, min_v=0.5, max_v=1.0)

    print("*** Starting network")
    net.build()
    c0.start()

    # Mesh links automatically created when mesh nodes are in range
    net.meshRouting('hybrid')  # Set mesh routing protocol

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    
    # Test with different node counts
    for num_nodes in [10, 25, 50, 100]:
        create_mesh_topology(num_nodes)
