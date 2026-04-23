import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from datetime import datetime, timedelta



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
        segmented[mask_stress > 0] = [39, 174, 245]
        segmented[mask_bare > 0] = [166, 166, 149]
        return segmented


    def show_weather_chart(self, weather_data: dict):

        start_date = datetime.strptime(weather_data["date"], "%Y-%m-%d") - timedelta(days=6)
        dates = [(start_date + timedelta(days=i)).strftime("%d.%m") for i in range(7)]

        fig, axes = plt.subplots(3, 1, figsize=(10, 8))

        # Niederschlag
        axes[0].bar(dates, weather_data["precipitation_daily"], color="#3498db")
        axes[0].set_title("Niederschlag (mm)")
        axes[0].set_ylabel("mm")

        # Temperatur
        axes[1].plot(dates, weather_data["temperature_daily"], color="#e74c3c", marker="o")
        axes[1].set_title("Temperatur (°C)")
        axes[1].set_ylabel("°C")

        # Sonnenschein
        sunshine_hours = [s / 3600 for s in weather_data["sunshine_daily"]]
        axes[2].bar(dates, sunshine_hours, color="#f39c12")
        axes[2].set_title("Sonnenschein (Stunden)")
        axes[2].set_ylabel("h")

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)