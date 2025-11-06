import base64
import requests
from runwayml import RunwayML, TaskFailedError
from cache import compute_cache_key, get_cached_video, cache_video
from config import INITIAL_VIDEO_WIDTH, INITIAL_VIDEO_HEIGHT

with open("runway_api_key.txt") as f:
    API_KEY = f.read().strip()


def generate_ai_video_from_image(image_path, prompt, duration_seconds, output_ai_video_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()

    data_uri = f"data:image/png;base64,{base64.b64encode(image_data).decode('utf-8')}"

    model = 'gen4_turbo'
    ratio = f'{INITIAL_VIDEO_WIDTH}:{INITIAL_VIDEO_HEIGHT}'

    cache_key = compute_cache_key(model, data_uri, prompt, duration_seconds)
    cached_video_path = get_cached_video(cache_key)

    if cached_video_path:
        output_ai_video_path = cached_video_path
    else:
        client = RunwayML(api_key=API_KEY)

        task = client.image_to_video.create(
            model=model,
            prompt_image=data_uri,
            prompt_text=prompt,
            ratio=ratio,
            duration=duration_seconds,
        ).wait_for_task_output()

        video_url = task.output[0] if isinstance(task.output, list) else task.output
        download_video(video_url, output_ai_video_path, cache_key)

    return output_ai_video_path


def download_video(url, output_path, cache_key=None):
    response = requests.get(url)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"Vídeo IA guardado en: {output_path}")

    if cache_key:
        cache_video(cache_key, output_path)

    return True

