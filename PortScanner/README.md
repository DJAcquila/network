## Description

A simple port scanner

## Usage
```shell
$ python portscan.py 127.0.0.1 "80 8080 23 39"
```
- At the end of the execution of the analyzer, will have a file with name 'aux.pcp'. You can execute this file with wireshark to obtain more information about the tracking.

## Port Scanner

A port scanner is an application designed to probe a server or host for open ports. This is often used by administrators to verify security policies of their networks and by attackers to identify network services running on a host and exploit vulnerabilities.

A port scan or portscan is a process that sends client requests to a range of server port addresses on a host, with the goal of finding an active port; this is not a nefarious process in and of itself. The majority of uses of a port scan are not attacks, but rather simple probes to determine services available on a remote machine. [Text of Wikipedia](https://en.wikipedia.org/wiki/Port_scanner)
