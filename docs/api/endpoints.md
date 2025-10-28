# REST API-Endpunkte

## Inhaltsverzeichnis / Table of Contents

### In diesem Dokument
- [Basis-URL](#basis-url)
- [Authentifizierung](#authentifizierung)
  - [POST /auth/login](#post-authlogin)
  - [POST /auth/logout](#post-authlogout)
  - [POST /auth/refresh](#post-authrefresh)
  - [GET /auth/login/{provider}](#get-authloginprovider)
  - [GET /auth/callback/{provider}](#get-authcallbackprovider)
- [E-Mail-Verwaltung](#e-mail-verwaltung)
  - [GET /emails](#get-emails)
  - [GET /emails/{id}](#get-emailsid)
  - [POST /emails](#post-emails)
  - [DELETE /emails/{id}](#delete-emailsid)
  - [POST /emails/{id}/reply](#post-emailsidreply)
  - [POST /emails/{id}/forward](#post-emailsidforward)
- [Suche](#suche)
  - [GET /search](#get-search)
- [KI-Operationen](#ki-operationen)
  - [POST /ai/classify](#post-aiclassify)
  - [POST /ai/generate-tags](#post-aigenerate-tags)
  - [POST /ai/summarize](#post-aisummarize)
  - [GET /ai/suggestions](#get-aisuggestions)
- [Kontoverwaltung](#kontoverwaltung)
  - [GET /accounts](#get-accounts)
  - [POST /accounts](#post-accounts)
  - [PUT /accounts/{id}](#put-accountsid)
  - [DELETE /accounts/{id}](#delete-accountsid)
  - [POST /accounts/{id}/sync](#post-accountsidsync)
- [Dokumentation](#dokumentation)
  - [GET /docs/{path}](#get-docspath)
  - [PUT /docs/{path}](#put-docspath)
- [WebSocket-Ereignisse](#websocket-ereignisse)

### Verwandte Dokumente
- [WebSocket-Ereignisse](./websocket.md)
- [API-Fehlercodes](./errors.md)
- [Entwicklungsumgebung](../deployment/development.md)
- [Docker-Konfiguration](../deployment/docker.md)

---

## Basis-URL
```
http://localhost:9000/api
```

## Authentifizierung

### POST /auth/login
Anmeldung mit E-Mail/Passwort oder OAuth
```json
{
  "email": "benutzer@beispiel.com",
  "password": "passwort123"
}
```

### POST /auth/logout
Aktuelle Session abmelden

### POST /auth/refresh
Access-Token aktualisieren

### GET /auth/login/{provider}
OAuth-Login-Umleitung

### GET /auth/callback/{provider}
OAuth-Callback-Handler

## E-Mail-Verwaltung

### GET /emails
E-Mails mit Paginierung auflisten
```
Query-Parameter:
- page: int (Standard: 1)
- limit: int (Standard: 50)
- folder: string
- search: string
```

### GET /emails/{id}
Spezifische E-Mail abrufen

### POST /emails
Neue E-Mail senden
```json
{
  "to": ["empfaenger@beispiel.com"],
  "subject": "Betreff",
  "body": "E-Mail-Inhalt",
  "attachments": []
}
```

### DELETE /emails/{id}
E-Mail löschen

### POST /emails/{id}/reply
Auf E-Mail antworten

### POST /emails/{id}/forward
E-Mail weiterleiten

## Suche

### GET /search
Semantische Suche
```
Abfrage-Parameter:
- q: string (erforderlich)
- limit: int
- from_date: datetime
- to_date: datetime
```

## KI-Operationen

### POST /ai/classify
E-Mails klassifizieren
```json
{
  "email_ids": ["id1", "id2"]
}
```

### POST /ai/generate-tags
Tags für E-Mails generieren

### POST /ai/summarize
E-Mail-Thread zusammenfassen

### GET /ai/suggestions
KI-Vorschläge für aktuellen Kontext abrufen

## Kontoverwaltung

### GET /accounts
E-Mail-Konten auflisten

### POST /accounts
E-Mail-Konto hinzufügen
```json
{
  "email": "benutzer@beispiel.com",
  "imap_server": "imap.gmail.com",
  "imap_port": 993,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "password": "app_password"
}
```

### PUT /accounts/{id}
Kontoeinstellungen aktualisieren

### DELETE /accounts/{id}
Konto entfernen

### POST /accounts/{id}/sync
Manuelle Synchronisation auslösen

## Dokumentation

### GET /docs/{path}
Dokumentationsinhalt abrufen

### PUT /docs/{path}
Dokumentation aktualisieren

## WebSocket-Ereignisse
Siehe [WebSocket-Ereignisse-Dokumentation](./websocket.md)