# UI/UX Mockups & Design System

## 📚 Inhaltsverzeichnis

### In diesem Dokument
- [Design Philosophy](#design-philosophy)
- [Color System](#color-system)
- [Component Library](#component-library)
- [Responsive Breakpoints](#responsive-breakpoints)
- [Interaction States](#interaction-states)
- [Animations & Transitions](#animations--transitions)
- [Accessibility Features](#accessibility-features)
- [AI Visual Indicators](#ai-visual-indicators)
- [Mobile Gestures](#mobile-gestures)
- [Implementation Guidelines](#implementation-guidelines)
- [Next Steps](#next-steps)

### Verwandte Dokumente
- [🎨 Frontend-Architektur](./frontend-architecture.md) - UI-Architektur
- [🧩 Frontend-Komponenten](./frontend-components.md) - Komponenten-Bibliothek
- [📊 Frontend State Management](./frontend-state-management.md) - Zustand-Verwaltung
- [🌍 Internationalisierung](./internationalization.md) - i18n-System und Übersetzungen
- [📘 Benutzerhandbuch](./user-guide.md) - Bedienungsanleitung

## Design Philosophy

### Core Principles
1. **KI-First Design**: Interface designed around AI interactions
2. **Adaptive Layouts**: Dynamic adjustment based on context
3. **Progressive Disclosure**: Show complexity only when needed
4. **Zero Friction**: Minimize clicks for common actions

## Color System

### Light Theme
```css
:root {
  /* Primary */
  --primary-50: #eff6ff;
  --primary-500: #3b82f6;
  --primary-700: #1d4ed8;
  
  /* Neutral */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-900: #111827;
  
  /* Semantic */
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
  --info: #3b82f6;
  
  /* AI Colors */
  --ai-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --ai-accent: #8b5cf6;
}
```

### Dark Theme
```css
:root[data-theme="dark"] {
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --text-primary: #f1f5f9;
  --border: #334155;
}
```

## Component Library

### 1. Smart Email List Item

```ascii
┌─────────────────────────────────────────────────────┐
│ ○ │ ★ │ John Doe                      │ 2 min ago  │
│   │   │ Project Update - Q1 Results   │ AI: High   │
├───┴───┴────────────────────────────────┴────────────┤
│ Hey team, I wanted to share the Q1 results...       │
│                                                      │
│ 📎 report.pdf  📷 2 images                          │
│                                                      │
│ [Smart Reply] [Summarize] [Schedule] [→ More]       │
└─────────────────────────────────────────────────────┘
```

**Features:**
- AI Priority Badge
- Smart Action Buttons
- Attachment Preview
- Read/Unread State
- Star/Flag Options

### 2. AI Assistant Panel

```ascii
┌─────────────────────────────────────┐
│ 🤖 AI Assistant          [_][□][X] │
├─────────────────────────────────────┤
│ Context: Email from John Doe        │
│ ┌───────────────────────────────┐  │
│ │ This email contains:          │  │
│ │ • Q1 financial results        │  │
│ │ • 15% revenue increase        │  │
│ │ • 2 action items for you      │  │
│ └───────────────────────────────┘  │
│                                     │
│ Suggested Actions:                  │
│ ┌───────────────────────────────┐  │
│ │ 📅 Schedule review meeting    │  │
│ │ 📝 Create task for action item│  │
│ │ 💬 Generate response          │  │
│ └───────────────────────────────┘  │
│                                     │
│ ┌───────────────────────────────┐  │
│ │ Ask me anything...            │  │
│ └───────────────────────────────┘  │
│         [Send] [Voice] [Clear]      │
└─────────────────────────────────────┘
```

### 3. Adaptive Dashboard Layout

#### Morning Focus Mode
```ascii
┌──────────────────────────────────────────────────────────┐
│ MailMind  [🔍 Search]  [🔔 3]  [👤 Profile]            │
├────────────┬─────────────────────────────────────────────┤
│            │  Good Morning! Here's what needs attention:  │
│   Quick    │  ┌──────────────────────────────────────┐  │
│   Actions  │  │ 📧 5 Urgent  📅 3 Meetings  ✅ 8 Tasks│  │
│            │  └──────────────────────────────────────┘  │
│  [Compose] │                                              │
│  [Calendar]│  Priority Inbox                             │
│  [Tasks]   │  ┌──────────────────────────────────────┐  │
│  [Archive] │  │ • CEO: Budget approval needed         │  │
│            │  │ • Client: Contract questions          │  │
│   Recent   │  │ • Team: Standup in 30 minutes        │  │
│   Folders  │  └──────────────────────────────────────┘  │
│            │                                              │
│  > Inbox   │  📊 AI Insights                            │
│  > Sent    │  ┌──────────────────────────────────────┐  │
│  > Drafts  │  │ Peak email time: 9-11 AM             │  │
│  > Archive │  │ Response time improved by 23%         │  │
│            │  │ 3 emails need follow-up today        │  │
└────────────┴─────────────────────────────────────────────┘
```

#### Deep Work Mode
```ascii
┌──────────────────────────────────────────────────────────┐
│ 🎯 Focus Mode Active  |  Email: Project Alpha Discussion  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  From: Sarah Chen <sarah@company.com>                    │
│  To: You, Team Alpha                                     │
│  Subject: Re: Project Alpha - Technical Architecture     │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                   │    │
│  │  Hi everyone,                                     │    │
│  │                                                   │    │
│  │  After reviewing the proposed architecture...     │    │
│  │                                                   │    │
│  │  [Full email content with formatting]            │    │
│  │                                                   │    │
│  └─────────────────────────────────────────────────┘    │
│                                                           │
│  AI Analysis:                                            │
│  • Key Decision: Database selection                      │
│  • Action Required: Review by Friday                     │
│  • Sentiment: Positive but concerned about timeline      │
│                                                           │
│  [Reply] [Reply All] [Forward] [Create Task] [Summarize] │
└──────────────────────────────────────────────────────────┘
```

### 4. Smart Compose Interface

```ascii
┌──────────────────────────────────────────────────────────┐
│ New Message                                   [−][□][✕] │
├──────────────────────────────────────────────────────────┤
│ To: [john@example.com] [+ Add]     [CC] [BCC]           │
│ Subject: [Re: Project Update      ]  🤖 AI Assist       │
├──────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────┐     │
│ │ AI Suggestions:                                  │     │
│ │ • Acknowledge receipt of update ✓               │     │
│ │ • Mention the 15% increase ✓                    │     │
│ │ • Propose next steps                            │     │
│ └─────────────────────────────────────────────────┘     │
│                                                           │
│ Hi John,                                                 │
│                                                           │
│ Thanks for sharing the Q1 results. The 15% revenue      │
│ increase is impressive! |                                │
│                                                           │
│ [AI is suggesting: "I'd like to discuss the growth      │
│  strategies that contributed to this success."]          │
│                                                           │
│ Best regards,                                            │
│ [Your name]                                              │
│                                                           │
│ Tone: [Professional ▼]  Length: [Concise ▼]             │
│                                                           │
│ [📎 Attach] [🎨 Format] [📅 Schedule] [Send →]          │
└──────────────────────────────────────────────────────────┘
```

### 5. Search & Filter Interface

```ascii
┌──────────────────────────────────────────────────────────┐
│ 🔍 "emails about project alpha with attachments"         │
├──────────────────────────────────────────────────────────┤
│                                                           │
│ AI Understanding:                                        │
│ ✓ Topic: Project Alpha                                   │
│ ✓ Has: Attachments                                       │
│ ✓ Time: All time                                         │
│                                                           │
│ Refine: [Last Week ▼] [Any Sender ▼] [All Folders ▼]   │
│                                                           │
│ Results (23 emails):                                     │
│ ┌─────────────────────────────────────────────────┐     │
│ │ 95% │ Alpha Architecture Proposal │ 2 days ago  │     │
│ │     │ 📎 architecture.pdf         │             │     │
│ ├─────────────────────────────────────────────────┤     │
│ │ 89% │ Re: Alpha Timeline         │ 5 days ago  │     │
│ │     │ 📎 gantt_chart.xlsx        │             │     │
│ ├─────────────────────────────────────────────────┤     │
│ │ 76% │ Alpha Budget Discussion    │ 1 week ago  │     │
│ │     │ 📎 budget_v2.pdf           │             │     │
│ └─────────────────────────────────────────────────┘     │
│                                                           │
│ Related: [Meeting Notes] [Team Members] [Timeline]       │
└──────────────────────────────────────────────────────────┘
```

## Responsive Breakpoints

### Desktop (1440px+)
- 3-column layout
- Full feature set
- Expanded panels

### Tablet (768px - 1439px)
- 2-column layout
- Collapsible sidebar
- Touch-optimized

### Mobile (< 768px)
- Single column
- Bottom navigation
- Swipe gestures

## Interaction States

### Hover States
```css
.email-item:hover {
  background: var(--gray-50);
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transform: translateX(2px);
}
```

### Loading States
```ascii
┌─────────────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ░░░░░░░░░░░░░░░░░░░        │
│ ░░░░░░░░░░░░░░              │
└─────────────────────────────┘
```

### Empty States
```ascii
┌─────────────────────────────────┐
│                                 │
│         📭                      │
│    No emails found              │
│                                 │
│  Try adjusting your filters     │
│  or search terms                │
│                                 │
│    [Clear Filters]              │
└─────────────────────────────────┘
```

## Animations & Transitions

### Micro-interactions
```css
/* Panel slide */
@keyframes slideIn {
  from { transform: translateX(100%); }
  to { transform: translateX(0); }
}

/* AI thinking */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Success feedback */
@keyframes checkmark {
  0% { stroke-dashoffset: 100; }
  100% { stroke-dashoffset: 0; }
}
```

## Accessibility Features

### Keyboard Navigation
- Tab through all interactive elements
- Arrow keys for list navigation
- Escape to close modals
- Keyboard shortcuts for all actions

### Screen Reader Support
```html
<button aria-label="Archive email" role="button">
  <span class="sr-only">Archive</span>
  <ArchiveIcon aria-hidden="true" />
</button>
```

### Focus Indicators
```css
:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
```

## AI Visual Indicators

### AI Processing
```ascii
⠋ AI is thinking...
⠙ AI is analyzing...
⠹ AI is generating...
⠸ AI is learning...
```

### AI Confidence Levels
```ascii
[████████░░] 80% confident
[██████████] 100% confident
[████░░░░░░] 40% needs review
```

### AI Suggestions Badge
```ascii
┌──────────────┐
│ 💡 3 AI Tips │
└──────────────┘
```

## Mobile Gestures

### Swipe Actions
```ascii
← Swipe left:  Archive
→ Swipe right: Mark as read
↓ Pull down:   Refresh
↑ Swipe up:    Quick actions
```

### Long Press Menu
```ascii
┌─────────────┐
│ Reply       │
│ Forward     │
│ Archive     │
│ Delete      │
│ Mark unread │
│ Add flag    │
└─────────────┘
```

## Implementation Guidelines

### Component Structure
```typescript
// Example: Smart Email Item Component
interface EmailItemProps {
  email: Email
  layout: 'compact' | 'comfortable' | 'expanded'
  aiInsights?: AIInsight[]
  onAction: (action: EmailAction) => void
  isSelected: boolean
  showPreview: boolean
}

const EmailItem: React.FC<EmailItemProps> = ({
  email,
  layout,
  aiInsights,
  onAction,
  isSelected,
  showPreview
}) => {
  // Component implementation
}
```

### State Management Pattern
```typescript
// UI State Store
interface UIStore {
  layout: LayoutConfig
  theme: Theme
  panels: PanelState[]
  filters: FilterState
  
  // Actions
  setLayout: (layout: LayoutConfig) => void
  togglePanel: (panelId: string) => void
  updateFilters: (filters: FilterState) => void
  
  // AI-driven updates
  applyAISuggestion: (suggestion: AISuggestion) => void
  learnFromInteraction: (interaction: UserInteraction) => void
}
```

## Next Steps

1. **Interactive Prototypes**: Figma/Sketch files
2. **Component Development**: React component library
3. **User Testing**: Validate flows with real users
4. **AI Training**: Collect interaction data
5. **Iterative Refinement**: Based on feedback