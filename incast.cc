/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include <fstream>
#include <iostream>
#include <string>

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/stats-module.h"
#include "ns3/traffic-control-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("IncastScript");


std::string outputRep = "outputs/";    // base name for trace files, etc

static void
CwndChange (Ptr<OutputStreamWrapper> stream, uint32_t oldCwnd, uint32_t newCwnd)
{
  //NS_LOG_UNCOND (Simulator::Now ().GetSeconds () << "\t" << newCwnd);
  *stream->GetStream () << Simulator::Now ().GetSeconds () << "," << oldCwnd << "," << newCwnd << std::endl;
}

static void
TraceCwnd (int nbSenders)    // Trace changes to the congestion window ; N :: number of senders
{
  for(int i=0; i<nbSenders; ++i)
	{
	  std::ostringstream filenameStream;
	  filenameStream << outputRep << "cwnd-" << i <<".txt";
	  std::string cwndFilename = filenameStream.str();

	  std::ostringstream pathStream;
	  pathStream << "/NodeList/" << i <<"/$ns3::TcpL4Protocol/SocketList/0/CongestionWindow";
	  std::string path = pathStream.str();

	  AsciiTraceHelper ascii;
	  Ptr<OutputStreamWrapper> stream = ascii.CreateFileStream (cwndFilename);
	  *stream->GetStream () << "time"<< "," << "oldCwnd" << "," << "cwnd" << std::endl;
	  Config::ConnectWithoutContext (path, MakeBoundCallback (&CwndChange,stream));
	}

}

static void
RxDrop (Ptr<PcapFileWrapper> file, Ptr<const Packet> p)
{
  NS_LOG_UNCOND ("RxDrop at " << Simulator::Now ().GetSeconds ());
  file->Write (Simulator::Now (), p);
}


// New Tracer

//N --> switch

static void
SojournTracer (Ptr<OutputStreamWrapper>stream, Time val)
{
  *stream->GetStream () << Simulator::Now ().GetSeconds () << "," << val.ToDouble (Time::MS) << " ms" << std::endl;
}

static void
TraceSojourn (std::string sojournTrFileName, int N)
{
  AsciiTraceHelper ascii;
  if (sojournTrFileName.compare ("") == 0)
    {
      NS_LOG_DEBUG ("No trace file for sojourn provided");
      return;
    }
  else
    {
	  std::ostringstream pathStream;
	  pathStream << "/NodeList/" << N <<"/$ns3::TrafficControlLayer/RootQueueDiscList/" << N << "/SojournTime";
	  std::string path = pathStream.str();
      Ptr<OutputStreamWrapper> stream = ascii.CreateFileStream (sojournTrFileName.c_str ());
      *stream->GetStream () << "time"<< "," << "sojournTime" << std::endl;
      Config::ConnectWithoutContext (path, MakeBoundCallback (&SojournTracer, stream));
    }
}

static void
QueueLengthTracer (Ptr<OutputStreamWrapper>stream, uint32_t oldval, uint32_t newval)
{
  *stream->GetStream () << Simulator::Now ().GetSeconds () << "," << oldval << "," << newval << std::endl;
}

static void
TraceQueueLength (std::string queueLengthTrFileName, int N)
{
  AsciiTraceHelper ascii;
  if (queueLengthTrFileName.compare ("") == 0)
    {
      NS_LOG_DEBUG ("No trace file for queue length provided");
      return;
    }
  else
    {
	  std::ostringstream pathStream;
	  pathStream << "/NodeList/" << N <<"/$ns3::TrafficControlLayer/RootQueueDiscList/" << N << "/PacketsInQueue";
	  std::string path = pathStream.str();
      Ptr<OutputStreamWrapper> stream = ascii.CreateFileStream (queueLengthTrFileName.c_str ());
      *stream->GetStream () << "time"<< "," << "oldval" << "," << "newval" << std::endl;
      Config::ConnectWithoutContext (path, MakeBoundCallback (&QueueLengthTracer, stream));
    }
}

