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

    def _save_uploaded_file(self, video_file) -> str:
        import tempfile
        suffix = f".{video_file.name.split('.')[-1]}"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(video_file.getbuffer())
            return tmp.name

    def get_first_frame(self, video_file) -> np.ndarray:
        video_path = self._save_uploaded_file(video_file)

        try:
            cap = cv2.VideoCapture(video_path)
            ret, frame = cap.read()
            cap.release()

            if not ret:
                raise ValueError("Erster Frame konnte nicht geladen werden")

            return frame
        finally:
            if os.path.exists(video_path):
                os.remove(video_path)