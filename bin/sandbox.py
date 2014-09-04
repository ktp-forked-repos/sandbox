# vim: sw=4:ts=4:et
#

import os
import logging
from subprocess import Popen, PIPE
import re

# globals
global_config = None
base_directory = None

# local constants
_SANDBOX_HOME = 'SANDBOX_HOME'
VBOX = 'VBoxManage -q'

def _vbox(*args):
    r = [ 'VBoxManage', '-q' ]
    r.extend(args)
    return r

def initialize():
    global base_directory
    if not _SANDBOX_HOME in os.environ:
        logging.warning("missing environment variable SANDBOX_HOME, assuming current working directory")
        base_directory = os.getcwd()
    else:
        base_directory = os.environ[_SANDBOX_HOME]

# utility functions
def create_sandbox(source_vm, dest_vm, snapshot=None):
    assert source_vm is not None
    assert source_vm != ''
    assert dest_vm is not None
    assert dest_vm != ''
    assert snapshot is not None
    assert snapshot != ''

    # make sure the trace directory exists
    if not os.path.exists(os.path.join(base_directory, 'traces')):
        logging.fatal("trace directory does not exist")
        return False

    if not clone_vm(source_vm, dest_vm, snapshot):
        logging.error("clone_vm failed")
        return False

    # delete previous trace files
    trace_file = os.path.join(base_directory, 'traces', "{0}.pcap".format(dest_vm))
    if os.path.exists(trace_file):
        try:
            os.remove(trace_file)
        except Exception, e:
            logging.error("unable to delete trace file {0}: {1}".format(
                trace_file, str(e)))

    # TODO check to see what state the source VM was in
    if not modify_vm(dest_vm, trace_file=trace_file):
        logging.error("modify_vm failed")
        return False

    #$vm_cmd modifyvm "$dst_vm" --memory 1024 --boot1 dvd --boot2 disk --nic1 bridged --bridgeadapter1 malware0 --nictrace1 on --nictracefile1 "$SANDBOX/traces/$dst_vm.pcap"

    shared_path = os.path.join(base_directory, 'shared', dest_vm)
    if not os.path.isdir(shared_path):
        try:
            os.path.makedir(shared_path)
        except Exception, e:
            logging.error("unable to create dir {0}: {1}".format(
                shared_path, str(e)))

    if has_shared_folder(dest_vm, 'shared'):
        if not remove_shared_folder(dest_vm, 'shared'):
            logging.error("unable to remove shared folder")
            return False

    if not add_shared_folder(dest_vm, 'shared', shared_path):
        logging.error("unable to add shared folder")
        return False

    return True

    # reset the shared folder
    #mkdir -p "$SANDBOX/shared/$dst_vm"
    #$vm_cmd sharedfolder remove "$dst_vm" --name shared
    #$vm_cmd sharedfolder add "$dst_vm" --name shared --hostpath "$SANDBOX/shared/$dst_vm"

def vm_exists(vm):
    """Returns True if a given vm exists, false otherwise."""
    (stdout, stderr, returncode) = show_vm_info(vm)
    return returncode == 0

def show_vm_info(vm):
    p = Popen(_vbox('showvminfo', vm), stdout=PIPE, stderr=PIPE)
    (stdout, stderr) = p.communicate()
    return (stdout, stderr, p.returncode)

def clone_vm(source_vm, dest_vm, snapshot=None):
    assert source_vm is not None
    assert source_vm != ''
    assert dest_vm is not None
    assert dest_vm != ''
    assert snapshot is not None
    assert snapshot != ''

    p = Popen(_vbox('clonevm', 
        source_vm, 
        '--snapshot', snapshot, 
        '--mode', 'machine',
        '--options', 'link',
        '--name', dest_vm,
        '--register'))
    p.wait()

    return p.returncode == 0

def modify_vm(vm, trace_file=None):
    assert vm is not None
    assert vm != ''
    
    args = _vbox('modifyvm', vm)
    if trace_file is not None:
        args.extend(['--nictrace1', 'on',  '--nictracefile1', trace_file])
    
    # anything to do?
    if len(args) == 3:
        return None

    p = Popen(args)
    p.wait()
    
    return p.returncode == 0

def has_shared_folder(vm, name):
    assert vm is not None
    assert vm != ''
    assert name is not None 
    assert name != ''

    (stdout, stderr, result) = show_vm_info(vm)
    for line in stdout:
        m = re.search(r"Name: '([^']+)', Host path:", line)
        if m:
            if m.group(1) == name:
                return True

    return False

def remove_shared_folder(vm, name):
    assert vm is not None
    assert vm != ''
    assert name is not None 
    assert name != ''

    p = Popen(_vbox('sharedfolder', 'remove', vm, '--name', name))
    p.wait()

    return p.returncode == 0

def add_shared_folder(vm, name, path):
    assert vm is not None
    assert vm != ''
    assert name is not None 
    assert name != ''
    assert path is not None 
    assert path != ''
    assert os.path.isabs(path)

    p = Popen(_vbox('sharedfolder', 'add', vm, '--name', name, '--hostpath', path))
    p.wait()

    return p.returncode == 0
