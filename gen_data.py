import json
import pandas as pd
from tqdm import tqdm

userID_dict = {}

with open("data/sasrec_data_1.txt", "w+") as of:
    #of.write("userID\titemID\n")
    for line in tqdm(open("raw_data/train.jsonl")):
        js = json.loads(line.strip("\n"))
        events = js["events"]
        events = events[-50:]
        session_id = js['session']
        if len(events) >= 7:
            userID = session_id
            if userID not in userID_dict:
                userID_dict[userID] = len(userID_dict)
            for ev in events:
                of.write("{}\t{}\n".format(userID_dict[userID], ev['aid']))

    for line in tqdm(open("raw_data/test.jsonl")):
        js = json.loads(line.strip("\n"))
        events = js["events"]
        events = events[-50:]
        session_id = js['session']

        userID = session_id
        if userID not in userID_dict:
            userID_dict[userID] = len(userID_dict)
        for ev in events:
            of.write("{}\t{}\n".format(userID_dict[userID], ev['aid']))

userID_list = []
mapped_userID_list = []
for userID, mapped_userID in userID_dict.items():
    userID_list.append(userID)
    mapped_userID_list.append(mapped_userID)

df = pd.DataFrame({"userID": userID_list, "mapped_userID": mapped_userID_list})
df.to_csv("data/user_id_map.csv", sep="\t", index=False, header=False)

print (len(df))











