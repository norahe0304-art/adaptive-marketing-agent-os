# Agency Agents Design System
## 1. Atmosphere & Identity
A quiet operating-room board for strategy sign-off: dense enough for architecture, calm enough for decisions. The signature is layered clarity: each layer states what it owns, why it exists, and what it refuses.
## 2. Color
### Palette
| Role | Token | Light | Dark | Usage |
|------|-------|-------|------|-------|
| Surface/primary | --surface-primary | #F7F4EC | #171A18 | Main document background |
| Surface/secondary | --surface-secondary | #FFFFFF | #20241F | Repeated panels and tables |
| Surface/elevated | --surface-elevated | #EFE8DA | #272B25 | Callouts and decision bands |
| Text/primary | --text-primary | #17211F | #F5F2EA | Headlines and body |
| Text/secondary | --text-secondary | #58645E | #BEC7BF | Explanatory copy |
| Text/tertiary | --text-tertiary | #7C867F | #8F9A93 | Labels and metadata |
| Border/default | --border-default | #D8D0C1 | #3C433D | Structural borders |
| Border/subtle | --border-subtle | #E8E1D5 | #303630 | Soft dividers |
| Accent/primary | --accent-primary | #2F6F4E | #76B58B | Confirmed strategy and links |
| Accent/secondary | --accent-secondary | #B0762E | #D79A4E | Learning and caution |
| Accent/critical | --accent-critical | #9A463D | #D2776D | Risks and must-not-do items |
| Accent/info | --accent-info | #496B7A | #83A9B8 | Workflow and reference mapping |
### Rules
- Use semantic tokens only; do not introduce one-off colors.
- Green means locked strategy, amber means learning, red means risk, blue-gray means workflow.
- No purple-blue AI gradients, no decorative glows, no pure black.
## 3. Typography
### Scale
| Level | Size | Weight | Line Height | Tracking | Usage |
|-------|------|--------|-------------|----------|-------|
| Display | 40px | 760 | 1.08 | 0 | Page title |
| H1 | 32px | 720 | 1.18 | 0 | Major section headers |
| H2 | 24px | 700 | 1.25 | 0 | Subsection headers |
| H3 | 18px | 700 | 1.35 | 0 | Card titles |
| Body/lg | 18px | 450 | 1.65 | 0 | Lead paragraphs |
| Body | 16px | 430 | 1.65 | 0 | Default text |
| Body/sm | 14px | 430 | 1.55 | 0 | Secondary text |
| Caption | 12px | 650 | 1.35 | 0.04em | Labels and tags |
### Font Stack
- Primary: system sans stack with PingFang SC / Microsoft YaHei fallback for Chinese.
- Mono: SFMono-Regular, ui-monospace, Menlo, Consolas, monospace.
### Rules
- No negative letter spacing.
- CJK text uses generous line-height and natural wrapping.
- Body text never below 14px.
## 4. Spacing & Layout
### Base Unit
All spacing derives from 4px.
| Token | Value | Usage |
|-------|-------|-------|
| --space-1 | 4px | Hairline gaps |
| --space-2 | 8px | Inline groups |
| --space-3 | 12px | Compact padding |
| --space-4 | 16px | Standard rhythm |
| --space-5 | 20px | Card padding |
| --space-6 | 24px | Section inner gap |
| --space-8 | 32px | Group gap |
| --space-10 | 40px | Section padding |
| --space-12 | 48px | Major separation |
| --space-16 | 64px | Page rhythm |
### Grid
- Max content width: 1320px.
- Breakpoints: 720px, 980px, 1180px.
- Mobile collapses to one column with no horizontal scroll.
### Rules
- Use CSS grid for stable structures.
- Cards are for repeated items only. Page sections are full-width bands.
- Border radius is capped at 8px.
## 5. Components
### Strategy Band
- **Structure**: full-width section with constrained inner content.
- **Variants**: primary, muted, decision.
- **Spacing**: --space-10 to --space-16.
- **States**: static.
- **Accessibility**: semantic section with heading.
- **Motion**: none.
### Layer Card
- **Structure**: title, short statement, What / Why / Owns / Not rows.
- **Variants**: truth, work, learning.
- **Spacing**: --space-5.
- **States**: hover border emphasis only.
- **Accessibility**: clear heading hierarchy.
- **Motion**: transform-only hover.
### Sign-off Checklist
- **Structure**: native checkbox plus label text.
- **Variants**: approve, defer.
- **Spacing**: --space-4.
- **States**: focus, checked, hover.
- **Accessibility**: native form controls.
- **Motion**: none.
## 6. Motion & Interaction
| Type | Duration | Easing | Usage |
|------|----------|--------|-------|
| Micro | 120ms | ease-out | Hover and focus |
| Standard | 220ms | ease-in-out | Section affordance |
### Rules
- Only animate transform, opacity, border-color, and background-color.
- Respect reduced motion by disabling transitions.
- No continuous motion.
## 7. Depth & Surface
### Strategy
borders-only
| Type | Value | Usage |
|------|-------|-------|
| Default | 1px solid var(--border-default) | Panels and tables |
| Subtle | 1px solid var(--border-subtle) | Internal dividers |
Depth comes from tonal bands and borders, not shadows.
