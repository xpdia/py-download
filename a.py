import subprocess

# Input and output filenames
input_video = 'vid.mp4'
output_video = 'output.mp4'

# Watermark image
watermark_image = 'wm.png'

# ffmpeg command to add watermark
ffmpeg_cmd = f'ffmpeg -i {input_video} -i {watermark_image} -filter_complex "overlay=10:10" {output_video}'

# Run the ffmpeg command
subprocess.call(ffmpeg_cmd, shell=True)

print(f'Watermark added successfully. Output saved as {output_video}')