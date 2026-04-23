from services.claude_sync import ClaudeServiceSync


class LawnHealthBot:
    def __init__(self, llm: ClaudeServiceSync):
        self.llm = llm

    @property
    def system_prompt(self) -> str:
        return """Role:
Du bist ein erfahrener Greenkeeper mit Fachwissen in Rasenpflege, Bodenanalyse und Pflanzenkrankheiten.

Task:
Analysiere den Zustand eines Rasens basierend auf den bereitgestellten Analysedaten und bewerte seine Gesundheit. Identifiziere mögliche Probleme (z. B. Nährstoffmangel, Krankheiten, Schädlingsbefall, Bodenverdichtung, Bewässerungsfehler) und erkläre die Ursachen. Gib konkrete, umsetzbare Empfehlungen zur Verbesserung der Rasenqualität.

Input:
- Health Score: [0-100]
- Gesund: [%]
- Trockenstress: [%]
- Kahle Stellen/Moos: [%]
- Wetterdaten der letzten 7 Tage
- Kürzlich gemäht: [Ja/Nein]

Format:
1. Gesamtbewertung (Skala 1–10) + kurze Begründung
2. Diagnose der wichtigsten Probleme (max. 5 Punkte)
3. Ursachenanalyse (je Problem kurz erklären)
4. Konkrete Maßnahmen (klare Handlungsschritte, priorisiert)
5. Präventive Tipps zur langfristigen Rasengesundheit

Constraints:
- Schreibe klar, präzise und praxisnah
- Vermeide allgemeine Floskeln
- Gib nur Empfehlungen, die realistisch umsetzbar sind
- Maximal 300–400 Wörter
- Das Video kann Nicht-Rasen Bereiche enthalten (Bäume, Gebäude, Schatten). Berücksichtige das bei deiner Bewertung und weise den User darauf hin.
- Schatten können die Trockenstress-Werte erhöhen. Berücksichtige das bei deiner Bewertung."""

    def get_recommendations(self, analysis_data: dict, weather_data: dict, recently_mowed: bool = False) -> str:
        from datetime import datetime, timedelta

        start_date = datetime.strptime(weather_data["date"], "%Y-%m-%d") - timedelta(days=6)
        days = [(start_date + timedelta(days=i)).strftime("%A") for i in range(7)]

        day_translation = {
            "Monday": "Montag", "Tuesday": "Dienstag", "Wednesday": "Mittwoch",
            "Thursday": "Donnerstag", "Friday": "Freitag", "Saturday": "Samstag",
            "Sunday": "Sonntag"
        }

        precipitation_by_day = "\n".join([
            f"    {day_translation[day]}, {(start_date + timedelta(days=i)).strftime('%d.%m')}: {rain}mm"
            for i, (day, rain) in enumerate(zip(days, weather_data["precipitation_daily"]))
        ])

        mowed_hint = "Ja – Trockenstress-Werte könnten erhöht sein." if recently_mowed else "Nein"

        message = f"""
        Health Score: {analysis_data["health_score"]}/100
        Gesund: {analysis_data["healthy_pct"]}%
        Trockenstress: {analysis_data["stress_pct"]}%
        Kahle Stellen/Moos: {analysis_data["bare_pct"]}%

        Wetterdaten der letzten 7 Tage:
        Standort: {weather_data["city"]}
        Jahreszeit: {weather_data["season"]}
        Gesamtniederschlag: {weather_data["precipitation_total"]}mm
        Durchschnittstemperatur: {weather_data["temperature_avg"]}°C

        Niederschlag pro Tag:
{precipitation_by_day}

        Kürzlich gemäht: {mowed_hint}
        """
        return self.llm.chat(message, self.system_prompt, [])