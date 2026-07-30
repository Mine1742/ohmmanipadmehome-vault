#time

need sync time for auth protocols, including the local admin account.
if all auth goes away then need to safe mode reset the clock to get admin credentials back in order to make time synch changes and further TS


w32tm /resync
w32tm /query /status
w32tm /config /manualpeerlist:"time.windows.com,0x1" /syncfromflags:manual /reliable:YES /update
net stop w32time && net start w32time
