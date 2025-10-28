# Dokumentationsstruktur

## Inhaltsverzeichnis

- [📚 Vollständige Dokumentationsübersicht](#-vollständige-dokumentationsübersicht)
  - [Hierarchische Organisation](#hierarchische-organisation)
- [📑 Datei-Verzeichnis](#-datei-verzeichnis)
- [🔗 Navigation JSON](#-navigation-json)
- [📝 Metadaten-Struktur](#-metadaten-struktur)
- [🎯 Verwendung im Code](#-verwendung-im-code)
  - [React-Router Integration](#react-router-integration)
  - [Blazor Integration](#blazor-integration)
- [🔄 Aktualisierungsworkflow](#-aktualisierungsworkflow)

## In diesem Dokument

- **[Vollständige Dokumentationsübersicht](#-vollständige-dokumentationsübersicht)**: Hierarchische Organisation aller Dokumentationsdateien
- **[Datei-Verzeichnis](#-datei-verzeichnis)**: Tabellarische Übersicht aller Dokumentationsdateien mit Status
- **[Navigation JSON](#-navigation-json)**: Strukturiertes Navigationsschema für die Anwendung
- **[Metadaten-Struktur](#-metadaten-struktur)**: Frontmatter-Struktur für Dokumentationsmetadaten
- **[Verwendung im Code](#-verwendung-im-code)**: Integration der Dokumentationsstruktur in React und Blazor
- **[Aktualisierungsworkflow](#-aktualisierungsworkflow)**: Prozess für Hinzufügen und Aktualisieren von Dokumentation

## Verwandte Dokumente

- **[Entwicklung](./DEVELOPMENT.md)**: Entwicklungsrichtlinien und -prozesse
- **[Internationalisierung](./internationalization.md)**: Mehrsprachige Dokumentationsstandards
- **[AI-Agenten](./ai-agents.md)**: KI-unterstützte Dokumentationsgenerierung
- **[Benutzer-Flows](./user-flows.md)**: Dokumentation von Benutzerinteraktionen
- **[Authentifizierung](./AUTHENTICATION.md)**: Auth-bezogene Dokumentationsstruktur

## 📚 Vollständige Dokumentationsübersicht

### Hierarchische Organisation

```
📚 MailMind Dokumentation
│
├── 📖 docs/README.md (Hauptmenü - Diese Datei)
│
├── 🏠 Erste Schritte
│   ├── README.md - Projekt-Übersicht
│   ├── quick-start.md - Schnellstart-Anleitung  
│   ├── installation.md - Installationshandbuch
│   ├── configuration.md - Konfiguration
│   └── user-guide.md - Benutzerhandbuch
│
├── 🏗️ Architektur
│   ├── CLAUDE.md - System-Architektur
│   ├── backend-architecture.md - Backend-Design
│   ├── frontend-architecture.md - Frontend mit i18n
│   ├── frontend-components.md - Komponenten-Bibliothek
│   ├── frontend-state-management.md - State Management
│   └── ui-mockups.md - UI-Designs
│
├── 🤖 KI & RAG-System
│   ├── ai-agents.md - KI-Agenten Dokumentation
│   ├── agent-architecture.md - Agent-Orchestrierung
│   ├── email-pipeline.md - E-Mail-Verarbeitung
│   ├── ai-interaction-rules.md - KI-Regelsystem
│   ├── vector-database.md - Vektor-Speicher
│   └── src/ai/agents/README.md - Agent-Implementierung
│
├── 🔐 Authentifizierung
│   ├── AUTHENTICATION.md - Auth-Übersicht
│   ├── AUTH_FLOWS.md - Auth-Abläufe
│   ├── oauth-providers.md - OAuth-Integration
│   └── user-flows.md - Benutzer-Flows
│
├── 🌍 Internationalisierung
│   └── internationalization.md - i18n-System
│
├── 🔌 API-Dokumentation
│   ├── api/endpoints.md - REST API Referenz
│   ├── api/websocket.md - WebSocket-Kommunikation
│   └── api/errors.md - API-Fehlercodes
│
├── 🚀 Deployment
│   ├── deployment/development.md - Entwicklungsumgebung
│   ├── deployment/docker.md - Docker-Setup
│   └── deployment/production.md - Produktionsumgebung
│
├── 💻 Entwicklung
│   ├── DEVELOPMENT.md - Entwicklerhandbuch
│   ├── DOCUMENTATION_STRUCTURE.md - Diese Datei
│   ├── CLAUDE_CODE_INSTRUCTIONS.md - Claude Code Setup
│   └── CLAUDE_CODE_STATUS.md - Claude Code Status
│
└── 🤝 Claude Agents
    ├── .claude/agents/api-developer.md - API-Entwicklung
    ├── .claude/agents/backend-specialist.md - Backend-Expertise
    ├── .claude/agents/devops-specialist.md - DevOps & Deployment
    ├── .claude/agents/email-processor.md - E-Mail-Verarbeitung
    ├── .claude/agents/frontend-specialist.md - Frontend-Entwicklung
    ├── .claude/agents/product-owner.md - Produktmanagement
    ├── .claude/agents/qa-specialist.md - Qualitätssicherung
    ├── .claude/agents/scrum-master.md - Agile Prozesse
    └── .claude/agents/search-engine.md - Suchfunktionen
```

## 📑 Datei-Verzeichnis

| Datei | Pfad | Beschreibung | Sprache | Status |
|-------|------|--------------|---------|--------|
| **Hauptmenü** | `/docs/README.md` | Zentrale Navigation | DE | ✅ |
| **Projekt-Übersicht** | `/README.md` | Projekt-README | EN | ✅ |
| **System-Architektur** | `/CLAUDE.md` | Technische Übersicht | EN | ✅ |
| **Schnellstart** | `/docs/quick-start.md` | Quick Start Guide | DE | ✅ |
| **Installation** | `/docs/installation.md` | Installationsanleitung | DE | ✅ |
| **Konfiguration** | `/docs/configuration.md` | Konfigurations-Guide | DE | ✅ |
| **Benutzerhandbuch** | `/docs/user-guide.md` | Vollständige Anleitung | DE | ✅ |
| **Backend-Architektur** | `/docs/backend-architecture.md` | Server-Architektur | DE | ✅ |
| **Frontend-Architektur** | `/docs/frontend-architecture.md` | UI-Architektur | EN | ✅ |
| **Frontend-Komponenten** | `/docs/frontend-components.md` | Komponenten-Bibliothek | DE | ✅ |
| **Frontend State Management** | `/docs/frontend-state-management.md` | Zustand-Verwaltung | DE | ✅ |
| **UI-Mockups** | `/docs/ui-mockups.md` | Design-Mockups | DE | ✅ |
| **KI-Agenten** | `/docs/ai-agents.md` | Agent-System | DE | ✅ |
| **Agent-Architektur** | `/docs/agent-architecture.md` | Agent-Design | DE | ✅ |
| **E-Mail-Pipeline** | `/docs/email-pipeline.md` | Verarbeitungs-Pipeline | DE | ✅ |
| **KI-Interaktionsregeln** | `/docs/ai-interaction-rules.md` | Regelsystem | DE | ✅ |
| **Vektor-Datenbank** | `/docs/vector-database.md` | Vector DB Guide | DE | ✅ |
| **Authentifizierung** | `/docs/AUTHENTICATION.md` | Auth-System | DE | ✅ |
| **Auth-Flows** | `/docs/AUTH_FLOWS.md` | Ablauf-Diagramme | DE | ✅ |
| **OAuth-Provider** | `/docs/oauth-providers.md` | OAuth-Setup | DE | ✅ |
| **Benutzer-Flows** | `/docs/user-flows.md` | User Journey | DE | ✅ |
| **Internationalisierung** | `/docs/internationalization.md` | i18n-System | DE | ✅ |
| **API Endpoints** | `/docs/api/endpoints.md` | REST API Referenz | EN | ✅ |
| **WebSocket API** | `/docs/api/websocket.md` | WebSocket-Kommunikation | EN | ✅ |
| **API Fehler** | `/docs/api/errors.md` | API-Fehlercodes | EN | ✅ |
| **Development Setup** | `/docs/deployment/development.md` | Entwicklungsumgebung | EN | ✅ |
| **Docker Deployment** | `/docs/deployment/docker.md` | Container-Setup | EN | ✅ |
| **Production Deployment** | `/docs/deployment/production.md` | Produktionsumgebung | EN | ✅ |
| **Entwicklung** | `/docs/DEVELOPMENT.md` | Dev Guide | EN | ✅ |
| **Dokumentationsstruktur** | `/docs/DOCUMENTATION_STRUCTURE.md` | Diese Datei | DE | ✅ |
| **Claude Code Instructions** | `/CLAUDE_CODE_INSTRUCTIONS.md` | Claude Setup | EN | ✅ |
| **Claude Code Status** | `/CLAUDE_CODE_STATUS.md` | Claude Status | EN | ✅ |
| **Agent Implementation** | `/src/ai/agents/README.md` | Agent Code | EN | ✅ |
| **API Developer** | `/.claude/agents/api-developer.md` | API-Entwicklung | EN | ✅ |
| **Backend Specialist** | `/.claude/agents/backend-specialist.md` | Backend-Expertise | EN | ✅ |
| **DevOps Specialist** | `/.claude/agents/devops-specialist.md` | DevOps & Deploy | EN | ✅ |
| **Email Processor** | `/.claude/agents/email-processor.md` | E-Mail-Verarbeitung | EN | ✅ |
| **Frontend Specialist** | `/.claude/agents/frontend-specialist.md` | Frontend-Entwicklung | EN | ✅ |
| **Product Owner** | `/.claude/agents/product-owner.md` | Produktmanagement | EN | ✅ |
| **QA Specialist** | `/.claude/agents/qa-specialist.md` | Qualitätssicherung | EN | ✅ |
| **Scrum Master** | `/.claude/agents/scrum-master.md` | Agile Prozesse | EN | ✅ |
| **Search Engine** | `/.claude/agents/search-engine.md` | Suchfunktionen | EN | ✅ |

## 🔗 Navigation JSON

```json
{
  "navigation": [
    {
      "id": "home",
      "title": "Dokumentation",
      "path": "/docs/README.md",
      "icon": "📚"
    },
    {
      "id": "getting-started",
      "title": "Erste Schritte",
      "icon": "🏠",
      "children": [
        {
          "id": "overview",
          "title": "Übersicht",
          "path": "/README.md"
        },
        {
          "id": "quick-start",
          "title": "Schnellstart",
          "path": "/docs/quick-start.md"
        },
        {
          "id": "installation",
          "title": "Installation",
          "path": "/docs/installation.md"
        },
        {
          "id": "configuration",
          "title": "Konfiguration",
          "path": "/docs/configuration.md"
        },
        {
          "id": "user-guide",
          "title": "Benutzerhandbuch",
          "path": "/docs/user-guide.md"
        }
      ]
    },
    {
      "id": "architecture",
      "title": "Architektur",
      "icon": "🏗️",
      "children": [
        {
          "id": "system-overview",
          "title": "System-Übersicht",
          "path": "/CLAUDE.md"
        },
        {
          "id": "backend-arch",
          "title": "Backend-Architektur",
          "path": "/docs/backend-architecture.md"
        },
        {
          "id": "frontend-arch",
          "title": "Frontend-Architektur",
          "path": "/docs/frontend-architecture.md"
        },
        {
          "id": "frontend-components",
          "title": "Frontend-Komponenten",
          "path": "/docs/frontend-components.md"
        },
        {
          "id": "frontend-state",
          "title": "Frontend State Management",
          "path": "/docs/frontend-state-management.md"
        },
        {
          "id": "ui-mockups",
          "title": "UI-Mockups",
          "path": "/docs/ui-mockups.md"
        }
      ]
    },
    {
      "id": "ai-system",
      "title": "KI & RAG-System",
      "icon": "🤖",
      "children": [
        {
          "id": "ai-agents",
          "title": "KI-Agenten",
          "path": "/docs/ai-agents.md"
        },
        {
          "id": "agent-architecture",
          "title": "Agent-Architektur",
          "path": "/docs/agent-architecture.md"
        },
        {
          "id": "email-pipeline",
          "title": "E-Mail-Pipeline",
          "path": "/docs/email-pipeline.md"
        },
        {
          "id": "ai-rules",
          "title": "KI-Interaktionsregeln",
          "path": "/docs/ai-interaction-rules.md"
        },
        {
          "id": "vector-db",
          "title": "Vektor-Datenbank",
          "path": "/docs/vector-database.md"
        }
      ]
    },
    {
      "id": "authentication",
      "title": "Authentifizierung",
      "icon": "🔐",
      "children": [
        {
          "id": "auth-overview",
          "title": "Übersicht",
          "path": "/docs/AUTHENTICATION.md"
        },
        {
          "id": "auth-flows",
          "title": "Auth-Abläufe",
          "path": "/docs/AUTH_FLOWS.md"
        },
        {
          "id": "oauth-providers",
          "title": "OAuth-Provider",
          "path": "/docs/oauth-providers.md"
        },
        {
          "id": "user-flows",
          "title": "Benutzer-Flows",
          "path": "/docs/user-flows.md"
        }
      ]
    },
    {
      "id": "i18n",
      "title": "Internationalisierung",
      "icon": "🌍",
      "children": [
        {
          "id": "internationalization",
          "title": "Mehrsprachigkeit",
          "path": "/docs/internationalization.md"
        }
      ]
    },
    {
      "id": "development",
      "title": "Entwicklung",
      "icon": "💻",
      "children": [
        {
          "id": "dev-guide",
          "title": "Entwicklerhandbuch",
          "path": "/docs/DEVELOPMENT.md"
        },
        {
          "id": "doc-structure",
          "title": "Dokumentationsstruktur",
          "path": "/docs/DOCUMENTATION_STRUCTURE.md"
        }
      ]
    }
  ]
}
```

## 📝 Metadaten-Struktur

Jede Dokumentationsdatei sollte mit folgendem Frontmatter beginnen:

```yaml
---
title: "Dokumenttitel"
category: "Kategorie"
order: 1
tags: ["tag1", "tag2"]
lastUpdated: "2024-01-01"
author: "Autor"
language: "de"
---
```

## 🎯 Verwendung im Code

### React-Router Integration

```tsx
// src/frontend/src/routes/DocRoutes.tsx
import { Route, Routes } from 'react-router-dom';
import DocViewer from '../components/DocViewer';
import navigation from '../../../docs/navigation.json';

export const DocRoutes = () => {
  return (
    <Routes>
      <Route path="/docs" element={<DocViewer navigation={navigation} />} />
      <Route path="/docs/*" element={<DocViewer navigation={navigation} />} />
    </Routes>
  );
};
```

### Blazor Integration

```csharp
// src/frontend/Pages/Documentation.razor
@page "/docs/{*path}"
@inject NavigationManager Navigation
@inject HttpClient Http

<div class="documentation-viewer">
    <NavigationMenu Items="@navigationItems" />
    <MarkdownContent Source="@currentDocument" />
</div>

@code {
    [Parameter] public string Path { get; set; }
    private List<NavItem> navigationItems;
    private string currentDocument;

    protected override async Task OnInitializedAsync()
    {
        navigationItems = await LoadNavigation();
        currentDocument = await LoadDocument(Path);
    }
}
```

## 🔄 Aktualisierungsworkflow

1. **Neue Dokumentation hinzufügen**:
   - Datei in `/docs/` erstellen
   - In `/docs/README.md` verlinken
   - In diese Struktur-Datei aufnehmen
   - Navigation JSON aktualisieren

2. **Dokumentation aktualisieren**:
   - Datei bearbeiten
   - `lastUpdated` im Frontmatter ändern
   - Versionierung beachten

3. **Übersetzung hinzufügen**:
   - Sprachsuffix verwenden (z.B. `guide.en.md`)
   - In i18n-System registrieren

---

*Letzte Aktualisierung: Januar 2024*