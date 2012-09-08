# arohacs fabfile.py Documentation

## License information

[site]: http://www.adamrohacs.com "adamrohacs.com website"
[license]: http://www.gnu.org/licenses/gpl.html "gnu.org license"
[repo]: https://github.com/arohacs/fabfile "vibhelm repository"
[contact id]: http://www.adamrohacs.com/contact "Contact Adam Rohacs"
fabfile by [Adam Rohacs][site] is licensed under a [GNU General Public License][license] and is based on a work at [github.com][repo].  

### Anatomy of the project name

This is my fabfile.py script which leverages fab - the fabric binary - and so the name should be self-explanatory.

### Version information
This is a python 2.7.x script and may not work correctly or at all when invoked by python 3. Please check your version by typing: python -V  

#### OS Platform support and Testing
This program has been tested with Python 2.7 under virtualenvs and with python2 on Arch Linux. It might or might not work on a non-Linux/Unix platform. Use at your own risk, and modify at your leisure according to the GNU license. 


[git clone url]: http://git-scm.com/book/en/Git-Basics-Getting-a-Git-Repository

### Usage
[Clone][git clone url] the repository to a directory of your choice: 
$ git clone git://github.com/arohacs/fabfile.git

Run the program with python version 2.7, for example:   
$ fab --options 

### Features

With this software, you can:  

* **Start** and **stop** headless virtualbox machines
* **Start** and **stop** remote services
* **Push** and **pull** to dev machines and production machines 
* **Start** VirtualBox hosts in headless mode  
* **Deploy** via Push and Pull with rsync


### History
I needed some automation to help me with Django development and deployment. Through trial and error, I developed this script. For security, all host names and user names are redacted, but it shouldn't be hard for you to figure out where to change variables. 


