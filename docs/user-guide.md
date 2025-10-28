# Benutzerhandbuch

## Willkommen bei MailMind

MailMind revolutioniert Ihre E-Mail-Verwaltung durch intelligente KI-Unterstützung und semantische Suche.

## 📚 Inhaltsverzeichnis

### In diesem Dokument
- [Willkommen bei MailMind](#willkommen-bei-mailmind)
- [Erste Schritte](#erste-schritte)
- [E-Mail-Management](#e-mail-management)
- [Intelligente Suche](#intelligente-suche)
- [KI-Funktionen](#ki-funktionen)
- [Tastaturkürzel](#tastaturkürzel)
- [Erweiterte Funktionen](#erweiterte-funktionen)
- [Tipps & Tricks](#tipps--tricks)

### Verwandte Dokumente
- [⚡ Schnellstart](./quick-start.md) - Schnelle Einrichtung
- [⚙️ Konfiguration](./configuration.md) - Systemkonfiguration
- [🧠 KI-Agenten](./ai-agents.md) - Agent-System Dokumentation
- [🎨 Frontend-Architektur](./frontend-architecture.md) - UI-Architektur
- [📧 E-Mail-Pipeline](./email-pipeline.md) - E-Mail-Verarbeitungsfluss

## Erste Schritte

### Anmeldung

1. Öffnen Sie MailMind unter `http://localhost:3000`
2. Melden Sie sich mit Ihren Zugangsdaten an
3. Bei der ersten Anmeldung werden Sie durch die Einrichtung geführt

### Dashboard-Übersicht

Das Dashboard zeigt:
- **Posteingang**: Neue und ungelesene E-Mails
- **Kategorien**: Automatisch organisierte E-Mails
- **Schnellzugriff**: Wichtige E-Mails und Aktionen
- **Statistiken**: E-Mail-Aktivität und Insights

## E-Mail-Management

### E-Mails lesen

#### Listenansicht
- Klicken Sie auf eine E-Mail für Vorschau
- Doppelklick öffnet Vollansicht
- Rechtsklick für Kontextmenü

#### Detailansicht
- **Header**: Absender, Empfänger, Datum
- **Inhalt**: Formatierter E-Mail-Text
- **Anhänge**: Download und Vorschau
- **KI-Insights**: Tags, Kategorie, Zusammenfassung

### E-Mails organisieren

#### Automatische Organisation
- E-Mails werden automatisch kategorisiert
- Hierarchische Tags werden zugewiesen
- Prioritäten werden erkannt

#### Manuelle Organisation
- Drag & Drop in Ordner
- Tags hinzufügen/entfernen
- Priorität anpassen
- Notizen hinzufügen

### E-Mails verfassen

#### Neue E-Mail
1. Klicken Sie auf "Neue E-Mail" oder `Strg/Cmd + N`
2. Füllen Sie Empfänger, Betreff und Inhalt
3. Optional: Anhänge hinzufügen
4. Senden oder als Entwurf speichern

#### Antworten und Weiterleiten
- **Antworten**: Klick auf Antworten-Button oder `R`
- **Allen antworten**: `A`
- **Weiterleiten**: `F`
- **KI-Antwortvorschläge**: Werden automatisch generiert

## Intelligente Suche

### Semantische Suche

Die KI versteht natürliche Sprache:

```
Beispiele:
- "E-Mails von letzter Woche über das Budget"
- "Wichtige Nachrichten von Kunden"
- "Anhänge mit Präsentationen"
- "Unbeantwortete E-Mails von heute"
```

### Erweiterte Suchoperatoren

| Operator | Beschreibung | Beispiel |
|----------|-------------|----------|
| `from:` | Von Absender | `from:john@example.com` |
| `to:` | An Empfänger | `to:team@company.com` |
| `subject:` | Im Betreff | `subject:Meeting` |
| `has:` | Mit Eigenschaft | `has:attachment` |
| `is:` | Status | `is:unread`, `is:starred` |
| `category:` | In Kategorie | `category:work` |
| `tag:` | Mit Tag | `tag:important` |
| `date:` | Datum | `date:2024-01-15` |
| `before:` | Vor Datum | `before:2024-01-01` |
| `after:` | Nach Datum | `after:2024-01-01` |

### Suchfilter kombinieren

```
from:john@example.com has:attachment after:2024-01-01
subject:Budget is:unread category:work
```

## KI-Funktionen

### Auto-Kategorisierung

E-Mails werden automatisch kategorisiert in:
- **Persönlich**: Private Kommunikation
- **Arbeit**: Geschäftliche E-Mails
- **Werbung**: Marketing und Angebote
- **Newsletter**: Abonnements
- **Benachrichtigungen**: System-Updates
- **Spam**: Unerwünschte E-Mails

### Intelligentes Tagging

Tags werden hierarchisch vergeben:
```
Projekt
├── Projektname
│   ├── Phase
│   └── Teilaufgabe
```

### Zusammenfassungen

Für lange E-Mails oder Threads:
- **Kurzzusammenfassung**: 2-3 Sätze
- **Schlüsselpunkte**: Bullet Points
- **Aktionspunkte**: To-Dos extrahiert

### Antwortvorschläge

KI generiert kontextbewusste Vorschläge:
- **Ton**: Formell, informell, freundlich
- **Länge**: Kurz, mittel, ausführlich
- **Stil**: Geschäftlich, persönlich

## Tastaturkürzel

### Allgemein

| Kürzel | Aktion |
|--------|--------|
| `Strg/Cmd + K` | Schnellsuche |
| `Strg/Cmd + N` | Neue E-Mail |
| `Strg/Cmd + ,` | Einstellungen |
| `Esc` | Schließen/Abbrechen |

### Navigation

| Kürzel | Aktion |
|--------|--------|
| `↑/↓` | E-Mail auswählen |
| `Enter` | E-Mail öffnen |
| `Space` | Vorschau |
| `g i` | Zum Posteingang |
| `g s` | Zu gesendeten |
| `g d` | Zu Entwürfen |

### E-Mail-Aktionen

| Kürzel | Aktion |
|--------|--------|
| `R` | Antworten |
| `A` | Allen antworten |
| `F` | Weiterleiten |
| `E` | Archivieren |
| `Del` | Löschen |
| `S` | Stern vergeben |
| `U` | Als ungelesen |
| `M` | Verschieben |
| `L` | Label hinzufügen |

### Erweiterte Aktionen

| Kürzel | Aktion |
|--------|--------|
| `Shift + A` | Alle auswählen |
| `Strg/Cmd + Enter` | Senden |
| `Strg/Cmd + S` | Als Entwurf |
| `Strg/Cmd + P` | Drucken |

## Erweiterte Funktionen

### Smart Folders

Erstellen Sie dynamische Ordner mit Regeln:

```yaml
Name: "Wichtige Projekte"
Regeln:
  - from: "@wichtiger-kunde.de"
  - subject contains: "Projekt X"
  - priority: hoch
  - received: letzte 30 Tage
```

### Automatisierung

#### E-Mail-Regeln

Erstellen Sie Wenn-Dann-Regeln:
```
WENN: E-Mail von chef@firma.de
DANN: 
  - Markiere als wichtig
  - Verschiebe in "Chef" Ordner
  - Sende Benachrichtigung
```

#### Geplante Aktionen

- **Verzögertes Senden**: E-Mail später senden
- **Wiedervorlage**: E-Mail zu bestimmtem Zeitpunkt wieder zeigen
- **Auto-Archivierung**: Alte E-Mails automatisch archivieren

### Vorlagen

#### E-Mail-Vorlagen erstellen

1. Verfassen Sie eine E-Mail
2. Speichern als Vorlage
3. Variablen einfügen: `{{name}}`, `{{datum}}`

#### Vorlage verwenden

1. Neue E-Mail → Vorlage wählen
2. Variablen werden automatisch ersetzt
3. Anpassen und senden

### Integrationen

#### Kalender-Integration

- Termine aus E-Mails extrahieren
- Einladungen direkt annehmen/ablehnen
- Verfügbarkeit prüfen

#### Aufgaben-Integration

- To-Dos aus E-Mails erstellen
- Deadlines setzen
- Status verfolgen

### Spracheinstellungen

#### Sprache wechseln

1. **Über die Einstellungen**
   - Einstellungen → Sprache & Region
   - Gewünschte Sprache auswählen
   - Änderungen werden sofort übernommen

2. **Schnellwechsel**
   - Klick auf Sprachflagge in der Toolbar
   - Dropdown mit verfügbaren Sprachen
   - Tastenkürzel: `Ctrl+Shift+L`

#### Verfügbare Sprachen

**Vollständig unterstützt (Tier 1)**
- 🇩🇪 Deutsch
- 🇬🇧 Englisch  
- 🇪🇸 Spanisch
- 🇫🇷 Französisch

**Erweitert unterstützt (Tier 2)**
- 🇮🇹 Italienisch
- 🇵🇹 Portugiesisch
- 🇳🇱 Niederländisch
- 🇵🇱 Polnisch

**Basis-Unterstützung (Tier 3)**
- 🇯🇵 Japanisch
- 🇨🇳 Chinesisch (vereinfacht)
- 🇰🇷 Koreanisch
- 🇷🇺 Russisch

#### Regionale Einstellungen

- **Datumsformat**: TT.MM.JJJJ oder MM/TT/JJJJ
- **Zeitformat**: 24-Stunden oder 12-Stunden (AM/PM)
- **Währung**: EUR, USD, GBP, etc.
- **Zahlenformat**: 1.000,00 oder 1,000.00

#### KI-Sprachverarbeitung

Die KI-Agenten verstehen und antworten in Ihrer gewählten Sprache:
- E-Mail-Kategorisierung in lokaler Sprache
- Zusammenfassungen in Ihrer Sprache
- Antwortvorschläge kulturell angepasst
- Tagging mit lokalen Begriffen

## Tipps & Tricks

### Produktivitäts-Tipps

1. **Zero-Inbox-Methode**
   - Bearbeiten Sie E-Mails sofort
   - 2-Minuten-Regel anwenden
   - Archivieren oder löschen

2. **Batch-Verarbeitung**
   - Bestimmte Zeiten für E-Mails
   - Ähnliche E-Mails gruppiert bearbeiten
   - Ablenkungen minimieren

3. **KI optimal nutzen**
   - Vertrauen Sie der Auto-Kategorisierung
   - Nutzen Sie Zusammenfassungen für lange Threads
   - Lassen Sie Antworten vorschlagen

### Suchstrategien

1. **Breite Suche starten**
   ```
   "Projekt Budget"
   ```

2. **Ergebnisse verfeinern**
   ```
   "Projekt Budget" from:manager after:2024-01-01
   ```

3. **Semantische Variationen**
   ```
   "Kosten", "Ausgaben", "Finanzen"
   ```

### Datenschutz-Tipps

1. **Sensible Daten**
   - Nutzen Sie verschlüsselte Ordner
   - Aktivieren Sie 2FA
   - Regelmäßige Passwort-Änderungen

2. **KI-Datenschutz**
   - KI-Verarbeitung kann deaktiviert werden
   - Lokale Verarbeitung bevorzugen
   - Daten werden nicht an Dritte weitergegeben

## Fehlerbehebung

### Häufige Probleme

#### E-Mails werden nicht synchronisiert
- Prüfen Sie Internetverbindung
- Verifizieren Sie E-Mail-Kontoeinstellungen
- Schauen Sie in Logs: Einstellungen → System → Logs

#### Suche findet nichts
- Warten Sie auf Indizierung (kann einige Minuten dauern)
- Prüfen Sie Suchsyntax
- Nutzen Sie erweiterte Suchoperatoren

#### KI-Funktionen nicht verfügbar
- Prüfen Sie API-Schlüssel in Einstellungen
- Verifizieren Sie Internetverbindung
- Kontaktieren Sie Support bei anhaltenden Problemen

## Support

### Hilfe erhalten

- **In-App-Hilfe**: `F1` oder `?`
- **Dokumentation**: [docs.mailmind.com](http://docs.mailmind.com)
- **Community-Forum**: [forum.mailmind.com](http://forum.mailmind.com)
- **E-Mail-Support**: support@mailmind.com

### Feedback geben

Wir schätzen Ihr Feedback:
- **Feature-Anfragen**: In-App Feedback-Button
- **Bug-Reports**: GitHub Issues
- **Verbesserungsvorschläge**: Community-Forum