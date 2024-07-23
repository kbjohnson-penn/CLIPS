# CLIPS - Crowdsourcing Likely Insights from Patient Encounter Snippets

## Introduction
The CLIPS project is part of the REDUCE (Reimagining Documentation Using Computation from Clinical Encounters) initiative, which aims to leverage multi-modal data from clinical encounters to enhance clinical documentation. CLIPS focuses on gathering insights from clinical encounter videos through crowdsourcing. This repository is set up to distribute your repository of videos into two one-minute halves for this purpose.

## CLIPS Objectives
1. **Primary Objective:** Collect qualitative and quantitative data on diverse perspectives regarding clinical encounter videos.
2. **Primary Outcome:** Comprehensive set of annotations per video segment, categorized into both categorical labels and free-form text descriptions.
3. **Secondary Outcomes:** Demographic and mediator data such as medical experience, age, language preference, race, ethnicity, occupation, and current state of residence.

## Integration and Tools
CLIPS integrates REDCap with Amazon AWS and an embeddable content delivery network for efficient video handling and scalable data collection. This integration addresses the challenge of embedding a library of video segments of varied lengths for crowdsourced ground truth labeling in REDCap.

## Key Features
- **Efficient Video Management:** Handles varied segmented video libraries using a content delivery network (CDN).
- **Metadata- driven survey URL generation:** Dynamically generates survey URLs based on video metadata.
- **One URL with access to multiple surveys:** Provides a single URL point of access that can direct participants to the same survey with different media content.

## Repository Structure
This repository contains all the necessary components to replicate and extend the CLIPS project. The structure is as follows:
```
.
├── 1 - REDCap Survey
│   ├── README.md
│   ├── CLIPSSurveyREDCap.xml
├── 2 - Video Preprocessing
│   ├── README.md
│   ├── split_videos.sh
├── 3 - Accessible Video URLs CSV Generation
│   ├── Box, Inc.
│   │   ├── README.md
│   │   ├── generate_videos_csv.py
├── 4 - AWS Backend
│   ├── README.md
│   ├── aws_lambda_function.py
```

## Getting Started
### Prerequisites
- Python
- REDCap access
- AWS account
- A content delivery network
- An Amazon Mechanical Turk Requester account with increased payment limits

### Installation
1. Clone the repository:
```
git clone https://github.com/kbjohnson-penn/CLIPS.git
cd CLIPS
```
2. Configure your survey variables for REDCap, your AWS account, your content delivery network (Box was used for our purposes), and your Amazon Mechanical Turk Requester account.

### Hosting the Project

1. Follow the instructions in 

2. Preprocessing Videos:
    - Place your videos in the same directory as [split_videos.sh](https://github.com/kbjohnson-penn/CLIPS/blob/main/2%20-%20Video%20Preprocessing/split_videos.sh)
    - Ensure the script has execution, read, and write permissions:
        ```
        chmod +rwx split_videos.sh
        ```
    - Run the script to split your videos into one-minute segments:
        ```
        ./split_videos.sh
        ```

3. Generate a CSV file with all your video names and URLs (this step is [CDN-specific](https://github.com/kbjohnson-penn/CLIPS/tree/main/3%20-%20Accessible%20Video%20URLs%20CSV%20Generation)).

4. Host the CSV file in an AWS S3 bucket with accessible permissions from your Lambda function.

5. Deploy AWS Lambda Functions for URL Redirect: [aws_lambda_function.py](https://github.com/kbjohnson-penn/CLIPS/blob/main/4%20-%20AWS%20Backend/aws_lambda_function.py)

## Contributing

We welcome contributions from the community, especially for expanding the list of supported CDNs that embed in REDCap.

## License

This project is licensed under the Creative Commons Attribution 4.0 International License. You must give appropriate credit, provide a link to the license, and indicate if changes were made. See the [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/) for details.

[![Creative Commons License](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/)

## Acknowledgements

We would like to thank the team at the University of Pennsylvania, contributors, and supporting staff who have made this project possible.
