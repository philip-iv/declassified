# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"

  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    #apt-get upgrade -y
    debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
    debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
    apt-get install -y mysql-server mysql-client
    mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS declassified;"
    apt-get install -y curl
    curl -sL https://deb.nodesource.com/setup | sudo bash -
    sudo apt-get install -y nodejs
    sudo apt-get install -y python-pip
    sudo apt-get install -y python-dev libxml2-dev libxslt1-dev zlib1g-dev
    sudo pip install -r /vagrant/scraper/requirements.txt
  SHELL
end
