import streamlit as st
import os
from dotenv import load_dotenv
from bots.lawn_health_bot import LawnHealthBot
from services.claude_sync import ClaudeServiceSync
from modules.video_processor import VideoProcessor
from modules.analysis import LawnAnalyzer
from modules.lawn_visualizer import LawnVisualizer

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
llm = ClaudeServiceSync(api_key=api_key)
bot = LawnHealthBot(llm=llm)

st.title("🌱 Lawn Health Analyzer")

file = st.file_uploader("Video hochladen", type=["mp4", "mov"])

if file is not None:
    if st.button("🔍 Analyse starten"):
        with st.spinner("Frames werden extrahiert..."):
            processor = VideoProcessor()
            frames = processor.extract_frames(file)

        with st.spinner("Rasen wird analysiert..."):
            analyzer = LawnAnalyzer()
            analysis_data = analyzer.analyze_frames(frames)

        with st.spinner("Greenkeeper analysiert..."):
            recommendations = bot.get_recommendations(analysis_data)

        visualizer = LawnVisualizer()
        visualizer.show_metrics(analysis_data)
        visualizer.show_chart(analysis_data)
        st.write(recommendations)