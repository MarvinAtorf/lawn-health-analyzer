import streamlit as st
import os
from dotenv import load_dotenv
from bots.lawn_health_bot import LawnHealthBot
from services.claude_sync import ClaudeServiceSync
from modules.video_processor import VideoProcessor
from modules.analysis import LawnAnalyzer
from modules.lawn_visualizer import LawnVisualizer
from modules.weather_service import WeatherService
from modules.grass_detector import GrassDetector
import cv2
from modules.pdf_exporter import PDFExporter

if 'analysis_data' not in st.session_state:
    st.session_state['analysis_data'] = None

if 'recommendations' not in st.session_state:
    st.session_state['recommendations'] = None

if 'weather_data' not in st.session_state:
    st.session_state['weather_data'] = None

if 'last_city' not in st.session_state:
    st.session_state['last_city'] = None

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
llm = ClaudeServiceSync(api_key=api_key)
bot = LawnHealthBot(llm=llm)
grass_detector = GrassDetector(model_path="model/grass_detector.pth")

st.title("🌱 Lawn Health Analyzer")

city = st.text_input("📮 PLZ eingeben", placeholder="z.B. 33142")
date = st.date_input("📅 Datum des Videos")

if not city:
    city = "33142"

if st.session_state['weather_data'] is None or st.session_state['last_city'] != city:
    st.session_state['last_city'] = city
    try:
        weather_service = WeatherService()
        st.session_state['weather_data'] = weather_service.get_weather_for_city(
            city,
            date.strftime("%Y-%m-%d")
        )
    except Exception as e:
        st.error(f"❌ PLZ nicht gefunden: {e}")
        st.session_state['weather_data'] = None

if st.session_state['weather_data'] is not None:
    current_weather = st.session_state['weather_data']
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Niederschlag gesamt (7 Tage)", f"{current_weather['precipitation_total']:.1f}mm")
    with col2:
        st.metric("Ø Temperatur (7 Tage)", f"{current_weather['temperature_avg']}°C")
    with col3:
        st.metric("Jahreszeit", current_weather['season'])

recently_mowed = st.checkbox("🌿 Rasen wurde kürzlich gemäht")
sauerer_boden = st.checkbox("🌿 Boden ist sauer")
file = st.file_uploader("Video hochladen", type=["mp4", "mov"])

if file is not None:
    processor = VideoProcessor()
    first_frame = processor.get_first_frame(file)
    rgb_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)
    st.divider()
    st.text("Vorschau:")
    st.image(rgb_frame, caption="Vorschau", use_container_width=True)

    if st.button("🔍 Analyse starten"):
        with st.spinner("🌤️ Wetterdaten werden geladen..."):
            weather_service = WeatherService()
            st.session_state['weather_data'] = weather_service.get_weather_for_city(
                city,
                date.strftime("%Y-%m-%d")
            )

        with st.spinner("Frames werden extrahiert..."):
            processor = VideoProcessor()
            frames = processor.extract_frames(file)

        with st.spinner("Rasen wird analysiert..."):
            analyzer = LawnAnalyzer()
            st.session_state['analysis_data'] = analyzer.analyze_frames(frames, grass_detector)

        with st.spinner("Greenkeeper analysiert..."):
            st.session_state['recommendations'] = bot.get_recommendations(
                st.session_state['analysis_data'],
                st.session_state['weather_data'],
                recently_mowed,
                sauerer_boden
            )

if st.session_state['analysis_data'] is not None:
    analysis_data = st.session_state['analysis_data']
    recommendations = st.session_state['recommendations']

    visualizer = LawnVisualizer()
    visualizer.show_metrics(analysis_data)
    visualizer.show_chart(analysis_data)
    visualizer.show_weather_chart(st.session_state['weather_data'])

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
    st.divider()
    if st.button("📄 PDF exportieren"):
        pdf_exporter = PDFExporter()
        pdf_bytes = pdf_exporter.export(
            analysis_data,
            st.session_state['weather_data'],
            recommendations,
            analysis_data['all_frames'][0],
            segmented,
            date.strftime("%d.%m.%Y")
        )
        st.download_button(
            label="📥 PDF herunterladen",
            data=pdf_bytes,
            file_name="lawn_health_report.pdf",
            mime="application/pdf"
        )
    st.divider()
    st.subheader("💬 Fragen an den Greenkeeper")

    # Chat History anzeigen
    for message in st.session_state['chat_history']:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User Input
    if prompt := st.chat_input("Stelle eine Frage zum Greenkeeper-Report..."):
        # User Message anzeigen
        with st.chat_message("user"):
            st.write(prompt)

        # Zur History hinzufügen
        st.session_state['chat_history'].append({"role": "user", "content": prompt})

        # Claude aufrufen mit Report als Kontext
        with st.chat_message("assistant"):
            with st.spinner("Greenkeeper antwortet..."):
                response = bot.ask_followup(
                    prompt,
                    recommendations,
                    st.session_state['chat_history']
                )
            st.write(response)

        # Antwort zur History hinzufügen
        st.session_state['chat_history'].append({"role": "assistant", "content": response})