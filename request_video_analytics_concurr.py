# importing the requests library
import requests
import sys
import time

output = open("o.txt", "w")

URL = "http://localhost:9411/zipkin/api/v2/traces"
PARAMS = {'serviceName':'decoder', 'limit':2000}
r = requests.get(url = URL, params = PARAMS)
frames = sys.argv[1]

all_data = r.json()
all_data = sorted(all_data, key=lambda x: x[0]['timestamp'])

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

all_data_chunks = list(divide_chunks(all_data, int(frames)+1))

for j in range(0, len(all_data_chunks)):
    recog_diff = []
    output.write("TRACE " + str(j) + ": " + str(all_data_chunks[j][0][0]['timestamp']) + "\n")
    for i in range(0, len(all_data_chunks[j])):
        data = all_data_chunks[j][i]
        filtered = list(filter(lambda d: 'videoservice.videodecoder/decode' in d["name"], data))
        if (len(filtered) != 0):
            streaming_timestamp = filtered[0]['timestamp']
            decode_timestamp = filtered[1]['timestamp']
            decode_diff = decode_timestamp - streaming_timestamp
            output.write("Decode Diff: " + str(decode_diff) + "\n")

        filtered = list(filter(lambda d: d["name"] == 'helloworld.greeter/sayhello', data))
        if (len(filtered) != 0):
            duration = filtered[0]['duration']
            output.write("Trace Duration: " + str(duration) + "\n")

        recog_times = []
        filtered = list(filter(lambda d: d["name"] == '/videoservice.objectrecognition/recognise', data))
        if (len(filtered) != 0):
            recog_times = [elem['timestamp'] for elem in filtered]
            recog_times.sort()
            local_diff = recog_times[1] - recog_times[0]
            # print("local diff: " + str(local_diff))
            recog_diff.append(local_diff)

    # Once done, calculate max recognition time
    max_recog = max(recog_diff, default=0)
    output.write("Max Recog Diff: " + str(max_recog) + "\n")
    output.write("-----------------------------------------\n")

output.close()
