# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"
    config.vm.network "private_network", ip: "192.168.100.100"
    config.vm.synced_folder ".", "/vagrant", type: "nfs"
    config.vm.hostname = "openpress"

    # The project web server
    config.vm.network :forwarded_port, guest: 8000, host: 8000
    # Elastic search port
    config.vm.network :forwarded_port, guest: 9200, host: 9200

    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", "1024"]
    end

    config.vm.provision "shell", path: "vagrant/apt_update.sh"
    config.vm.provision "shell", path: "vagrant/general_packages.sh"
    config.vm.provision "shell", path: "vagrant/python.sh"
    config.vm.provision "shell", path: "vagrant/apache.sh"
    #config.vm.provision "shell", path: "vagrant/git.sh"
    config.vm.provision "shell", path: "vagrant/elasticsearch.sh"
    config.vm.provision "shell", path: "vagrant/ocr.sh"
    config.vm.provision "shell", path: "vagrant/start_server.sh"

end
