import ns.internet_apps
import ns.core
import ns.network
import ns.internet
import ns.point_to_point
import ns.applications
import ns.internet
import ns.csma
#import ipv4_alternate_routing_helper


def main (argv):

	cmd = ns.core.CommandLine ()
	sampleMetric = 1
	cmd.AddValue ("AlternateCost",
                "This metric is used in the example script between n3 and n1 ", 
                "1")

	cmd.Parse (sys.argv)
	print "Create nodes."
	c = ns.network.NodeContainer ()
	n0n2 = ns.network.NodeContainer ()
	n1n2 = ns.network.NodeContainer ()
	n3n2 = ns.network.NodeContainer ()
	n1n3 = ns.network.NodeContainer ()
	n0 = ns.network.Node()
	n1 = ns.network.Node()
	n2 = ns.network.Node()
	n3 = ns.network.Node()

	n0n2.Add(n0)
	n0n2.Add(n2)
	n1n2.Add(n1)
	n1n2.Add(n2)
	n3n2.Add(n3)
	n3n2.Add(n2)
	n1n3.Add(n1)
	n1n3.Add(n3)
	c.Add(n0)
	c.Add(n1)
	c.Add(n2)
	c.Add(n3)
	#n0n2 = ns.network.NodeContainer (c.Get (0), c.Get (2))
	#n1n2 = ns.network.NodeContainer (c.Get (1), c.Get (2))
	#n3n2 = ns.network.NodeContainer (c.Get (3), c.Get (2))
	#n1n3 = ns.network.NodeContainer (c.Get (1), c.Get (3))

	print "Create channels."
	p2p = ns.point_to_point.PointToPointHelper ()
	p2p.SetDeviceAttribute ("DataRate", ns.core.StringValue ("5Mbps"))
	p2p.SetChannelAttribute ("Delay", ns.core.StringValue ("2ms"))
	d0d2 = p2p.Install (n0n2)
	d1d2 = p2p.Install (n1n2)

	p2p.SetDeviceAttribute ("DataRate", ns.core.StringValue ("1500kbps"))
	p2p.SetChannelAttribute ("Delay", ns.core.StringValue ("10ms"))
 	d3d2 = p2p.Install (n3n2)
 	p2p.SetChannelAttribute ("Delay", ns.core.StringValue ("100ms"))
 	d1d3 = p2p.Install (n1n3)

 	stack = ns.internet.InternetStackHelper ()
	stack.Install (c)

	print "Assign IP Addresses."
	ipv4 = ns.internet.Ipv4AddressHelper ()
	ipv4.SetBase (ns.network.Ipv4Address ("10.0.0.0"), ns.network.Ipv4Mask ("255.255.255.0"))
	i0i2 = ipv4.Assign (d0d2)
	ipv4.SetBase (ns.network.Ipv4Address ("10.1.1.0"), ns.network.Ipv4Mask ("255.255.255.0"))
	i1i2 = ipv4.Assign (d1d2)
	ipv4.SetBase (ns.network.Ipv4Address ("10.2.2.0"), ns.network.Ipv4Mask ("255.255.255.0"))
	i3i2 = ipv4.Assign (d3d2)
	ipv4.SetBase (ns.network.Ipv4Address ("10.3.3.0"), ns.network.Ipv4Mask ("255.255.255.0"))
	i1i3 = ipv4.Assign (d1d3)
	i1i3.SetMetric (0, sampleMetric)
	i1i3.SetMetric (1, sampleMetric)
	ns.internet.Ipv4GlobalRoutingHelper.PopulateRoutingTables()
	print "Create Applications."
	# 
	# Create a BulkSendApplication and install it on node 0
	# 
	port = 9  # well-known echo port number

	onoff = ns.applications.OnOffHelper ("ns3::UdpSocketFactory", ns.network.InetSocketAddress (i1i2.GetAddress (0), port))

	# Set the amount of data to send in bytes.  Zero is unlimited. ?
	onoff.SetConstantRate (ns.network.DataRate ("300b/s"))
	apps = onoff.Install (c.Get (3))
	apps.Start (ns.core.Seconds (1.1))
	apps.Stop (ns.core.Seconds (10.0))

	##onoff.SetConstantRate (DataRate ("448kb/s"));

	# 
	# Create a packet sink to receive these packets
	# 
	sink = ns.applications.PacketSinkHelper ("ns3::UdpSocketFactory", ns.network.InetSocketAddress (ns.network.Ipv4Address.GetAny (), port))
	apps = sink.Install (c.Get (1))
	apps.Start (ns.core.Seconds (1.1))
	apps.Stop (ns.core.Seconds (10.0))


	ascii = ns.network.AsciiTraceHelper ()
	p2p.EnableAsciiAll (ascii.CreateFileStream ("simple-alternate-routing.tr"))
	p2p.EnablePcapAll ("simple-alternate-routing")

	print "Run Simulation."
	ns.core.Simulator.Run ()
	ns.core.Simulator.Destroy ()
	print "Done."



	# ns.core.Simulator.Destroy ()
if __name__ == '__main__':
    import sys
    main (sys.argv)

