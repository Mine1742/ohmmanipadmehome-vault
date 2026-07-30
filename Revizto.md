#revizto
Need License > Paul chiappetta
and Group permission

install from the company portal once in the proper group

access to job model  ? 


Examples
Installation with default parameters
msiexec /i "Revizto(x64)-5.10.0.71080.msi" /q /qn /l*v "log.log"
Installation with proxy server setup
msiexec /i "Revizto(x64)-5.10.0.71080.msi" /q /qn /l*v "log.log" PROXY_IS_ON="true" HOST="192.168.1.1" PORT="1345" PROXYUSERNAME="username" PASSWORD="123"
Installation with specific plug-ins (Revit and Navisworks)
msiexec /i "Revizto(x64)-5.10.0.71080.msi" /q /qn /l*v "D:\Temp\log.log" PLUGINS="revit,navisworks"
Installation with updates disabled
msiexec /i "Revizto(x64)-5.10.0.71080.msi" /q /qn /l*v "D:\Temp\log.log" UPDATES_DISABLE="true"
Installation that does not create desktop shortcuts
msiexec /i "Revizto(x64)-5.10.0.71080.msi" /q /qn /l*v "D:\Temp\log.log" NOICONS="true"