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
#print(data)

filtered = list(filter(lambda d: 'videoservice.videodecoder/decode' in d["name"], data))
print(len(filtered))
streaming_timestamp = filtered[0]['timestamp']
print(streaming_timestamp)
decode_timestamp = filtered[1]['timestamp']
print(decode_timestamp)
diff = decode_timestamp - streaming_timestamp
print(diff)

recog_times = []

filtered = list(filter(lambda d: d["name"] == '/videoservice.objectrecognition/recognise', data))
print(len(filtered))
recog_times = [elem['timestamp'] for elem in filtered]
recog_times.sort()

diff1 = recog_times[5] - recog_times[4]
diff2 = recog_times[3] - recog_times[2]
diff3 = recog_times[1] - recog_times[0]

sum = diff + diff1 + diff2 + diff3

duration = data[1]['duration']

output = open("output_va.txt", "a")
output.write("URL: " + URL + "\n")
output.write("" + str(streaming_timestamp) + "\n")
output.write("" + str(decode_timestamp) + "\n")
output.write("Diff: " + str(diff) + "\n")
output.write("" + str(recog_times) + "\n")
output.write("Sum: " + str(sum) + "\n")
output.write("Duration: " + str(duration) + "\n")
output.close()
