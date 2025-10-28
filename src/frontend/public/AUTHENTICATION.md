# Authentication Requirements

## Overview
MailMind requires a flexible, secure authentication system supporting multiple login providers to accommodate different user preferences and organizational requirements.

## Authentication Methods

### 1. OAuth 2.0 Providers

#### Google OAuth
- **Use Case**: Personal Gmail users, Google Workspace accounts
- **Benefits**: Seamless integration with Gmail accounts
- **Scopes Required**:
  - `openid` - User identification
  - `email` - Email address access
  - `profile` - Basic profile information
  - `https://www.googleapis.com/auth/gmail.readonly` - Read Gmail messages
  - `https://www.googleapis.com/auth/gmail.send` - Send emails

#### Microsoft OAuth (Azure AD)
- **Use Case**: Office 365 users, Outlook.com accounts, corporate Microsoft environments
- **Benefits**: Enterprise SSO, Azure AD integration
- **Scopes Required**:
  - `openid` - User identification
  - `email` - Email address
  - `profile` - User profile
  - `Mail.Read` - Read mail
  - `Mail.Send` - Send mail

#### Apple Sign In
- **Use Case**: Apple ecosystem users, privacy-focused users
- **Benefits**: Privacy features (Hide My Email), biometric authentication
- **Requirements**:
  - Apple Developer account
  - Service ID configuration
  - Private key for token validation

### 2. Traditional Authentication

#### Email + Password
- **Use Case**: Users preferring traditional login, custom email servers
- **Requirements**:
  - Strong password policy (min 8 chars, complexity requirements)
  - Password hashing (bcrypt/argon2)
  - Email verification flow
  - Password reset functionality
  - Rate limiting for brute force protection

### 3. Enterprise Authentication (Future)

#### SAML 2.0
- **Use Case**: Enterprise SSO integration
- **Support**: Okta, OneLogin, AD FS

#### LDAP/Active Directory
- **Use Case**: On-premise enterprise deployments
- **Support**: Direct AD integration

## Technical Implementation

### Backend Requirements

#### Authentication Service Structure
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

#### API Endpoints
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