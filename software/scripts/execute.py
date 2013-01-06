#
# analyze_malware.py
# 
#

import sys
from subprocess import call, Popen, PIPE
from optparse import OptionParser
import os.path
import time
import os

def execute_program(program, params, output):
	Popen(params, stdout=output)

# check to see if we are in auto mode
if not os.path.exists(r'Z:\auto'):
	sys.exit(0)

out_file = open(r'Z:\before.csv', 'wb')
p = Popen([r'Y:\tools\ss\autorunsc.exe', '-a', '-c', '--accepteula'], STDOUT=out_file)
p.wait()
out_file.close()

procmon = Popen([r'Y:\tools\ss\procmon.exe', '/BackingFile', '/NoFilter', r'Z:\capture.pml'])
capturebat = Popen([r'C:\Program Files\Capture\CaptureBAT.exe', '-c', '-l', r'Z:\capture.log'])

os.start(r'Z:\target.exe')

time.sleep(1)

call([r'Y:\tools\ss\procmon.exe', '/Terminate'])
call([r'Y:\tools\ss\pskill.exe', '-accepteula', 'CaptureBAT.exe'])

call([r'Y:\tools\ss\procmon.exe', '/OpenLog', r'Z:\capture.pml', '/SaveAs', r'Z:\capture.csv'])

out_file = open(r'Z:\after.csv', 'wb')
p = Popen([r'Y:\tools\ss\autorunsc.exe', '-a', '-c', '--accepteula'], STDOUT=out_file)
p.wait()
out_file.close()

#call([r'C:\Program Files\MANDIANT\Memoryze\MemoryDD.bat' '-o' r'Z:\\'])

open(r'Z:\done', 'wb')
