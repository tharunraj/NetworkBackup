from netmiko import ConnectHandler
import getpass
import sys
import time
import datetime


####Device Credentials

USER = 'YourUserName'
PASSWORD = 'YourPassword'

##getting system date

day=time.strftime('%d')
month=time.strftime('%m')
year=time.strftime('%Y')
today=day+"-"+month+"-"+year
now = datetime.datetime.now()

##initialising device
device = {
    'device_type': 'cisco_ios',
     'username': USER,
    'password': PASSWORD,
    }

#########opening IP file which contains Device IPs lie by line

ipfile=open("/tmp/inputfile")
for line in ipfile:
 try:
     device['ip']=line.strip("\n")
     print("\n\nConnecting Device ",line)
     net_connect = ConnectHandler(**device)
     #net_connect.enable()
     time.sleep(1)
     print ("Reading the running config ")
     output = net_connect.send_command('terminal pager lines 0\n')
     time.sleep(3)
     print("Executing 'sh run'")
     output1 = net_connect.send_command('sh run')
     time.sleep(3)
     filename_prefix='/tmp/Device'+ '='+device['ip']
     print("Generating Result...")
     print("Please Wait........!")
     filename = "%s_%.2i\%.2i\%i_%.2i:%.2i:%.2i" % (filename_prefix,now.day,now.month,now.year,now.hour,now.minute,now.second)
     ff = open(filename, 'a')
     ff.write(output1)
     ff.close()
 except:
           print ("Access to "+device['ip']+" failed,backup did not taken")
           print(device['ip'])
           filename='/tmp/FailedIPs_'+ today
           ff=open(filename,'a')
           ff.write(device['ip'])
           ff.write('\n')
           ff.close( )
ipfile.close()
print ("\nAll device backup completed")
