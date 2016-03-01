from datetime import datetime
from email.mime.text import MIMEText
import sys
import os, os.path
import smtplib
import platform
import ConfigParser

#get app directory
appDirectory = os.path.dirname(os.path.abspath('__file__'))

#find config file
configParser = ConfigParser.RawConfigParser()
configFilePath = appDirectory + '\\email-vpn-logs.config'

#read in config
configParser.read(configFilePath)

logFilePath = configParser.get('Log', 'logFilePath')

userFlagStart = configParser.get('Flags', 'userFlagStart')                               
userFlagEnd = configParser.get('Flags', 'userFlagEnd') 
timeStampFlagStart = configParser.get('Flags', 'timeStampFlagStart')                             
timeStampFlagEnd = configParser.get('Flags', 'timeStampFlagEnd') 
IPFlagStart = configParser.get('Flags', 'IPFlagStart')                   
IPFlagEnd = configParser.get('Flags', 'IPFlagEnd') 

emailTo = configParser.get('Email', 'emailTo')  
emailFrom = configParser.get('Email', 'emailFrom')
SMTPServer = configParser.get('Email', 'SMTPServer')
SMTPUsername = configParser.get('Email', 'SMTPUsername')
SMTPPassword = configParser.get('Email', 'SMTPPassword')
SMTPPort = configParser.get('Email', 'SMTPPort')

users = ''
times = ''
IPs = ''

desktop = appDirectory

def readNewFile(path):                                                   #open latest log file
     fileName = path + "\\" + max(os.listdir(path))
     log = open(fileName, 'r')
     print fileName + " determined to be latest file"
     return log
     
def parseLog(log, users, times, IPs):                                    #parse out needed properties
     while True:
          line = log.readline()
          for item in line.split(userFlagEnd):                           # grab users
               if userFlagStart in item:               
                     users += item [ item.find(userFlagStart)+len(userFlagStart) : ] + ","
          for item in line.split(timeStampFlagEnd):
               if timeStampFlagStart in item:
                    times += item [ item.find(timeStampFlagStart)+len(timeStampFlagStart) : ]+ ","
          for item in line.split(IPFlagEnd):
               if IPFlagStart in item:
                    IPs += item [ item.find(IPFlagStart)+len(IPFlagStart) : ]+ ","
               
          if line == '':
               log.close()
               print "User data captured"
               return users, times, IPs

def formatFile(users, times, IPs): #put everything in array
     usersL = users.split(',')
     timesL = times.split(',')
     IPsL = IPs.split(',')     
     x=0
     newFile = open(desktop + 'temp_email.txt','w')
     newFile.write("REPORT DATE: " + str(datetime.now()) + "\n\n" + "LOG FILE PATH: " + logFilePath + "\n")
     newFile.write("=" * 100+"\n")
     while x < len(usersL):         
          newFile.write("\n" + usersL[x] + "\n " +timesL[x] + "\n" + IPsL[x]+"\n") 
          x+=1
     newFile.close()
     print "Formatting file for email..."
     

def sendEmail (desktop):
     print "Sending email..."
     fp = open(desktop + 'temp_email.txt', 'rb')
     # Create a text/plain message
     msg = MIMEText(fp.read())
     fp.close()

     me = emailFrom
     you = emailTo       

     msg['Subject'] = 'VPN Usage For ' + str(datetime.now())
     msg['From'] = me
     msg['To'] = you

     # Send the message via our own SMTP server, but don't include the
     # envelope header.
     s = smtplib.SMTP(SMTPServer, SMTPPort)
     s.login(SMTPUsername, SMTPPassword)
     s.sendmail(me, [you], msg.as_string())
     s.quit()
     print "SUCCESS!"
     
def main ():
     users = ''
     times = ''
     IPs = ''
     log = readNewFile(logFilePath)
     users, times, IPs = parseLog(log, users, times, IPs)
     formatFile(users, times, IPs)
     sendEmail(desktop)
     os.remove(desktop + 'temp_email.txt')
     sys.exit()

main()

