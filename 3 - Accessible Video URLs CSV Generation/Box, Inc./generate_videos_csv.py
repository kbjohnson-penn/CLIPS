import requests
import json
import csv
import re

# Replace with your actual folder number and Box token
folder_number = 123456789101  # The folder number in Box containing your video files, this can be found in the URL when accessing online
box_token = "********************************"  # Replace with your actual token from Box Postman authorization

# Get folder file contents
url = f'https://api.box.com/2.0/folders/{folder_number}/items?limit=1000'
headers = {
    'Authorization': f'Bearer {box_token}'
}
response = requests.get(url, headers=headers)

# Define a function to extract parts of the filename for sorting
def sort_key(filename):
    # This regular expression looks for the last occurrence of '_Part_' followed by numbers.
    match = re.match(r"^(.*_Part_)(\d+)(\.(mp4|mov|avi|mkv))$", filename)
    if match:
        # Return a tuple (base part, numeric part as integer)
        return (match.group(1), int(match.group(2)))
    else:
        # Return the filename as is if no matching format is present
        return (filename, 0)

# URL template for generating shared links
url_template = "https://api.box.com/2.0/files/{file_ID}?fields=shared_link"
payload = json.dumps({
    "shared_link": {
        "access": "open",
        "unshared_at": None,
        "permissions": {
            "can_download": False,
            "can_preview": True,
            "can_edit": False
        }
    }
})

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {box_token}'
}

# Prepare data for CSV, ensuring it's sorted by the filename with custom sorting key
sorted_entries = sorted(response.json()['entries'], key=lambda x: sort_key(x['name']))
csv_data = [["name", "link", "watched_1", "watched_2", "watched_3", "watched_4", "watched_5"]]

# Iterate over each sorted file entry and make the API call
for entry in sorted_entries:
    file_id = entry["id"]
    name = entry["name"]
    url = url_template.format(file_ID=file_id)
    
    response = requests.put(url, headers=headers, data=payload)
    if response.status_code == 200:
        response_data = response.json()
        shared_link = response_data.get("shared_link", {}).get("url", "")
        csv_data.append([name, shared_link, "", "", "", "", ""])
    else:
        print(f"Failed to get shared link for file ID {file_id}")

# Write the data to a CSV file
csv_file_path = "sorted_videos_list.csv"
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

print(f"CSV file '{csv_file_path}' generated successfully.")
