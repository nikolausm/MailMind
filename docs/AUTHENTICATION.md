# Authentifizierungs-Anforderungen

## Inhaltsverzeichnis

- [Übersicht](#übersicht)
- [Authentifizierungsmethoden](#authentifizierungsmethoden)
  - [1. OAuth 2.0 Anbieter](#1-oauth-20-anbieter)
  - [2. Traditionelle Authentifizierung](#2-traditionelle-authentifizierung)
  - [3. Enterprise-Authentifizierung (Zukunft)](#3-enterprise-authentifizierung-zukunft)
- [Technische Implementierung](#technische-implementierung)
  - [Backend-Anforderungen](#backend-anforderungen)
  - [API-Endpunkte](#api-endpunkte)
- [Security Requirements](#security-requirements)
  - [Token Management](#token-management)
  - [Session Security](#session-security)
  - [Data Protection](#data-protection)
- [Database Schema](#database-schema)
  - [Users Table](#users-table)
  - [OAuth Accounts Table](#oauth-accounts-table)
  - [Sessions Table](#sessions-table)
- [Frontend Requirements](#frontend-requirements)
  - [Login UI Components](#login-ui-components)
  - [User Experience](#user-experience)
- [Environment Variables](#environment-variables)
- [Implementation Priorities](#implementation-priorities)
  - [Phase 1 - Core Authentication](#phase-1---core-authentication)
  - [Phase 2 - OAuth Integration](#phase-2---oauth-integration)
  - [Phase 3 - Enhanced Security](#phase-3---enhanced-security)
  - [Phase 4 - Enterprise Features](#phase-4---enterprise-features)
- [Success Metrics](#success-metrics)
- [Compliance Requirements](#compliance-requirements)

## In diesem Dokument

- **[Übersicht](#übersicht)**: Einführung in die Authentifizierungs-Anforderungen
- **[Authentifizierungsmethoden](#authentifizierungsmethoden)**: OAuth 2.0, traditionelle und Enterprise-Methoden
- **[Technische Implementierung](#technische-implementierung)**: Backend-Struktur und API-Endpunkte
- **[Security Requirements](#security-requirements)**: Token-Management und Datenschutz
- **[Database Schema](#database-schema)**: Datenbank-Strukturen für Benutzer und Sessions
- **[Frontend Requirements](#frontend-requirements)**: UI-Komponenten und Benutzererfahrung
- **[Implementation Priorities](#implementation-priorities)**: Phasenweise Umsetzung

## Verwandte Dokumente

- **[Auth-Flows](./AUTH_FLOWS.md)**: Detaillierte Authentifizierungs-Abläufe
- **[OAuth-Anbieter](./oauth-providers.md)**: Spezifische OAuth-Provider-Konfigurationen
- **[Benutzer-Flows](./user-flows.md)**: Benutzerinteraktionen und -Erfahrungen
- **[Entwicklung](./DEVELOPMENT.md)**: Entwicklungsrichtlinien
- **[Internationalisierung](./internationalization.md)**: Mehrsprachige Unterstützung

## Übersicht

MailMind benötigt ein flexibles, sicheres Authentifizierungssystem, das mehrere Login-Anbieter unterstützt, um verschiedenen Benutzerpräferenzen und organisatorischen Anforderungen gerecht zu werden.

## Authentifizierungsmethoden

### 1. OAuth 2.0 Anbieter

#### Google OAuth
- **Anwendungsfall**: Persönliche Gmail-Nutzer, Google Workspace-Konten
- **Vorteile**: Nahtlose Integration mit Gmail-Konten
- **Erforderliche Scopes**:
  - `openid` - Benutzeridentifikation
  - `email` - E-Mail-Adresszugriff
  - `profile` - Grundlegende Profilinformationen
  - `https://www.googleapis.com/auth/gmail.readonly` - Gmail-Nachrichten lesen
  - `https://www.googleapis.com/auth/gmail.send` - E-Mails versenden

#### Microsoft OAuth (Azure AD)
- **Anwendungsfall**: Office 365-Nutzer, Outlook.com-Konten, Unternehmens-Microsoft-Umgebungen
- **Vorteile**: Enterprise SSO, Azure AD-Integration
- **Erforderliche Scopes**:
  - `openid` - Benutzeridentifikation
  - `email` - E-Mail-Adresse
  - `profile` - Benutzerprofil
  - `Mail.Read` - E-Mails lesen
  - `Mail.Send` - E-Mails senden

#### Apple Sign In
- **Anwendungsfall**: Apple-Ökosystem-Nutzer, datenschutzbewusste Nutzer
- **Vorteile**: Datenschutzfunktionen (Hide My Email), biometrische Authentifizierung
- **Anforderungen**:
  - Apple Developer-Konto
  - Service-ID-Konfiguration
  - Privater Schlüssel für Token-Validierung

### 2. Traditionelle Authentifizierung

#### E-Mail + Passwort
- **Anwendungsfall**: Nutzer, die traditionelle Anmeldung bevorzugen, benutzerdefinierte E-Mail-Server
- **Anforderungen**:
  - Starke Passwort-Richtlinie (min. 8 Zeichen, Komplexitätsanforderungen)
  - Passwort-Hashing (bcrypt/argon2)
  - E-Mail-Verifizierungsablauf
  - Passwort-Reset-Funktionalität
  - Rate Limiting für Brute-Force-Schutz

### 3. Enterprise-Authentifizierung (Zukunft)

#### SAML 2.0
- **Anwendungsfall**: Enterprise SSO-Integration
- **Unterstützung**: Okta, OneLogin, AD FS

#### LDAP/Active Directory
- **Anwendungsfall**: On-Premise-Enterprise-Deployments
- **Unterstützung**: Direkte AD-Integration

## Technische Implementierung

### Backend-Anforderungen

#### Authentifizierungsservice-Struktur
```python
src/backend/
├── auth/
│   ├── __init__.py
│   ├── providers/
│   │   ├── google.py      # Google OAuth handler
│   │   ├── microsoft.py   # Microsoft OAuth handler
│   │   ├── apple.py       # Apple Sign In handler
│   │   └── email.py       # Email/password handler
│   ├── models/
│   │   ├── user.py        # User model
│   │   ├── session.py     # Session management
│   │   └── oauth.py       # OAuth tokens storage
│   ├── middleware/
│   │   ├── jwt.py         # JWT validation
│   │   └── rate_limit.py  # Rate limiting
│   └── routes/
│       ├── auth.py        # Auth endpoints
│       └── user.py        # User management
```

#### API-Endpunkte
```
POST   /auth/register          # Email/password registration
POST   /auth/login             # Email/password login
POST   /auth/logout            # Logout
POST   /auth/refresh           # Refresh JWT token
POST   /auth/forgot-password   # Password reset request
POST   /auth/reset-password    # Password reset confirmation
GET    /auth/verify-email      # Email verification

GET    /auth/google            # Initiate Google OAuth
GET    /auth/google/callback   # Google OAuth callback
GET    /auth/microsoft         # Initiate Microsoft OAuth
GET    /auth/microsoft/callback # Microsoft OAuth callback
GET    /auth/apple             # Initiate Apple Sign In
POST   /auth/apple/callback    # Apple Sign In callback

GET    /auth/me                # Get current user info
PATCH  /auth/me                # Update user profile
DELETE /auth/me                # Delete account
```

### Security Requirements

#### Token Management
- **JWT Tokens**: Short-lived access tokens (15 min)
- **Refresh Tokens**: Long-lived refresh tokens (7 days)
- **Token Rotation**: Automatic refresh token rotation
- **Revocation**: Token blacklist for logout/revocation

#### Session Security
- **Secure Cookies**: HttpOnly, Secure, SameSite=Strict
- **CSRF Protection**: Double-submit cookie pattern
- **Session Timeout**: Configurable idle timeout
- **Device Tracking**: Optional device fingerprinting

#### Data Protection
- **Password Hashing**: Argon2id or bcrypt
- **Encryption**: AES-256 for sensitive data at rest
- **TLS**: Enforce HTTPS for all auth endpoints
- **PII Handling**: Comply with GDPR/CCPA

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    password_hash VARCHAR(255),  -- NULL for OAuth-only users
    full_name VARCHAR(255),
    avatar_url TEXT,
    auth_provider VARCHAR(50),   -- 'local', 'google', 'microsoft', 'apple'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    mfa_secret VARCHAR(255)
);
```

#### OAuth Accounts Table
```sql
CREATE TABLE oauth_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,
    provider_user_id VARCHAR(255) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP,
    scopes TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(provider, provider_user_id)
);
```

#### Sessions Table
```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    device_info JSONB,
    ip_address INET,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_activity TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);
```

### Frontend Requirements

#### Login UI Components
- Universal login page with provider buttons
- Social login buttons (Google, Microsoft, Apple)
- Email/password form with validation
- "Remember me" checkbox
- Password strength indicator
- Two-factor authentication support

#### User Experience
- Single Sign-On (SSO) flow
- Account linking (connect multiple providers)
- Profile management interface
- Security settings page
- Active sessions management
- Account deletion workflow

### Environment Variables

```env
# OAuth - Google
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:9000/auth/google/callback

# OAuth - Microsoft
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret
MICROSOFT_REDIRECT_URI=http://localhost:9000/auth/microsoft/callback

# OAuth - Apple
APPLE_CLIENT_ID=your_apple_client_id
APPLE_TEAM_ID=your_apple_team_id
APPLE_KEY_ID=your_apple_key_id
APPLE_PRIVATE_KEY=your_apple_private_key
APPLE_REDIRECT_URI=http://localhost:9000/auth/apple/callback

# Security
JWT_SECRET=your_jwt_secret_key
JWT_REFRESH_SECRET=your_jwt_refresh_secret
ENCRYPTION_KEY=your_encryption_key

# Email Service (for verification/reset)
EMAIL_FROM=noreply@mailmind.app
SENDGRID_API_KEY=your_sendgrid_key  # or other email service
```

## Implementation Priorities

### Phase 1 - Core Authentication
1. Email + Password authentication
2. JWT token management
3. User registration/login
4. Password reset flow
5. Email verification

### Phase 2 - OAuth Integration
1. Google OAuth (primary for Gmail users)
2. Microsoft OAuth (for Outlook users)
3. Account linking functionality
4. OAuth token refresh handling

### Phase 3 - Enhanced Security
1. Two-factor authentication (TOTP)
2. Apple Sign In
3. Device management
4. Audit logging
5. Rate limiting and abuse prevention

### Phase 4 - Enterprise Features
1. SAML 2.0 support
2. LDAP/AD integration
3. Custom SSO providers
4. Admin user management

## Success Metrics
- Login success rate > 95%
- OAuth flow completion > 90%
- Password reset completion > 85%
- Average authentication time < 2 seconds
- Zero security breaches

## Compliance Requirements
- GDPR compliance for EU users
- CCPA compliance for California users
- SOC 2 Type II for enterprise
- OAuth 2.0 best practices
- OWASP authentication guidelines