# MailMind Dokumentation

## 📚 Inhaltsverzeichnis

### In diesem Dokument
- [📚 Inhaltsverzeichnis](#-inhaltsverzeichnis)
- [🔍 Schnellnavigation](#-schnellnavigation)
- [📊 Dokumentationsstatus](#-dokumentationsstatus)
- [🔄 Letzte Aktualisierungen](#-letzte-aktualisierungen)
- [📝 Konventionen](#-konventionen)

### 🏠 Erste Schritte
- [📖 Übersicht](../README.md) - Projekt-Übersicht und Architektur
- [⚡ Schnellstart](quick-start.md) - Schnelle Einrichtung
- [📥 Installation](installation.md) - Detaillierte Installationsanleitung
- [⚙️ Konfiguration](configuration.md) - Systemkonfiguration
- [📘 Benutzerhandbuch](user-guide.md) - Vollständige Bedienungsanleitung

### 🏗️ Architektur
- [🏢 System-Übersicht](../CLAUDE.md) - Technische Architektur
- [🔙 Backend-Architektur](backend-architecture.md) - Server-Architektur
- [🎨 Frontend-Architektur](frontend-architecture.md) - UI-Architektur mit i18n
- [🧩 Frontend-Komponenten](frontend-components.md) - Komponenten-Bibliothek
- [📊 Frontend State Management](frontend-state-management.md) - Zustand-Verwaltung
- [📐 UI-Mockups](ui-mockups.md) - Design-Entwürfe

### 🤖 KI & RAG-System
- [🧠 KI-Agenten](ai-agents.md) - Agent-System Dokumentation
- [🏛️ Agent-Architektur](agent-architecture.md) - Agent-Design und Orchestrierung
- [📧 E-Mail-Pipeline](email-pipeline.md) - E-Mail-Verarbeitungsfluss
- [🎯 KI-Interaktionsregeln](ai-interaction-rules.md) - Regelsystem für KI
- [🗂️ Vektor-Datenbank](vector-database.md) - Embedding-Speicherung
- [📝 Agent Implementation](../src/ai/agents/README.md) - Agent-Implementierung

### 🔐 Authentifizierung
- [🔒 Authentifizierung Übersicht](AUTHENTICATION.md) - Auth-System
- [🔄 Auth-Abläufe](AUTH_FLOWS.md) - Detaillierte Auth-Flows
- [🌐 OAuth-Provider](oauth-providers.md) - OAuth-Integration
- [👤 Benutzer-Flows](user-flows.md) - User Journey

### 🌍 Internationalisierung
- [🗣️ Mehrsprachigkeit](internationalization.md) - i18n-System und Übersetzungen

### 🔌 API-Dokumentation
- [📡 API Endpoints](api/endpoints.md) - REST API Referenz
- [🔗 WebSocket API](api/websocket.md) - WebSocket-Kommunikation
- [⚠️ Fehlerbehandlung](api/errors.md) - API-Fehlercodes

### 🚀 Deployment
- [💻 Development Setup](deployment/development.md) - Entwicklungsumgebung
- [🐳 Docker Deployment](deployment/docker.md) - Container-Setup
- [🏭 Production Deployment](deployment/production.md) - Produktionsumgebung

### 💻 Entwicklung
- [🔧 Entwicklungshandbuch](DEVELOPMENT.md) - Entwickler-Dokumentation
- [📋 Dokumentationsstruktur](DOCUMENTATION_STRUCTURE.md) - Diese Übersicht
- [🤖 Claude Code Setup](../CLAUDE_CODE_INSTRUCTIONS.md) - Claude Code Konfiguration
- [📊 Claude Code Status](../CLAUDE_CODE_STATUS.md) - Claude Code Status

### 🤝 Claude Agents
- [🔌 API Developer](../.claude/agents/api-developer.md) - API-Entwicklung
- [⚙️ Backend Specialist](../.claude/agents/backend-specialist.md) - Backend-Expertise
- [🏗️ DevOps Specialist](../.claude/agents/devops-specialist.md) - DevOps & Deployment
- [📧 Email Processor](../.claude/agents/email-processor.md) - E-Mail-Verarbeitung
- [🎨 Frontend Specialist](../.claude/agents/frontend-specialist.md) - Frontend-Entwicklung
- [📋 Product Owner](../.claude/agents/product-owner.md) - Produktmanagement
- [🧪 QA Specialist](../.claude/agents/qa-specialist.md) - Qualitätssicherung
- [🏃 Scrum Master](../.claude/agents/scrum-master.md) - Agile Prozesse
- [🔍 Search Engine](../.claude/agents/search-engine.md) - Suchfunktionen

## 🔍 Schnellnavigation

### Nach Funktion
- **E-Mail-Management**: [Pipeline](email-pipeline.md) | [KI-Agenten](ai-agents.md) | [Benutzerhandbuch](user-guide.md) | [Email Processor](../.claude/agents/email-processor.md)
- **KI-Features**: [Agent-Architektur](agent-architecture.md) | [Interaktionsregeln](ai-interaction-rules.md) | [Vektor-DB](vector-database.md) | [Agent Impl](../src/ai/agents/README.md)
- **API & Backend**: [Endpoints](api/endpoints.md) | [WebSocket](api/websocket.md) | [Errors](api/errors.md) | [Backend Spec](../.claude/agents/backend-specialist.md)
- **Authentifizierung**: [Übersicht](AUTHENTICATION.md) | [Flows](AUTH_FLOWS.md) | [OAuth](oauth-providers.md) | [User Flows](user-flows.md)
- **Benutzeroberfläche**: [Frontend](frontend-architecture.md) | [Komponenten](frontend-components.md) | [State](frontend-state-management.md) | [Mockups](ui-mockups.md) | [i18n](internationalization.md)
- **Deployment**: [Development](deployment/development.md) | [Docker](deployment/docker.md) | [Production](deployment/production.md) | [DevOps](../.claude/agents/devops-specialist.md)
- **Setup**: [Installation](installation.md) | [Konfiguration](configuration.md) | [Schnellstart](quick-start.md)

### Nach Zielgruppe
- **👤 Endbenutzer**: [Benutzerhandbuch](user-guide.md) | [Schnellstart](quick-start.md)
- **👨‍💻 Entwickler**: [DEVELOPMENT.md](DEVELOPMENT.md) | [Backend](backend-architecture.md) | [Frontend](frontend-architecture.md) | [API](api/endpoints.md) | [Claude Agents](../.claude/agents/api-developer.md)
- **🏗️ Architekten**: [System-Übersicht](../CLAUDE.md) | [Agent-Architektur](agent-architecture.md) | [Claude Setup](../CLAUDE_CODE_INSTRUCTIONS.md)
- **🔒 Security**: [Auth-System](AUTHENTICATION.md) | [OAuth](oauth-providers.md) | [User Flows](user-flows.md)
- **🚀 DevOps**: [Deployment](deployment/production.md) | [Docker](deployment/docker.md) | [DevOps Agent](../.claude/agents/devops-specialist.md)
- **🧪 QA**: [Testing](DEVELOPMENT.md) | [QA Agent](../.claude/agents/qa-specialist.md)
- **📋 Product Management**: [Product Owner](../.claude/agents/product-owner.md) | [Scrum Master](../.claude/agents/scrum-master.md)

## 📊 Dokumentationsstatus

| Kategorie | Vollständigkeit | Sprache | Dateien |
|-----------|----------------|---------|---------|
| Architektur | ✅ 100% | DE/EN | 6 Dateien |
| KI-System | ✅ 100% | DE | 6 Dateien |
| Authentifizierung | ✅ 100% | DE | 4 Dateien |
| API-Dokumentation | ✅ 100% | EN | 3 Dateien |
| Deployment | ✅ 100% | EN | 3 Dateien |
| Claude Agents | ✅ 100% | EN | 9 Dateien |
| Frontend | ✅ 100% | EN/DE | 4 Dateien |
| Benutzerhandbuch | ✅ 100% | DE | 3 Dateien |
| Internationalisierung | ✅ 100% | DE | 1 Datei |
| **Gesamt** | **✅ 100%** | **DE/EN** | **43 MD-Dateien** |

## 🔄 Letzte Aktualisierungen

- **2024-01**: Internationalisierung hinzugefügt
- **2024-01**: Agent-Architektur refaktoriert
- **2024-01**: E-Mail-Pipeline optimiert
- **2024-01**: Benutzerhandbuch vervollständigt

## 📝 Konventionen

- **Sprache**: Primär Deutsch, technische Begriffe in Englisch
- **Diagramme**: ASCII-Art für Kompatibilität
- **Code-Beispiele**: Mit Syntax-Highlighting
- **Links**: Relative Pfade für lokale Navigation

---

*Diese Dokumentation wird kontinuierlich aktualisiert. Bei Fragen oder Verbesserungsvorschlägen erstellen Sie bitte ein Issue im Repository.*