static void
EveryDropTracer (Ptr<OutputStreamWrapper>stream, Ptr<const QueueDiscItem> item)
{
  *stream->GetStream () << Simulator::Now ().GetSeconds () << "," << item << std::endl;
}

static void
TraceEveryDrop (std::string everyDropTrFileName, int N)
{
  AsciiTraceHelper ascii;
  if (everyDropTrFileName.compare ("") == 0)
    {
      NS_LOG_DEBUG ("No trace file for every drop event provided");
      return;
    }
  else
    {
	  std::ostringstream pathStream;
	  pathStream << "/NodeList/" << N <<"/$ns3::TrafficControlLayer/RootQueueDiscList/" << N << "/Drop";
	  std::string path = pathStream.str();
      Ptr<OutputStreamWrapper> stream = ascii.CreateFileStream (everyDropTrFileName.c_str ());
      *stream->GetStream () << "time"<< "," << "item" << std::endl;
      Config::ConnectWithoutContext (path, MakeBoundCallback (&EveryDropTracer, stream));
    }
}

static void
DroppingStateTracer (Ptr<OutputStreamWrapper>stream, bool oldVal, bool newVal)
{
  if (oldVal == false && newVal == true)
    {
      NS_LOG_INFO ("Entering the dropping state");
      *stream->GetStream () << Simulator::Now ().GetSeconds () << " ";
    }
  else if (oldVal == true && newVal == false)
    {
      NS_LOG_INFO ("Leaving the dropping state");
      *stream->GetStream () << Simulator::Now ().GetSeconds ()  << std::endl;
    }
}

static void
TraceDroppingState (std::string dropStateTrFileName, int N, std::string qdisc)
{
	// Only for Codel or Cobalt
  AsciiTraceHelper ascii;
  if (dropStateTrFileName.compare ("") == 0)
    {
      NS_LOG_DEBUG ("No trace file for dropping state provided");
      return;
    }
  else
    {
	  std::string q_;
	  if (qdisc.compare ("FIFO") == 0)
	    {
	      q_ = "PfifoFastQueueDisc";
	    }
	  else if (qdisc.compare ("FQ") == 0)
	    {
	      q_ = "FqCoDelQueueDisc";
	    }
	  else
	    {
	      NS_LOG_DEBUG ("No suitable qdisc");
	      return;
	    }
	  std::ostringstream pathStream;
	  pathStream << "/NodeList/" << N <<"/$ns3::TrafficControlLayer/RootQueueDiscList/16/$ns3::" << q_ <<"/DropState";
	  std::string path = pathStream.str();
      Ptr<OutputStreamWrapper> stream = ascii.CreateFileStream (dropStateTrFileName.c_str ());
      *stream->GetStream () << "time"<< std::endl;
      Config::ConnectWithoutContext (path, MakeBoundCallback (&DroppingStateTracer, stream));
    }
}


void
SwitchPacketsInQueueTracer (Ptr<OutputStreamWrapper> stream, uint32_t oldValue, uint32_t newValue)
{
	*stream->GetStream () << Simulator::Now ().GetSeconds () << "," << oldValue << "," << newValue << std::endl;
}

void
TracePacketsInQueue (std::string packetsInQueueTrFileName, Ptr<Queue<Packet> > queue)
{
	AsciiTraceHelper ascii;
	Ptr<OutputStreamWrapper> stream = ascii.CreateFileStream (packetsInQueueTrFileName);
	*stream->GetStream () << "time"<< "," << "oldValue" << "," << "newValue" << std::endl;
	queue->TraceConnectWithoutContext ("PacketsInQueue", MakeBoundCallback (&SwitchPacketsInQueueTracer, stream));
}
// End New Tracer


