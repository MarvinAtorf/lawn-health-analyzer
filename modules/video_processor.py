import cv2
import numpy as np
import tempfile
import os

class VideoProcessor:
    def __init__(self, sample_rate: int = 5):
        self.sample_rate = sample_rate

    def extract_frames(self, video_file) -> list:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(video_file.read())
            tmp_path = tmp.name

        cap = cv2.VideoCapture(tmp_path)
        frame_list = []
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % self.sample_rate == 0:
                frame_list.append(frame)
            frame_count += 1

        cap.release()
        os.remove(tmp_path)
        return frame_list