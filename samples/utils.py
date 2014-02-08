import argparse
from os import sys
import random
from sys import path
from os import getcwd
import os, sys, inspect, pprint

# this is a hack to get the hp driver module
# and it's utils module on the search path.
cmd_folder = os.path.realpath(os.path.abspath("..") )
if cmd_folder not in sys.path:
     sys.path.insert(0, cmd_folder)

from hplefthandclient import client, exceptions


def get_volumes(cl):
    print "Get Volumes"
    try:
       volumes = cl.getVolumes()
       if volumes:
           for volume in volumes['members']:
               print "Found '%s'" % volume['name']
    except exceptions.HTTPUnauthorized as ex:
       print "You must login first"
    except Exception as ex:
       print ex
    print "Complete\n"

def get_volume(cl, name):
    print "Get Volume %s" % name
    try:
        vol = cl.getVolume(name)
        pprint.pprint(vol)
    except exceptions.HTTPUnauthorized as ex:
       print "You must login first"
    except Exception as ex:
       print ex
    print "Complete\n"

def get_hosts(cl):
    print "Get Hosts"
    try:
       hosts = cl.getHosts()
       if hosts:
           for host in hosts['members']:
               pprint.pprint(host)
#               print "Found '%s'" % host['name']
    except exceptions.HTTPUnauthorized as ex:
       print "You must login first"
    except Exception as ex:
       print ex

def get_host(cl,hostname):
    try:
        host = cl.getHost(hostname)
        pprint.pprint(host)
    except exceptions.HTTPUnauthorized as ex:
       print "You must login first"
    except Exception as ex:
       print ex

def delete_host(cl,hostname):
    try:
        host = cl.deleteHost(hostname)
    except exceptions.HTTPUnauthorized as ex:
       print "You must login first"
    except Exception as ex:
       print ex

def get_host_vluns(cl,hostname):
    try:
        host = cl.getHostVLUNs(hostname)
        pprint.pprint(host)
    except exceptions.HTTPUnauthorized as ex:
       print "You must login first"
    except Exception as ex:
       print ex

def delete_host_vluns(cl, hostName):
    try:
        vluns = cl.getHostVLUNs(hostName)
        if vluns:
            for vlun in vluns:
                print "Deleting VLUN %s " % vlun['volumeName']
                cl.deleteVLUN(vlun['volumeName'], vlun['lun'], 
                              vlun['hostname'], vlun['portPos'])

    except exceptions.HTTPUnauthorized as ex:
        print "You must login"
    except Exception as ex:
        print ex

def get_ports(cl):
    try:
        ports = cl.getPorts()
        pprint.pprint(ports)
    except exceptions.HTTPUnauthorized as ex:
       print "You must login first"
    except Exception as ex:
       print ex


def get_vluns(cl):
    print "Get VLUNs"
    try:
        vluns = cl.getVLUNs()
        if vluns:
            pprint.pprint(vluns)
            for vlun in vluns['members']:
                pprint.pprint(vlun)
                print "Found VLUN '%s'" % vlun['volumeName']
    except exceptions.HTTPUnauthorized as ex:
       print "You must login first"
    except Exception as ex:
       print ex


def get_vlun(cl,vlunname):
    try:
        vlun = cl.getVLUN(vlunname)
        pprint.pprint(vlun)
    except exceptions.HTTPUnauthorized as ex:
       print "You must login first"
    except Exception as ex:
       print ex


def get_cpgs(cl):
    print "Get CPGs"
    try:
        cpgs = cl.getCPGs()
        if cpgs:
            for cpg in cpgs['members']:
                print "Found CPG '%s'" % cpg['name']
    except exceptions.HTTPUnauthorized as ex:
       print "You must login first"
    except Exception as ex:
       print ex

def get_cpg(cl, name):
    try:
        cpg = cl.getCPG(name)
        pprint.pprint(cpg)
    except exceptions.HTTPUnauthorized as ex:
       print "You must login first"
    except Exception as ex:
       print ex
