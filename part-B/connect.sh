#!/usr/bin/env bash

# Sets bridge s1 to use OpenFlow 1.3
ovs-vsctl set bridge s1 protocols=OpenFlow13 

# Sets bridge s2 to use OpenFlow 1.3
ovs-vsctl set bridge s2 protocols=OpenFlow13 

# Sets bridge s3 to use OpenFlow 1.3
ovs-vsctl set bridge s3 protocols=OpenFlow13 

# Sets bridge r1 to use OpenFlow 1.3
ovs-vsctl set bridge r1 protocols=OpenFlow13

# Sets bridge r2 to use OpenFlow 1.3
ovs-vsctl set bridge r2 protocols=OpenFlow13 

# Print the protocols that each switch supports
for switch in s1 s2 s3 r1 r2;
do
  protos=$(ovs-vsctl get bridge $switch protocols)
  echo "Switch $switch supports $protos"
done

# Avoid having to write "-O OpenFlow13" before all of your ovs-ofctl commands.
ofctl='ovs-ofctl -O OpenFlow13'

# Alice <--> Bob

# OVS rules for s1
$ofctl add-flow s1 \
    actions=output:2

$ofctl add-flow s1 \
    actions=output:1

# OVS rules for r1
$ofctl add-flow r1 \
    dl_src=0A:00:0E:FE:00:02, dl_dst=0A:00:01:01:00:01, action=output:2

$ofctl add-flow r1 \
    dl_src=0A:00:04:01:00:01, dl_dst=0A:00:0A:01:00:02, actions=output:1

# OVS rules for s2
$ofctl add-flow s2 \
    actions=output:2

$ofctl add-flow s2 \
    actions=output:1


# Print the flows installed in each switch
for switch in s1 s2 s3 r1 r2;
do
    echo "Flows installed in $switch:"
    $ofctl dump-flows $switch
    echo ""
done
