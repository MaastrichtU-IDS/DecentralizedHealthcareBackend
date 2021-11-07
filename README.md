# LUCE Technical Prototype & LuceVM

The technical prototype of LUCE is accessible via LuceVM.

LuceVM is a self-contained virtual machine to facilitate web3 development. It encapsulates a Python-Django-Ethereum development stack and allows us to compile, deploy and interact with Ethereum Smart Contracts in a seamless manner. It was created primarily to facilitate the development of the LUCE technical prototype but can be used to support other blockchain-focused research as well.

This repository explains how to set-up LuceVM to access the LUCE Prototype.

Soon a web-hosted version will be made available as well.

## Usage of LuceVM
LuceVm works on all major operating systems (Linux, Mac and Windows).

* First make sure [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/) are installed
  * On macOS High Sierra and Mojave the VirtualBox installation may fail
  * [This blog post](https://medium.com/@DMeechan/fixing-the-installation-failed-virtualbox-error-on-mac-high-sierra-7c421362b5b5) explains how to fix that
  * On Windows, ensure that [Hyper-V is enabled](https://www.vagrantup.com/docs/hyperv/)
* Check if `git` is installed and if not install from [here](https://git-scm.com)
  * To check if git is installed run `git --version` in the terminal 
  * If it is installed it will return the version number
* Then clone the LUCE base folder from github and start the VM as follows:

```bash
cd ~/path/to/desired/location/
git clone https://github.com/arnoan/LUCE.git
cd ./LUCE/luce_vm 
vagrant up  # start LuceVM
vagrant ssh -c 'bash start_servers.sh' 	# start the servers
```

Visit `http://127.0.0.1:8000` in your browser to access the LUCE Data Exchange.
Demo accounts:  
provider@luce.com &nbsp; | provider  
requester@luce.com  | requester  

For research usage the Jupyter notebook environment is accessible via `http://127.0.0.1:8888`.  
The password is: `luce`.

Once finished the virtual machine can be stopped using either `vagrant halt`, `vagrant suspend` and completely removed using `vagrant destroy`. See below for the differences.

## Further Information

*Q: How do I stop the virtual machine when I am finished working?*   
From within the same terminal where lucevm was started:
```
vagrant suspend
```
This hibernates the virtual machine. That way the next time it is started via `vagrant up` it will start much faster and continue in exactly the same state as you left off. There is no need to manually start the servers again.

*Q: How do I resume the machine?*   
No matter the state (hibernated, shut down, or not-yet-existent), we always use the same command to start up:
```
vagrant up
```
If the machine was previously hibernated `vagrant up` is all that is needed. If the machine was shut down or completely destroyed the servers need to be manually started again with `vagrant ssh -c 'bash start_servers.sh'`.

*Q: How do I stop the machine completely?*   
The machine can be shut down completely via `vagrant halt` - in that case the servers have to be started again the next time LuceVM is booted. Finally `vagrant destroy` can be used to completely destroy the virtual machine instance. (All changes within the Luce Data Exchange and in the Jupyter python notebooks and are still preserved even if the machine is destroyed. That is because all application code for Jupyter, Django, the Datbase etc. are actually sotred on the host machine filesystem. This data is automatically shared with the VM again when a new machine instance is created.)

*Q: How can I update to the latest data contained in this github repository?*  
To update, first navigate to your local LUCE folder: `cd ~/path/to/LUCE/`  
Then run the following in the terminal:  
```bash
git fetch origin # this downloads all new content from github
git reset --hard origin/master # this replaces all local LUCE content with the newest updates

# To update to the latest release of lucevm & lucedb custom boxes:
vagrant destroy lucevm lucedb -f # destroy currently running instances of boxes
vagrant box update # this ensures you are using the latest lucevm and lucedb boxes
```

**Warning:** Note that by running `git reset` all LUCE files that may have been changed locally will be overwritten with the latest version from Github. In order to experiment locally with Jupyter notebooks without the possibility of them accidentally being over-written please create a `/jupyter/safe_storage_area/` folder. The contents of this folder are not synchronised with the github repository. Not even when `git reset` is executed. Please store all files you wish to keep safe in that folder.

*Q: How can I delete LuceVM completely?*   
To delete LuceVM we first destroy all currently instantiated machines. Then we remove the base images and - if desired - delete the folder containing all LUCE related application data.
```
vagrant -f destroy lucevm lucedb # this destroys all machines

# Remove both custom base images from the system:
vagrant box remove arnoan/lucevm 
vagrant box remove arnoan/lucedb 
```
Then simply delete the folder to which this repository was cloned.  
There are no other places where information is stored.  
