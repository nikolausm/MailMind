# API-Fehlercodes

## Inhaltsverzeichnis / Table of Contents

### In diesem Dokument
- [Fehler-Response-Format](#fehler-response-format)
- [Authentifizierungsfehler (AUTH)](#authentifizierungsfehler-auth)
- [Validierungsfehler (VAL)](#validierungsfehler-val)
- [Ressourcenfehler (RES)](#ressourcenfehler-res)
- [E-Mail-Fehler (EMAIL)](#e-mail-fehler-email)
- [KI-Verarbeitungsfehler (AI)](#ki-verarbeitungsfehler-ai)
- [Serverfehler (SRV)](#serverfehler-srv)
- [Rate Limiting (RATE)](#rate-limiting-rate)
- [Fehlerbehandlung-Beispiele](#fehlerbehandlung-beispiele)
  - [Client-seitig](#client-seitig)
  - [Server-seitig](#server-seitig)

### Verwandte Dokumente
- [REST API-Endpunkte](./endpoints.md)
- [WebSocket-Ereignisse](./websocket.md)
- [Entwicklungsumgebung](../deployment/development.md)
- [Produktiv-Deployment](../deployment/production.md)

---

## Fehler-Response-Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Menschenlesbare Fehlermeldung",
    "details": {},
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

## Authentifizierungsfehler (AUTH)

| Code | HTTP Status | Beschreibung |
|------|-------------|-------------|
| AUTH001 | 401 | Ungültige Anmeldedaten |
| AUTH002 | 401 | Token abgelaufen |
| AUTH003 | 401 | Token ungültig |
| AUTH004 | 403 | Unzureichende Berechtigungen |
| AUTH005 | 400 | Konto gesperrt |
| AUTH006 | 400 | Konto nicht verifiziert |
| AUTH007 | 429 | Zu viele Anmeldeversuche |
| AUTH008 | 400 | OAuth-Anbieter-Fehler |
| AUTH009 | 400 | Ungültiges Refresh-Token |
| AUTH010 | 403 | Session abgelaufen |

## Validierungsfehler (VAL)

| Code | HTTP Status | Beschreibung |
|------|-------------|-------------|
| VAL001 | 400 | Erforderliches Feld fehlt |
| VAL002 | 400 | Ungültiges Feldformat |
| VAL003 | 400 | Feldwert außerhalb des Bereichs |
| VAL004 | 400 | Ungültige E-Mail-Adresse |
| VAL005 | 400 | Passwort zu schwach |
| VAL006 | 413 | Request zu groß |
| VAL007 | 400 | Ungültiges Datumsformat |
| VAL008 | 400 | Doppelter Eintrag |

## Ressourcenfehler (RES)

| Code | HTTP Status | Beschreibung |
|------|-------------|-------------|
| RES001 | 404 | Ressource nicht gefunden |
| RES002 | 410 | Ressource gelöscht |
| RES003 | 409 | Ressourcenkonflikt |
| RES004 | 423 | Ressource gesperrt |
| RES005 | 403 | Zugriff verweigert |

## E-Mail-Fehler (EMAIL)

| Code | HTTP Status | Beschreibung |
|------|-------------|-------------|
| EMAIL001 | 500 | IMAP-Verbindung fehlgeschlagen |
| EMAIL002 | 500 | SMTP-Verbindung fehlgeschlagen |
| EMAIL003 | 400 | Ungültiger Empfänger |
| EMAIL004 | 507 | Postfach voll |
| EMAIL005 | 400 | Anhang zu groß |
| EMAIL006 | 500 | Synchronisation fehlgeschlagen |
| EMAIL007 | 400 | Ungültiger Ordner |

## KI-Verarbeitungsfehler (AI)

| Code | HTTP Status | Beschreibung |
|------|-------------|-------------|
| AI001 | 500 | LLM-API-Fehler |
| AI002 | 503 | KI-Service nicht verfügbar |
| AI003 | 429 | KI-Rate-Limit überschritten |
| AI004 | 500 | Vektor-DB-Fehler |
| AI005 | 500 | Embedding-Generierung fehlgeschlagen |
| AI006 | 400 | Nicht unterstützter Inhaltstyp |
| AI007 | 504 | KI-Verarbeitung-Timeout |

## Serverfehler (SRV)

| Code | HTTP Status | Beschreibung |
|------|-------------|-------------|
| SRV001 | 500 | Interner Serverfehler |
| SRV002 | 503 | Service nicht verfügbar |
| SRV003 | 504 | Gateway-Timeout |
| SRV004 | 502 | Bad Gateway |
| SRV005 | 507 | Speicher voll |
| SRV006 | 500 | Datenbankfehler |

## Rate Limiting (RATE)

| Code | HTTP Status | Beschreibung |
|------|-------------|-------------|
| RATE001 | 429 | API-Rate-Limit überschritten |
| RATE002 | 429 | E-Mail-Sync-Rate-Limit |
| RATE003 | 429 | KI-Verarbeitung-Rate-Limit |

## Fehlerbehandlung-Beispiele

### Client-seitig
```javascript
try {
  const response = await fetch('/api/emails');
  const data = await response.json();
  
  if (!response.ok) {
    switch(data.error.code) {
      case 'AUTH002':
        // Token aktualisieren
        await refreshToken();
        break;
      case 'RATE001':
        // Warten und erneut versuchen
        await delay(data.error.details.retryAfter);
        break;
      default:
        showError(data.error.message);
    }
  }
} catch (error) {
  console.error('Anfrage fehlgeschlagen:', error);
}
```

### Server-seitig
```python
from fastapi import HTTPException

def handle_error(code: str, message: str, status_code: int):
    raise HTTPException(
        status_code=status_code,
        detail={
            "error": {
                "code": code,
                "message": message,
                "timestamp": datetime.utcnow()
            }
        }
    )
```