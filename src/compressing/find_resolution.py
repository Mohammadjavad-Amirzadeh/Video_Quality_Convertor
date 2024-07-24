from moviepy.editor import VideoFileClip

def get_quality(input_path):
    clip = VideoFileClip(input_path)
    resolution = clip.size[1] 
    return resolution