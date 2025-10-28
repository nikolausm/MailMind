# OAuth Providers Configuration

## Inhaltsverzeichnis

- [Supported Providers](#supported-providers)
  - [Google OAuth 2.0](#google-oauth-20)
  - [Microsoft Azure AD](#microsoft-azure-ad)
  - [Apple Sign In](#apple-sign-in)
- [Setup Instructions](#setup-instructions)
  - [Google](#google)
  - [Microsoft](#microsoft)
  - [Apple](#apple)
- [Environment Variables](#environment-variables)

## In diesem Dokument

- **[Supported Providers](#supported-providers)**: OAuth-Provider-Konfigurationen
- **[Setup Instructions](#setup-instructions)**: Einrichtungsanleitungen für jeden Provider
- **[Environment Variables](#environment-variables)**: Erforderliche Umgebungsvariablen

## Verwandte Dokumente

- **[Authentifizierung](./AUTHENTICATION.md)**: Übergreifende Authentifizierungs-Anforderungen
- **[Auth-Flows](./AUTH_FLOWS.md)**: Detaillierte Authentifizierungs-Abläufe
- **[Benutzer-Flows](./user-flows.md)**: Benutzerinteraktionen
- **[Entwicklung](./DEVELOPMENT.md)**: Entwicklungsrichtlinien

## Supported Providers

### Google OAuth 2.0
```yaml
provider: google
client_id: ${GOOGLE_CLIENT_ID}
client_secret: ${GOOGLE_CLIENT_SECRET}
redirect_uri: http://localhost:9000/api/auth/callback/google
scopes: [openid, email, profile]
```

### Microsoft Azure AD
```yaml
provider: microsoft
client_id: ${MICROSOFT_CLIENT_ID}
client_secret: ${MICROSOFT_CLIENT_SECRET}
tenant_id: ${MICROSOFT_TENANT_ID}
redirect_uri: http://localhost:9000/api/auth/callback/microsoft
scopes: [openid, email, profile, offline_access]
```

### Apple Sign In
```yaml
provider: apple
client_id: ${APPLE_CLIENT_ID}
team_id: ${APPLE_TEAM_ID}
key_id: ${APPLE_KEY_ID}
private_key: ${APPLE_PRIVATE_KEY}
redirect_uri: http://localhost:9000/api/auth/callback/apple
scopes: [name, email]
```

## Setup Instructions

### Google
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials
3. Add authorized redirect URIs
4. Copy Client ID and Secret

### Microsoft
1. Go to [Azure Portal](https://portal.azure.com/)
2. Register application in Azure AD
3. Configure authentication settings
4. Create client secret

### Apple
1. Enroll in [Apple Developer Program](https://developer.apple.com/)
2. Create Service ID for web authentication
3. Configure web authentication settings
4. Create private key for Sign in with Apple

## Environment Variables
```bash
# Google
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_secret

# Microsoft
MICROSOFT_CLIENT_ID=your_client_id
MICROSOFT_CLIENT_SECRET=your_secret
MICROSOFT_TENANT_ID=your_tenant_id

# Apple
APPLE_CLIENT_ID=your_client_id
APPLE_TEAM_ID=your_team_id
APPLE_KEY_ID=your_key_id
APPLE_PRIVATE_KEY_PATH=/path/to/key.p8
```