import streamlit as st
import os
from dotenv import load_dotenv
from bots.lawn_health_bot import LawnHealthBot
from services.claude_sync import ClaudeServiceSync
from modules.video_processor import VideoProcessor
from modules.analysis import LawnAnalyzer
from modules.lawn_visualizer import LawnVisualizer

if 'analysis_data' not in st.session_state:
    st.session_state['analysis_data'] = None

if 'recommendations' not in st.session_state:
    st.session_state['recommendations'] = None

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
            st.session_state['analysis_data'] = analyzer.analyze_frames(frames)

        with st.spinner("Greenkeeper analysiert..."):
            st.session_state['recommendations'] = bot.get_recommendations(
                st.session_state['analysis_data']
            )

if st.session_state['analysis_data'] is not None:
    analysis_data = st.session_state['analysis_data']
    recommendations = st.session_state['recommendations']

    visualizer = LawnVisualizer()
    visualizer.show_metrics(analysis_data)
    visualizer.show_chart(analysis_data)

    frame_index = st.slider(
        "Frame auswählen",
        min_value=0,
        max_value=len(analysis_data['all_frames']) - 1,
        value=0
    )
    segmented = visualizer.create_segmented_frame(
        analysis_data['all_frames'][frame_index],
        analysis_data['all_masks_healthy'][frame_index],
        analysis_data['all_masks_stress'][frame_index],
        analysis_data['all_masks_bare'][frame_index]
    )
    visualizer.show_frames(analysis_data['all_frames'][frame_index], segmented)
    st.write(recommendations)