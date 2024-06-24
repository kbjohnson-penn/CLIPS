# Box Video Link Generator

This script fetches video files from a specified Box folder, generates shared links for each file, sorts them by their filenames, and outputs the information into a CSV file that tracks viewership.

## Setup

1. Replace the `folder_number` with the folder number in Box containing your video files.
2. Replace `box_token` with your actual token from Box Postman authorization.

## Usage

1. Run the script:
    ```bash
    python box_video_link_generator.py
    ```

2. The script will create a CSV file named `sorted_videos_list.csv` in the same directory.

## Dependencies

- `requests`
- `json`
- `csv`
- `re`

Make sure to install the necessary Python packages before running the script:
```bash
pip install requests
```