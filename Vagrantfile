# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"
  
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    #apt-get upgrade -y
    debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
    debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
    apt-get install -y mysql-server mysql-client
    mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS declassified;"
    mysql -uroot -proot -e "CREATE TABLE IF NOT EXISTS declassified.professors(name VARCHAR(30) NOT NULL, rating DECIMAL(2,1), tags VARCHAR(255), PRIMARY KEY (name));"
    mysql -uroot -proot -e "CREATE TABLE IF NOT EXISTS declassified.classes(name VARCHAR(30) NOT NULL, section VARCHAR(255) NOT NULL, professor VARCHAR(30) NOT NULL, crn INT NOT NULL, PRIMARY KEY (crn), FOREIGN KEY (professor) REFERENCES declassified.professors(name));"
    apt-get install -y curl
    curl -sL https://deb.nodesource.com/setup | sudo bash -
    sudo apt-get install -y nodejs
  SHELL
end
