import cv2
import numpy as np

class LawnAnalyzer:

    def analyze_frames(self, frames: list, grass_detector=None) -> dict:
        total_healthy = 0
        total_stress = 0
        total_bare = 0

        lower_healthy = np.array([35, 40, 40])
        upper_healthy = np.array([90, 255, 255])
        lower_stress = np.array([10, 30, 40])
        upper_stress = np.array([35, 255, 255])
        lower_bare = np.array([0, 0, 50])
        upper_bare = np.array([180, 40, 255])

        all_frames = []
        all_masks_healthy = []
        all_masks_stress = []
        all_masks_bare = []

        for frame in frames:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # CNN Maske anwenden (optional)
            if grass_detector is not None:
                grass_mask = grass_detector.predict(frame)
                hsv[grass_mask == 0] = 0
                shadow_mask = hsv[:, :, 2] < 60  # V < 60 = zu dunkel
                hsv[shadow_mask] = 0  # Schatten ignorieren

            mask_healthy = cv2.inRange(hsv, lower_healthy, upper_healthy)
            mask_stress = cv2.inRange(hsv, lower_stress, upper_stress)
            mask_bare = cv2.inRange(hsv, lower_bare, upper_bare)

            all_frames.append(frame)
            all_masks_healthy.append(mask_healthy)
            all_masks_stress.append(mask_stress)
            all_masks_bare.append(mask_bare)

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
            'all_frames': all_frames,
            'all_masks_healthy': all_masks_healthy,
            'all_masks_stress': all_masks_stress,
            'all_masks_bare': all_masks_bare
        }