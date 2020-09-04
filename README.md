# Tripwire
A basic telegram bot reads from auth.log of remote server and reports using python.
It reads from auth.log file of your server. It searches for the log file in its directory. It is recommended to using a crontab to backup your auth.log in the same directory that this script exists. Please don't give root access or don't put in inside "/var/log". Just don't.

  ``` 
  pip3 -m install requirements.txt
  python3 Trigger.py 
  ```
  Before running with python3 don't forget to add your telegram bot token to Trigger.py and your log file name to tripwire.py.
  After that it should work just fine.
  
