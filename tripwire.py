from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests
import telegram
import json
import re

class GatherLogs:

    def __init__(self, token):
        self.bot = telegram.Bot(token)
        self.update = Updater(token=token, use_context=True)
        self.dispatch = self.update.dispatcher

    # This function is for creating command instances easier.
    def createHandler(self, command, commandfunction):
        start_handler = CommandHandler(command=command, callback=commandfunction)
        self.dispatch.add_handler(start_handler)

    # Opens and reads your backed up logfile. Then makes "grep" operation based on pattern given as parameter.
    def droplog(self, pattern):
        logfile = open("log.log") #Enter your log file to read.
        lines = list(logfile.readlines())
        list_of_matches = []

        for line in lines:
            if re.search(pattern, line):
                list_of_matches.append(line)

        return list_of_matches

    #Enumerates through backed-up data granted acces lines and sends date-time and IP that access granted.
    def granted(self, update, context):
        pattern = "Accepted publickey for root"
        rawlogin = self.droplog(pattern)
        send = ""

        for parse in rawlogin:
            ip = parse.split()
            time_date = ip[0] + ip[1] + "  >> " + ip[2]

            if ip[10] == "": #Add your whitelisted IPs
                send = f"Connection granted to owner. Login time: {time_date}"

            else:
                intruder = ip[10]
                send = f"INTRUDER ALERT: {intruder} -> Intrusion Time: {time_date}"

        context.bot.send_message(chat_id=update.effective_chat.id, text=send)

    # Shows unsuccessful login attempts. Then uses geoip get request to search about intruder IP and writes information to Report.txt
    # Only when command is used it sends Report.txt
    def denied(self, update, context):
        pattern = "Disconnected from authenticating user"
        line = self.droplog(pattern)
        send_report = open("Report.txt", "w")

        for row in line:
            raw = row.split()
            IP = raw[10]
            port = raw[12]
            time_date = raw[0] + raw[1] + "  >> " + raw[2]

            IPloc = self.geoip(IP)
            IPloc["Port"] = port
            IPloc["Time-Date"] = time_date

            send_report.write(str(json.dump(IPloc, send_report))+"\n\n\n")

        last_report = open("Report.txt", "rb")
        context.bot.send_document(chat_id=update.effective_chat.id, document=last_report)

    #Internet connection is necessary, geoip information is extracted by get request to http://ipwhois.app/json url.
    def geoip(self, loginIP):
        url = "http://ipwhois.app/json/" + loginIP
        request = requests.get(url)
        json_data = json.loads(request.text)

        return json_data