int
main (int argc, char *argv[])
{
  int tcpSegmentSize = 1446; //1000  // +54 => 1500
  int minRTO = 200;
  //unsigned int runtime = 60;   // seconds
  Time startTime = Seconds (0);
  Time runtime = Seconds (120);
  Time measurementTime = Seconds (5);
  Time stopTime = startTime + runtime + measurementTime;
  int maxStartTime = 0;    // microseconds 100 = 0.1ms

  int N = 2;
  double rttNoLoad = 0.1;  //ms
  std::string delaySenders = "0.02ms";   //10us
  std::string delayReceiver = "0.08ms";  //40us   ==> RTT_noload = 2* (10 + 40) = 100 us
  std::string C= "1Gbps";             // 1Gbps
  std::string C1 = "1000Mbps";           //1Gbps
  uint32_t SRU = 256000;       // 0 means "unlimited"   Fixed SRU
  //uint32_t D = 1000000;               // Fixed block D = 1MB
  //uint32_t maxBytes = 1;       // 0 means "unlimited"

  std::string qdisc = "FIFO";       //PfifoFast or FqCoDel for "FQ"
  std::string tcpCC = "TcpNewReno";      // Tcp Congestion COntrol
  //uint32_t queueDiscSize = 1000;  //in packets
  uint32_t queueSize = 10;        //in packets

  uint16_t sinkPort = 5400;
  Address sinkAddress;
  Address anyAddress;
  std::string probeType;
  std::string tracePath;


  CommandLine cmd;
  // Here, we define command line options overriding some of the above.

  //cmd.AddValue ("runtime", "How long the applications should send data", runtime);
  cmd.AddValue ("outputRep", "Output Repertory", outputRep);
  cmd.AddValue ("tcpCC", "TCP Congestion Control", tcpCC);
  cmd.AddValue ("qdisc", " Queuing discipline to use at the switch", qdisc);
  cmd.AddValue ("tcpSegmentSize", "TCP segment size", tcpSegmentSize);
  cmd.AddValue ("minRTO", "Minimum Retransmission Timeout in (ms)", minRTO);
  cmd.AddValue ("C", "Switch--Receiver bottleneck link BWD Eg. 1Gbps", C);
  cmd.AddValue ("rttNoLoad", "Delay on the Sender--Switch (20%) +  Switch--Receiver (80%) links Eg. 0.1ms = 0.02ms + 0.08ms = 100us", rttNoLoad);
  cmd.AddValue ("SRU", "Server Request Unit", SRU);
  cmd.AddValue ("queueSize", "Queue or Buffer size in number of packets", queueSize);
  cmd.AddValue ("nbSenders", "Number of Incast Senders", N);

  cmd.Parse (argc, argv);

  std::ostringstream str_1, str_2;
  str_1 << rttNoLoad*0.2 <<"ms";
  delaySenders = str_1.str();
  str_2 << rttNoLoad*0.8 <<"ms";
  delayReceiver = str_2.str();



  Config::SetDefault ("ns3::TcpSocketBase::MinRto", TimeValue (MilliSeconds (minRTO)));
  Config::SetDefault ("ns3::TcpSocket::SegmentSize", UintegerValue (tcpSegmentSize));
  Config::SetDefault ("ns3::TcpSocket::DelAckCount", UintegerValue (0));
  Config::SetDefault ("ns3::TcpL4Protocol::SocketType", StringValue ("ns3::TcpNewReno"));


  NodeContainer senderNodes;
  NodeContainer switchNode;
  NodeContainer receiverNode;
  senderNodes.Create (N);
  switchNode.Create (1);
  receiverNode.Create (1);

  NodeContainer senderSwitchNodes = NodeContainer(senderNodes, switchNode);
  NodeContainer switchReceiverNodes = NodeContainer(switchNode, receiverNode);
  NodeContainer allNodes = NodeContainer (senderNodes, switchNode, receiverNode);

  //Collect an adjacency list of senderNodes to switchNode for the p2p topology
  std::vector<NodeContainer> sendersAdjacencyList (N);
  for(uint32_t i=0; i<sendersAdjacencyList.size (); ++i)
    {
	  sendersAdjacencyList[i] = NodeContainer (senderNodes.Get (i), switchNode);
    }

  // Install link Senders -to- S1
  PointToPointHelper p2pSenders;
  p2pSenders.SetDeviceAttribute ("DataRate", StringValue (C1));
  p2pSenders.SetChannelAttribute ("Delay", StringValue (delaySenders));

  std::vector<NetDeviceContainer> senderDeviceAdjacencyList (N);
  for(uint32_t i=0; i<senderDeviceAdjacencyList.size (); ++i)
    {
      senderDeviceAdjacencyList[i] = p2pSenders.Install (sendersAdjacencyList[i]);
    }

  // Install link S1 -to- Receiver
  PointToPointHelper p2pReceiver;
  p2pReceiver.SetDeviceAttribute ("DataRate", StringValue (C+"Mbps"));
  p2pReceiver.SetChannelAttribute ("Delay", StringValue (delayReceiver));
  //p2pReceiver.SetQueue ("ns3::DropTailQueue", "MaxSize", StringValue (std::to_string(queueSize) + "p"));   // Device queue vs tclayer queue

  NetDeviceContainer receiverDevices;
  receiverDevices = p2pReceiver.Install (switchNode.Get (0), receiverNode.Get(0));


  //The type of queue disc installed on a NetDevice can be modified through the traffic control helper:
  // FqCoDelQueueDisc: The default maximum size is 10024 packets

  // Bottleneck link traffic control configuration
  TrafficControlHelper tchPfifo;
  tchPfifo.SetRootQueueDisc ("ns3::PfifoFastQueueDisc", "MaxSize",
                             StringValue (std::to_string(queueSize) + "p"));
  TrafficControlHelper tchCoDel;
  tchCoDel.SetRootQueueDisc ("ns3::CoDelQueueDisc");
  Config::SetDefault ("ns3::CoDelQueueDisc::MaxSize", StringValue (std::to_string(queueSize) + "p"));

  TrafficControlHelper tchFqCoDel;
  tchFqCoDel.SetRootQueueDisc ("ns3::FqCoDelQueueDisc");
  Config::SetDefault ("ns3::FqCoDelQueueDisc::MaxSize", StringValue (std::to_string(queueSize) + "p"));

  InternetStackHelper stack;
  stack.Install (allNodes);

  Ptr<PointToPointNetDevice> switchRcv = DynamicCast<PointToPointNetDevice> (receiverDevices.Get (0));
  //switchRcv.SetQueue ("ns3::DropTailQueue", "MaxSize", StringValue (std::to_string(queueSize) + "p"));
  //p2pReceiver.SetQueue ("ns3::DropTailQueue", "MaxSize", StringValue (std::to_string(queueSize) + "p"));  //Device queue

  //TC - qdisc
  if (qdisc.compare ("FIFO") == 0)
    {
      tchPfifo.Install (switchRcv);
    }
  else if (qdisc.compare ("FQ") == 0)
    {
      tchFqCoDel.Install (switchRcv);
    }
  else
    {
      //NS_LOG_DEBUG ("Invalid switch queue disc type");
      std::cout << "Invalid switch queue disc type" << std::endl;
      exit (1);
    }

  // IPV4
  Ipv4AddressHelper address;
  //// Senders
  std::vector<Ipv4InterfaceContainer> senderInterfaceAdjacencyList (N);
  for(uint32_t i=0; i<senderInterfaceAdjacencyList.size (); ++i)
    {
      std::ostringstream subnet;
      subnet<<"10.1."<<i+1<<".0";
      address.SetBase (subnet.str ().c_str (), "255.255.255.0");
      senderInterfaceAdjacencyList[i] = address.Assign (senderDeviceAdjacencyList[i]);
    }
  //// Receiver- Sink
  address.SetBase ("10.1.254.0", "255.255.255.0");
  Ipv4InterfaceContainer receiverInterfaces = address.Assign (receiverDevices);

  sinkAddress = InetSocketAddress (receiverInterfaces.GetAddress (1), sinkPort);
  anyAddress = InetSocketAddress (Ipv4Address::GetAny (), sinkPort);
  probeType = "ns3::Ipv4PacketProbe";
  tracePath = "/NodeList/*/$ns3::Ipv4L3Protocol/Tx";
  //tracePath1 = "/NodeList/17/$ns3::Ipv4L3Protocol/Rx";

  // Create router nodes, initialize routing database and set up the routing tables in the nodes.
  //Turn on global static routing
  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

  // Create a packet sink on to receive packets
  PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", anyAddress);
  ApplicationContainer sinkApps = packetSinkHelper.Install (receiverNode);
  sinkApps.Start (startTime);
  sinkApps.Stop (stopTime);


  // Randomize the start time between 0 and 0.1ms
  Ptr<UniformRandomVariable> uniformRv = CreateObject<UniformRandomVariable> ();
  uniformRv->SetStream (0);

  ApplicationContainer senderApps;
  //std::vector<Ptr<Socket>> senderSocketList (N);
  for(uint32_t i=0; i<senderNodes.GetN (); ++i)
    {
	  BulkSendHelper sourceAhelper ("ns3::TcpSocketFactory",  sinkAddress);
	  sourceAhelper.SetAttribute ("MaxBytes", UintegerValue (SRU));
	  sourceAhelper.SetAttribute ("SendSize", UintegerValue (tcpSegmentSize));
	  ApplicationContainer senderAppC = sourceAhelper.Install (senderNodes.Get (i));
	  senderAppC.Start (startTime + MicroSeconds (uniformRv->GetInteger (0, maxStartTime)));  // 0 et100us = 0.1ms
	  senderAppC.Stop (stopTime);

    }


  //configure tracing

  Simulator::Schedule((startTime + MicroSeconds (maxStartTime + 1)),&TraceCwnd, N);

  PcapHelper pcapHelper;
  Ptr<PcapFileWrapper> file = pcapHelper.CreateFile (outputRep + "pcap.pcap", std::ios::out, PcapHelper::DLT_PPP);
  senderDeviceAdjacencyList[0].Get (1)->TraceConnectWithoutContext ("PhyRxDrop", MakeBoundCallback (&RxDrop, file));


  // PCap
  //p2pReceiver.EnablePcap (outputRep + "sink",receiverNode,true);

  //Queuing
  TraceSojourn (outputRep + "sojourn.txt", N);
  TraceQueueLength (outputRep + "queuelen.txt", N);
  TraceEveryDrop (outputRep + "drop.txt", N);
//  TraceDroppingState (outputRep + "drop-state.txt", N, qdisc);

  Ptr<Queue<Packet> > switchQueue = switchRcv->GetQueue ();
  TracePacketsInQueue (outputRep + "switchDevice_qlen.txt", switchQueue);

  //add startTime + MicroSeconds (maxStartTime + 1)
  Simulator::Schedule(Seconds(1.0000001),&TraceSojourn, outputRep + "sojourn.txt", N);
  Simulator::Schedule(Seconds(1.0000001),&TraceQueueLength, outputRep + "queuelen.txt", N);
  Simulator::Schedule(Seconds(1.0000001),&TraceEveryDrop, outputRep + "drop.txt", N);

  // Flow monitor
  Ptr<FlowMonitor> flowMonitor;
  FlowMonitorHelper flowHelper;
  flowMonitor = flowHelper.InstallAll();

  Simulator::Stop (stopTime + TimeStep (1));   //  cleanuptime
  Simulator::Run ();
  Simulator::Destroy ();

  flowMonitor->SerializeToXmlFile(outputRep +"flowmon_stats.xml", true, true);

  Ptr<PacketSink> sink1 = DynamicCast<PacketSink> (sinkApps.Get (0));
  std::cout << "Total Bytes Received from Senders: " << sink1->GetTotalRx () << std::endl;

  return 0;
}

