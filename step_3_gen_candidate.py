import json

item_2_item_list = {}
for line in open("data/step_2_result.txt"):
    key_item_id, item_list = line.strip('\n').split("\t")
    if len(item_list) == 0:
        continue
    item_list = [item for item in item_list.split(',') if len(item) > 0]
    item_dict = {}
    l = []
    for item in item_list:
        item_id, cnt = item.split(":", 1)
        l.append((item_id, int(cnt)))
    item_2_item_list[int(key_item_id)] = l

of =  open("data/result.txt", "w+")
of.write("session_type,labels\n")

for line in open("raw_data/test.jsonl"):
    js = json.loads(line.strip("\n"))
    session_id = js['session']
    d = {}
    events = js['events']
    events = events[-20:]
    for ev in events:
        item_id = ev['aid']
        l = item_2_item_list.get(item_id, [])
        for item_id2, cnt in l:
            if item_id2 in d:
                d[item_id2] += cnt
            else:
                d[item_id2] = cnt

    l = [(item_id, cnt) for item_id, cnt in d.items()]
    l = sorted(l, key=lambda x:x[1], reverse=True)[:20]
    values = " ".join([item_id for item_id, _ in l])
    of.write(f"{session_id}_clicks,{values}\n")
    of.write(f"{session_id}_carts,{values}\n")
    of.write(f"{session_id}_orders,{values}\n")

of.close()
        