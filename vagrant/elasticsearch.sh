    #!/usr/bin/env bash

mkdir -p /var/lock/provision
export DEBIAN_FRONTEND=noninteractive


if [ ! -f /var/lock/provision/jdk7 ]; then
    apt-get install  -y -q python-software-properties
    add-apt-repository -y ppa:webupd8team/java

    echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
    echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections


    apt-get update
    apt-get install  -y -q oracle-java7-installer oracle-java7-set-default

    if [ $? == 0 ]; then
        touch /var/lock/provision/jdk7
    fi
fi



if [ ! -f /var/lock/provision/elasticsearch ]; then
   wget -O - http://packages.elasticsearch.org/GPG-KEY-elasticsearch | apt-key add -
   echo "deb http://packages.elasticsearch.org/elasticsearch/1.2/debian stable main" >> /etc/apt/sources.list.d/elasticsearch.list
   apt-get update
   apt-get install -y -q elasticsearch
   pip install elasticsearch

   if [ $? == 0 ]; then
       update-rc.d elasticsearch defaults 95 10
       /etc/init.d/elasticsearch start

        touch /var/lock/provision/elasticsearch
   fi
fi


if [ ! -f /var/lock/provision/elasticsearch_head ]; then
  /usr/share/elasticsearch/bin/plugin -install mobz/elasticsearch-head


   if [ $? == 0 ]; then
        touch /var/lock/provision/elasticsearch_head
   fi
fi

