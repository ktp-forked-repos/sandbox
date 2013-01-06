Y:\tools\ss\procmon.exe /Terminate
Y:\tools\ss\pskill.exe -accepteula CaptureBAT.exe
Y:\tools\ss\autorunsc.exe -a -c > z:\after.csv
Y:\tools\ss\procmon.exe /OpenLog z:\capture.pml /SaveAs z:\capture.csv
REM start MemoryDump "C:\Program Files\MANDIANT\Memoryze\MemoryDD.bat" -o Z:\
