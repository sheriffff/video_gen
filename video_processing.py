from moviepy import (
    VideoFileClip,
    concatenate_videoclips,
    CompositeVideoClip,
    TextClip,
    clips_array,
    ColorClip,
    AudioFileClip,
)

from config import (
    FINAL_VIDEO_TEXT_FONT_SIZE,
    FINAL_VIDEO_BITRATE,
    FINAL_VIDEO_FPS,
    FINAL_VIDEO_THREADS,
    FINAL_VIDEO_PRESET
)


def extract_first_frame(video_path, output_path):
    with VideoFileClip(video_path) as clip:
        clip.save_frame(output_path, t=0)
        duration = int(clip.duration)
        if duration < 2:
            duration = 2
        elif duration > 10:
            duration = 10
        print(f"Fotograma guardado en {output_path}. Duración: {duration}s")

        return duration


def create_final_montage(real_video_path, ai_video_path, output_path, text_overlay):
    print("Iniciando montaje de vídeo...")
    # acaba 1080x1920
    # cada uno 1080x960

    # Load videos (960x960)
    real_video = VideoFileClip(real_video_path)
    ai_video = VideoFileClip(ai_video_path)

    # Create black background clips (1080x960)
    real_bg = ColorClip(size=(1080, 960), color=(0, 0, 0), duration=real_video.duration)
    ai_bg = ColorClip(size=(1080, 960), color=(0, 0, 0), duration=ai_video.duration)

    # Center the 960px videos on the 1080px backgrounds (adds 60px padding on each side)
    real_clip = CompositeVideoClip([real_bg, real_video.with_position('center')], size=(1080, 960))
    ai_clip = CompositeVideoClip([ai_bg, ai_video.with_position('center')], size=(1080, 960))

    duration_real = real_clip.duration
    duration_ai = ai_clip.duration

    real_frame_clip = real_clip.to_ImageClip(t=0).with_duration(duration_ai)
    ai_frame_clip = ai_clip.to_ImageClip(t=0).with_duration(duration_real)

    part_A = clips_array([
        [real_clip],
        [ai_frame_clip]
    ])

    part_B = clips_array([
        [real_frame_clip],
        [ai_clip]
    ])

    final_clip = concatenate_videoclips([part_A, part_B])

    font = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
    # font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    # font = '/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf'
    # font = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
    # font = '/usr/share/fonts/truetype/ubuntu/Ubuntu[wdth,wght].ttf'
    # font = '/usr/share/fonts/truetype/msttcorefonts/arialbd.ttf'  # Arial Bold
    # font = 'Arial'  # Font name (only this one works without path)

    txt_clip = TextClip(
        text=text_overlay,
        font_size=FINAL_VIDEO_TEXT_FONT_SIZE,
        color='white',
        font=font,
        stroke_color='black',
        stroke_width=3
    )
    txt_clip = txt_clip.with_position(('center', 'center')).with_duration(final_clip.duration)

    video = CompositeVideoClip([final_clip, txt_clip])

    # Add audio to the video
    audio = AudioFileClip('audio_ia2.mp3')
    video = video.with_audio(audio)

    video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        threads=FINAL_VIDEO_THREADS,
        preset=FINAL_VIDEO_PRESET,
        bitrate=FINAL_VIDEO_BITRATE,
        fps=FINAL_VIDEO_FPS
    )

    print(f"¡Vídeo final guardado en: {output_path}!")
