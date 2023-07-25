#!/usr/bin/python

"""Topology with 10 switches and 10 hosts
"""

from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel

class CSLRTopo( Topo ):
    def __init__( self ):
                "Create Topology"

                # Initialize topology
                Topo.__init__( self )

                # Add hosts
                alice = self.addHost('alice')
                bob = self.addHost('bob')
                carol = self.addHost('carol')

                # Add switches
                s1 = self.addSwitch( 's1', listenPort=6634 )
                s2 = self.addSwitch( 's2', listenPort=6635 )
                s3 = self.addSwitch( 's3', listenPort=6636 )
                r1 = self.addSwitch( 'r1', listenPort=6637 )
                r2 = self.addSwitch( 'r2', listenPort=6638 )

                # Add links between hosts and switches
                self.addLink( alice, s1 ) # alice-eth0 <-> s1-eth1
                self.addLink( bob, s2 ) # bob-eth0 <-> s2-eth1
                self.addLink( carol, s3) # carol-eth0 <-> s3-eth1

                # Add links between switches, with bandwidth 100Mbps
                self.addLink( s1, r1, bw=100 )
                self.addLink( s2, r1, bw=100 )
                self.addLink( s2, r2, bw=100 )
                self.addLink( s3, r2, bw=100 )

def run():
        "Create and configure network"
        topo = CSLRTopo()
        net = Mininet( topo=topo, link=TCLink, controller=None )

        # Set interface IP and MAC addresses for hosts
        alice = net.get( 'alice' )
        alice.intf( 'alice-eth0' ).setIP( '10.1.1.17', 24 )
        alice.intf( 'alice-eth0' ).setMAC( 'aa:aa:aa:aa:aa:aa' )

        bob = net.get( 'bob' )
        bob.intf( 'bob-eth0' ).setIP( '10.4.4.48', 24 )
        bob.intf( 'bob-eth0' ).setMAC( 'b0:b0:b0:b0:b0:b0' )

        carol = net.get( 'carol' )
        carol.intf( 'carol-eth0' ).setIP( '10.6.6.69', 24 )
        carol.intf( 'carol-eth0' ).setMAC( 'cc:cc:cc:cc:cc:cc' )

        # Set interface MAC address for switches (NOTE: IP
        # addresses are not assigned to switch interfaces)
        s1 = net.get( 's1' )
        s1.intf( 's1-eth1' ).setMAC( '0A:00:00:01:00:01' )
        s1.intf( 's1-eth2' ).setMAC( '0A:00:0A:01:00:02' )

        s2 = net.get( 's2' )
        s2.intf( 's2-eth1' ).setMAC( '0A:00:01:01:00:01' )
        s2.intf( 's2-eth2' ).setMAC( '0A:00:0A:FE:00:02' )
        s2.intf( 's2-eth3' ).setMAC( '0A:00:0C:01:00:03' )

        s3 = net.get( 's3' )
        s3.intf( 's3-eth1' ).setMAC( '0A:00:02:01:00:01' )
        s3.intf( 's3-eth2' ).setMAC( '0A:00:0B:FE:00:02' )

        r1 = net.get( 'r1' )
        r1.intf( 'r1-eth1' ).setMAC( '0A:00:04:01:00:01' )
        r1.intf( 'r1-eth2' ).setMAC( '0A:00:0E:FE:00:02' )

        r2 = net.get( 'r2' )
        r2.intf( 'r2-eth1' ).setMAC( '0A:00:05:01:00:01' )
        r2.intf( 'r2-eth2' ).setMAC( '0A:00:10:FE:00:02' )

        net.start()

        # Add routing table entries for hosts (NOTE: The gateway
		# IPs 10.0.X.1 are not assigned to switch interfaces)
        alice.cmd( 'route add default gw 10.1.1.14 dev alice-eth0' )
        bob.cmd( 'route add default gw 10.4.4.14 dev bob-eth0' )
        carol.cmd( 'route add default gw 10.6.6.46 dev carol-eth0' )

        # Add arp cache entries for hosts
        alice.cmd( 'arp -s 10.1.1.14 0A:00:00:01:00:01 -i alice-eth0' )
        bob.cmd( 'arp -s 10.4.4.14 0A:00:0A:FE:00:02 -i bob-eth0' )
        carol.cmd( 'arp -s 10.6.6.46 0A:00:0B:FE:00:02 -i carol-eth0' )

        # Open Mininet Command Line Interface
        CLI(net)

        # Teardown and cleanup
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
