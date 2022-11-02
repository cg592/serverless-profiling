# importing the requests library
import requests
import sys

# api-endpoint
URL = sys.argv[1]

# location given here
location = "delhi technological university"

# defining a params dict for the parameters to be sent to the API
PARAMS = {'address':location}

# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)

# extracting data in json format
data = r.json()

output = open("output_va_concurr_3frames_2replica_medium.txt", "a")
output.write("URL: " + URL + "\n")

filtered = list(filter(lambda d: 'videoservice.videodecoder/decode' in d["name"], data))
if (len(filtered) != 0):
    print(len(filtered))
    streaming_timestamp = filtered[0]['timestamp']
    print(streaming_timestamp)
    decode_timestamp = filtered[1]['timestamp']
    print(decode_timestamp)
    decode_diff = decode_timestamp - streaming_timestamp
    print(decode_diff)
    output.write("" + str(streaming_timestamp) + "\n")
    output.write("" + str(decode_timestamp) + "\n")
    output.write("Decode_diff: " + str(decode_diff) + "\n")

filtered = list(filter(lambda d: d["name"] == 'helloworld.greeter/sayhello', data))
if (len(filtered) != 0):
    duration = filtered[0]['duration']
    output.write("Duration: " + str(duration) + "\n")

recog_times = []
filtered = list(filter(lambda d: d["name"] == '/videoservice.objectrecognition/recognise', data))
if (len(filtered) != 0):
    print(len(filtered))
    recog_times = [elem['timestamp'] for elem in filtered]
    recog_times.sort()

    recog_diff = recog_times[1] - recog_times[0]

    output.write("" + str(recog_times) + "\n")
    output.write("Recog_diff: " + str(recog_diff) + "\n")

output.close()
