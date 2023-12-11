# Internet

## Ping
- What does `ping`'s `-o` flag do? Can you try it out?
    - The `-o` flag makes `ping` send a single ICMP packet request and wait for the response.
- Can you `ping` a domain like google.com?
    - Yes. We can `ping google.com`. A DNS lookup reveals the IP address which corresponds to google.com and then `ping`s that.
- What about diy.com? Why?
    - No. Some websites have firewall settings which prevent `ping`, probably to avoid D/DoS attacks like "ping of death", where oversized, fragmented packets are sent to the server and can cause errors as it tries to reassemble them.
- Can you ping your own computer? Is there any purpose to such a thing?
    - Yes. This could be a good idea for a couple of reasons:
        - Diagnosing network connectivity problems on the local machine
        - Checking that the hosts file is set up for localhost
- What does the `-f` flag do and why does the manual advise you not to use it?
    - The `-f` flag stands for "flood" and sends `ECHO_REQUEST`s as fast as possible. This could create some backlog in the network stack, affecting performance. For this reason, using `ping -f` externally could be considered an attempted network attack.
- Could a `ping` ever respond with more than one packet? Can you find a way to use `ping` such that it does?
    - Requests and responses have a 1:1 relationship, so there is no way to cause more than one response per `ping`.
    - However, `ping -c {number} {address}` will send `{number}` of packets to `{address}`. This results in `{number}` of responses, also.

## Traceroute
- How can we use traceroutes -q flag to speed up tracing a route?
    - `traceroute -q {number} {address}` sets the number of queries at each hop to `number`. The default is 3, but setting to 1 would reduce the time taken to trace the route.
- What does the -r flag for traceroute do? 
    - It traces a route to a host on an attached (directly connected) network.
    - An attached network here means that the machine calling traceroute can communicate with it without involving a router or switch.
- What about on ping?
    - The same bypassing of normal routing tables as with traceroute, only working with directly attached networks.
- When might it be useful?
    - The -r flag might be useful for testing connections between machines that ought to be in the same network segment or subnet.
    - Also, if the routing daemon (which is in charge of monitoring which connections are available for communication within a network) drops an interface (meaning that it no longer lists the interface in the routing tables), the -r flag can be used to probe the route anyway. This could identify issues related to the dropped interface/route.
- What techniques do High Frequency Trading systems use to minimise latency?
    - The time it takes for data to get from one place to another is called latency. Very low latency connections are desirable by various groups, but for High Frequency Trading in the finance industry it can mean huge sums of money.
    - Having the minimal physical distance between connection end points (i.e. minimise signal travel time).
    - Have well-optimised network switch use, so longer routes are used less frequently.
- Try to trace a route between your computer and every continent on Earth. Which continents are easy or hard to reach — and why?
    - I used geotraceroute.com to find some IP addresses coresponding with various countries.
    - Africa
        - 13.244.55.174, 19 hops; South Africa
    - Asia
        - 136.232.148.178, 64+ hops, not resolved; India
        - 125.214.190.223, 64+ hops, not resolved, Sri Lanka
        - 202.47.238.118, 17 hops; Thailand
    - Antarctica
        - Potentially not possible to trace to Antarctica, since connections there are handled via satellite.
    - Europe
        - 193.247.170.254, 13 hops; Switzerland
    - North America
        - 174.136.100.234, 16 hops; LA, USA
    - Oceania
        - 103.25.56.18, 28 hops; Australia
    - South America
        - 187.0.196.36, 19 hops; Brazil
- How does traceroute actually work out routes?
    - It sends packets with incrementally higher TTL, such that the TTL reaches 0 at each successive server. This triggers an ICMP Time Exceeded message to be returned, indicating that a server has been reached and providing the IP address (in most cases).
- What is a 'ttl'?
    - TTL is "time-to-live". This is the number of servers a packet can pass through before becoming invalid.
- What is a 'time exceeded' reply?
    - The ICMP Time Exceeded message is sent when a packet reaches a TTL of 0 and is discarded by the server. It contains information about the server (e.g. the server's IP address and information about the packet itself).

## Telnet
__The xf.mkrs.link connection did not work, so I tested with a socket run via Python.__
- What was telnet originaly used for?
- Why should this not be done now?
- What are the different layers of the Internet Protocol Stack?
- What is the difference between TCP and UDP?
- How does a 'packet frame segment diagram' relate to the different layers of the Internet Protocol Stack?
- How does a TCP handshake work?
- In TCP, what happens if a packet gets lost and how is this achieved?
- Is it a problem if two packets in a WiFi network are transmitted simultaneously?