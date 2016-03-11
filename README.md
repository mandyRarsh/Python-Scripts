# Python-Scripts

getRadiusVPNLogs is specifically designed to:

1. grab the log file from a mapped drive 
2. parse out the needed text 
3. put it in a temporary file 
4. load that file into an e-mail 
5. send the email 
6. then delete the temporary file

# Requires Python 2.7 interpreter

# Build/Use instructions
1. Use Py2Exe to create executable (http://www.py2exe.org/index.cgi/Tutorial)
2. Alter example.ini to match needed settings
3. Run .exe in same directory as .ini
4. Use flag/argument to run:
  a. first argument is name of .ini file
  b. second argument is -repeats or -norepeats depending on if repeated user entries in log should be captured


