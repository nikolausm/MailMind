# KI-Agenten-Architektur

## Inhaltsverzeichnis

- [Übersicht](#übersicht)
- [Agenten-Hierarchie](#agenten-hierarchie)
- [Agent-Rollen und Verantwortlichkeiten](#agent-rollen-und-verantwortlichkeiten)
  - [Orchestrator - Das Gehirn](#orchestrator---das-gehirn)
- [Agent-Typen](#agent-typen)
  - [Kern-Agenten (Immer aktiv)](#kern-agenten-immer-aktiv)
  - [Analyse-Agenten (Bei Bedarf)](#analyse-agenten-bei-bedarf)
  - [Response-Agenten (Auf Anfrage)](#response-agenten-auf-anfrage)
- [Agent-Kommunikation](#agent-kommunikation)
  - [Nachrichten-Protokoll](#nachrichten-protokoll)
  - [Entscheidungs-Matrix](#entscheidungs-matrix)
- [Intelligenz-Merkmale](#intelligenz-merkmale)
  - [Lernfähigkeit](#lernfähigkeit)
  - [Konfliktlösung](#konfliktlösung)
  - [Qualitätssicherung](#qualitätssicherung)
- [Integration mit E-Mail-Pipeline](#integration-mit-e-mail-pipeline)
- [Erweiterbarkeit](#erweiterbarkeit)
  - [Neuen Agent hinzufügen](#neuen-agent-hinzufügen)
- [Best Practices](#best-practices)

## In diesem Dokument

- **[Übersicht](#übersicht)**: Einführung in die Agenten-Architektur
- **[Agenten-Hierarchie](#agenten-hierarchie)**: Struktureller Aufbau des Systems
- **[Agent-Typen](#agent-typen)**: Klassifizierung und Rollen der verschiedenen Agenten
- **[Agent-Kommunikation](#agent-kommunikation)**: Interaktionsmuster zwischen Agenten
- **[Intelligenz-Merkmale](#intelligenz-merkmale)**: KI-Fähigkeiten und Lernmechanismen
- **[Erweiterbarkeit](#erweiterbarkeit)**: Hinzufügen neuer Agenten

## Verwandte Dokumente

- **[KI-Agenten](./ai-agents.md)**: Detaillierte Agent-Implementierungen
- **[E-Mail-Pipeline](./email-pipeline.md)**: Technische Verarbeitungspipeline
- **[AI-Interaktions-Regeln](./ai-interaction-rules.md)**: Interaktionsrichtlinien
- **[Vektor-Datenbank](./vector-database.md)**: Such-Integration
- **[Entwicklung](./DEVELOPMENT.md)**: Entwicklungsrichtlinien

## Übersicht

MailMind nutzt ein spezialisiertes Multi-Agenten-System, bei dem jeder Agent eine klar definierte Rolle in der E-Mail-Intelligenz übernimmt. Diese Dokumentation fokussiert auf die **Agent-Designs und deren Zusammenarbeit**.

> **Siehe auch**: [E-Mail-Pipeline](./email-pipeline.md) für den technischen Verarbeitungsfluss

## Agenten-Hierarchie

```
                    ┌─────────────────────────────┐
                    │     Agent-Orchestrator     │
                    │   (Zentrale Intelligenz)    │
                    └─────────────┬───────────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
         ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
         │ Kern-Agenten │ │   Analyse-   │ │  Response-   │
         │              │ │   Agenten    │ │   Agenten    │
         └──────────────┘ └──────────────┘ └──────────────┘
              │                 │                 │
     ┌────────┼────────┐       │                 │
     ▼        ▼        ▼       ▼                 ▼
 Classifier Tagger  Search  Summary          Response
```

## Agent-Rollen und Verantwortlichkeiten

### Orchestrator - Das Gehirn
- **Rolle**: Zentrale Koordination und Entscheidungsfindung
- **Verantwortung**: Aufgabenverteilung, Konfliktlösung, Qualitätssicherung
- **Intelligenz**: Entscheidet welche Agenten wann aktiviert werden

## Agent-Typen

### Kern-Agenten (Immer aktiv)

#### 🏷️ Klassifizierungs-Agent
```yaml
Rolle: E-Mail-Kategorisierer
Intelligenz: Mustererkennung, Kontext-Analyse
Entscheidungen:
  - Kategorie (6 Typen)
  - Priorität (3 Stufen)
  - Vertrauenswert (0-1)
```

#### 🔖 Tagging-Agent
```yaml
Rolle: Hierarchische Organisation
Intelligenz: Themen-Extraktion, Beziehungs-Mapping
Entscheidungen:
  - Haupt-Tags
  - Unter-Tags
  - Kontext-Tags
```

#### 🔍 Such-Agent
```yaml
Rolle: Semantische Indizierung
Intelligenz: Embedding-Generation, Ähnlichkeits-Berechnung
Entscheidungen:
  - Vektor-Repräsentation
  - Relevanz-Scores
  - Such-Optimierung
```

### Analyse-Agenten (Bei Bedarf)

#### 📝 Zusammenfassungs-Agent
```yaml
Rolle: Inhalts-Kondensierung
Intelligenz: Wichtigkeits-Bewertung, Kontext-Bewahrung
Aktivierung: E-Mails > 1000 Zeichen
```

### Response-Agenten (Auf Anfrage)

#### 💬 Antwort-Agent
```yaml
Rolle: Kommunikations-Assistent
Intelligenz: Stil-Anpassung, Kontext-Verständnis
Aktivierung: Benutzer-Anfrage oder Auto-Response-Regel
```

## Agent-Kommunikation

### Nachrichten-Protokoll

```python
class AgentMessage:
    """Standardisiertes Kommunikationsformat zwischen Agenten"""
    agent_id: str
    message_type: Literal["request", "response", "broadcast"]
    payload: dict
    priority: int
    timestamp: datetime
```

### Entscheidungs-Matrix

| Szenario | Aktivierte Agenten | Orchestrator-Logik |
|----------|-------------------|-------------------|
| Neue E-Mail | Classifier, Tagger, Search | Parallel, keine Abhängigkeiten |
| Lange E-Mail | + Summary | Conditional auf Länge |
| Meeting-Einladung | + Response | Pattern-Match "meeting" |
| Kundensupport | Alle | Priorität = Hoch |

## Intelligenz-Merkmale

### Lernfähigkeit
- **Feedback-Loop**: Benutzer-Korrekturen fließen zurück
- **Pattern-Learning**: Häufige Muster werden erkannt
- **Personalisierung**: Anpassung an Benutzer-Präferenzen

### Konfliktlösung
```python
def resolve_classification_conflict(classifications):
    """Wenn Agenten unterschiedlicher Meinung sind"""
    if all_agree(classifications):
        return classifications[0]
    
    # Gewichtete Abstimmung basierend auf Confidence
    weighted_votes = calculate_weighted_consensus(classifications)
    return select_highest_confidence(weighted_votes)
```

### Qualitätssicherung
- **Confidence Thresholds**: Mindest-Vertrauen für Aktionen
- **Fallback-Mechanismen**: Bei Unsicherheit → manuelle Review
- **Monitoring**: Kontinuierliche Leistungsüberwachung

## Integration mit E-Mail-Pipeline

> Die technische Implementierung der E-Mail-Verarbeitung ist in der [E-Mail-Pipeline-Dokumentation](./email-pipeline.md) beschrieben.

## Erweiterbarkeit

### Neuen Agent hinzufügen

1. **Agent-Interface implementieren**:
```python
class CustomAgent(BaseAgent):
    def process(self, email: Email) -> AgentResult:
        # Ihre Logik hier
        pass
```

2. **Im Orchestrator registrieren**:
```python
orchestrator.register_agent('custom', CustomAgent())
```

3. **Aktivierungslogik definieren**:
```python
if email.matches_pattern('custom_trigger'):
    activate_agent('custom')
```

## Best Practices

1. **Single Responsibility**: Jeder Agent hat genau eine Aufgabe
2. **Loose Coupling**: Agenten kennen sich nicht direkt
3. **High Cohesion**: Verwandte Funktionen im selben Agent
4. **Fail-Safe**: Ausfall eines Agenten stoppt nicht das System
5. **Observable**: Alle Agenten-Aktionen sind nachvollziehbar