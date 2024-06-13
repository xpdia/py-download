import subprocess

def apply_lut_and_watermark(input_video, lut_file, watermark_file, output_video):
    command = [
        'ffmpeg',
        '-i', input_video,            # Input video file
        '-i', watermark_file,         # Input watermark image
        '-filter_complex', (
            f"[0:v]scale=1080:1920[v0];"       # Scale input video to match watermark size if necessary
            f"[v0]lut3d='{lut_file}'[v1];"     # Apply LUT to the scaled video
            f"[v1][1:v]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2"  # Overlay watermark
        ),
        '-c:v', 'h264_nvenc',         # Encode using NVIDIA's H.264 encoder
        '-pix_fmt', 'yuv420p',        # Ensure pixel format compatibility
        '-b:v', '10M',                # Bitrate for the video
        '-preset', 'slow',            # Preset for the encoder (adjust as needed)
        '-c:a', 'aac',                # Encode audio to AAC format
        '-b:a', '192k',               # Bitrate for audio
        '-y',                         # Overwrite output file without asking
        output_video                  # Output video file
    ]

    subprocess.run(command, check=True)

# Example usage
input_video = 'assets/vid.mp4'
lut_file = 'assets/lut.cube'
watermark_file = 'assets/wm.png'
output_video = 'output.mp4'

apply_lut_and_watermark(input_video, lut_file, watermark_file, output_video)
