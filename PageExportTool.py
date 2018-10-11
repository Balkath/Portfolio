import requests
import json
import csv



base_url = "https://api.sandbox.ecrimex.net"
phish_endpoint = "/phish"

headers = {
    'Authorization': "",
    'Content-Type': "application/json"
    }

def extractPhishData(endpoint):
    url = base_url + endpoint
    response = requests.request("GET", url, headers=headers)
    data = json.dumps(response.json())
    api_data = json.loads(data)
    links = api_data['_links']
    api_phish = api_data['_embedded']['phish']
    return_data = {'phish': api_phish, 'links': links}
    return return_data

output_data = []

temp_data = extractPhishData(phish_endpoint)

links = temp_data['links']

output_data.extend(temp_data['phish'])

while 'next' in links:
    next_url = links['next']['href']
    new_phish_data = extractPhishData(next_url)
    links = new_phish_data['links']
    output_data.extend(new_phish_data['phish'])

# Below is how you export data into a CSV file.

with open('Output_Phish_Data.csv', 'w',newline='') as new_csv_file:
    fieldnames = ['_links','id','url','brand','confidence_level','date_discovered','modified','asn','ip','domain','metadata','status']
    csv_writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames, delimiter= ',')
    csv_writer.writeheader()

    for line in output_data:
        csv_writer.writerow(line)




