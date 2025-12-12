# Intercepting Thick Client TCP and TLS Traffic

![rw-book-cover](https://miro.medium.com/v2/resize:fit:1200/1*dCAeSTFDF-b8kM-DmJd9yQ.png)

## Metadata
- Author: [[Sourav Kalal]]
- Full Title: Intercepting Thick Client TCP and TLS Traffic
- Category: #articles
- Summary: Intercepting thick-client TCP/TLS traffic is hard because many desktop apps use non‑HTTP or custom protocols protected by TLS. InterceptSuite is a one‑click SOCKS5 TLS MITM proxy with a simple GUI to intercept and modify non‑HTTP TCP/TLS traffic. On Windows you use Proxifier to route the app to InterceptSuite and then view the captured traffic.
- URL: https://share.google/yfOww2wXByij5W0zb

## Full Document
Intercepting and analysing the traffic is one of the important parts of the pentest, whether it’s a mobile, web or desktop application. On the web, it’s easy to intercept. In the case of mobile applications, it’s easy to intercept unless there are security mitigation implementations, but those are often bypassed. In all those cases, the web or mobile app protocol used is HTTP/s, which means we have the option to intercept easily via BurpSuite.

When it comes to a Desktop Thick client application, it’s always easy to intercept when the HTTP/S protocol is used. In some rare cases, it requires different methods, and to intercept HTTP/s, but it’s always possible as we have different tools and proxy applications like BurpSuite, ZAP available to intercept the HTTP/s traffic. In many cases, applications don’t use the HTTP protocol, instead, they use different protocols. In most cases, it’s based on a protocol or custom protocol and with TLS, which makes it hard to intercept, as there are no direct, easy solutions to intercept on TCP+TLS traffic.

We can set up the MITMProxy application, but it requires multiple setups and does not always work with non-TCP + TLS traffic.

To make things easy, similar to BurpSuite, like single click install and setup proxy, I have created InterceptSuite, which uses Socks5 proxy, with 1 click installation and easy to intercept and modify the tick client TCP and TLS traffic with a modern GUI.

To get started, go to the InterceptSuite GitHub Repository, navigate to the release page and download the installer EXE for Windows, PKG for MacOS or RPM, Deb, and App Image file for Linux.

[#### GitHub - InterceptSuite/InterceptSuite: A TLS MITM proxy for Non-HTTP traffic, with support for TLS…

##### A TLS MITM proxy for Non-HTTP traffic, with support for TLS upgrades like STARTTLS, PostgreSQL, and more. …

github.com](https://github.com/InterceptSuite/InterceptSuite/?source=post_page-----72fab07fffe7---------------------------------------)

If not, you can directly download it from the [InterceptSuite website](http://interceptsuite.com/Download).

To test the TCP Intercept, I am using the BetaFast Vulnerable Thick Client application.

[#### GitHub - NetSPI/BetaFast: Vulnerable thick client applications used as examples in the Introduction…

##### Vulnerable thick client applications used as examples in the Introduction to Hacking Desktop Applications blog series …

github.com](https://github.com/NetSPI/BetaFast?source=post_page-----72fab07fffe7---------------------------------------)

InterceptSuite make use of Socks5 Proxy; for some reason, Windows does not support Socks proxy. In order to redirect the application traffic to any proxy server, including for an unaware application, the best option is Proxifier.

![](https://miro.medium.com/v2/resize:fit:700/1*6Lk0SXiVw3WEhqbhXDvyug.png)
Install and open the Proxifier application and navigate to the Profile → Proxy Server.

![](https://miro.medium.com/v2/resize:fit:700/1*tNbHbSaismx6tuMt3OlJhw.png)
Click on the Add button and enter the interceptSuite proxy server IP and port. Default is 127.0.0.1 port 4444, select protocol as SOCKS Version 5.

We can now configure Proxifier to redirect traffic from specific applications, IP addresses, or ports to the proxy. To do this, navigate to Profile → Proxyification Rules.

![](https://miro.medium.com/v2/resize:fit:700/1*FkjJoJ5so4xazjFm27ENnw.png)
We need to create two rules: the first rule will redirect the thick client traffic to our proxy application.

![](https://miro.medium.com/v2/resize:fit:700/1*kUARkL6gT6J8zzIcDXd5Yg.png)
The second rule will ensure that the traffic for the proxy application, which is InterceptSuite, goes directly to the server and does not go through the proxy again. This is important to prevent an endless redirect loop.

![](https://miro.medium.com/v2/resize:fit:700/1*iRQztJ-mTbwlHFelFZmkgA.png)
To view the TCP data between the BetaBank application and the server, open the BetaBank application, submit your credentials, and then navigate to the proxy history in InterceptSuite.

![](https://miro.medium.com/v2/resize:fit:700/1*dCAeSTFDF-b8kM-DmJd9yQ.png)
No more complex setup, just plug in InterceptSuite and start analysing TCP and TLS traffic instantly.
