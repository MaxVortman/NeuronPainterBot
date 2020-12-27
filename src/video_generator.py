import PIL
import cv2
import numpy as np
import src.image_generator


def gen_video(file_path, style):
    vidcap = cv2.VideoCapture(file_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('../data/output.mp4', fourcc, fps, (frame_width, frame_height))
    success, img = vidcap.read()
    while success:
        im_pil = PIL.Image.fromarray(img)
        out_img = src.image_generator.gen_img(im_pil, style)
        out.write(np.asarray(out_img))
        success, img = vidcap.read()
    vidcap.release()
    out.release()
