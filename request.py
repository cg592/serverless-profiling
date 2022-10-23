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

consumer_timestamp = data[2]['timestamp']
print(consumer_timestamp)
producer_timestamp = data[3]['timestamp']
print(producer_timestamp)

diff = consumer_timestamp - producer_timestamp
print(diff)

output = open("output.txt", "a")
output.write("URL: " + URL + "\n")
output.write("" + str(consumer_timestamp) + "\n")
output.write("" + str(producer_timestamp) + "\n")
output.write("" + str(diff) + "\n")
output.close()
