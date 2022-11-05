# importing the requests library
import requests
import sys

# api-endpoint
# URL = sys.argv[1]

# location given here
# location = "delhi technological university"
#
# # defining a params dict for the parameters to be sent to the API
# PARAMS = {'serviceName':'decoder'}
# PARAMS = {'serviceName':'video streaming@8d66540e82f8-fu'}
PARAMS = {'serviceName':'recog'}

# sending get request and saving the response as response object
# r = requests.get(url = URL, params = PARAMS)

# extracting data in json format
# data = r.json()

output = open("output_va_concurr_20frames_2replica_11522.txt", "a")
recog_diff = []

# for i in range(1, len(sys.argv)):
for i in range(1, 2):
    print("here")
    # URL = sys.argv[i]
    URL = "http://localhost:9411/zipkin/api/v2/traces"
    PARAMS = {'serviceName':'decoder'}
    r = requests.get(url = URL, params = PARAMS)
    # print(r)
    data = r.json()
    data = data[0]
    # print(data)
    output.write("URL: " + URL + "\n")

    filtered = list(filter(lambda d: 'videoservice.videodecoder/decode' in d["name"], data))
    if (len(filtered) != 0):
        # print(len(filtered))
        streaming_timestamp = filtered[0]['timestamp']
        # print(streaming_timestamp)
        decode_timestamp = filtered[1]['timestamp']
        # print(decode_timestamp)
        decode_diff = decode_timestamp - streaming_timestamp
        # print(decode_diff)
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
        recog_times = [elem['timestamp'] for elem in filtered]
        recog_times.sort()
        local_diff = recog_times[1] - recog_times[0]
        print("local diff: " + str(local_diff))
        recog_diff.append(local_diff)

# Once done, calculate max recognition time
max_recog = max(recog_diff, default=0)
output.write("Max Recog Diff: " + str(max_recog) + "\n")

output.close()
