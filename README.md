# 🌱 Lawn Health Analyzer

Ein KI-gestütztes Tool zur Analyse der Rasengesundheit via Drohnen-Video.
Das Tool extrahiert Frames aus dem Video, erkennt Gras via CNN, analysiert
die Rasengesundheit per HSV-Farb-Segmentierung, integriert Wetterdaten und
gibt mithilfe von Claude Sonnet 4.6 konkrete Empfehlungen eines erfahrenen Greenkeeepers.

## Features
- 📹 Video-Upload (MP4, MOV) mit Frame-Vorschau
- 🧠 CNN (U-Net) zur automatischen Gras/Nicht-Gras Erkennung
- 🔬 HSV-Farb-Segmentierung (gesund/trockenstress/kahl)
- 📊 Health Score (0-100)
- 🌤️ Wetterdaten der letzten 7 Tage (Open-Meteo API)
- 📈 Visualisierung (Pie-Chart, Wetter-Charts, Segmentiertes Bild)
- 🤖 KI-Empfehlungen via Claude Sonnet 4.6
- 💬 Follow-up Chatbot für Rückfragen
- 📄 PDF-Export des kompletten Reports
- 🌿 Checkbox für kürzlich gemähten Rasen

## Tech Stack
- Python
- Streamlit
- OpenCV
- PyTorch (U-Net CNN)
- Anthropic Claude API
- Matplotlib
- Open-Meteo API (Wetterdaten)
- Roboflow (Trainingsdaten)
- ReportLab (PDF Export)

## Installation

```bash
git clone https://github.com/MarvinAtorf/lawn-health-analyzer.git
cd lawn-health-analyzer
pip install -r requirements.txt
```

## Konfiguration

Erstelle eine `.env` Datei im Root-Verzeichnis:
und füge deinen Anthropic api-key ein

## Verwendung

```bash
streamlit run app.py
```

## Live Demo

👉 https://lawn-health-analyzer-noqgfecdsnhryvcy7p5rbu.streamlit.app/](https://lawn-health-analyzer.streamlit.app/

## Architektur

| Datei | Beschreibung |
|-------|-------------|
| `app.py` | Hauptapp, Streamlit UI |
| `bots/lawn_health_bot.py` | Greenkeeper-Bot, Claude-Prompt |
| `services/claude.py` | Anthropic API Service |
| `services/claude_sync.py` | Synchroner Wrapper für Streamlit |
| `modules/video_processor.py` | Frame-Extraktion via OpenCV |
| `modules/analysis.py` | HSV-Segmentierung, Health Score |
| `modules/lawn_visualizer.py` | Streamlit Visualisierung |
| `modules/grass_detector.py` | CNN Gras-Erkennung (U-Net) |
| `modules/weather_service.py` | Open-Meteo Wetterdaten API |
| `modules/pdf_exporter.py` | PDF-Export via ReportLab |

## CNN Training

Das Modell wurde trainiert mit:
- Eigene Drohnen-Aufnahmen (DJI Mini SE)
- Gelabelt via Roboflow (103 Bilder, 5 Klassen)
- U-Net Architektur mit PyTorch
- Binary Cross Entropy Loss (weighted)
- Google Colab T4 GPU

## Limitierungen

- Schatten können Trockenstress-Werte leicht erhöhen
- Beste Ergebnisse bei bewölktem Himmel (keine harten Schatten)
- CNN trainiert auf lokalem Datensatz – andere Regionen/Rasentypen können abweichen
