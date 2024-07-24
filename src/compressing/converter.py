from moviepy.editor import VideoFileClip

def convert_video(input_path, output_path, resolution):
    clip = VideoFileClip(input_path)
    clip_resized = clip.resize(height=resolution)
    clip_resized.write_videofile(output_path, codec='libx264')