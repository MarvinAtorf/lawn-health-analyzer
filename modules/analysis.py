import cv2
import numpy as np

class LawnAnalyzer:

    def analyze_frames(self, frames: list) -> dict:
        total_healthy = 0
        total_stress = 0
        total_bare = 0

        lower_healthy = np.array([35, 40, 40])
        upper_healthy = np.array([90, 255, 255])
        lower_stress = np.array([10, 30, 40])
        upper_stress = np.array([35, 255, 255])
        lower_bare = np.array([0, 0, 50])
        upper_bare = np.array([180, 40, 255])

        sample_frame = None
        sample_mask_healthy = None
        sample_mask_stress = None
        sample_mask_bare = None


        for frame in frames:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            mask_healthy = cv2.inRange(hsv, lower_healthy, upper_healthy)
            mask_stress = cv2.inRange(hsv, lower_stress, upper_stress)
            mask_bare = cv2.inRange(hsv, lower_bare, upper_bare)


            if sample_frame is None:
                sample_frame = frame
                sample_mask_healthy = mask_healthy
                sample_mask_stress = mask_stress
                sample_mask_bare = mask_bare


            total_healthy += cv2.countNonZero(mask_healthy)
            total_stress += cv2.countNonZero(mask_stress)
            total_bare += cv2.countNonZero(mask_bare)

        total_pixels = total_healthy + total_stress + total_bare
        healthy_pct = (total_healthy / total_pixels) * 100
        stress_pct = (total_stress / total_pixels) * 100
        bare_pct = (total_bare / total_pixels) * 100

        health_score = (healthy_pct * 1.0) - (stress_pct * 0.5) - (bare_pct * 1.5)
        health_score = max(0, min(100, health_score))

        return {
            'healthy_pct': healthy_pct,
            'stress_pct': stress_pct,
            'bare_pct': bare_pct,
            'health_score': health_score,
            'sample_frame': sample_frame ,
            'mask_healthy': sample_mask_healthy ,
            'mask_stress': sample_mask_stress ,
            'mask_bare': sample_mask_bare
        }