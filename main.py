from runway_api import generate_ai_video_from_image
from video_processing import extract_first_frame, create_final_montage
from preprocess import preprocess_video
from datetime import datetime
from pathlib import Path


if __name__ == "__main__":
    INPUT_VIDEO_PATH = "rubik.mp4"
    INPUT_PROMPT = "Cube explodes in his hands, and burns his hair"

    TEMP_DIR = Path("temp")
    TEMP_DIR.mkdir(exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    PREPROCESSED_VIDEO_PATH = str(TEMP_DIR / f"video_preprocessed_{now}.mp4")
    OUTPUT_FIRST_FRAME_PATH = str(TEMP_DIR / f"image_first_frame_{now}.png")
    OUTPUT_AI_VIDEO_PATH = str(TEMP_DIR / f"video_ai_{now}.mp4")
    OUTPUT_FINAL_VIDEO_PATH = f"video_final_{now}.mp4"

    video_to_process_path = preprocess_video(INPUT_VIDEO_PATH, PREPROCESSED_VIDEO_PATH)

    input_duration = extract_first_frame(video_to_process_path, OUTPUT_FIRST_FRAME_PATH)

    output_ai_video_path = generate_ai_video_from_image(OUTPUT_FIRST_FRAME_PATH, INPUT_PROMPT, input_duration, OUTPUT_AI_VIDEO_PATH)

    create_final_montage(
        video_to_process_path,
        output_ai_video_path,
        OUTPUT_FINAL_VIDEO_PATH,
        '¿Cuál es IA?'
    )
