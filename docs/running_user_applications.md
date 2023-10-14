# Running user applications
Implementing user services has been a difficult task for us so far. Here is a quick guide on how to run user applications on the two VM system.

Before starting this guide, make sure : 
- You have a working installation of the two VM system
- You have a started the Open5GS core services 
- You have started a gnodeB and a UE, where the UE has established a PDU session with the core network

## What is a user application?
A user application is a program that runs on the user equipment (UE) and communicates with some remote service. It may do some processing on the data it receives from the remote service and send the result back to the remote service. These can be as simple as running 'ping google.com. 

## What do we want to achieve?
We would like to run the user application and send all the information through the UE interface through the 5G connection. We just need to make sure that the user is communicating over the UE TUN interface. Lucky for us, UERANSIM has a solution built in. 
```
# ping command bind direcly to uesimtun0
ping -I uesimtun0 google.com

# curl command bind direcly to uesimtun0 
curl --interface uesimtun0 -X GET "https://httpbin.org/get"
  
--- 

# bind curl command via nr-binder
# nr-binder use pdu session ip
./nr-binder 10.45.0.3 curl -X GET "https://httpbin.org/get"

---

# bind python application via nr-binder
# request.pyt is simple python program which send http GET request
./nr-binder 10.45.0.3 python3 request.py
```

## How does it work?
With the binder app we are starting a user application but we are binding it to the IP address of the UE. This means that all the traffic from the user application will be sent through the UE interface.

> Note: The IP address of the UE is the IP address of the PDU session. uesimtun0 and 10.45.0.3 are example values.


## What should my user application do?
For starters, lets write a simple python program that connects to an API, generates a random image and stores it locally. There are websites such as [https://api-ninjas.com/](https://api-ninjas.com/) which can be used, and you can skip writing your own server. 

> Note: You should know how to write your own application, both client and server. This is just an example. 

Looking at the [Random Image API](https://api-ninjas.com/api/randomimage), we can see that we need to send a GET request to the server. We can use the python requests library to do this. 

```python
import requests
import shutil

category = 'nature'
api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category)
response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY', 'Accept': 'image/jpg'}, stream=True)
if response.status_code == requests.codes.ok:
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
else:
    print("Error:", response.status_code, response.text)
```

## References 
A large part of the information in this guide was taken from the [Medium Article](https://medium.com/rahasak/5g-core-network-setup-with-open5gs-and-ueransim-cd0e77025fd7) and [API Ninjas](https://api-ninjas.com/api) 
