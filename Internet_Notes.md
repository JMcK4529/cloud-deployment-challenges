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
*The xf.mkrs.link connection did not work, so I tested with a socket run via Python.*
- What was telnet originaly used for?
    - Remotely accessing a command-line interface.
- Why should this not be done now?
    - Telnet transfers 7-bit ASCII and cannot encrypt plaintext well. It is not secure.
- What are the different layers of the Internet Protocol Stack?
    - Application Layer
        - Communicating between applications e.g. web browsers.
        - Messages from one end's application are readable by the application at the other end.
        - Protocols used here include: HTTP, FTP, SMTP, DNS
    - Transport Layer
        - Collects the application layer message and adds a header to form a segment.
        - A socket at the sending end of the transport layer passes the message to the network layer.
        - At the receiving end, the reverse happens.
        - Uses a port number to identify the correct socket/application.
    - Network Layer
        - Receives the message and destination from the transport layer.
        - Adds a header and trailer, then sends a datagram.
        - Protocols used include: IPv4 and IPv6. These are the IP addresses.
        - ICMP is also used, but only for error reporting (containing no message information).
    - Link Layer
        - Communication between switches, routers, etc. occurs here.
        - At this level, the data packet is called a frame.
        - Mostly implemented in network adapters/network interface cards.
    - Physical Layer
        - The physical connections between devices e.g. fibre-optic, ethernet, etc.
        - The frame is broken down into bits, transmitted, then reassembled at the receiving side.
- What is the difference between TCP and UDP?
    - TCP and UDP are transport layer protocols.
    - TCP is reliable and connection-oriented, meaning it establishes a connection before transmitting data.
    - UDP is less reliable, but fast. It sends data without checking for a connection.
- How does a 'packet frame segment diagram' relate to the different layers of the Internet Protocol Stack?
    - << Frame Header | Network Header | Transport Header | Data | Frame Trailer >>
    - Packet(  Frame<  Datagram{  Segment[  ~Data~  ]  }  >  )
- How does a TCP handshake work?
    - Synchronise: The client sends a TCP segment with the SYN flag set to the server. This indicates that the client is trying to establish a connection with the server.
    - Synchronise-Acknowledge: The server reads the original segment and checks that it was not damaged (by reference to a checksum). If this is the case, a segment is sent back to the client with both SYN and ACK flags set.
    - Acknowledge: The client receives the new segment, checks it, then acknowledges that data is correctly being sent from server to client by sending a segment with only the ACK flag set.
    - By using this 3-way handshake, it can be confirmed that data is being reliably sent and received in both directions.
- In TCP, what happens if a packet gets lost and how is this achieved?
    - Timeout and Retransmission
        - When a TCP segment is sent, a timer starts. If an acknowledgement is no received by the time the timer expires, the segment is re-sent.
    - Selective Repeat
        - Each sent packet has a sequence number. If any packet is not received, it is re-sent without the need to send any other packets again.
    - Fast Retransmit
        - If a packet is dropped for some reason, it can lead to duplicate acknowledgements.
        - If three duplicates are detected, this triggers a retransmission of the segment even if no timeouts have occurred.
    - Congestion Window
        - The number of bytes that can be sent at any one time. It is maintained and updated by the client.
        - There is also a sliding window which controls how much data is received by the server (by limiting what is sent).
        - The sliding window is adjusted based on feedback from the server.
        - The client sends data which is less than the congestion and receive (sliding) windows.
- Is it a problem if two packets in a WiFi network are transmitted simultaneously?
    - Yes. If two WiFi nodes try to send data at the same time, this can cause a collision.
    - There are collision detection and resolution procedures:
        - Carrier Sense Multiple Access with Collision Avoidance (CSMA/CA): check if the channel is busy, then transmit if clear.
        - Expect ACK packet for each frame transmission, assume collision if not received. Back off for a random time to avoid a loop of collisions, then try again.

## Curl
- What is TLS?
    - This stands for Transport Layer Security.
    - It uses encryption to prevent eavesdropping and tampering.
- When have you used TLS today?
    - TLS is commonly used for HTTPS, so I use it whenever I use my web browser.
- What does BGP stand for?
    - Border Gateway Protocol. 
- What is BGP's purpose on the internet?
    - It is a protocol that outlines how autonomous systems (like internet service providers or content delivery networks - networks that have a common route to the internet) should organise communication traffic.
    - BGP determines the most efficient paths between networks and uses this to facilitate transmissions.
- What are the differences between HTTP/1.0, HTTP/1.1 and HTTP/2?
    - HTTP/1.0
        - Available methods: GET, POST, HEAD
        - No persistent connections (each request/response pair requires a new connection)
    - HTTP/1.1
        - Available methods: GET, POST, HEAD, PUT, PATCH, DELETE, CONNECT, TRACE, OPTIONS
        - Persistent connections introduced (several requests can be executed using a single connection)
        - Optional compression/decompression
    - HTTP/2.0
        - Available methods: as with HTTP/1.1
        - Request multiplexing introduced (so multiple requests can be sent simultaneously via the same connection)
        - Automatic compression/decompression
        - Server push introduced (proactively sends data to the client before requests)
- Can you use telnet to manually make a HTTP/1.1 request to http://www.example.org ?
```
➜ ✗ telnet example.org 80
Trying 93.184.216.34...
Connected to example.org.
Escape character is '^]'.
GET / HTTP/1.1
Host: example.org
Connection: close

HTTP/1.1 200 OK
Accept-Ranges: bytes
Age: 537695
Cache-Control: max-age=604800
Content-Type: text/html; charset=UTF-8
Date: Mon, 11 Dec 2023 14:39:44 GMT
Etag: "3147526947"
Expires: Mon, 18 Dec 2023 14:39:44 GMT
Last-Modified: Thu, 17 Oct 2019 07:18:26 GMT
Server: ECS (dce/26AB)
Vary: Accept-Encoding
X-Cache: HIT
Content-Length: 1256
Connection: close

<!doctype html>
<html>
<head>
    <title>Example Domain</title>

    <meta charset="utf-8" />
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style type="text/css">
    body {
        background-color: #f0f0f2;
        margin: 0;
        padding: 0;
        font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;

    }
    div {
        width: 600px;
        margin: 5em auto;
        padding: 2em;
        background-color: #fdfdff;
        border-radius: 0.5em;
        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);
    }
    a:link, a:visited {
        color: #38488f;
        text-decoration: none;
    }
    @media (max-width: 700px) {
        div {
            margin: 0 auto;
            width: auto;
        }
    }
    </style>
</head>

<body>
<div>
    <h1>Example Domain</h1>
    <p>This domain is for use in illustrative examples in documents. You may use this
    domain in literature without prior coordination or asking for permission.</p>
    <p><a href="https://www.iana.org/domains/example">More information...</a></p>
</div>
</body>
</html>
Connection closed by foreign host.
```
- Without using a HTTP library, write a HTTP server that is fully featured enough to respond to requests from your web browser and have them displayed. For this you will need to understand the HTTP protocol, how to parse HTTP requests, and how to send responses.
    - A good attempt so far in HTTP_server.py
    - It works with telnet but not the browser, as the browser sends the GET request as one long string including headers, etc.
    - Current functionality depends on socket.recv which updates from terminal on carriage return...
    - Can fix this by looking for \r\n in each input string.
