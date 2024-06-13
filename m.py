import os
import glob
import threading
from queue import Queue
import subprocess

def process_video(input_video, lut_file, watermark_file, output_video):
    """Process a single video with LUT and watermark."""
    try:
        # Check for GPU availability using nvidia-smi (if installed)
        gpu_available = subprocess.run(['nvidia-smi', '-L'], capture_output=True).stdout.decode().find('qsv') != -1
    except FileNotFoundError:
        gpu_available = False

    # Select hardware encoder based on GPU availability (qsv preferred)
    encoder = 'h264_qsv' if gpu_available else 'h264_nvenc'

    # Prioritize speed with faster preset (acknowledging potential quality loss)
    preset = 'fast'

    command = [
        'ffmpeg',
        '-i', input_video,
        '-i', watermark_file,
        '-filter_complex', (
            f"[0:v]scale=1080:1920[v0];"
            f"[v0]lut3d='{lut_file}'[v1];"
            f"[v1][1:v]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2"
        ),
        '-c:v', encoder,
        '-pix_fmt', 'yuv420p',
        '-b:v', '10M',
        '-preset', preset,
        '-c:a', 'aac',
        '-b:a', '192k',
        '-y',
        output_video
    ]

    subprocess.run(command, check=True)

def video_worker(queue, lut_file, watermark_file, output_dir):
    """Worker function to process videos from the queue."""
    while True:
        input_video = queue.get()
        if input_video is None:
            break
        video_name = os.path.basename(input_video)
        output_video = os.path.join(output_dir, video_name)
        process_video(input_video, lut_file, watermark_file, output_video)
        queue.task_done()

def process_videos(input_dir, lut_file, watermark_file, output_dir, max_workers=50):
    """Process all videos in input_dir using multiple threads."""
    os.makedirs(output_dir, exist_ok=True)
    video_files = glob.glob(os.path.join(input_dir, '*.mp4'))

    queue = Queue()
    for video_file in video_files:
        queue.put(video_file)

    threads = []
    for _ in range(max_workers):
        thread = threading.Thread(target=video_worker, args=(queue, lut_file, watermark_file, output_dir))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    queue.join()

    # Stop workers
    for _ in range(max_workers):
        queue.put(None)

    for thread in threads:
        thread.join()

# Example usage
input_dir = 'video'
lut_file = 'assets/lut.cube'
watermark_file = 'assets/wm.png'
output_dir = 'output'

process_videos(input_dir, lut_file, watermark_file, output_dir, max_workers=50)