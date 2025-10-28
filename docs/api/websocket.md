# WebSocket-Ereignisse

## Inhaltsverzeichnis / Table of Contents

### In diesem Dokument
- [Verbindung](#verbindung)
- [Authentifizierung](#authentifizierung)
- [Event-Typen](#event-typen)
  - [Server → Client](#server--client)
    - [new_email](#new_email)
    - [email_processed](#email_processed)
    - [sync_status](#sync_status)
    - [ai_suggestion](#ai_suggestion)
  - [Client → Server](#client--server)
    - [subscribe](#subscribe)
    - [unsubscribe](#unsubscribe)
    - [ping](#ping)
- [Verbindungs-Management](#verbindungs-management)
  - [Wiederverbindungs-Strategie](#wiederverbindungs-strategie)
  - [Fehlerbehandlung](#fehlerbehandlung)

### Verwandte Dokumente
- [REST API-Endpunkte](./endpoints.md)
- [API-Fehlercodes](./errors.md)
- [Entwicklungsumgebung](../deployment/development.md)
- [Docker-Konfiguration](../deployment/docker.md)

---

## Verbindung
```
ws://localhost:9000/ws
```

## Authentifizierung
Auth-Token nach Verbindung senden:
```json
{
  "type": "auth",
  "token": "jwt_token_hier"
}
```

## Event-Typen

### Server → Client

#### new_email
Neue E-Mail empfangen
```json
{
  "type": "new_email",
  "data": {
    "email_id": "uuid",
    "subject": "Neue E-Mail",
    "sender": "absender@beispiel.com",
    "preview": "E-Mail-Vorschautext..."
  }
}
```

#### email_processed
E-Mail-KI-Verarbeitung abgeschlossen
```json
{
  "type": "email_processed",
  "data": {
    "email_id": "uuid",
    "classification": "work",
    "priority": 85,
    "tags": ["project", "urgent"],
    "summary": "Kurze Zusammenfassung..."
  }
}
```

#### sync_status
Synchronisationsoperations-Status
```json
{
  "type": "sync_status",
  "data": {
    "account_id": "uuid",
    "status": "syncing|completed|error",
    "progress": 75,
    "message": "Synchronisiere Ordner INBOX..."
  }
}
```

#### ai_suggestion
KI-generierter Vorschlag
```json
{
  "type": "ai_suggestion",
  "data": {
    "suggestion_type": "response|action|organization",
    "content": "Vorgeschlagener Antworttext...",
    "confidence": 0.92
  }
}
```

### Client → Server

#### subscribe
Spezifische Events abonnieren
```json
{
  "type": "subscribe",
  "events": ["new_email", "email_processed"]
}
```

#### unsubscribe
Events abbestellen
```json
{
  "type": "unsubscribe",
  "events": ["sync_status"]
}
```

#### ping
Verbindung aufrechterhalten
```json
{
  "type": "ping"
}
```

## Verbindungs-Management

### Wiederverbindungs-Strategie
```javascript
class WebSocketManager {
  connect() {
    this.ws = new WebSocket('ws://localhost:9000/ws');
    
    this.ws.onclose = () => {
      // Exponentielles Backoff
      setTimeout(() => this.connect(), this.reconnectDelay);
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, 30000);
    };
    
    this.ws.onopen = () => {
      this.reconnectDelay = 1000;
      this.authenticate();
    };
  }
}
```

### Fehlerbehandlung
```json
{
  "type": "error",
  "data": {
    "code": "AUTH_FAILED",
    "message": "Authentifizierung fehlgeschlagen"
  }
}
```