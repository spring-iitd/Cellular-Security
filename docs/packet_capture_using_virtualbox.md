While using the multi-device machine setup esp in different locations it may be difficult to manage the VMs. The followoing commands can help us manage if we are using virtualbox as the provider.  

Here is a quick guide to record traffic from virtualbox images run through vagrant. 

1. Make sure the networking within the virtual machine is `public`, when booting up select a public network which has almost no traffic. 
2. Start the VMs and then close them to have the virtualbox images registered with VBoxManage.
3. Identify which interface/adapter you need to record. You will need this later. 
4. Check that the VMs are listed but are not running with the following commands.

```shell
VBoxManage list vms
VBoxManage list runningvms
```

5. Before launching the VMs start recording traffic on the interface of choice using the following command: 
```shell
VBoxManage modifyvm "ueransim" --nictrace2 on --nictracefile2 file.pcap 
# Template
# VBoxManage modifyvm [your-vm] --nictrace[adapter-number] on --nictracefile[adapter-number] file.pcap
```
6. The only way to stop recording traffic is to switch off the virtual machines. You should do tha with vagrant commands. 

There should be a pcap file in your VM folder.