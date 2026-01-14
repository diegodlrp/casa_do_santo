Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.network "forwarded_port", guest: 8000, host: 8000  # Django dev server
  config.vm.network "forwarded_port", guest: 4200, host: 4200  # Angular dev server
  config.vm.network "forwarded_port", guest: 5173, host: 5173  # Svelte dev server

  config.vm.network "private_network", type: "dhcp"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3-pip python3-venv python3-dev build-essential
    apt-get install -y nodejs npm

    # Optional: Symlink node & npm if not recognized globally
    ln -s /usr/bin/nodejs /usr/bin/node || true

    npm install -g @angular/cli
  SHELL
end
