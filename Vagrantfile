# -*- mode: ruby -*-

Vagrant.configure("2") do |config|
  config.vm.synced_folder "configurations", "/home/vagrant/configurations"
  config.vm.synced_folder "shared", "/home/vagrant/shared"
  config.vm.box_check_update = true
  config.vm.synced_folder ".", "/vagrant", disabled: false
  config.vagrant.plugins = ["vagrant-proxyconf"] 
  
  if Vagrant.has_plugin?("vagrant-proxyconf")
    config.proxy.http     = "" # http://proxy61.iitd.ac.in:3128/
    config.proxy.https    = "" # http://proxy61.iitd.ac.in:3128/
    config.proxy.no_proxy = "localhost,127.0.0.1"
  end 

  config.vm.define "core_nw" do |core_nw|
    core_nw.vm.network "private_network", type:"dhcp", name:"vboxnet0"
    core_nw.vm.box = "core-nw"
    core_nw.vm.provider :virtualbox do |vb|
      vb.name = "core_nw"
      vb.memory = 1024
      vb.cpus = 1
    end
  
    core_nw.trigger.after :up,:reload do |trigger|
      trigger.info = "Machine is up!"
      trigger.run_remote = {path: "./scripts/sim.sh"}
    end
  end 

  config.vm.define "ran_ue_nw" do |ran_ue_nw|
    ran_ue_nw.vm.box = "ran-ue-nw"
    ran_ue_nw.vm.network "private_network", type:"dhcp", name:"vboxnet0"
    ran_ue_nw.vm.provider :virtualbox do |vb|
      vb.name = "ran_ue_nw"
      vb.memory = 1024
      vb.cpus = 1
    end

  end
end
