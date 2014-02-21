# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  config.vm.network :forwarded_port, guest: 8000, host: 8000

  config.vm.network "private_network", ip: "192.168.100.100"
  config.vm.synced_folder ".", "/vagrant", type: "nfs"

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  config.vm.provision :shell do |shell|
    shell.inline = <<-EOS
      set -e
      mkdir -p /var/lock/provision
      export DEBIAN_FRONTEND=noninteractive

      if [ ! -f /var/lock/provision/apt_update ]; then
        apt-get update -y -q
        touch /var/lock/provision/apt_update
      fi

      if [ ! -f /var/lock/provision/apt_packages ]; then
        apt-get install -y -q python-pip python-dev build-essential cmake pkg-config libgtk2.0-dev python-numpy

        # optional for OCR
        apt-get install -y -q libopencv-dev python-opencv opencv-doc

        touch /var/lock/provision/apt_packages
      fi

      if [ ! -f /var/lock/provision/virtualenv ]; then
        pip install virtualenv

        rm -rf ~/venv
        virtualenv ~/venv
        source ~/venv/bin/activate
        cd /vagrant
        pip install -r requirements.txt

        touch /var/lock/provision/virtualenv
      fi

      touch /var/lock/provision/completed
    EOS
  end

  config.vm.provision :shell, :path => "./vagrant/bootstrap.sh"

  config.vm.provision :shell do |shell|
    shell.inline = <<-EOS
      [ -f /var/lock/provision/completed ] || exit 1

      cd /vagrant/backend
      source ~/venv/bin/activate
      killall python 2>/dev/null
      python manage.py syncdb --noinput

      # root/root
      # ignore all errors since the user can pre-exist
      echo 'INSERT INTO "auth_user" VALUES(1,"pbkdf2_sha256$10000$fQ14C0o4Rccf$YE32evpiUOxASrEMiGQEtw4xglE1B0R3nm339rxY8Iw=","2014-02-17 22:16:51.758659",1,"root","","","admin@example.com",1,1,"2014-02-17 22:16:51.758659");' | python manage.py dbshell > /dev/null 2>&1 | :

      python manage.py runserver 0.0.0.0:8000
    EOS
  end
end
