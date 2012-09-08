# Copyright 2011-2012 Adam Rohacs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from fabric.api import local
from fabric.contrib.project import rsync_project 
from fabric.api import *
from fabric.api import env, run
import re
import subprocess
from subprocess import PIPE, Popen, STDOUT, call
import ssh

env.forward_agent = True
env.user = 'user'
env.key_filename = ('/home/user/.ssh/filename')
envdir = ['/home/user/dir/']
env.roledefs = {
    'test': ['user@host'],
    'test2': ['user@host'],
    'vm': ['host_IP'],
    'prod': ['user@host']
} 

def vmheadless(vm='host', cmd='start'):
    '''usage: vmheadless:vm="vm name",cmd="start/stop"'''
    full_cmd = ''
    if cmd == 'start':
        full_cmd = 'VBoxHeadless -s ' + vm + ' --vrde=off' ' &' #don't need vrde if I'm only ssh'ing to the box
    elif cmd == 'stop':
        full_cmd += 'VBoxManage controlvm ' + vm + ' savestate'
    print "press enter to do the following:", full_cmd
    raw_input()
    local(full_cmd)

def rundev(name="host",proj='myproj'): #can change name of env as needed for command
    '''usage: rundev:name="host",proj="myproj"'''
    print "starting dev server..."
    local("cd /home/user/directory ; python manage.py runserver --insecure" % (name, proj))

def deploy(pushorpull='push',remoteenv='env',project='myproj',svName='',sshPort=):
    '''usage: fab deploy:pushorpull="push/pull",remotenv="myenv",project="myproj",svName="",sshPort="'''
    #svName='django' normally, but changed for first deploy to prevent failure
    print env.host_string
    wordlist=[] #parse data from 'pwd' command
    output = subprocess.Popen(['pwd'],\
        stdout=subprocess.PIPE).communicate()[0] #get location of virtualenv
    words = output.split('/') #use regex to split directories
    counter = 0 #keep track of which part is which 
    myDirShard = '' #will contain part of dir that I want
    for index in words:
        if counter > 0: #once we have passed the .virtualenv directory
            myDirShard += '/' + str(index).rstrip()
        if 'virtualenv' in index: #let us know when to start counting
            counter +=1
    myDirShard += '/' #add slashes so directory can be used as-is

    devdir = '/home/user/dir/'+ myDirShard #make dev dir for use with pull/push
    remotedir = str(env.host_string) + ":~/.virtualenvs" + '/' + remoteenv + '/' + project 
    print "Dev directory = {0} and remote directory = {1} - correct?".format(devdir,remotedir)
    print "Press enter if this is ok, or control-c to exit: "
    raw_input()
    if svName: #for first deploy, svName should not yet exist as there is no project to use runit against
        print"Stopping Django on {0} - press enter to continue or control-c to exit: ".format(env.host_string)
        raw_input()
        args = ('stop',svName,sshPort)
        _django(*args) #stop django so I can pull the database or push it back with other changes  
    
    if pushorpull == 'push':
        print "I will push {0} to {1}, ok?".format(devdir, remotedir)
        raw_input("press 'enter' to continue ...")
        local('rsync -avz -e "ssh -p %s" --progress %s %s' % (sshPort, devdir, remotedir))
    elif pushorpull == 'pull':
        print "I will pull {0} to {1}, ok?".format(remotedir, devdir)
        raw_input("press 'enter' to continue ...")
        local('rsync -avz -e "ssh -p %s" --progress %s %s' % (sshPort, remotedir, devdir))
    if svName:
        print"Starting Django on {0} ...".format(env.host_string)
        args = ('start',svName,sshPort)
        _django(*args)
    
    getmem()
    
def _django(DjangoCmd='restart',svName='myServiceName',sshPort=):
    #print "I will perform this option: {0}".format('sudo sv '+ DjangoCmd + " " + svName)
    #raw_input("press enter")
    env.host_string += ':' + sshPort
    sudo('sv %s %s' % (DjangoCmd, svName))

def getmem():
    ''' runs free -m command '''
    run('   free -m')

def _agent_run(cmd):

    #for h in env.hosts:
    for h in env.roledefs:
        try:
            host, port = h.split(':')
            local('ssh -p %s -A %s %s' % (port, host, cmd))
        except ValueError:
            local('ssh -A %s %s' % (h, cmd))
            
