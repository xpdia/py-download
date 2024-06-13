import os
import yt_dlp

# Define the directory to save the downloaded videos
save_directory = 'assets'

# Create the directory if it doesn't exist
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Define the options for yt_dlp
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    'outtmpl': os.path.join(save_directory, '%(title)s.%(ext)s'),
    'merge_output_format': 'mp4',
}

# Function to download a video from YouTube
def download_video(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Example usage
if __name__ == '__main__':
    video_url = "https://m.youtube.com/watch?v=se50viFJ0AQ"
    download_video(video_url)
    print(f"Video has been downloaded and saved to the '{save_directory}' directory.")