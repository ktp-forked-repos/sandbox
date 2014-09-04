# vim: sw=4:ts=4:et
#
# guest VM action
# brought to you by the cat fancier society
#

# the tools we'll be a-needin'
# autorunsc
# handle
# procmon
# capturebat
# procdump

# start up and configure yourself
## read some file with configuration settings
## set IP address
## set DNS ?
## wait for things to settle down...
## execute before actions
### autorunsc
### handles
### process list
### anything else from the LR stuff we've got
## start capturebat
## start procmon
## get ready to execute malware
## signal that we're ready for snapshot!
## watch for new malware file
## execute malware file
## sleep for a bit
## stop procmon
## stop capturebat?
## execute after actions
### auturunsc
### handles
### process list
### parse procmon output
### optionally dump process memory
### copy all the stuff over to the transfer point
### signal that we're done
# host takes another snapshot
# hard drive is cloned from this snapshot into a file for mounting
# mount the filesystem readonly
# copy all the modified files out (as per procmon and capturebat)
# parse all the things
# say bye bye to cuckoo
