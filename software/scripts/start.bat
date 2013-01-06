Y:\tools\ss\autorunsc.exe -a -c > Z:\before.csv
start Y:\tools\ss\procmon.exe /NoFilter /Minimized /BackingFile Z:\capture.pml
start "CaptureBAT" "C:\Program Files\Capture\CaptureBAT.exe" -c -l Z:\capture.log
