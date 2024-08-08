from mininet.net import Mininet
from mininet.node import Controller, OVSController, OVSKernelAP
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.wifi.link import mesh

def meshNetwork():
    net = Mininet(controller=Controller, accessPoint=OVSKernelAP)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='meshNet', mode='g', channel='1')
    sta1 = net.addStation('sta1')
    sta2 = net.addStation('sta2')
    sta3 = net.addStation('sta3')
    c1 = net.addController('c1', controller=OVSController)

    info("*** Configuring WiFi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(sta1, intf='sta1-wlan0', cls=mesh, ssid='meshNet')
    net.addLink(sta2, intf='sta2-wlan0', cls=mesh, ssid='meshNet')
    net.addLink(sta3, intf='sta3-wlan0', cls=mesh, ssid='meshNet')

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    meshNetwork()
