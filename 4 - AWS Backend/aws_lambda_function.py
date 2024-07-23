import boto3
import csv
import json
import re
import random
from io import StringIO
from collections import defaultdict

# Define the survey URL as a variable
SURVEY_URL = "" #Add your base REDCap Survey URL here

def generate_random_number(length=8):
    digits = [str(x) for x in range(10)]
    random_number = ''.join(random.choice(digits) for _ in range(length))
    return random_number

def extract_part_number(filename):
    match = re.match(r"^(.*_Part_)(\d+)(\.(mp4|mov|avi|mkv))$", filename)
    return int(match.group(2)) if match else 0

def read_state(s3_client, bucket, state_key):
    try:
        response = s3_client.get_object(Bucket=bucket, Key=state_key)
        state_data = response['Body'].read().decode('utf-8').strip()
        if state_data:
            return list(map(int, state_data.split()))
        else:
            # Return default values if the file is empty
            return [0, 0, 0]
    except Exception as e:
        print(f"Error reading state: {e}")
        # Return default values if there's an error reading the file
        return [0, 0, 0]

def write_state(s3_client, bucket, state_key, video_index, round_index, batch_index):
    state_data = f"{video_index} {round_index} {batch_index}"
    s3_client.put_object(Bucket=bucket, Key=state_key, Body=state_data)

def lambda_handler(event, context):
    s3_bucket = "clipsdata"
    s3_key = "videos_list.csv"
    state_key = "script_state.txt"
    s3_client = boto3.client('s3')

    # Read CSV data from S3
    try:
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
        csv_data = response['Body'].read().decode('utf-8')
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f"Failed to read CSV: {str(e)}")}

    data = StringIO(csv_data)
    reader = csv.DictReader(data)
    rows = list(reader)
    header = reader.fieldnames

    watched_columns = ['watched_1', 'watched_2', 'watched_3', 'watched_4', 'watched_5']
    watched_indexes = [header.index(col) for col in watched_columns]

    video_groups = defaultdict(list)
    for row in rows:
        base_name = "_".join(row['name'].split("_")[:-1])
        video_groups[base_name].append(row)

    sorted_groups = sorted(video_groups.keys())

    current_video_index, current_round_index, current_batch_index = read_state(s3_client, s3_bucket, state_key)
    video_name = sorted_groups[current_video_index]
    group = sorted(video_groups[video_name], key=lambda x: extract_part_number(x['name']))

    first_batch_size = len(group) // 2 + len(group) % 2
    second_batch_size = len(group) // 2

    batch_start_index = 0 if current_batch_index == 0 else first_batch_size
    batch_end_index = first_batch_size if current_batch_index == 0 else len(group)

    all_videos = ""
    for i, row in enumerate(group[batch_start_index:batch_end_index], 1):
        row[watched_columns[current_round_index]] = 'x'
        video_name = f"video_{i}={row['link']}"
        all_videos += "&" + video_name if i > 1 else video_name

    if current_batch_index == 0:
        current_batch_index = 1
    else:
        current_batch_index = 0
        current_video_index += 1
        if current_video_index >= len(sorted_groups):
            current_video_index = 0
            current_round_index += 1
            if current_round_index >= len(watched_columns):
                current_round_index = 0

    write_state(s3_client, s3_bucket, state_key, current_video_index, current_round_index, current_batch_index)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)
    s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=output.getvalue())

    target_url = f"{SURVEY_URL}&{all_videos}&sp={generate_random_number()}"
    html_content = f"<html><head><title>Redirecting...</title><script type='text/javascript'>window.location.href = '{target_url}';</script></head><body><p>If you are not redirected, <a href='{target_url}'>click here to continue</a>.</p></body></html>"

    return {'statusCode': 200, 'headers': {'Content-Type': 'text/html'}, 'body': html_content}
