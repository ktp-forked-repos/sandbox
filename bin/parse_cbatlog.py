#!/usr/bin/python

import sys
import csv

registry_modified = []
registry_deleted = []
file_modified = []
file_deleted = []
program_started = []
program_stopped = []

by_program = {}
name_lookup = { 
    'registry_modified': 'Registry Values Modified',
    'registry_deleted': 'Registry Values Deleted',
    'file_modified': 'Files Modified',
    'file_deleted': 'Files Deleted',
    'program_started': 'Processes Created',
    'program_stopped': 'Processes Terminated' }

for line in csv.reader(open(sys.argv[1], 'rb')):
    ftime, ftype, faction, fsource, fdest = line

    if not fsource in by_program:
        by_program[fsource] = { 
            'registry_modified': [], 
            'registry_deleted': [], 
            'file_modified': [], 
            'file_deleted': [], 
            'program_started': [], 
            'program_stopped': [] }

    if ftype == "registry" and faction.startswith("Set"):
        if not fdest in registry_modified:
            registry_modified.append(fdest)
        if not fdest in by_program[fsource]['registry_modified']:
            by_program[fsource]['registry_modified'].append(fdest)
    elif ftype == "registry" and faction.startswith("Delete"):
        if not fdest in registry_deleted:
            registry_deleted.append(fdest)
        if not fdest in by_program[fsource]['registry_deleted']:
            by_program[fsource]['registry_deleted'].append(fdest)
    elif ftype == "file" and faction == "Write":
        if not fdest in file_modified:
            file_modified.append(fdest)
        if not fdest in by_program[fsource]['file_modified']:
            by_program[fsource]['file_modified'].append(fdest)
    elif ftype == "file" and faction == "Delete":
        if not fdest in file_deleted:
            file_deleted.append(fdest)
        if not fdest in by_program[fsource]['file_deleted']:
            by_program[fsource]['file_deleted'].append(fdest)
    elif ftype == "process" and faction == "created":
        if not fdest in program_started:
            program_started.append(fdest)
        if not fdest in by_program[fsource]['program_started']:
            by_program[fsource]['program_started'].append(fdest)
    elif ftype == "process" and faction == "terminated":
        if not fdest in program_stopped:
            program_stopped.append(fdest)
        if not fdest in by_program[fsource]['program_stopped']:
            by_program[fsource]['program_stopped'].append(fdest)
    else:
        print "error parsing line: {0}".format(','.join(line))
        sys.exit(1)

            
print "================================================================================"
print "*** Files Modified ***"
for f in file_modified:
    print f
print
print "*** Files Deleted ***"
for f in file_deleted:
    print f
print
print "*** Registry Values Modified ***"
for r in registry_modified:
    print r
print
print "*** Registry Values Deleted ***"
for r in registry_deleted:
    print r
print
print "*** Processes Started ***"
for p in program_started:
    print p
print
print "*** Processes Terminated ***"
for p in program_stopped:
    print p
print
for p in by_program.keys():
    print "================================================================================"
    print "=== {0} ===".format(p)
    for k in ['registry_modified', 'registry_deleted', 'file_modified', 'file_deleted', 'program_started', 'program_stopped']:
        if len(by_program[p][k]) > 0:
            print "*** {0} ***".format(name_lookup[k])
            for r in by_program[p][k]:
                print r
    print

