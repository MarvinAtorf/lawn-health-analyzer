import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class LawnVisualizer:
    def show_frames(self, original_frame: np.ndarray, segmented_frame: np.ndarray):
        """
        Display original and segmented frames side by side for comparison.

        Parameters:
        - original_frame (np.ndarray): The original frame captured by the camera.
        - segmented_frame (np.ndarray): The frame after applying lawn segmentation.
        """
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original")
            rgb_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
            st.image(rgb_frame)

        with col2:
            st.subheader("Segmentiert")
            st.image(segmented_frame)


    def show_metrics(self, analysis_data: dict):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Health Score", f"{analysis_data['health_score']:.1f}/100")
        with col2:
            st.metric("🟢 Gesund", f"{analysis_data['healthy_pct']:.1f}%")
        with col3:
            st.metric("🟡 Trockenstress", f"{analysis_data['stress_pct']:.1f}%")
        with col4:
            st.metric("⚪ Kahle Stellen", f"{analysis_data['bare_pct']:.1f}%")

    def show_chart(self, analysis_data: dict):
        labels = ["Gesund", "Trockenstress", "Kahle Stellen/Moos"]
        values = [
            analysis_data['healthy_pct'],
            analysis_data['stress_pct'],
            analysis_data['bare_pct']
        ]
        colors = ["#2ecc71", "#f39c12", "#95a5a6"]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, colors=colors, autopct="%1.1f%%")
        st.pyplot(fig)

    def create_segmented_frame(self, frame: np.ndarray, mask_healthy: np.ndarray, mask_stress: np.ndarray,mask_bare: np.ndarray) -> np.ndarray:
        segmented = np.zeros_like(frame)
        segmented[mask_healthy > 0] = [46, 204, 113]
        segmented[mask_healthy > 0] = [46, 204, 113]
        return segmented
