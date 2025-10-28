# Internationalisierung (i18n) & Lokalisierung (l10n)

## Inhaltsverzeichnis

- [Übersicht](#übersicht)
- [Unterstützte Sprachen](#unterstützte-sprachen)
  - [Tier 1 - Vollständig unterstützt](#tier-1---vollständig-unterstützt)
  - [Tier 2 - Basis-Unterstützung](#tier-2---basis-unterstützung)
  - [Tier 3 - Geplant](#tier-3---geplant)
- [Architektur](#architektur)
  - [Frontend-Lokalisierung](#frontend-lokalisierung)
- [Implementation](#implementation)
  - [1. Spracherkennung](#1-spracherkennung)
  - [2. Übersetzungs-Struktur](#2-übersetzungs-struktur)
  - [3. Blazor-Integration](#3-blazor-integration)
  - [4. Komponenten-Verwendung](#4-komponenten-verwendung)
- [KI-Mehrsprachigkeit](#ki-mehrsprachigkeit)
  - [1. E-Mail-Verarbeitung](#1-e-mail-verarbeitung)
  - [2. Sprachspezifische KI-Modelle](#2-sprachspezifische-ki-modelle)
- [Formatierung & Lokalisierung](#formatierung--lokalisierung)
  - [1. Datum & Zeit](#1-datum--zeit)
  - [2. Zahlen & Währungen](#2-zahlen--währungen)
  - [3. RTL-Unterstützung](#3-rtl-unterstützung)
- [Übersetzungs-Workflow](#übersetzungs-workflow)
  - [1. String-Extraktion](#1-string-extraktion)
  - [2. Übersetzungs-Management](#2-übersetzungs-management)
  - [3. Qualitätssicherung](#3-qualitätssicherung)
- [Benutzer-Features](#benutzer-features)
  - [1. Sprachauswahl](#1-sprachauswahl)
  - [2. Automatische Übersetzung](#2-automatische-übersetzung)
  - [3. Sprach-Präferenzen](#3-sprach-präferenzen)
- [Testing](#testing)
  - [1. i18n Unit Tests](#1-i18n-unit-tests)
  - [2. Visual Regression Tests](#2-visual-regression-tests)
- [Performance-Optimierung](#performance-optimierung)
  - [1. Lazy Loading](#1-lazy-loading)
  - [2. CDN-Strategie](#2-cdn-strategie)
- [Migration & Updates](#migration--updates)
  - [Neue Sprache hinzufügen](#neue-sprache-hinzufügen)
- [Best Practices](#best-practices)

## In diesem Dokument

- **[Übersicht](#übersicht)**: Einführung in Mehrsprachigkeit und globale Benutzerunterstützung
- **[Unterstützte Sprachen](#unterstützte-sprachen)**: Tier-System für Sprachunterstützung (Tier 1-3)
- **[Architektur](#architektur)**: Frontend-Lokalisierungsarchitektur und Systemdesign
- **[Implementation](#implementation)**: Spracherkennung, Übersetzungsstrukturen und Blazor-Integration
- **[KI-Mehrsprachigkeit](#ki-mehrsprachigkeit)**: Mehrsprachige E-Mail-Verarbeitung und sprachspezifische Modelle
- **[Formatierung](#formatierung--lokalisierung)**: Datum/Zeit, Zahlen/Währungen und RTL-Unterstützung
- **[Übersetzungs-Workflow](#übersetzungs-workflow)**: String-Extraktion, Management und Qualitätssicherung
- **[Benutzer-Features](#benutzer-features)**: Sprachauswahl, automatische Übersetzung und Präferenzen
- **[Testing](#testing)**: Unit Tests und Visual Regression Tests für i18n
- **[Performance](#performance-optimierung)**: Lazy Loading und CDN-Strategien
- **[Migration](#migration--updates)**: Neue Sprachen hinzufügen und Updates verwalten

## Verwandte Dokumente

- **[Benutzer-Flows](./user-flows.md)**: Benutzerinteraktionen und mehrsprachige UI-Anpassungen
- **[Authentifizierung](./AUTHENTICATION.md)**: Mehrsprachige Authentifizierungs-Oberflächen
- **[AI-Agenten](./ai-agents.md)**: Mehrsprachige KI-Agenten und Sprachverarbeitung
- **[Email-Pipeline](./email-pipeline.md)**: Mehrsprachige E-Mail-Verarbeitung
- **[Entwicklung](./DEVELOPMENT.md)**: Entwicklungsrichtlinien für i18n
- **[Dokumentations-Struktur](./DOCUMENTATION_STRUCTURE.md)**: Mehrsprachige Dokumentation

## Übersicht

MailMind unterstützt vollständige Mehrsprachigkeit für eine globale Benutzerbasis. Das System erkennt automatisch die Benutzersprache und passt sich dynamisch an.

## Unterstützte Sprachen

### Tier 1 - Vollständig unterstützt
| Sprache | Code | Region | UI | E-Mail-KI | Dokumentation |
|---------|------|--------|----|-----------| --------------|
| Deutsch | de-DE | Deutschland | ✅ | ✅ | ✅ |
| Englisch | en-US | USA | ✅ | ✅ | ✅ |
| Englisch | en-GB | UK | ✅ | ✅ | ✅ |
| Spanisch | es-ES | Spanien | ✅ | ✅ | ✅ |
| Französisch | fr-FR | Frankreich | ✅ | ✅ | ✅ |

### Tier 2 - Basis-Unterstützung
| Sprache | Code | Region | UI | E-Mail-KI | Dokumentation |
|---------|------|--------|----|-----------| --------------|
| Italienisch | it-IT | Italien | ✅ | ✅ | ⏳ |
| Portugiesisch | pt-BR | Brasilien | ✅ | ✅ | ⏳ |
| Niederländisch | nl-NL | Niederlande | ✅ | ✅ | ⏳ |
| Polnisch | pl-PL | Polen | ✅ | ⏳ | ⏳ |
| Japanisch | ja-JP | Japan | ✅ | ✅ | ⏳ |

### Tier 3 - Geplant
- Chinesisch (zh-CN)
- Koreanisch (ko-KR)
- Arabisch (ar-SA)
- Russisch (ru-RU)
- Türkisch (tr-TR)

## Architektur

### Frontend-Lokalisierung

```
┌─────────────────────────────────────────────┐
│            Browser/Client                    │
│                                              │
│  ┌─────────────────────────────────────┐    │
│  │     Language Detection Service       │    │
│  │  - Browser Language                  │    │
│  │  - User Preference                   │    │
│  │  - GeoIP Fallback                   │    │
│  └──────────────┬──────────────────────┘    │
│                 │                            │
│  ┌──────────────▼──────────────────────┐    │
│  │     i18n Resource Manager           │    │
│  │  - Lazy Loading                     │    │
│  │  - Caching                          │    │
│  │  - Fallback Chain                   │    │
│  └──────────────┬──────────────────────┘    │
│                 │                            │
│  ┌──────────────▼──────────────────────┐    │
│  │     UI Component Rendering          │    │
│  │  - Dynamic Text Replacement         │    │
│  │  - RTL Support                      │    │
│  │  - Number/Date Formatting           │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

## Implementation

### 1. Spracherkennung

```typescript
class LanguageDetector {
    detectUserLanguage(): string {
        // Priorität 1: Gespeicherte Benutzereinstellung
        const savedLang = localStorage.getItem('user_language');
        if (savedLang && this.isSupported(savedLang)) {
            return savedLang;
        }
        
        // Priorität 2: Browser-Sprache
        const browserLang = navigator.language;
        if (this.isSupported(browserLang)) {
            return browserLang;
        }
        
        // Priorität 3: Accept-Language Header
        const acceptLang = this.parseAcceptLanguage();
        if (acceptLang && this.isSupported(acceptLang)) {
            return acceptLang;
        }
        
        // Priorität 4: GeoIP-basierte Erkennung
        const geoLang = await this.detectFromGeoIP();
        if (geoLang && this.isSupported(geoLang)) {
            return geoLang;
        }
        
        // Fallback
        return 'en-US';
    }
}
```

### 2. Übersetzungs-Struktur

```json
// locales/de-DE/common.json
{
    "navigation": {
        "inbox": "Posteingang",
        "sent": "Gesendet",
        "drafts": "Entwürfe",
        "archive": "Archiv",
        "trash": "Papierkorb",
        "settings": "Einstellungen"
    },
    "actions": {
        "compose": "Verfassen",
        "reply": "Antworten",
        "forward": "Weiterleiten",
        "delete": "Löschen",
        "archive": "Archivieren",
        "mark_as_read": "Als gelesen markieren",
        "mark_as_unread": "Als ungelesen markieren"
    },
    "messages": {
        "loading": "Lade E-Mails...",
        "no_emails": "Keine E-Mails vorhanden",
        "error_loading": "Fehler beim Laden der E-Mails",
        "search_placeholder": "E-Mails durchsuchen..."
    },
    "ai_features": {
        "categorizing": "Kategorisiere E-Mail...",
        "generating_tags": "Generiere Tags...",
        "creating_summary": "Erstelle Zusammenfassung...",
        "suggesting_response": "Schlage Antwort vor..."
    }
}
```

### 3. Blazor-Integration

```csharp
// Blazor Localization Service
public class LocalizationService
{
    private readonly IJSRuntime _jsRuntime;
    private Dictionary<string, Dictionary<string, string>> _translations;
    private string _currentLanguage;

    public async Task InitializeAsync()
    {
        _currentLanguage = await DetectUserLanguage();
        await LoadTranslations(_currentLanguage);
    }

    public string Translate(string key, params object[] args)
    {
        var keys = key.Split('.');
        var current = _translations[_currentLanguage];
        
        foreach (var k in keys)
        {
            if (current.ContainsKey(k))
            {
                var value = current[k];
                if (args.Length > 0)
                {
                    return string.Format(value, args);
                }
                return value;
            }
        }
        
        // Fallback to key if translation not found
        return key;
    }
    
    public async Task ChangeLanguage(string languageCode)
    {
        _currentLanguage = languageCode;
        await LoadTranslations(languageCode);
        await _jsRuntime.InvokeVoidAsync("localStorage.setItem", 
            "user_language", languageCode);
        StateHasChanged?.Invoke();
    }
}
```

### 4. Komponenten-Verwendung

```razor
@* Blazor Component with i18n *@
@inject LocalizationService L10n

<div class="email-list-header">
    <h2>@L10n.Translate("navigation.inbox")</h2>
    <button @onclick="Compose">
        @L10n.Translate("actions.compose")
    </button>
</div>

@if (IsLoading)
{
    <div class="loading">
        @L10n.Translate("messages.loading")
    </div>
}
else if (!Emails.Any())
{
    <div class="empty-state">
        @L10n.Translate("messages.no_emails")
    </div>
}
```

## KI-Mehrsprachigkeit

### 1. E-Mail-Verarbeitung

```python
class MultilingualEmailProcessor:
    def __init__(self):
        self.language_detector = LanguageDetector()
        self.translators = {
            'de': GermanProcessor(),
            'en': EnglishProcessor(),
            'es': SpanishProcessor(),
            'fr': FrenchProcessor(),
        }
    
    async def process_email(self, email: Email):
        # Erkenne Sprache der E-Mail
        email_language = self.language_detector.detect(email.body)
        
        # Wähle passenden Processor
        processor = self.translators.get(
            email_language[:2], 
            self.translators['en']  # Fallback
        )
        
        # Verarbeite in Original-Sprache
        result = await processor.process(email)
        
        # Übersetze UI-Elemente in Benutzersprache
        if email_language != user.language:
            result.ui_elements = await self.translate_ui(
                result.ui_elements, 
                email_language, 
                user.language
            )
        
        return result
```

### 2. Sprachspezifische KI-Modelle

```python
class GermanProcessor:
    def __init__(self):
        self.classifier = load_model('bert-base-german-cased')
        self.tagger = GermanTagger()
        self.summarizer = GermanSummarizer()
    
    async def classify(self, email):
        # Deutsche Kategorien
        categories = {
            'persönlich': 'personal',
            'arbeit': 'work',
            'werbung': 'advertising',
            'newsletter': 'newsletter',
            'benachrichtigung': 'notification',
            'spam': 'spam'
        }
        
        result = await self.classifier.predict(email)
        return categories.get(result, result)
```

## Formatierung & Lokalisierung

### 1. Datum & Zeit

```typescript
class DateTimeFormatter {
    format(date: Date, locale: string): string {
        const options: Intl.DateTimeFormatOptions = {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        
        return new Intl.DateTimeFormat(locale, options).format(date);
    }
    
    formatRelative(date: Date, locale: string): string {
        const rtf = new Intl.RelativeTimeFormat(locale, {
            numeric: 'auto'
        });
        
        const daysDiff = Math.floor((Date.now() - date.getTime()) / 86400000);
        
        if (daysDiff === 0) return this.getLocalizedToday(locale);
        if (daysDiff === 1) return this.getLocalizedYesterday(locale);
        if (daysDiff < 7) return rtf.format(-daysDiff, 'day');
        
        return this.format(date, locale);
    }
}
```

### 2. Zahlen & Währungen

```typescript
class NumberFormatter {
    formatNumber(value: number, locale: string): string {
        return new Intl.NumberFormat(locale).format(value);
    }
    
    formatCurrency(value: number, locale: string, currency?: string): string {
        const curr = currency || this.getCurrencyForLocale(locale);
        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: curr
        }).format(value);
    }
    
    formatFileSize(bytes: number, locale: string): string {
        const units = this.getLocalizedUnits(locale);
        const index = Math.floor(Math.log(bytes) / Math.log(1024));
        const size = (bytes / Math.pow(1024, index)).toFixed(2);
        
        return `${this.formatNumber(parseFloat(size), locale)} ${units[index]}`;
    }
}
```

### 3. RTL-Unterstützung

```css
/* RTL Support for Arabic, Hebrew, etc. */
[dir="rtl"] {
    .email-list {
        direction: rtl;
        text-align: right;
    }
    
    .email-item {
        flex-direction: row-reverse;
    }
    
    .sidebar {
        right: 0;
        left: auto;
        border-right: none;
        border-left: 1px solid var(--border-color);
    }
    
    .action-buttons {
        flex-direction: row-reverse;
    }
}
```

## Übersetzungs-Workflow

### 1. String-Extraktion

```bash
# Extrahiere alle übersetzbare Strings
npm run i18n:extract

# Generiert:
# - locales/extracted/de-DE.json
# - locales/extracted/en-US.json
# - etc.
```

### 2. Übersetzungs-Management

```yaml
# .github/workflows/translations.yml
translation_workflow:
  triggers:
    - neue_strings_hinzugefügt
    - manuelle_anforderung
  
  schritte:
    1. String-Extraktion
    2. Upload zu Übersetzungsplattform (Crowdin/Lokalise)
    3. Benachrichtigung an Übersetzer
    4. Review-Prozess
    5. Automatischer Pull Request
```

### 3. Qualitätssicherung

```typescript
class TranslationValidator {
    validate(translations: TranslationFile): ValidationResult {
        const errors = [];
        
        // Prüfe auf fehlende Übersetzungen
        for (const key of requiredKeys) {
            if (!translations[key]) {
                errors.push(`Missing: ${key}`);
            }
        }
        
        // Prüfe Platzhalter
        for (const [key, value] of Object.entries(translations)) {
            const placeholders = value.match(/\{(\d+)\}/g);
            const expectedPlaceholders = this.getExpectedPlaceholders(key);
            
            if (!this.placeholdersMatch(placeholders, expectedPlaceholders)) {
                errors.push(`Placeholder mismatch: ${key}`);
            }
        }
        
        // Prüfe Länge (für UI-Elemente)
        for (const [key, value] of Object.entries(translations)) {
            const maxLength = this.getMaxLength(key);
            if (maxLength && value.length > maxLength) {
                errors.push(`Too long: ${key} (${value.length}/${maxLength})`);
            }
        }
        
        return { valid: errors.length === 0, errors };
    }
}
```

## Benutzer-Features

### 1. Sprachauswahl

```razor
@* Language Selector Component *@
<div class="language-selector">
    <select @onchange="OnLanguageChange">
        @foreach (var lang in SupportedLanguages)
        {
            <option value="@lang.Code" selected="@(lang.Code == CurrentLanguage)">
                @lang.NativeName - @lang.EnglishName
            </option>
        }
    </select>
</div>

@code {
    private async Task OnLanguageChange(ChangeEventArgs e)
    {
        await LocalizationService.ChangeLanguage(e.Value.ToString());
        await InvokeAsync(StateHasChanged);
    }
}
```

### 2. Automatische Übersetzung

```python
class AutoTranslator:
    """Übersetzt E-Mails automatisch in Benutzersprache"""
    
    async def translate_email(self, email: Email, target_language: str):
        if email.language == target_language:
            return email  # Keine Übersetzung nötig
        
        # Cache-Check
        cache_key = f"{email.id}:{target_language}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        # Übersetze
        translated = Email(
            subject=await self.translate_text(email.subject, email.language, target_language),
            body=await self.translate_text(email.body, email.language, target_language),
            original_language=email.language,
            is_translated=True
        )
        
        # Cache speichern
        await self.cache.set(cache_key, translated, ttl=86400)
        
        return translated
```

### 3. Sprach-Präferenzen

```typescript
interface LanguagePreferences {
    // UI-Sprache
    interfaceLanguage: string;
    
    // E-Mail-Anzeige
    autoTranslate: boolean;
    showOriginalLanguage: boolean;
    
    // KI-Funktionen
    aiResponseLanguage: string;
    summaryLanguage: string;
    
    // Formatierung
    dateFormat: 'DD/MM/YYYY' | 'MM/DD/YYYY' | 'YYYY-MM-DD';
    timeFormat: '12h' | '24h';
    firstDayOfWeek: 0 | 1 | 6; // Sonntag, Montag, Samstag
    
    // Regionale Einstellungen
    timezone: string;
    currency: string;
}
```

## Testing

### 1. i18n Unit Tests

```typescript
describe('Localization Service', () => {
    it('should detect browser language', () => {
        navigator.language = 'de-DE';
        const detected = service.detectLanguage();
        expect(detected).toBe('de-DE');
    });
    
    it('should fallback to English', () => {
        navigator.language = 'xx-XX';
        const detected = service.detectLanguage();
        expect(detected).toBe('en-US');
    });
    
    it('should translate nested keys', () => {
        const translated = service.translate('navigation.inbox');
        expect(translated).toBe('Posteingang');
    });
    
    it('should format dates correctly', () => {
        const date = new Date('2024-01-15');
        const formatted = formatter.format(date, 'de-DE');
        expect(formatted).toBe('15. Januar 2024');
    });
});
```

### 2. Visual Regression Tests

```typescript
describe('i18n Visual Tests', () => {
    const languages = ['en-US', 'de-DE', 'ar-SA', 'ja-JP'];
    
    languages.forEach(lang => {
        it(`should render correctly in ${lang}`, async () => {
            await page.setLanguage(lang);
            await page.goto('/inbox');
            
            const screenshot = await page.screenshot();
            expect(screenshot).toMatchImageSnapshot({
                customSnapshotIdentifier: `inbox-${lang}`
            });
        });
    });
});
```

## Performance-Optimierung

### 1. Lazy Loading

```typescript
class TranslationLoader {
    private cache = new Map<string, any>();
    
    async loadTranslations(locale: string, namespace: string) {
        const cacheKey = `${locale}:${namespace}`;
        
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }
        
        // Lade nur benötigte Übersetzungen
        const translations = await import(
            /* webpackChunkName: "i18n-[request]" */
            `./locales/${locale}/${namespace}.json`
        );
        
        this.cache.set(cacheKey, translations.default);
        return translations.default;
    }
}
```

### 2. CDN-Strategie

```yaml
CDN-Konfiguration:
  Übersetzungen:
    - Pfad: /static/locales/
    - Cache: 1 Woche
    - Komprimierung: Brotli
    
  Fonts (für nicht-lateinische Schriften):
    - Pfad: /static/fonts/
    - Cache: 1 Jahr
    - Preload: Critical fonts
```

## Migration & Updates

### Neue Sprache hinzufügen

1. **Konfiguration erweitern**:
```typescript
// config/languages.ts
export const SUPPORTED_LANGUAGES = [
    // ... existing
    { code: 'pl-PL', name: 'Polski', rtl: false }
];
```

2. **Übersetzungen erstellen**:
```bash
npm run i18n:add-language pl-PL
```

3. **KI-Support hinzufügen**:
```python
# ai/processors/polish_processor.py
class PolishProcessor(BaseProcessor):
    # Implementation
```

4. **Tests hinzufügen**:
```bash
npm run test:i18n pl-PL
```

## Best Practices

1. **Immer Fallbacks definieren**: Jede Übersetzung sollte einen Fallback haben
2. **Kontextuelle Übersetzungen**: Gleiche Wörter können unterschiedliche Übersetzungen brauchen
3. **Platzhalter verwenden**: Für dynamische Inhalte immer Platzhalter nutzen
4. **Längen beachten**: UI-Texte können in anderen Sprachen länger werden
5. **Kulturelle Anpassung**: Nicht nur übersetzen, sondern kulturell anpassen
6. **Continuous Localization**: Übersetzungen als Teil des CI/CD-Prozesses