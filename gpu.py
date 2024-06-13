import subprocess

# Input and output filenames
input_video = 'vid.mp4'
output_video = 'output.mp4'

# Watermark image
watermark_image = 'wm.png'

# ffmpeg command with optimizations
ffmpeg_cmd = (
    f'ffmpeg -i {input_video} -i {watermark_image} '
    '-filter_complex "[0:v][1:v]overlay=10:10" '
    '-c:v h264_nvenc -preset fast '  # Example of using NVIDIA NVENC for hardware acceleration
    f'{output_video}'
)

# Run the ffmpeg command
subprocess.call(ffmpeg_cmd, shell=True)

print(f'Watermark added successfully. Output saved as {output_video}')