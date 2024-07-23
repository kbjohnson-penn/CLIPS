# Box Video Link Generator

This script fetches video files from a specified Box folder, generates shared links for each file, sorts them by their filenames, and outputs the information into a CSV file that tracks viewership.

## Requirements

- Python 3.x
- `requests` library
- `json` library
- `csv` library
- `re` library

Make sure to install the necessary Python packages before running the script:
```bash
pip install requests
```

## Setup

1. Replace the `folder_number` with the folder number in Box containing your video files.
2. Replace `box_token` with your actual token from Box Postman authorization.

## Usage

Run the script:

```bash
python box_video_link_generator.py
```

**Output:**

The script will create a CSV file named `sorted_videos_list.csv` in the same directory.

## Script Details

### Parameters

- `folder_number`: The ID number of the Box folder containing the videos.
- `box_token`: The authorization token for accessing Box.

### Processing Steps

1. Authenticate with Box using the provided token.
2. Fetch the list of video files from the specified folder.
3. Generate shared links for each video file.
4. Sort the video files by their filenames.
5. Output the sorted list with shared links into a CSV file.

### Example Output

For video files in the Box folder, the output CSV file will contain columns like:

- `filename`: The name of the video file.
- `shared_link`: The generated shared link for the video.
- Placeholder columns for backend tracking of viewership (initially empty).
    - `watched_1`
    - `watched_2`
    - `watched_3`
    - `watched_4`
    - `watched_5`

### Notes

- Make sure the Box folder number and token are correctly set to avoid authentication issues.
- The script assumes the presence of video files in the specified folder and will sort and generate links for all videos found.

## Conclusion

This script automates the process of generating shared links for video files in a Box folder and outputs them into a CSV file for easy tracking and management. Ensure to update the folder number and token in the script for it to function correctly.
