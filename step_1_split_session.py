'''
如果间隔30分钟没有动作，则认为是新的session的开始，这个文件
主要分割大的session，减少item-cf的数据量

结果文件格式：每一行是一个session，session中的itemId由逗号分隔。
'''
import json

with open("./data/step_1_result.txt", "w+") as of:
    
    for idx, line in enumerate(open("raw_data/train.jsonl")):
        sessions = []
        last_events = []

        session_second_idx = 1
        js = json.loads(line.strip())
        session_id = str(js['session'])
        events = js['events']

        i = 0;
        j = 1;
        while i < len(events):
            if i == 0:
                last_events = []
                last_events.append(events[i])
            elif i > 0:
                if events[i]['ts'] - events[i-1]['ts'] > 30*60*1000:
                    sessions.append(("{}-{}".format(session_id, session_second_idx), last_events))
                    session_second_idx += 1
                    last_events = []
                    last_events.append(events[i])
                else:
                    last_events.append(events[i])
            i += 1

        if len(last_events) > 0:
            sessions.append(("{}-{}".format(session_id, session_second_idx), last_events))

        for session_id, events in sessions:
            event_aid_l = []
            for ev in events:
                event_aid_l.append(str(ev['aid']))
            of.write(",".join(event_aid_l)+"\n")

        



        
