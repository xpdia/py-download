import subprocess

def apply_lut_and_watermark(input_video, lut_file, watermark_file, output_video):
    # Construct the ffmpeg command
    command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-hwaccel', 'cuda',  # Enable CUDA acceleration
        '-i', input_video,  # Input video file
        '-i', watermark_file,  # Input watermark image
        '-filter_complex', f"[0:v]hwupload_cuda,format=nv12,hwdownload,format=nv12,lut3d='{lut_file}',hwupload_cuda[video];[video][1:v]overlay_cuda=(main_w-overlay_w)/2:(main_h-overlay_h)/2,hwdownload",  # Apply LUT and overlay watermark using GPU
        '-c:v', 'h264_nvenc',  # Use NVENC for encoding
        '-c:a', 'copy',  # Copy audio stream without re-encoding
        output_video  # Output video file
    ]

    # Execute the command
    subprocess.run(command, check=True)

# Input and output files
input_video = 'assets/vid.mp4'
lut_file = 'assets/lut.cube'
watermark_file = 'assets/wm.png'
output_video = 'outputxgpu.mp4'

# Apply LUT and watermark
apply_lut_and_watermark(input_video, lut_file, watermark_file, output_video)
