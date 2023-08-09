import requests
import getpass
from datetime import datetime
import csv
import pandas as pd
import json

requests.packages.urllib3.disable_warnings()

#Set Row Size
pd.options.display.max_rows = 10000

# Current Date/Time
current_date = datetime.now().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H:%M:%S")
print("\n" + current_time, current_date)

# Enter Aruba Controller
print("\nLogging into Aruba Controller....")
controller = input("\nEnter Aruba Controller: ")

# Enter Username And Password
username = input("\nUsername: ")
pswd = getpass.getpass('Password: ')

# Open File To Write Logs
results = open("user-table.txt", "a")

# Log into Aruba Controller and retrieve UIDARUBA for API access
r = requests.get(url='https://' + controller + ':4343/v1/api/login?username='
                     + username + '&password=' + pswd, verify=False)
logindata = r.json()
uid = logindata['_global_result']['UIDARUBA']
cookies = {'SESSION': uid}
print("\n\n Your UID for this sessions is: " + uid + "\n")

getusers_data = requests.get(
url = "https://" + controller + ":4343/v1/configuration/showcommand?json=1&command=show+user-table&UIDARUBA=" + uid, verify=False,
    cookies=cookies)
users = getusers_data.json()

#print(users)
df = pd.DataFrame (users.get('Users'))
#df_users = df[['IP','MAC','Name','Role','Age(d:h:m)','Auth','AP name','Profile','Type']]
df_users = df[['Name','Role','Age(d:h:m)']]
print(df_users)

print("\n\nUsers Table File created: User-Table.txt " + current_time, current_date, "\n", file=results)
print("\n" + df_users, file=results)
print("\nEnd " + current_time, current_date, file=results)
