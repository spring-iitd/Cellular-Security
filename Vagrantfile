# -*- mode: ruby -*-

Vagrant.configure("2") do |config|
  config.vm.synced_folder "configurations", "/home/vagrant/configurations"
  config.vm.synced_folder "shared", "/home/vagrant/shared"
  config.vm.synced_folder ".", "/vagrant", disabled: false
  config.vagrant.plugins = ["vagrant-proxyconf"] 
  
  if Vagrant.has_plugin?("vagrant-proxyconf")
    config.proxy.http     = "" # http://proxy61.iitd.ac.in:3128/
    config.proxy.https    = "" # http://proxy61.iitd.ac.in:3128/
    config.proxy.no_proxy = "localhost,127.0.0.1"
  end 

  config.vm.define "core_nw" do |core_nw|
    core_nw.vm.network "private_network", ip:"192.168.56.100"
    core_nw.vm.network "forwarded_port", guest: 9999, host: 9999
    core_nw.vm.box = "core-nw"
    
    core_nw.vm.provider :virtualbox do |vb|
      vb.name = "core_nw"
      vb.memory = 4096
      vb.cpus = 4
      # Use the following to do packet capture automatically when the machine is booted.
      vb.customize ["modifyvm", :id, "--nictrace1", "on", "--nictracefile1", "pcaps/nictrace1.pcap"]
      vb.customize ["modifyvm", :id, "--nictrace2", "on", "--nictracefile2", "pcaps/nictrace2.pcap"]
      # Use the following to reduce the effectiveness of CPU
      # vb.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
      vb.check_guest_additions = false
    end
  
    core_nw.trigger.after :up,:reload do |trigger|
      trigger.info = "Machine is up!"
      trigger.run_remote = {path: "./scripts/sim.sh"}
    end
  end 

  config.vm.define "ran_ue_nw" do |ran_ue_nw|
    ran_ue_nw.vm.box = "ran-ue-nw"
    ran_ue_nw.vm.network "private_network", ip:"192.168.56.120"
    ran_ue_nw.vm.provider :virtualbox do |vb|
      vb.name = "ran_ue_nw"
      vb.memory = 2048
      vb.cpus = 4
      vb.check_guest_additions = false
    end

  end
end
