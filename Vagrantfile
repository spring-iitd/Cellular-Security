# -*- mode: ruby -*-

Vagrant.configure("2") do |config|
  config.vm.synced_folder "configurations", "/home/vagrant/configurations"
  config.vm.synced_folder "shared", "/home/vagrant/shared"
  config.vm.box_check_update = true
  config.vm.synced_folder ".", "/vagrant", disabled: false

  if Vagrant.has_plugin?("vagrant-proxyconf")
    config.proxy.http     = "" # http://proxy61.iitd.ac.in:3128/
    config.proxy.https    = "" # http://proxy61.iitd.ac.in:3128/
    config.proxy.no_proxy = "localhost,127.0.0.1"
  end 

  config.vm.define "core_nw" do |core_nw|
    core_nw.vm.network "public_network", ip: "192.168.56.100"
    core_nw.vm.box = "core-nw"
    core_nw.vm.provider :virtualbox do |vb|
      vb.name = "core_nw"
      vb.memory = 1024
      vb.cpus = 1
    end

    core_nw.trigger.after :up do |trigger|
      trigger.name = "Finished Message"
      trigger.info = "Machine is up!"
      config.vm.provision :shell, :run => 'always', :privileged => true, inline: <<-SHELL
        # This script will run everytime that the system bootsup 
        sudo sh /home/vagrant/open5gs/misc/netconf.sh
        echo "--- Adding a route for the UE to have WAN connectivity over SGi/N6 -------"
        ### Enable IPv4/IPv6 Forwarding
        sudo sysctl -w net.ipv4.ip_forward=1
        sudo sysctl -w net.ipv6.conf.all.forwarding=1
        ### Add NAT Rule
        sudo iptables -t nat -A POSTROUTING -s 10.45.0.0/16 ! -o ogstun -j MASQUERADE
        sudo ip6tables -t nat -A POSTROUTING -s 2001:db8:cafe::/48 ! -o ogstun -j MASQUERADE
      SHELL
    end
  end 

  config.vm.define "ran_ue_nw" do |ran_ue_nw|
    ran_ue_nw.vm.box = "ran-ue-nw"
    ran_ue_nw.vm.network "public_network", ip: "192.168.56.120"

    ran_ue_nw.vm.provider :virtualbox do |vb|
      vb.name = "ran_ue_nw"
      vb.memory = 1024
      vb.cpus = 1
    end

  end
end
