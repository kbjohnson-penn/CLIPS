#!/bin/bash
# This script is video-format specific
# Update the parameters below to closely match your original video's encoding, this information can be found for your video files by using the "ffmpeg -i {file_name}" command
video_bitrate="740k"
audio_bitrate="125k"
framerate="29.97"
resolution="1280x720"
codec_video="libx264"
codec_audio="aac"
preset="medium"

# Loop through all specified video file types in the current directory
for file in *.{mp4,mov,avi,mkv}; do
    # Check if file exists to avoid processing non-existing file patterns
    if [ ! -e "$file" ]; then
        continue
    fi

    echo "Processing $file"

    # Extract the file extension
    extension="${file##*.}"

    # Extract the duration using ffmpeg, convert to seconds
    duration=$(ffmpeg -i "$file" 2>&1 | grep "Duration" | cut -d ' ' -f 4 | sed s/,// | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 }' | awk '{print int($1)}')

    # Check if duration was successfully retrieved
    if [ -z "$duration" ]; then
        echo "Could not determine duration of $file"
        continue # Skip this file and move to the next
    fi

    echo "Duration: $duration seconds"

    # Calculate the number of full 1-minute parts and the length of the last segment
    parts=$((duration / 60))
    last_part=$((duration % 60))

    # If the last segment is less than 30 seconds and not the first segment, reduce the count of parts
    if [ "$last_part" -lt 30 ] && [ "$last_part" -gt 0 ] && [ "$parts" -gt 0 ]; then
        append_last_part=true
        parts=$((parts - 1))
    else
        append_last_part=false
    fi

    # Extract parts with re-encoding and closely match original settings
    for ((i=0; i<parts; i++)); do
        start=$((i * 60))
        ffmpeg -i "$file" -ss "$start" -t 60 -c:v "$codec_video" -b:v "$video_bitrate" -r "$framerate" -s "$resolution" -c:a "$codec_audio" -b:a "$audio_bitrate" -preset "$preset" "${file%.*}_Part_$((i+1)).${extension}"
    done

    # Handle last segment if it needs to be appended
    if [ "$append_last_part" = true ]; then
        start=$((parts * 60))
        ffmpeg -i "$file" -ss "$start" -c:v "$codec_video" -b:v "$video_bitrate" -r "$framerate" -s "$resolution" -c:a "$codec_audio" -b:a "$audio_bitrate" -preset "$preset" "${file%.*}_Part_$((parts + 1)).${extension}"
    elif [ "$last_part" -ge 30 ]; then
        start=$((parts * 60))
        ffmpeg -i "$file" -ss "$start" -t "$last_part" -c:v "$codec_video" -b:v "$video_bitrate" -r "$framerate" -s "$resolution" -c:a "$codec_audio" -b:a "$audio_bitrate" -preset "$preset" "${file%.*}_Part_$((parts + 1)).${extension}"
    fi

done

echo "All videos processed."
