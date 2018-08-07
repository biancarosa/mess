NODE_COUNT = 3

Vagrant.configure("2") do |config|
  
  config.vm.network "private_network", type: "dhcp"

  (1..NODE_COUNT).each do |i|
    config.vm.define "node#{i}" do |subconfig|
      subconfig.vm.box = "ubuntu/xenial64"
      subconfig.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "playbook-node.yml"
      end
      subconfig.vm.hostname = "node#{i}"
      subconfig.vm.network :private_network, ip: "10.0.0.1#{i}"
    end
  end

end
