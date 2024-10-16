# -*- mode: ruby -*-

# Core Network Configurarion
OPEN5GS_IPv4_ADDR = "192.168.56.100"
UPF_OPEN5GS_IPv4_ADDR = "192.168.56.101"
OPEN5GS_VCPU = "1"
OPEN5GS_VRAM = "1024"

# Attack Box Configurarion
RAN_VRAM1 = "8192"
RAN_VCPU1 = "8"
RAN0_IPv4_ADDR = "192.168.56.120"
RAN1_IPv4_ADDR = "192.168.56.121"
RAN2_IPv4_ADDR = "192.168.56.122"
RAN3_IPv4_ADDR = "192.168.56.123"
RAN4_IPv4_ADDR = "192.168.56.124"
RAN5_IPv4_ADDR = "192.168.56.125"
RAN6_IPv4_ADDR = "192.168.56.126"
RAN7_IPv4_ADDR = "192.168.56.127"
RAN8_IPv4_ADDR = "192.168.56.128"
RAN9_IPv4_ADDR = "192.168.56.129"


# Benign Box Configurarion
UE0_IPv4_ADDR = "192.168.56.130"
UE_VRAM1 = "2048"
UE_VCPU1 = "2"


Vagrant.configure("2") do |config|
  # config.vm.synced_folder "configurations", "/home/vagrant/configurations"
  config.vm.synced_folder "shared", "/home/vagrant/shared"
  # config.vm.synced_folder "shared", "/home/vagrant/pwd"
  config.vm.synced_folder ".", "/vagrant", disabled: false
  config.vagrant.plugins = ["vagrant-proxyconf"] 
  
  if Vagrant.has_plugin?("vagrant-proxyconf")
    config.proxy.http     = "" #"http://proxy61.iitd.ac.in:3128/"
    config.proxy.https    = "" #"http://proxy61.iitd.ac.in:3128/"
    config.proxy.no_proxy = "localhost,127.0.0.1"
  end 

  config.vm.define "core_nw" do |core_nw|
    core_nw.vm.box = "core-nw-1-0"
    # core_nw.vm.network "private_network", type:"dhcp", name:"vboxnet0"
    # You can alternatively fix the IPs for the boxes with: 
    core_nw.vm.network "private_network", ip: OPEN5GS_IPv4_ADDR
    core_nw.vm.network "private_network", ip: UPF_OPEN5GS_IPv4_ADDR
    # You can do simple portforwarding with
    # core_nw.vm.network "forwarded_port", guest: 9999, host: 9999
    core_nw.vm.network "forwarded_port", host: 9999, guest: 9999, auto_correct: true
    core_nw.vm.network "forwarded_port", host: 9091, guest: 9091, auto_correct: true
    core_nw.vm.network "forwarded_port", host: 9092, guest: 9092, auto_correct: true
    core_nw.vm.network "forwarded_port", host: 9093, guest: 9093, auto_correct: true
    core_nw.vm.network "forwarded_port", host: 9094, guest: 9094, auto_correct: true

    core_nw.vm.provider :virtualbox do |vb|
      vb.name = "core_nw"
      vb.memory = OPEN5GS_VRAM
      vb.cpus = OPEN5GS_VCPU
      # Use the following to do packet capture automatically when the machine is booted.
      vb.customize ["modifyvm", :id, "--nictrace1", "on", "--nictracefile1", "pcaps/nictrace1.pcap"]
      vb.customize ["modifyvm", :id, "--nictrace2", "on", "--nictracefile2", "pcaps/nictrace2.pcap"]
      # Use the following to reduce the effectiveness of CPU
      # vb.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
      vb.check_guest_additions = false
    end
  
    core_nw.trigger.after :up,:reload do |trigger|
      trigger.info = "Machine is up!"
      trigger.run_remote = {path: "./shared/scripts/sim.sh"}
    end
  end 

  config.vm.define "ran_nw" do |ran_ue_nw|
    ran_ue_nw.vm.box = "ran-ue-nw"
    # ran_ue_nw.vm.network "private_network", type:"dhcp", name:"vboxnet0"
    # You can alternatively fix the IPs for the boxes with: 
    # ran_ue_nw.vm.network "private_network", ip:"192.168.56.120"
    ran_ue_nw.vm.network "private_network", ip: RAN0_IPv4_ADDR
    ran_ue_nw.vm.network "private_network", ip: RAN1_IPv4_ADDR
    ran_ue_nw.vm.network "private_network", ip: RAN2_IPv4_ADDR
    ran_ue_nw.vm.network "private_network", ip: RAN3_IPv4_ADDR
    ran_ue_nw.vm.network "private_network", ip: RAN4_IPv4_ADDR
    ran_ue_nw.vm.network "private_network", ip: RAN5_IPv4_ADDR
    ran_ue_nw.vm.network "private_network", ip: RAN6_IPv4_ADDR
    ran_ue_nw.vm.network "private_network", ip: RAN7_IPv4_ADDR
    ran_ue_nw.vm.network "private_network", ip: RAN8_IPv4_ADDR
    ran_ue_nw.vm.network "private_network", ip: RAN9_IPv4_ADDR
    

    ran_ue_nw.vm.provider :virtualbox do |vb|
      vb.name = "ran_ue_nw"
      vb.memory = RAN_VRAM1
      vb.cpus = RAN_VCPU1
      vb.check_guest_additions = false
    end
  end

  # VM 3: UE Simulator
  config.vm.define "ue_nw" do |ue|
    ue.vm.box = "ran-ue-nw"
    ue.vm.network "private_network", ip: UE0_IPv4_ADDR
    ue.vm.provider :parallels do |vb|
      vb.name = "ueB1"
      vb.update_guest_tools = true
      vb.memory = UE_VRAM1
      vb.cpus = UE_VCPU1
    end
  end 
end
