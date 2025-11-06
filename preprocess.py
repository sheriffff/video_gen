import subprocess
from moviepy import VideoFileClip
from config import INITIAL_VIDEO_RATIO


def preprocess_video(input_video_path, output_video_path):
    with VideoFileClip(input_video_path) as clip:
        width, height = clip.size

    current_ratio = width / height

    if abs(current_ratio - INITIAL_VIDEO_RATIO) > 0.01:
        print(f"Video detectado: {width}x{height} (ratio {current_ratio:.2f}). Cropendo a ratio {INITIAL_VIDEO_RATIO:.2f}...")

        if current_ratio > INITIAL_VIDEO_RATIO:
            new_width = int(height * INITIAL_VIDEO_RATIO)
            new_height = height
            x_offset = (width - new_width) // 2
            y_offset = 0
        else:
            new_width = width
            new_height = int(width / INITIAL_VIDEO_RATIO)
            x_offset = 0
            y_offset = (height - new_height) // 2

        cmd = [
            'ffmpeg',
            '-i', input_video_path,
            '-vf', f'crop={new_width}:{new_height}:{x_offset}:{y_offset}',
            '-c:a', 'copy',
            '-y',
            output_video_path
        ]

        print(f"Ejecutando ffmpeg crop: {new_width}x{new_height}")
        subprocess.run(cmd, check=True)
        print(f"Video recortado guardado en: {output_video_path}")
        return output_video_path
    else:
        print(f"Video ya tiene el ratio correcto ({width}x{height}). No necesita recorte.")
        return input_video_path


