'''
Created on Apr 28, 2014

@author: pkajan
'''
import csv
import json

x="""[ 
    { "pk": 22, "model": "auth.permission", "fields": 
        { "codename": "add_logentry", "name": "Can add log entry", "content_type": 8 } 
    }, 
    { "pk": 23, "model": "auth.permission", "fields": 
        { "codename": "change_logentry", "name": "Can change log entry", "content_type": 8 } 
    },
    { "pk": 24, "model": "auth.permission", "fields": 
        { "codename": "delete_logentry", "name": "Can delete log entry", "content_type": 8 } 
    }
]"""



file = open("data.json")
x = json.loads(x)

f = csv.writer(open("data.csv", "wb+"))


# 
# f.writerow(["pk", "model", "codename", "name", "content_type"])

for x in x:
    f.writerow([x["pk"], 
                x["model"], 
                x["fields"]["codename"], 
                x["fields"]["name"],
                x["fields"]["content_type"]])