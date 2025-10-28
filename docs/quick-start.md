# Schnellstart-Anleitung

## 📚 Inhaltsverzeichnis

### In diesem Dokument
- [Voraussetzungen](#voraussetzungen)
- [Anwendung starten](#anwendung-starten)
- [Grundlegende Nutzung](#grundlegende-nutzung)
- [API-Nutzung](#api-nutzung)
- [Konfiguration](#konfiguration)
- [Setup testen](#setup-testen)
- [Fehlerbehebung](#fehlerbehebung)
- [Nächste Schritte](#nächste-schritte)

### Verwandte Dokumente
- [📖 Installation](./installation.md) - Detaillierte Installationsanleitung
- [📘 Benutzerhandbuch](./user-guide.md) - Vollständige Bedienungsanleitung
- [⚙️ Konfiguration](./configuration.md) - Systemkonfiguration
- [📡 API-Dokumentation](./api/endpoints.md) - REST API Referenz
- [🧠 KI-Agenten](./ai-agents.md) - Agent-System Dokumentation

Willkommen bei MailMind! Diese Anleitung hilft Ihnen, schnell loszulegen.

## Voraussetzungen

Stellen Sie sicher, dass Sie den [Installationsprozess](./installation.md) abgeschlossen haben.

## Anwendung starten

### 1. Entwicklungsserver starten

Der einfachste Weg, MailMind zu starten, ist der einheitliche Entwicklungsbefehl:

```bash
npm run dev
```

Dies startet:
- **Backend-API** auf http://localhost:9000
- **Frontend** auf http://localhost:3000

### 2. Ersteinrichtung

#### E-Mail-Konto konfigurieren

1. Navigieren Sie zu Einstellungen → E-Mail-Konten
2. Klicken Sie auf "Konto hinzufügen"
3. Geben Sie Ihre E-Mail-Anmeldedaten ein:
   - E-Mail-Adresse
   - Passwort oder App-spezifisches Passwort
   - IMAP/SMTP-Serverdetails (automatisch erkannt für gängige Anbieter)

#### Bestehende E-Mails importieren

```bash
# E-Mails der letzten 30 Tage importieren
python scripts/import_emails.py --days 30

# Alle E-Mails importieren (kann länger dauern)
python scripts/import_emails.py --all
```

## Grundlegende Nutzung

### E-Mail-Verwaltung

#### E-Mails anzeigen
- Navigieren Sie zum Posteingang, um Ihre E-Mails zu sehen
- Verwenden Sie die Suchleiste für semantische Suche
- Filtern Sie nach Tags, Datum oder Wichtigkeit

#### Intelligente Funktionen
- **Auto-Tagging**: E-Mails werden automatisch kategorisiert
- **Intelligente Suche**: Verwenden Sie natürlichsprachliche Anfragen
- **KI-Zusammenfassungen**: Erhalten Sie schnelle Zusammenfassungen langer E-Mail-Verläufe

### Suchbeispiele

Probieren Sie diese Suchanfragen aus, um die semantische Suche in Aktion zu sehen:

- "E-Mails über Projektfristen"
- "Nachrichten von John über Budget"
- "dringende Kundenbeschwerden"
- "Besprechungseinladungen für nächste Woche"

### Tastaturkürzel

| Tastenkürzel | Aktion |
|----------|--------|
| `Strg/Cmd + K` | Schnellsuche |
| `Strg/Cmd + N` | Neue E-Mail verfassen |
| `R` | Auf ausgewählte E-Mail antworten |
| `A` | Allen antworten |
| `F` | E-Mail weiterleiten |
| `E` | E-Mail archivieren |
| `Entf` | E-Mail löschen |
| `S` | E-Mail markieren/Markierung entfernen |
| `U` | Als ungelesen markieren |

## API-Nutzung

### Authentifizierung

Holen Sie sich ein API-Token unter Einstellungen → API-Token

```bash
# Beispiel-API-Aufruf
curl -H "Authorization: Bearer IHR_TOKEN" \
     http://localhost:9000/api/emails/search?q=wichtig
```

### Python-Client

```python
from mailmind import MailMindClient

client = MailMindClient(api_key="IHR_TOKEN")

# E-Mails suchen
results = client.search("Projektupdates")

# E-Mail per ID abrufen
email = client.get_email("email_id")

# E-Mail senden
client.send_email(
    to="empfaenger@example.com",
    subject="Hallo",
    body="E-Mail-Inhalt"
)
```

### JavaScript/TypeScript-Client

```typescript
import { MailMindClient } from '@mailmind/client';

const client = new MailMindClient({
  apiKey: 'IHR_TOKEN',
  baseUrl: 'http://localhost:9000'
});

// E-Mails suchen
const results = await client.search('Projektupdates');

// E-Mail per ID abrufen
const email = await client.getEmail('email_id');
```

## Konfiguration

### KI-Einstellungen

Konfigurieren Sie das KI-Verhalten in `config/ai_settings.yaml`:

```yaml
classification:
  enabled: true
  confidence_threshold: 0.7

tagging:
  enabled: true
  max_tags: 5
  hierarchical: true

summarization:
  enabled: true
  max_length: 200
```

### E-Mail-Synchronisationseinstellungen

Konfigurieren Sie die E-Mail-Synchronisation unter Einstellungen → Synchronisation:

- **Synchronisationshäufigkeit**: Wie oft auf neue E-Mails geprüft wird
- **Synchronisationstiefe**: Wie viele Tage Verlauf beibehalten werden
- **Auto-Kategorisierung**: KI-Kategorisierung aktivieren/deaktivieren
- **Echtzeit-Synchronisation**: WebSocket-Verbindungen aktivieren

## Setup testen

### 1. Test-E-Mail senden

```bash
python scripts/send_test_email.py
```

### 2. KI-Verarbeitung überprüfen

Prüfen Sie, ob E-Mails verarbeitet werden:

```bash
# Verarbeitungsstatus prüfen
curl http://localhost:9000/api/status

# Verarbeitungsprotokolle anzeigen
tail -f logs/ai_processing.log
```

### 3. Suche testen

```bash
# Semantische Suche testen
curl "http://localhost:9000/api/emails/search?q=wichtige+besprechungen"
```

## Fehlerbehebung

### E-Mails werden nicht synchronisiert

1. E-Mail-Anmeldedaten in Einstellungen prüfen
2. IMAP/SMTP-Einstellungen verifizieren
3. Protokolle prüfen: `tail -f logs/email_sync.log`

### KI-Funktionen funktionieren nicht

1. API-Schlüssel in `.env`-Datei verifizieren
2. KI-Dienststatus prüfen: `http://localhost:9000/api/ai/status`
3. KI-Protokolle überprüfen: `tail -f logs/ai_service.log`

### Suche findet keine Ergebnisse

1. Sicherstellen, dass E-Mails indiziert sind: `python scripts/reindex_emails.py`
2. Vektor-Datenbankverbindung prüfen
3. Verifizieren, dass der Embedding-Dienst läuft

## Nächste Schritte

- [Benutzerhandbuch](./user-guide.md)
- [API-Dokumentation](./api/README.md)
- [Konfigurationsanleitung](./configuration.md)
- [KI-Agenten-Dokumentation](./ai-agents.md)