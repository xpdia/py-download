import subprocess

def apply_lut_and_watermark(input_video, lut_file, watermark_file, output_video):
    # Construct the ffmpeg command
    command = [
        'ffmpeg',
        '-i', input_video,  # Input video file
        '-i', watermark_file,  # Input watermark image
        '-filter_complex', f"[0:v]lut3d='{lut_file}'[v0];[v0][1:v]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2",  # Apply LUT and overlay watermark
        '-c:a', 'copy',  # Copy audio stream without re-encoding
        output_video  # Output video file
    ]

    # Execute the command
    subprocess.run(command, check=True)

# Input and output files
input_video = 'assets/vid.mp4'
lut_file = 'assets/lut.cube'
watermark_file = 'assets/wm.png'
output_video = 'output.mp4'

# Apply LUT and watermark
apply_lut_and_watermark(input_video, lut_file, watermark_file, output_video)