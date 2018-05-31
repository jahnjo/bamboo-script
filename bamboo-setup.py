#!usr/bin/python2.7
import sys
import os
import tarfile
import subprocess

user = sys.argv[-1]

bambooHomeDir = '/home/{}/Bamboo/Bamboo-Home/'.format(user)
bambooInstallDir = '/home/{}/Bamboo/Bamboo-Install/'.format(user)
bambooDownloadLocation = '/home/{}/Downloads/atlassian-bamboo-6.5.0.tar.gz'.format(user) 
bambooDownloadLink = 'https://www.atlassian.com/software/bamboo/downloads/binary/atlassian-bamboo-6.5.0.tar.gz'
bambooInit = bambooInstallDir + 'atlassian-bamboo-6.5.0/atlassian-bamboo/WEB-INF/classes/bamboo-init.properties'
bambooHomeConfig = 'bamboo.home=' + bambooHomeDir 
startServer = bambooInstallDir + 'atlassian-bamboo-6.5.0/bin/start-bamboo.sh'
cmd = ['git','cmake','gcc','g++','lcov','cppcheck','python','perl','Digest:MD5 (perl module)']
absentCmd = []

#Going through dependencies for bamboo plugins and printing the dependencies that are needed.
def checkDependencies():
    print 'Checking for dependencies'
    for i in range(len(cmd)):
	if subprocess.call("type " + cmd[i],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE):
	    absentCmd.append(cmd[i])
    if len(absentCmd) > 0:
        print '\nDependencies still needed:'
        print "\n".join(absentCmd)
        print '\n'
    

#Installing pip so we can use pip install wget to download bamboo.
def getPip():
    if os.path.exists('get-pip.py'):
        print 'Pip is already installed'
    else:
        print 'Downloading pip'
        subprocess.call(["curl","https://bootstrap.pypa.io/get-pip.py","-o","get-pip.py"])
        subprocess.call("python get-pip.py", shell=True)
        subprocess.call([sys.executable,'-m','pip','install','wget'])

#Using wget to download bamboo.
def downloadBamboo():
    if os.path.exists(bambooDownloadLocation):
        print 'Bamboo already downloaded'
    else:
        print 'Downloading wget'
        wget.download(bambooDownloadLink,out=bambooDownloadLocation)

#Taking the tar.gz that was downloaded and extracting it to the bamboo install directory.
def extractBamboo():
    if os.path.exists(bambooInstallDir + 'atlassian-bamboo-6.5.0'):
       print 'Bamboo download already extracted'
    else:
       tar = tarfile.open(bambooDownloadLocation)
       tar.extractall(path=bambooInstallDir)
       tar.close()

#Making the bamboo home and bamboo install directories.    
def makeBambooDirectories():
    if not os.path.exists(bambooHomeDir):
       os.makedirs(bambooHomeDir)
    else:
       print '\nBamboo-Home already exists in the home directory'

    if not os.path.exists(bambooInstallDir):
       os.makedirs(bambooInstallDir)
    else:
       print '\nBamboo-Install already exists in the home directory'

#Used to change the location of bamboo-home within bamboo-init.properties
def configBambooHome():
    if os.path.exists(bambooInstallDir):
        if bambooHomeConfig in open(bambooInit).read():
            print 'Bamboo has already been configured'
        else:
            print '\nConfiguring bamboo properties'
            print 'Adding',bambooHomeConfig,'to',bambooInit
            subprocess.call("echo {} >> {}".format(bambooHomeConfig,bambooInit), shell=True)
            print 'Done configuring'
    else:
        print 'An error has occured bamboo install directory doesn\'t exists'
    
#Prompting the user to start the server
def startBambooServer():
    input = raw_input("Do you want to start the server? (y/n)\n")
    if input == 'y':
        subprocess.call("{}".format(startServer), shell=True)
    else:
        print 'Refer to wiki to start server'

getPip()
import wget
downloadBamboo()
makeBambooDirectories() 
extractBamboo()
configBambooHome()
checkDependencies()
startBambooServer()
