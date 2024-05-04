import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from pytubefix import YouTube, Channel
import os

CHANNEL_LINK = "https://www.youtube.com/@hubermanlab"


def get_videos_df_from_channel(channel_url):
    """
    Fetches video data from a YouTube channel and returns it as a DataFrame.

    Args:
        channel_url (str): The URL of the YouTube channel.

    Returns:
        pandas.DataFrame: A DataFrame containing video data.
    """
    # Instantiate Channel object
    channel = Channel(channel_url)
    df = pd.DataFrame()

    # Print number of videos in the channel
    print(f"There are {len(channel.videos)} videos in {channel.channel_name}")

    # Loop through videos in the channel
    for idx, video in enumerate(channel.videos):
        if idx % 10 == 0:
            print(f"Processing {idx}/{len(channel.videos)} video")

        # Collect video information
        video_info = {
            "video_id": video.video_id,
            "title": video.title,
            "publish_date": video.publish_date,
            "length": video.length,
            "thumbnail": video.thumbnail_url,
            "vid_info": video.vid_info,
        }

        try:
            # Get transcript for the video
            transcript = YouTubeTranscriptApi.get_transcript(video.video_id)
            video_info["transcript"] = TextFormatter().format_transcript(transcript)
        except:
            print("No transcripts available for", video.video_id)
            video_info["transcript"] = "NA"
            continue

        # Append video information to DataFrame
        df = pd.concat([df, pd.DataFrame([video_info])], ignore_index=True)

    return df


# Fetch video data from the Huberman Lab YouTube channel
hub_df = get_videos_df_from_channel(CHANNEL_LINK)

hub_df.to_csv("data/huberman_transcripts_050124.csv")

# Iterate over each row in the DataFrame and save transcripts as markdown files
for index, row in hub_df.iterrows():
    # Get the title and transcript
    title = row["title"]
    transcript = row["transcript"]

    # Define the filename for the markdown file
    filename = os.path.join("data", "transcripts", f"{title}.md")

    # Write transcript to markdown file
    with open(filename, "w") as file:
        file.write(transcript)
