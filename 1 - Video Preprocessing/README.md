# Video Preprocessing Script

This script is designed to support preprocessing videos by splitting common video format files such as `mp4,mov,avi,mkv` into 1-minute segments while maintaining the original video's encoding settings and quality.

## Requirements

- [`ffmpeg`](https://ffmpeg.org/) must be installed and accessible in your system's PATH.
- This script was tested on a Mac device with `ffmpeg` installed globally via [`Homebrew`](https://formulae.brew.sh/formula/ffmpeg).
- Alternatively, you can download a [static build](https://ffmpeg.org/download.html) of `ffmpeg` and place it in the same directory as this script and your video files.

## Usage

1. **Place the script in the directory containing your video files.**

2. **Update the encoding parameters to match your original video settings:**
   - `video_bitrate="740k"`
   - `audio_bitrate="125k"`
   - `framerate="29.97"`
   - `resolution="1280x720"`
   - `codec_video="libx264"`
   - `codec_audio="aac"`
   - `preset="medium"`

3. **Ensure the script has execution permissions:**

   ```bash
   chmod +x split_videos.sh
   ```

4. **Run the script:**

   ```bash
   ./split_videos.sh
   ```

## Script Details

### Parameters

- `video_bitrate`: Bitrate for the video stream.
- `audio_bitrate`: Bitrate for the audio stream.
- `framerate`: Frame rate of the video.
- `resolution`: Resolution of the video.
- `codec_video`: Video codec to be used.
- `codec_audio`: Audio codec to be used.
- `preset`: Preset for the ffmpeg encoder.

### Processing Steps

1. Loop through all video files in the current directory.
2. Extract the duration of each video file using `ffmpeg`.
3. Calculate the number of 1-minute segments and the duration of the last segment.
4. Split the video into 1-minute segments, re-encoding each segment to avoid black frames and ensure settings match the original.
5. Handle the last segment:
   - If the last segment is less than 30 seconds, append it to the previous segment.
   - Otherwise, process the last segment separately if it's 30 seconds or more.

### Example Output

For a video file named `example.mp4` with a duration of 2 minutes and 45 seconds, the output files will be:
- `example_Part_1.mp4` (1 minute)
- `example_Part_2.mp4` (1 minute)
- `example_Part_3.mp4` (45 seconds)

For a video file named `example2.mp4` with a duration of 3 minutes and 15 seconds, the output files will be:
- `example2_Part_1.mp4` (1 minute)
- `example2_Part_2.mp4` (1 minute)
- `example2_Part_3.mp4` (1 minute and 15 seconds)

### Notes

- If the script cannot determine the duration of a file, it will skip that file and move to the next.
- The script will display the processing status and the duration of each file being processed.

## Conclusion

This script automates splitting videos into manageable 1-minute segments while maintaining the original video's encoding settings. **Make sure to adjust the parameters to suit your video's encoding details.** Use the `ffmpeg -i {file_name}` command to view the parameters for your file and update these parameters in the script to ensure lossless quality output.