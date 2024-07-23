# S3 Video Link Processor

This script fetches video files from a specified S3 bucket, processes them in batches, tracks their viewership state, and generates a redirect URL for a survey, appending video links as parameters.

## Requirements

- An S3 bucket containing a CSV file generated with the structure defined in the [Accessible Video URLs CSV Generation](https://github.com/kbjohnson-penn/CLIPS/tree/main/2%20-%20Accessible%20Video%20URLs%20CSV%20Generation/Box%2C%20Inc.) repository.

## Setup

1. Replace the `SURVEY_URL` variable with your actual survey URL in the script.
2. Configure your AWS credentials to allow access to the S3 bucket containing the CSV file.
3. Set up an AWS API Gateway endpoint as a trigger for the Lambda function.
4. Ensure the API Gateway endpoint has a timeout setting of 5 seconds.

## Usage

Deploy the script `s3_video_link_processor.py`'s content as an AWS Lambda Python function and set up a trigger for it via an API Gateway endpoint.

**Output:**

When the API URL is accessed, the script will update the state file and video list CSV file in the specified S3 bucket and redirects to the survey URL with video links appended as parameters.

## Script Details

### Parameters

- `s3_bucket`: The name of the S3 bucket containing the video list and state files.
- `s3_key`: The name of the CSV file in the S3 bucket.
- `SURVEY_URL`: The base URL for the REDCap survey to which video links are appended as parameters.

### Processing Steps

1. Fetch the video list from the specified S3 bucket.
2. Group videos by their base name and sort them.
3. Read the current processing state from the state file.
4. Determine the current batch of videos to process and mark them as watched.
5. Update the state for the next invocation.
6. Write the updated video list and state back to the S3 bucket.
7. Generate a redirect URL with the video links and a random parameter.
8. Redirect the user to the generated URL.

### Example Output

For video files in the S3 bucket, the output includes:

- Updated state file in the S3 bucket, tracking which videos and batches have been processed.
- Updated video list CSV file with `watched` columns indicating which videos have been watched.
- A redirect to the survey URL, including video links and a random generated number parameter that the respondent can enter back in the survey platform for surveyor identification and validation.

## Conclusion

This script automates processing video files in an S3 bucket, tracking their viewership state, and generating a survey URL with video links appended as parameters to a REDCap survey URL.