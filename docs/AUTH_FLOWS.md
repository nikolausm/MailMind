# Authentifizierungsabläufe - Detaillierter Implementierungsleitfaden

## Inhaltsverzeichnis

- [E-Mail/Passwort-Login-Ablauf](#e-mailpasswort-login-ablauf)
  - [1. Registrierungsablauf](#1-registrierungsablauf)
  - [2. E-Mail-Bestätigungsablauf](#2-e-mail-bestätigungsablauf)
  - [3. Login-Ablauf mit Problemszenarien](#3-login-ablauf-mit-problemszenarien)
  - [4. Passwort-Zurücksetzen-Ablauf - Vollständiger Prozess](#4-passwort-zurücksetzen-ablauf---vollständiger-prozess)
- [Sicherheitsmaßnahmen für Login-Probleme](#sicherheitsmaßnahmen-für-login-probleme)
  - [1. Ratenbegrenzung](#1-ratenbegrenzung)
  - [2. Konto-Sperrungs-Eskalation](#2-konto-sperrungs-eskalation)
  - [3. Passwort-Anforderungen](#3-passwort-anforderungen)
  - [4. Login-Problem-Lösung](#4-login-problem-lösung)
- [E-Mail-Vorlagen](#e-mail-vorlagen)
  - [1. Verifizierungs-E-Mail](#1-verifizierungs-e-mail)
  - [2. Passwort-Reset-E-Mail](#2-passwort-reset-e-mail)
  - [3. Passwort-Änderungs-Bestätigung](#3-passwort-änderungs-bestätigung)
- [Implementierungs-Checkliste](#implementierungs-checkliste)
  - [Backend-Anforderungen](#backend-anforderungen)
  - [Frontend-Anforderungen](#frontend-anforderungen)
  - [Datenbank-Tabellen](#datenbank-tabellen)
  - [Überwachung & Alarme](#überwachung--alarme)
- [Fehlercode-Referenz](#fehlercode-referenz)

## In diesem Dokument

- **[E-Mail/Passwort-Login-Ablauf](#e-mailpasswort-login-ablauf)**: Detaillierte Registrierungs- und Login-Abläufe
- **[Sicherheitsmaßnahmen](#sicherheitsmaßnahmen-für-login-probleme)**: Ratenbegrenzung, Kontosperrung und Passwort-Anforderungen
- **[E-Mail-Vorlagen](#e-mail-vorlagen)**: Verifizierungs-, Reset- und Bestätigungs-E-Mails
- **[Implementierungs-Checkliste](#implementierungs-checkliste)**: Backend-, Frontend- und Datenbank-Anforderungen
- **[Fehlercode-Referenz](#fehlercode-referenz)**: Vollständige Übersicht der Auth-Fehlercodes

## Verwandte Dokumente

- **[Authentifizierung](./AUTHENTICATION.md)**: Übergreifende Authentifizierungs-Anforderungen
- **[OAuth-Anbieter](./oauth-providers.md)**: OAuth-Provider-spezifische Flows
- **[Benutzer-Flows](./user-flows.md)**: Benutzerinteraktionen und -Erfahrungen
- **[Entwicklung](./DEVELOPMENT.md)**: Entwicklungsrichtlinien
- **[Internationalisierung](./internationalization.md)**: Mehrsprachige Unterstützung

## E-Mail/Passwort-Login-Ablauf

### 1. Registrierungsablauf

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User    │     │ Frontend │     │   API    │     │ Database │     │  Email   │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                 │                 │                 │                 │
     │ Klick          │                 │                 │                 │
     │ Registrieren   │                 │                 │                 │
     │────────────────>│                 │                 │                 │
     │                 │                 │                 │                 │
     │ Registrierungs- │                 │                 │                 │
     │ formular        │                 │                 │                 │
     │<────────────────│                 │                 │                 │
     │                 │                 │                 │                 │
     │ E-Mail,         │                 │                 │                 │
     │ Passwort, Name  │                 │                 │                 │
     │────────────────>│                 │                 │                 │
     │                 │                 │                 │                 │
     │                 │ Eingabe lokal   │                 │                 │
     │                 │ validieren      │                 │                 │
     │                 │───────┐         │                 │                 │
     │                 │       │         │                 │                 │
     │                 │<──────┘         │                 │                 │
     │                 │                 │                 │                 │
     │                 │ POST            │                 │                 │
     │                 │ /auth/register  │                 │                 │
     │                 │────────────────>│                 │                 │
     │                 │                 │                 │                 │
     │                 │                 │ E-Mail-Format   │                 │
     │                 │                 │ validieren      │                 │
     │                 │                 │───────┐         │                 │
     │                 │                 │       │         │                 │
     │                 │                 │<──────┘         │                 │
     │                 │                 │                 │                 │
     │                 │                 │ Passwort-Stärke │                 │
     │                 │                 │ prüfen          │                 │
     │                 │                 │───────┐         │                 │
     │                 │                 │       │         │                 │
     │                 │                 │<──────┘         │                 │
     │                 │                 │                 │                 │
     │                 │                 │ Prüfen ob       │                 │
     │                 │                 │ E-Mail existiert│                 │
     │                 │                 │────────────────>│                 │
     │                 │                 │                 │                 │
     ╔═════════════════════════════════════════════════════════════════════╗
     ║ FALL 1: E-Mail bereits vorhanden                                     ║
     ╠═════════════════════════════════════════════════════════════════════╣
     │                 │                 │                 │                 │
     │                 │                 │ Benutzer        │                 │
     │                 │                 │ existiert       │                 │
     │                 │                 │<────────────────│                 │
     │                 │                 │                 │                 │
     │                 │ 409 Conflict    │                 │                 │
     │                 │<────────────────│                 │                 │
     │                 │                 │                 │                 │
     │ E-Mail bereits  │                 │                 │                 │
     │ registriert     │                 │                 │                 │
     │<────────────────│                 │                 │                 │
     │                 │                 │                 │                 │
     ╠═════════════════════════════════════════════════════════════════════╣
     ║ FALL 2: Neuer Benutzer                                               ║
     ╠═════════════════════════════════════════════════════════════════════╣
     │                 │                 │                 │                 │
     │                 │                 │ E-Mail          │                 │
     │                 │                 │ verfügbar       │                 │
     │                 │                 │<────────────────│                 │
     │                 │                 │                 │                 │
     │                 │                 │ Passwort hashen │                 │
     │                 │                 │ (Argon2)        │                 │
     │                 │                 │───────┐         │                 │
     │                 │                 │       │         │                 │
     │                 │                 │<──────┘         │                 │
     │                 │                 │                 │                 │
     │                 │                 │ Benutzerdaten-  │                 │
     │                 │                 │ satz erstellen  │                 │
     │                 │                 │────────────────>│                 │
     │                 │                 │                 │                 │
     │                 │                 │ Bestätigungs-   │                 │
     │                 │                 │ E-Mail senden   │                 │
     │                 │                 │────────────────────────────────>│
     │                 │                 │                 │                 │
     │                 │ 201 Created +   │                 │                 │
     │                 │ Bestätigung     │                 │                 │
     │                 │ gesendet        │                 │                 │
     │                 │<────────────────│                 │                 │
     │                 │                 │                 │                 │
     │ E-Mail prüfen   │                 │                 │                 │
     │ zur Bestätigung │                 │                 │                 │
     │<────────────────│                 │                 │                 │
     │                 │                 │                 │                 │
     ╚═════════════════════════════════════════════════════════════════════╝
```

#### Registrierungs-Request/Response

**Request:**
```json
POST /auth/register
{
  "email": "benutzer@beispiel.com",
  "password": "SicheresPasswort123!",
  "full_name": "Max Mustermann",
  "accept_terms": true
}
```

**Erfolg Response (201):**
```json
{
  "message": "Registrierung erfolgreich. Bitte prüfen Sie Ihre E-Mail zur Bestätigung Ihres Kontos.",
  "user_id": "uuid-hier",
  "email": "benutzer@beispiel.com",
  "verification_sent": true
}
```

**Fehler Responses:**
- `400 Bad Request` - Ungültige Eingabe (schwaches Passwort, ungültige E-Mail)
- `409 Conflict` - E-Mail bereits registriert

### 2. E-Mail-Bestätigungsablauf

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User    │     │  Email   │     │ Frontend │     │   API    │     │ Database │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                 │                 │                 │                 │
     │ Bestätigungs-   │                 │                 │                 │
     │ E-Mail öffnen   │                 │                 │                 │
     │────────────────>│                 │                 │                 │
     │                 │                 │                 │                 │
     │ Bestätigungslink klicken          │                 │                 │
     │──────────────────────────────────>│                 │                 │
     │                 │                 │                 │                 │
     │                 │                 │ GET /auth/      │                 │
     │                 │                 │ verify-email?   │                 │
     │                 │                 │ token=xxx       │                 │
     │                 │                 │────────────────>│                 │
     │                 │                 │                 │                 │
     │                 │                 │                 │ Token           │
     │                 │                 │                 │ validieren      │
     │                 │                 │                 │───────┐         │
     │                 │                 │                 │       │         │
     │                 │                 │                 │<──────┘         │
     │                 │                 │                 │                 │
     │                 │                 │                 │ Token-Ablauf    │
     │                 │                 │                 │ prüfen          │
     │                 │                 │                 │ (24 Stunden)    │
     │                 │                 │                 │───────┐         │
     │                 │                 │                 │       │         │
     │                 │                 │                 │<──────┘         │
     │                 │                 │                 │                 │
     ╔═════════════════════════════════════════════════════════════════════╗
     ║ FALL 1: Gültiger Token                                               ║
     ╠═════════════════════════════════════════════════════════════════════╣
     │                 │                 │                 │                 │
     │                 │                 │                 │ E-Mail als      │
     │                 │                 │                 │ bestätigt       │
     │                 │                 │                 │ markieren       │
     │                 │                 │                 │────────────────>│
     │                 │                 │                 │                 │
     │                 │                 │ 200 OK          │                 │
     │                 │                 │<────────────────│                 │
     │                 │                 │                 │                 │
     │ E-Mail bestätigt!│                 │                 │                 │
     │ Sie können sich  │                 │                 │                 │
     │ jetzt anmelden   │                 │                 │                 │
     │<──────────────────────────────────│                 │                 │
     │                 │                 │                 │                 │
     ╠═════════════════════════════════════════════════════════════════════╣
     ║ FALL 2: Ungültiger/Abgelaufener Token                                ║
     ╠═════════════════════════════════════════════════════════════════════╣
     │                 │                 │                 │                 │
     │                 │                 │ 400 Bad Request │                 │
     │                 │                 │<────────────────│                 │
     │                 │                 │                 │                 │
     │ Erneut-senden-   │                 │                 │                 │
     │ Option anzeigen  │                 │                 │                 │
     │<──────────────────────────────────│                 │                 │
     │                 │                 │                 │                 │
     │ "Erneut senden" klicken            │                 │                 │
     │──────────────────────────────────>│                 │                 │
     │                 │                 │                 │                 │
     │                 │                 │ POST /auth/     │                 │
     │                 │                 │ resend-         │                 │
     │                 │                 │ verification    │                 │
     │                 │                 │────────────────>│                 │
     │                 │                 │                 │                 │
     ╚═════════════════════════════════════════════════════════════════════╝
```

### 3. Login-Ablauf mit Problemszenarien

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  User    │     │ Frontend │     │   API    │     │ Database │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                 │                 │                 │
     │ E-Mail/Passwort │                 │                 │
     │ eingeben        │                 │                 │
     │────────────────>│                 │                 │
     │                 │                 │                 │
     │                 │ POST            │                 │
     │                 │ /auth/login     │                 │
     │                 │────────────────>│                 │
     │                 │                 │                 │
     │                 │                 │ Benutzer nach   │
     │                 │                 │ E-Mail suchen   │
     │                 │                 │────────────────>│
     │                 │                 │                 │
     ╔═══════════════════════════════════════════════════╗
     ║ FALL 1: Benutzer nicht gefunden                   ║
     ╠═══════════════════════════════════════════════════╣
     │                 │                 │                 │
     │                 │ 401 Ungültige   │                 │
     │                 │ Anmeldedaten    │                 │
     │                 │<────────────────│                 │
     │                 │                 │                 │
     │ E-Mail oder     │                 │                 │
     │ Passwort falsch │                 │                 │
     │<────────────────│                 │                 │
     │                 │                 │                 │
     ╠═══════════════════════════════════════════════════╣
     ║ FALL 2: Benutzer gefunden                         ║
     ╠═══════════════════════════════════════════════════╣
     │                 │                 │                 │
     │                 │                 │ Kontostatus     │
     │                 │                 │ prüfen          │
     │                 │                 │───────┐         │
     │                 │                 │       │         │
     │                 │                 │<──────┘         │
     │                 │                 │                 │
     ├─────────────────────────────────────────────────────┤
     │ FALL 2.1: E-Mail nicht bestätigt                   │
     ├─────────────────────────────────────────────────────┤
     │                 │ 403 E-Mail      │                 │
     │                 │ nicht bestätigt │                 │
     │                 │<────────────────│                 │
     │                 │                 │                 │
     │ Bestätigung     │                 │                 │
     │ erneut senden   │                 │                 │
     │ Button anzeigen │                 │                 │
     │<────────────────│                 │                 │
     │                 │                 │                 │
     ├─────────────────────────────────────────────────────┤
     │ FALL 2.2: Konto gesperrt (zu viele Versuche)       │
     ├─────────────────────────────────────────────────────┤
     │                 │ 423 Konto       │                 │
     │                 │ temporär        │                 │
     │                 │ gesperrt        │                 │
     │                 │<────────────────│                 │
     │                 │                 │                 │
     │ Zu viele        │                 │                 │
     │ Versuche.       │                 │                 │
     │ In 15 Min.      │                 │                 │
     │ erneut          │                 │                 │
     │<────────────────│                 │                 │
     │                 │                 │                 │
     ├─────────────────────────────────────────────────────┤
     │ FALL 2.3: Konto deaktiviert                         │
     ├─────────────────────────────────────────────────────┤
     │                 │ 403 Konto       │                 │
     │                 │ deaktiviert     │                 │
     │                 │<────────────────│                 │
     │                 │                 │                 │
     │ Support         │                 │                 │
     │ kontaktieren    │                 │                 │
     │<────────────────│                 │                 │
     │                 │                 │                 │
     ├─────────────────────────────────────────────────────┤
     │ FALL 2.4: Passwort-Prüfung                          │
     ├─────────────────────────────────────────────────────┤
     │                 │                 │ Passwort-Hash   │
     │                 │                 │ verifizieren    │
     │                 │                 │───────┐         │
     │                 │                 │       │         │
     │                 │                 │<──────┘         │
     │                 │                 │                 │
     │ FALL 2.4.1: Passwort stimmt überein                │
     │                 │                 │                 │
     │                 │                 │ JWT-Token       │
     │                 │                 │ generieren      │
     │                 │                 │───────┐         │
     │                 │                 │       │         │
     │                 │                 │<──────┘         │
     │                 │                 │                 │
     │                 │                 │ Login-Versuch   │
     │                 │                 │ protokollieren  │
     │                 │                 │────────────────>│
     │                 │                 │                 │
     │                 │ 200 OK + Token  │                 │
     │                 │<────────────────│                 │
     │                 │                 │                 │
     │ Zum Dashboard   │                 │                 │
     │ weiterleiten    │                 │                 │
     │<────────────────│                 │                 │
     │                 │                 │                 │
     │ FALL 2.4.2: Passwort falsch                        │
     │                 │                 │                 │
     │                 │                 │ Fehlgeschlagene │
     │                 │                 │ Versuche        │
     │                 │                 │ erhöhen         │
     │                 │                 │────────────────>│
     │                 │                 │                 │
     │                 │ 401 Ungültige   │                 │
     │                 │ Anmeldedaten    │                 │
     │                 │<────────────────│                 │
     │                 │                 │                 │
     │ E-Mail oder     │                 │                 │
     │ Passwort falsch │                 │                 │
     │<────────────────│                 │                 │
     │                 │                 │                 │
     ╚═══════════════════════════════════════════════════╝
```

#### Login Request/Response

**Request:**
```json
POST /auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "remember_me": true
}
```

**Erfolg Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 900,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "email_verified": true
  }
}
```

### 4. Passwort-Zurücksetzen-Ablauf - Vollständiger Prozess

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  User    │  │ Frontend │  │   API    │  │ Database │  │  Email   │  │  Redis   │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │              │              │              │              │              │
╔════════════════════════════════════════════════════════════════════════════════╗
║                        SCHRITT 1: Passwort-Reset anfordern                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
     │              │              │              │              │              │
     │ Passwort     │              │              │              │              │
     │ vergessen    │              │              │              │              │
     │ klicken      │              │              │              │              │
     │─────────────>│              │              │              │              │
     │              │              │              │              │              │
     │ E-Mail-      │              │              │              │              │
     │ Eingabe-     │              │              │              │              │
     │ formular     │              │              │              │              │
     │<─────────────│              │              │              │              │
     │              │              │              │              │              │
     │ E-Mail-      │              │              │              │              │
     │ Adresse      │              │              │              │              │
     │ eingeben     │              │              │              │              │
     │─────────────>│              │              │              │              │
     │              │              │              │              │              │
     │              │ POST /auth/  │              │              │              │
     │              │ forgot-      │              │              │              │
     │              │ password     │              │              │              │
     │              │─────────────>│              │              │              │
     │              │              │              │              │              │
     │              │              │ Prüfen ob    │              │              │
     │              │              │ Benutzer     │              │              │
     │              │              │ existiert    │              │              │
     │              │              │─────────────>│              │              │
     │              │              │              │              │              │
     ├──────────────────────────────────────────────────────────────────────────┤
     │ FALL 1: Benutzer existiert                                               │
     ├──────────────────────────────────────────────────────────────────────────┤
     │              │              │              │              │              │
     │              │              │ Sicheren     │              │              │
     │              │              │ Reset-Token  │              │              │
     │              │              │ generieren   │              │              │
     │              │              │─────┐        │              │              │
     │              │              │     │        │              │              │
     │              │              │<────┘        │              │              │
     │              │              │              │              │              │
     │              │              │ Token speichern              │              │
     │              │              │ (läuft in 1 Stunde ab)      │              │
     │              │              │─────────────────────────────────────────>│
     │              │              │              │              │              │
     │              │              │ Reset-Anfrage│              │              │
     │              │              │ protokol-    │              │              │
     │              │              │ lieren       │              │              │
     │              │              │─────────────>│              │              │
     │              │              │              │              │              │
     │              │              │ Reset-E-Mail senden         │              │
     │              │              │─────────────────────────────>│              │
     │              │              │              │              │              │
     │              │ 200 Reset-   │              │              │              │
     │              │ E-Mail       │              │              │              │
     │              │ gesendet     │              │              │              │
     │              │<─────────────│              │              │              │
     │              │              │              │              │              │
     ├──────────────────────────────────────────────────────────────────────────┤
     │ FALL 2: Benutzer existiert nicht                                         │
     ├──────────────────────────────────────────────────────────────────────────┤
     │              │              │              │              │              │
     │              │              │ Zufällig     │              │              │
     │              │              │ 200-500ms    │              │              │
     │              │              │ warten       │              │              │
     │              │              │─────┐        │              │              │
     │              │              │     │        │              │              │
     │              │              │<────┘        │              │              │
     │              │              │              │              │              │
     │              │ 200 Reset-   │              │              │              │
     │              │ E-Mail       │              │              │              │
     │              │ gesendet     │              │              │              │
     │              │ (gleiche     │              │              │              │
     │              │ Antwort)     │              │              │              │
     │              │<─────────────│              │              │              │
     │              │              │              │              │              │
     │ Prüfen Sie   │              │              │              │              │
     │ Ihre E-Mail  │              │              │              │              │
     │ für Reset-   │              │              │              │              │
     │ Link         │              │              │              │              │
     │<─────────────│              │              │              │              │
     │              │              │              │              │              │
╔════════════════════════════════════════════════════════════════════════════════╗
║                        SCHRITT 2: Reset-Token verifizieren                      ║
╚════════════════════════════════════════════════════════════════════════════════╝
     │              │              │              │              │              │
     │ Reset-E-Mail öffnen                        │              │              │
     │────────────────────────────────────────────>│              │              │
     │              │              │              │              │              │
     │ Reset-Link klicken          │              │              │              │
     │─────────────────────────────>│              │              │              │
     │              │              │              │              │              │
     │              │ GET /auth/   │              │              │              │
     │              │ verify-reset-│              │              │              │
     │              │ token?       │              │              │              │
     │              │ token=xxx    │              │              │              │
     │              │─────────────>│              │              │              │
     │              │              │              │              │              │
     │              │              │ Token-Existenz validieren   │              │
     │              │              │─────────────────────────────────────────>│
     │              │              │              │              │              │
     ├──────────────────────────────────────────────────────────────────────────┤
     │ FALL 1: Gültiger Token                                                   │
     ├──────────────────────────────────────────────────────────────────────────┤
     │              │              │              │              │              │
     │              │ 200 Token    │              │              │              │
     │              │ gültig       │              │              │              │
     │              │<─────────────│              │              │              │
     │              │              │              │              │              │
     │ Neues        │              │              │              │              │
     │ Passwort-    │              │              │              │              │
     │ Formular     │              │              │              │              │
     │ anzeigen     │              │              │              │              │
     │<─────────────│              │              │              │              │
     │              │              │              │              │              │
     ├──────────────────────────────────────────────────────────────────────────┤
     │ FALL 2: Ungültiger/Abgelaufener Token                                    │
     ├──────────────────────────────────────────────────────────────────────────┤
     │              │              │              │              │              │
     │              │ 400          │              │              │              │
     │              │ Ungültiger   │              │              │              │
     │              │ oder         │              │              │              │
     │              │ abgelaufener │              │              │              │
     │              │ Token        │              │              │              │
     │              │<─────────────│              │              │              │
     │              │              │              │              │              │
     │ Link         │              │              │              │              │
     │ abgelaufen.  │              │              │              │              │
     │ Neuen        │              │              │              │              │
     │ anfordern    │              │              │              │              │
     │<─────────────│              │              │              │              │
     │              │              │              │              │              │
╔════════════════════════════════════════════════════════════════════════════════╗
║                        SCHRITT 3: Neues Passwort setzen                         ║
╚════════════════════════════════════════════════════════════════════════════════╝
     │              │              │              │              │              │
     │ Neues        │              │              │              │              │
     │ Passwort     │              │              │              │              │
     │ zweimal      │              │              │              │              │
     │ eingeben     │              │              │              │              │
     │─────────────>│              │              │              │              │
     │              │              │              │              │              │
     │              │ Passwort-    │              │              │              │
     │              │ Überein-     │              │              │              │
     │              │ stimmung     │              │              │              │
     │              │ validieren   │              │              │              │
     │              │─────┐        │              │              │              │
     │              │     │        │              │              │              │
     │              │<────┘        │              │              │              │
     │              │              │              │              │              │
     │              │ POST /auth/  │              │              │              │
     │              │ reset-       │              │              │              │
     │              │ password     │              │              │              │
     │              │─────────────>│              │              │              │
     │              │              │              │              │              │
     │              │              │ Token erneut verifizieren   │              │
     │              │              │─────────────────────────────────────────>│
     │              │              │              │              │              │
     │              │              │ Passwort-    │              │              │
     │              │              │ stärke       │              │              │
     │              │              │ validieren   │              │              │
     │              │              │─────┐        │              │              │
     │              │              │     │        │              │              │
     │              │              │<────┘        │              │              │
     │              │              │              │              │              │
     │              │              │ Neues        │              │              │
     │              │              │ Passwort     │              │              │
     │              │              │ hashen       │              │              │
     │              │              │─────┐        │              │              │
     │              │              │     │        │              │              │
     │              │              │<────┘        │              │              │
     │              │              │              │              │              │
     │              │              │ Passwort     │              │              │
     │              │              │ aktualisieren│              │              │
     │              │              │─────────────>│              │              │
     │              │              │              │              │              │
     │              │              │ Verwendeten Token löschen   │              │
     │              │              │─────────────────────────────────────────>│
     │              │              │              │              │              │
     │              │              │ Alle         │              │              │
     │              │              │ Sitzungen    │              │              │
     │              │              │ invalidieren │              │              │
     │              │              │─────────────>│              │              │
     │              │              │              │              │              │
     │              │              │ Bestätigungs-E-Mail senden  │              │
     │              │              │─────────────────────────────>│              │
     │              │              │              │              │              │
     │              │ 200 Passwort │              │              │              │
     │              │ erfolgreich  │              │              │              │
     │              │ zurückgesetzt│              │              │              │
     │              │<─────────────│              │              │              │
     │              │              │              │              │              │
     │ Zur Anmeldung│              │              │              │              │
     │ weiterleiten │              │              │              │              │
     │<─────────────│              │              │              │              │
     │              │              │              │              │              │
```

#### Password Reset Endpoints

**1. Request Reset:**
```json
POST /auth/forgot-password
{
  "email": "user@example.com"
}

Response (always 200 to prevent email enumeration):
{
  "message": "If an account exists with this email, a reset link has been sent."
}
```

**2. Verify Token:**
```json
GET /auth/verify-reset-token?token=abc123xyz

Success (200):
{
  "valid": true,
  "email": "u***@example.com"  // Partially hidden
}

Error (400):
{
  "valid": false,
  "error": "Token expired or invalid"
}
```

**3. Passwort zurücksetzen:**
```json
POST /auth/reset-password
{
  "token": "abc123xyz",
  "new_password": "NewSecurePass456!",
  "confirm_password": "NewSecurePass456!"
}

Erfolg (200):
{
  "message": "Passwort erfolgreich zurückgesetzt. Bitte melden Sie sich mit Ihrem neuen Passwort an."
}
```

## Sicherheitsmaßnahmen für Login-Probleme

### 1. Ratenbegrenzung
```python
# Pro IP-Adresse
- Registrierung: 3 Versuche pro Stunde
- Login: 5 Versuche pro 15 Minuten
- Passwort-Reset: 3 Anfragen pro Stunde
- Verifizierung erneut senden: 3 pro Tag

# Pro E-Mail/Konto
- Login: 5 fehlgeschlagene Versuche = 15-Minütige Sperrung
- Passwort-Reset: 3 Anfragen pro Tag
```

### 2. Konto-Sperrungs-Eskalation
```
1-5 fehlgeschlagene Versuche: Keine Aktion
6-10 fehlgeschlagene Versuche: 15-Minütige Sperrung
11-15 fehlgeschlagene Versuche: 1-Stündige Sperrung
16-20 fehlgeschlagene Versuche: 24-Stündige Sperrung
20+ fehlgeschlagene Versuche: Konto benötigt Admin-Entsperrung
```

### 3. Passwort-Anforderungen
```javascript
{
  minLength: 8,
  maxLength: 128,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecialChars: true,
  prohibitedPatterns: [
    'password', 'qwerty', '12345678',
    // E-Mail-Teile des Benutzers
    // Häufige Tastaturmuster
  ],
  checkHaveIBeenPwned: true  // Prüfung gegen kompromittierte Passwörter
}
```

### 4. Login-Problem-Lösung

#### Häufige Probleme und Lösungen:

**Problem: "Ungültige Anmeldedaten" aber Benutzer ist sicher, dass Passwort korrekt ist**
```
Mögliche Ursachen:
1. Feststelltaste ist aktiviert
2. Passwort wurde kürzlich geändert
3. Konto verwendet OAuth (Google/Microsoft) nicht Passwort
4. Leerzeichen am Anfang/Ende der E-Mail

Backend-Prüfungen:
- Detaillierten Fehler protokollieren (nicht für Benutzer sichtbar)
- Prüfen ob Konto nur OAuth verwendet
- E-Mail-Eingabe trimmen
- Groß-/Kleinschreibung-unabhängiger E-Mail-Vergleich
```

**Problem: Konto gesperrt**
```
Automatische Entsperrung nach Timeout ODER
Manueller Entsperrungs-Prozess:
1. Benutzer fordert Entsperrung über Support an
2. Identitätsverifikation (Sicherheitsfragen/E-Mail)
3. Admin entsperrt manuell
4. Benutzer muss Passwort zurücksetzen
```

**Problem: E-Mail nicht verifiziert**
```
1. Spam-Ordner prüfen Erinnerung
2. Verifizierung erneut senden (max 3/Tag)
3. E-Mail-Adresse aktualisieren Option
4. Manuelle Verifizierung durch Support
```

## E-Mail-Vorlagen

### 1. Verifizierungs-E-Mail
```html
Betreff: Verifizieren Sie Ihr MailMind-Konto

Hallo {name},

Willkommen bei MailMind! Bitte verifizieren Sie Ihre E-Mail-Adresse, indem Sie auf den unten stehenden Link klicken:

[E-Mail verifizieren] {verification_link}

Dieser Link läuft in 24 Stunden ab.

Wenn Sie dieses Konto nicht erstellt haben, ignorieren Sie bitte diese E-Mail.

Mit freundlichen Grüßen,
Das MailMind-Team
```

### 2. Passwort-Reset-E-Mail
```html
Betreff: Setzen Sie Ihr MailMind-Passwort zurück

Hallo {name},

Wir haben eine Anfrage erhalten, Ihr Passwort zurückzusetzen. Klicken Sie auf den unten stehenden Link, um ein neues Passwort festzulegen:

[Passwort zurücksetzen] {reset_link}

Dieser Link läuft aus Sicherheitsgründen in 1 Stunde ab.

Wenn Sie dies nicht angefordert haben, ignorieren Sie bitte diese E-Mail. Ihr Passwort wird nicht geändert.

Aus Sicherheitsgründen wird dieses Passwort-Reset:
- Sie von allen Geräten abmelden
- Sie auffordern, sich mit Ihrem neuen Passwort erneut anzumelden

Mit freundlichen Grüßen,
Das MailMind-Team
```

### 3. Passwort-Änderungs-Bestätigung
```html
Betreff: Ihr MailMind-Passwort wurde geändert

Hallo {name},

Ihr Passwort wurde erfolgreich um {timestamp} geändert.

Details:
- IP-Adresse: {ip_address}
- Standort: {location}
- Gerät: {device}

Wenn Sie diese Änderung nicht vorgenommen haben, bitte:
1. Setzen Sie Ihr Passwort sofort zurück
2. Überprüfen Sie Ihre Kontoaktivität
3. Kontaktieren Sie den Support

Mit freundlichen Grüßen,
Das MailMind-Team
```

## Implementierungs-Checkliste

### Backend-Anforderungen
- [ ] Passwort-Stärke-Validator
- [ ] E-Mail-Verifizierungssystem
- [ ] Token-Generierung und -Speicherung (Redis)
- [ ] Ratenbegrenzungs-Middleware
- [ ] Konto-Sperrmechanismus
- [ ] Audit-Protokollierung für Auth-Ereignisse
- [ ] E-Mail-Service-Integration
- [ ] Passwort-Historie (Wiederverwendung verhindern)
- [ ] Sitzungsverwaltung
- [ ] CAPTCHA für wiederholte Fehlversuche

### Frontend-Anforderungen
- [ ] Passwort-Stärke-Indikator
- [ ] Passwort anzeigen/verbergen Toggle
- [ ] "Angemeldet bleiben" Checkbox
- [ ] Klare Fehlermeldungen
- [ ] Ladezustände für Auth-Operationen
- [ ] Automatische Weiterleitung nach Login
- [ ] Sitzungs-Timeout-Warnung
- [ ] Verifizierung erneut senden UI
- [ ] Passwort-Reset-Ablauf UI
- [ ] Konto-gesperrt-Meldungen

### Datenbank-Tabellen
- [ ] users-Tabelle mit Sperrfeldern
- [ ] password_reset_tokens-Tabelle
- [ ] login_attempts-Tabelle
- [ ] audit_log-Tabelle
- [ ] sessions-Tabelle
- [ ] email_verifications-Tabelle

### Überwachung & Alarme
- [ ] Fehlgeschlagene Login-Spitzen
- [ ] Passwort-Reset-Missbrauch
- [ ] Brute-Force-Versuche
- [ ] Konto-Enumerations-Versuche
- [ ] Ungewöhnliche Login-Muster
- [ ] Token-Ablaufraten

## Fehlercode-Referenz

| Code | Nachricht | Benutzeraktion |
|------|-----------|----------------|
| AUTH001 | Ungültige Anmeldedaten | E-Mail/Passwort prüfen |
| AUTH002 | E-Mail nicht verifiziert | E-Mail prüfen oder erneut senden |
| AUTH003 | Konto gesperrt | Warten oder Support kontaktieren |
| AUTH004 | Konto deaktiviert | Support kontaktieren |
| AUTH005 | Token abgelaufen | Neuen Token anfordern |
| AUTH006 | Token ungültig | Neuen Token anfordern |
| AUTH007 | Passwort zu schwach | Stärkeres Passwort wählen |
| AUTH008 | E-Mail existiert bereits | Andere E-Mail verwenden oder anmelden |
| AUTH009 | Ratenlimit überschritten | Vor erneutem Versuch warten |
| AUTH010 | Sitzung abgelaufen | Erneut anmelden |