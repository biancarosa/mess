Vagrant.configure("2") do |config|
  config.vm.network "private_network", type: "dhcp"
  config.vm.define "node1" do |node1|
    node1.vm.box = "ubuntu/xenial64"
    node1.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "playbook-node.yml"
    end
    node1.vm.hostname = "node1"
    node1.vm.network :private_network, ip: "10.0.0.11"
  end

  config.vm.define "node2" do |node2|
    node2.vm.box = "ubuntu/xenial64"
    node2.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "playbook-node.yml"
    end
    node2.vm.hostname = "node2"
    node2.vm.network :private_network, ip: "10.0.0.12"
  end

end
