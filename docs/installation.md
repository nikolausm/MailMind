# Installationsanleitung

## 📚 Inhaltsverzeichnis

### In diesem Dokument
- [Voraussetzungen](#voraussetzungen)
- [Schnellinstallation](#schnellinstallation)
- [Docker-Installation (Alternative)](#docker-installation-alternative)
- [Verifikation](#verifikation)
- [Fehlerbehebung](#fehlerbehebung)
- [Nächste Schritte](#nächste-schritte)

### Verwandte Dokumente
- [⚡ Schnellstart](./quick-start.md) - Schnelle Einrichtung
- [⚙️ Konfiguration](./configuration.md) - Systemkonfiguration
- [🔧 Development Setup](./DEVELOPMENT.md) - Entwicklungsumgebung
- [🐳 Docker Deployment](./deployment/docker.md) - Container-Setup
- [📖 Hauptdokumentation](./README.md) - Übersicht aller Dokumente

## Voraussetzungen

Bevor Sie MailMind installieren, stellen Sie sicher, dass Folgendes installiert ist:

- **Node.js** (v18 oder höher)
- **Python** (v3.11 oder höher)
- **npm** oder **yarn** Paketmanager
- **pip** Python-Paketmanager

## Schnellinstallation

### 1. Repository klonen

```bash
git clone https://github.com/yourusername/mailmind.git
cd mailmind
```

### 2. Backend-Abhängigkeiten installieren

```bash
# Virtuelle Umgebung erstellen
python -m venv venv

# Virtuelle Umgebung aktivieren
# Auf macOS/Linux:
source venv/bin/activate
# Auf Windows:
# venv\Scripts\activate

# Python-Abhängigkeiten installieren
pip install -r requirements.txt
```

### 3. Frontend-Abhängigkeiten installieren

```bash
cd src/frontend
npm install
# oder
yarn install
```

### 4. Umgebungskonfiguration

Erstellen Sie eine `.env`-Datei im Wurzelverzeichnis:

```env
# API-Schlüssel
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Vektor-Datenbank
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment

# Datenbank
DATABASE_URL=postgresql://user:password@localhost/mailmind

# E-Mail-Server (für Tests)
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 5. Datenbank-Setup

```bash
# Datenbankmigrationen ausführen
python scripts/setup_database.py
```

### 6. Anwendung starten

#### Entwicklungsmodus

Starten Sie beide Backend- und Frontend-Server:

```bash
# Vom Wurzelverzeichnis aus
npm run dev
```

Oder starten Sie sie separat:

```bash
# Backend (vom Wurzelverzeichnis)
npm run dev:backend

# Frontend (in einem anderen Terminal)
npm run dev:frontend
```

#### Produktionsmodus

```bash
# Frontend erstellen
cd src/frontend
npm run build

# Produktionsserver starten
npm run start:prod
```

## Docker-Installation (Alternative)

### Mit Docker Compose

```bash
# Alle Services erstellen und starten
docker-compose up --build

# Im Hintergrund ausführen
docker-compose up -d
```

### Manueller Docker-Build

```bash
# Backend erstellen
docker build -t mailmind-backend -f docker/backend.Dockerfile .

# Frontend erstellen
docker build -t mailmind-frontend -f docker/frontend.Dockerfile .

# Container ausführen
docker run -p 9000:9000 mailmind-backend
docker run -p 3000:3000 mailmind-frontend
```

## Verifikation

Nach der Installation überprüfen Sie, ob alles funktioniert:

1. **Backend-API**: Navigieren Sie zu http://localhost:9000/docs
2. **Frontend**: Navigieren Sie zu http://localhost:3000
3. **Gesundheitsprüfung**: http://localhost:9000/health

## Fehlerbehebung

### Häufige Probleme

#### Port bereits in Verwendung
```bash
# Ports in package.json ändern oder Umgebungsvariablen verwenden
PORT=3001 npm run dev:frontend
```

#### Probleme mit Python-Abhängigkeiten
```bash
# pip aktualisieren
pip install --upgrade pip

# Cache löschen und neu installieren
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

#### Probleme mit Node-Modulen
```bash
# node_modules löschen und neu installieren
rm -rf node_modules package-lock.json
npm install
```

## Nächste Schritte

- [Schnellstart-Anleitung](./quick-start.md)
- [Konfigurationsanleitung](./configuration.md)
- [Entwicklungssetup](./DEVELOPMENT.md)