To configure a flow on switch s1, use the following command:

```bash
ofctl add-flow s1 \
in_port=1,ip,nw_src=10.0.1.2,nw_dst=10.0.4.2,actions=mod_dl_src:0A:00:0C:01:00:03,mod_dl_dst:0A:00:0D:01:00:03,output=3

Explanation of the command:

in_port=1: Matches frames incoming on port 1.
ip: Matches the IP protocol.
nw_src=10.0.1.2: Matches packets with the source IP address 10.0.1.2.
nw_dst=10.0.4.2: Matches packets with the destination IP address 10.0.4.2.
mod_dl_src:0A:00:0C:01:00:03: Modifies the source MAC address of the packet to 0A:00:0C:01:00:03.
mod_dl_dst:0A:00:0D:01:00:03: Modifies the destination MAC address of the packet to 0A:00:0D:01:00:03 and directs it to the switch port with that MAC address.
output=3: Sends the packet out on port 3.