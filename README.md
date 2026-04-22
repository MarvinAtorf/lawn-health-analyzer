# 🌱 Lawn Health Analyzer

Ein KI-gestütztes Tool zur Analyse der Rasengesundheit via Drohnen-Video. 
Das Tool extrahiert Frames aus dem Video, analysiert die Rasengesundheit 
per HSV-Farb-Segmentierung und gibt mithilfe von Claude (Sonnet 4.6) 
konkrete Empfehlungen eines erfahrenen Greenkeeepers.

## Features
- 📹 Video-Upload (MP4, MOV)
- 🔬 HSV-Farb-Segmentierung (gesund/trockenstress/kahl)
- 📊 Health Score (0-100)
- 🤖 KI-Empfehlungen via Claude Sonnet 4.6
- 📈 Pie-Chart Visualisierung

## Tech Stack
- Python
- Streamlit
- OpenCV
- Anthropic Claude API
- Matplotlib

## Installation

```bash
git clone https://github.com/MarvinAtorf/lawn-health-analyzer.git
cd lawn-health-analyzer
pip install -r requirements.txt
```

## Konfiguration
Erstelle eine `.env` Datei im Root-Verzeichnis:

## Verwendung
```bash
streamlit run app.py
```

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