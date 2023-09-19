Using it to analyse pcap files over and over. There are tools like scapy or dpkt to understand and parse it. Pyshark uses tshark as a base to both capture and parsing rather than using a python native method of doing it. The same information as using wireshark.

Pyshark has two modes of working and can access the details within the packet specifically. Tough one is first. 

## Syntax and Explanation

```python 
# importing and opening the file
import pyshark 
pcap = pyshark.FileCapture("path")
# Accessing the packet: 
pcap[0]
pcap.next()
for pkt in pcap: 
	pass
# Printing the entire packet 
pkt.pretty_print()
print(pkt)
# Accessing a specific layers 
pkt.tcp 
pcap[0][2]
pkt["tcp"]
# Exploring fields 
pkt.tcp.field_names
pkt.tcp.scrport
pkt.tcp.get("foo") # getting value against "foo"
# Filtering 
pyshark.FileCapture("file", display_filter="http")
"http" in pkt # is there http layer in the packet 
[pkt.http.user_agent for pkt in pcap if "http" in pkt and pkt.http.has_field("user_agent")] # can write an iterative over the opened file
```

```python 
# Nested Fields 
https[0].tcp.flags_ack # gives out 1 or 0 against the flag 
https[0].tcp.checksum  # interprets and pulls value 
https[0].tcp.checksum.hex_value # shows as hex value same as conversion 
https[0].tcp.checksum.showname 

# Duplicate Fields, that appear more than once, more than one query response 
dnses = [pkt for pkt in pcap if "dns" in pkt and pkt.dns.count_answers.int_value == 2]
# by default it would pick the first one, if you know more than once then have to iterate and find further. It will return an object and not the string, the object needs to be unpacked further for each one of the values. The second part is true if you start using the all_fields in which it would look for all possible ones. 
[field.get_default_value() for field in pkt.dns.restp_name.all_fields]
```

PDML input - every packet is mapped to an XML there is alternate parsing option, which is JSON/EK parsing. tshark also allows exporting in the EK or json. 
Developer Note: This is a lot better. XML contains outputs and fields that the json one does not. EK might have more bugs. `use_json/use_ek` EK is also typed. It stores the actual value and not just string. 
```python
pcap = pyshark.FileCapture(path_capture, use_ek=True)
pkt.tcp.flags.ack # it was earlier flags_ack
pcap[94].dns.resp.name
```

### Other capture types 
1. LiveCapture
2. InMemCapture
3. FileCapture

```python 
live = pyshark. LiveCapture ("lo")
live.sniff(3) # run for 3 units of time and have it stored in live
live[0]
for pkt in live.sniff_continuously(): 
	print("Got pkt")
live.apply_on_packets(callback) # works on all packets 
```

### Integrating pyshark into applications 

- iterating vs loading packets: Iterating over python objects is easier and better than loading the entire files into memory before you start processing it. 
- asyncio: there are async equivalents for each of the functions 
- pyshark should not be included in production environment 
- this is slow.