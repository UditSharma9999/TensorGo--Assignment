# To use this package, simply install it via pip:
# !pip install realesrgan-ncnn-py  moviepy
# For Linux user:
# !apt install -y libomp5 libvulkan-dev


import cv2
import os
import gc
import numpy as np
from realesrgan_ncnn_py import Realesrgan
from moviepy.editor import ImageSequenceClip



def upscale_frame(upscaled_frames_path, model, videocapture):

    os.makedirs(upscaled_frames_path, exist_ok=True)

    new_width = 1280
    new_height = 720
    
    success, image = videocapture.read()
    count = 0
    while success:
        frame_image_path = f"{upscaled_frames_path}/frame_{count:04d}.png"

        enhanced_image = model.process_cv2(image)

        img = np.array(enhanced_image)
        img = cv2.resize(img, (new_width, new_height))
        cv2.imwrite(frame_image_path, img)

        success, image = videocapture.read()
        
        count += 1
        gc.collect()
    videocapture.release()


def frames_to_video(frames_dir, output_video_path, fps):
    frame_files = sorted([os.path.join(frames_dir, f) for f in os.listdir(frames_dir)])
    clip = ImageSequenceClip(frame_files, fps=fps)
    clip.write_videofile(output_video_path, codec='libx264')


def main():
    input_video_path = 'input.mp4'
    upscaled_frames_path = 'build/upscaled_frames'
    output_video_path = 'build/output_hd_video.mp4'

    os.makedirs("build", exist_ok=True)
    
    cap = cv2.VideoCapture(input_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    model = Realesrgan(gpuid=1)
    upscale_frame(upscaled_frames_path,  model, cap)
    frames_to_video(upscaled_frames_path, output_video_path, fps)

main()