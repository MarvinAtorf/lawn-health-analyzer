from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import numpy as np
import io


class PDFExporter:
    def __init__(self):
        self.styles = getSampleStyleSheet()

    def export(self, analysis_data: dict, weather_data: dict,
               recommendations: str, frame: np.ndarray,
               segmented_frame: np.ndarray, date: str) -> bytes:
        """
        Erstellt ein PDF mit allen Analyse-Ergebnissen.
        Returns: PDF als bytes (für Streamlit Download)
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Titel
        story.append(Paragraph("🌱 Lawn Health Analyzer – Report", self.styles['Title']))
        story.append(Spacer(1, 0.5 * cm))

        story.append(Paragraph(f"Datum: {date}", self.styles['Normal']))
        story.append(Spacer(1, 0.5 * cm))

        # Metriken
        story.append(Paragraph("Analyse-Ergebnisse", self.styles['Heading1']))
        story.append(Paragraph(f"Health Score: {analysis_data['health_score']:.1f}/100", self.styles['Normal']))
        story.append(Paragraph(f"Gesund: {analysis_data['healthy_pct']:.1f}%", self.styles['Normal']))
        story.append(Paragraph(f"Trockenstress: {analysis_data['stress_pct']:.1f}%", self.styles['Normal']))
        story.append(Paragraph(f"Kahle Stellen/Moos: {analysis_data['bare_pct']:.1f}%", self.styles['Normal']))
        story.append(Spacer(1, 0.5 * cm))

        # Wetter
        story.append(Paragraph("Wetterdaten", self.styles['Heading1']))
        story.append(Paragraph(f"Standort: {weather_data['city']}", self.styles['Normal']))
        story.append(Paragraph(f"Jahreszeit: {weather_data['season']}", self.styles['Normal']))
        story.append(
            Paragraph(f"Niederschlag (7 Tage): {weather_data['precipitation_total']:.1f}mm", self.styles['Normal']))
        story.append(Paragraph(f"Durchschnittstemperatur: {weather_data['temperature_avg']}°C", self.styles['Normal']))
        story.append(Spacer(1, 0.5 * cm))

        # Empfehlungen
        story.append(Paragraph("Greenkeeper-Report", self.styles['Heading1']))
        for line in recommendations.split('\n'):
            if line.strip():
                story.append(Paragraph(line, self.styles['Normal']))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()