---
name: Obsidian Command
colors:
  surface: '#0f131d'
  surface-dim: '#0f131d'
  surface-bright: '#353944'
  surface-container-lowest: '#0a0e17'
  surface-container-low: '#171c25'
  surface-container: '#1b2029'
  surface-container-high: '#262a34'
  surface-container-highest: '#31353f'
  on-surface: '#dfe2f0'
  on-surface-variant: '#bbc9ce'
  inverse-surface: '#dfe2f0'
  inverse-on-surface: '#2c303b'
  outline: '#869398'
  outline-variant: '#3c494d'
  surface-tint: '#40d7fd'
  primary: '#b8edff'
  on-primary: '#003642'
  primary-container: '#43d9ff'
  on-primary-container: '#005c6f'
  inverse-primary: '#00677d'
  secondary: '#b1c5ff'
  on-secondary: '#002c70'
  secondary-container: '#0262e6'
  on-secondary-container: '#e7ebff'
  tertiary: '#eae0ff'
  on-tertiary: '#390094'
  tertiary-container: '#d0bfff'
  on-tertiary-container: '#5e37be'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#b2ebff'
  primary-fixed-dim: '#40d7fd'
  on-primary-fixed: '#001f27'
  on-primary-fixed-variant: '#004e5e'
  secondary-fixed: '#dae2ff'
  secondary-fixed-dim: '#b1c5ff'
  on-secondary-fixed: '#001946'
  on-secondary-fixed-variant: '#00419e'
  tertiary-fixed: '#e8ddff'
  tertiary-fixed-dim: '#cebdff'
  on-tertiary-fixed: '#21005e'
  on-tertiary-fixed-variant: '#5026b0'
  background: '#0f131d'
  on-background: '#dfe2f0'
  surface-variant: '#31353f'
typography:
  display-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Manrope
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0em
  body-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.005em
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0em
  label-md:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.02em
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-dense: 0.5rem
  margin: 1.5rem
  margin-dense: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
  space-xxl: 2rem
---

## Brand & Style

This design system delivers a high-density, professional command environment tailored for Windows 10 desktop environments. It serves technical operators, researchers, and systems engineers who manage dual-runtime AI configurations (local quantization and remote orchestration).

The visual philosophy synthesizes high-performance desktop utility with an atmospheric midnight backdrop:
- **Atmospheric Restraint:** A deep, near-black space that foregrounds critical code, prompts, and analytical telemetry without high-frequency visual noise.
- **Architectural Layering:** Surface depths reflect computational proximity: darker hulls for underlying processes, illuminated elevated containers for active inference contexts.
- **Controlled Neural Aesthetics:** Precision-etched outlines, directional luminance, and optical glows denote AI status rather than decorative fantasy. No floating HUD elements or particle fields.

## Colors

The system uses a strictly controlled luminance palette engineered specifically for low-light, high-focus productivity:

- **Canvas & Hull Surfaces:**
  - Root Canvas (`#070B14`): Base system layer.
  - Secondary Workspace (`#0B1220`): Toolbars, side rails, and utility panels.
  - Primary Container Surface (`#101A2B`): Standard card layer, data tables, and input groups.
  - Elevated Container Surface (`#162238`): Context menus, command palettes, and floating inspectors.

- **Semantic Role Accents:**
  - **Local Processing / Primary Accent (`#43D9FF`):** Reserved for on-device inference, context streaming, local model telemetry, and active neural nodes.
  - **System Orchestration / Secondary Accent (`#367BFF`):** Controls, navigation states, shell operations, and standard action buttons.
  - **Cloud Runtime / Tertiary Accent (`#9B78FF`):** Remote API connections, third-party provider integrations, and multi-agent consensus flags.

- **System Diagnostics:**
  - **Operational (`#4BE0AC`):** Hardware parity, active sockets, and completed prompts.
  - **Cautionary (`#FFBD62`):** Token context threshold warnings, memory limits, and pending validations.
  - **Critical (`#FF637A`):** Socket timeouts, process termination, and context overflow.

- **Typography & Structural Contrast:**
  - Dominant Text: `#E9F4FF`
  - Secondary Demarcation: `#91A4BC`
  - Subdued / Trace Text: `#64758D`
  - Structural Hairline Border: `#26364D` (used at 1px thickness with low-opacity alpha falloffs).

## Typography

Typography establishes an information-dense desktop layout:

- **Manrope:** Provides structural weight for view titles, panel headers, and computational mode indicators. It balances geometric modernism with functional legibility.
- **Inter:** The default engine for interface interaction, multi-line agent conversation streams, system alerts, and analytical reports.
- **JetBrains Mono:** Handles token telemetry, hardware benchmarks (VRAM/RAM), execution logs, parameter sliders, and prompt injections.

Line heights are tightened specifically for desktop interfaces to ensure dense data presentation while maintaining readability over multi-hour working sessions.

## Layout & Spacing

The layout is built on a rigid 8px rhythmic grid with a 4px secondary sub-grid for internal component alignments:

- **Grid Architecture:** Multi-pane fluid master-detail split. Windows can be split horizontally or vertically into isolated inference panels, inspector channels, and dynamic prompt consoles.
- **Gutter Strategy:** 16px (`1rem`) default separation between high-level architectural regions (navigation panel, stream area, telemetry rail). Sub-panes and tool palettes drop to 8px (`gutter-dense`).
- **Edge Containment:** Window-frame padding conforms to 16px (`1rem`) margins, dynamically expanding to 24px (`1.5rem`) on ultra-wide desktop monitors (>= 2560px).
- **Desktop Scale Factors:** High information density is prioritized: row heights in telemetry grids default to 28px, toolbars lock to 40px, and command inputs remain anchored at 44px.

## Elevation & Depth

Visual hierarchy uses tonal surface layering combined with razor-thin structural borders rather than heavy drop shadows:

- **Baseline Depth (Level 0):** `#070B14` canvas ground, flat, non-elevated.
- **Integrated Trays (Level 1):** `#0B1220` with a 1px continuous border (`#26364D`, 40% opacity).
- **Active Structural Units (Level 2):** `#101A2B` with a 1px top-lit border (`rgba(67, 217, 255, 0.15)` along top edge, `#26364D` along side and bottom edges).
- **Floating Modals & Flyouts (Level 3):** `#162238` elevated by a direct 1px solid `#26364D` border, backed by a soft ambient shadow: `0 12px 32px -4px rgba(2, 6, 12, 0.7)`.
- **Active Inference / Focus Illumination:** Interactive panels or active runtime contexts display an inner accent ring: `box-shadow: inset 0 0 0 1px rgba(67, 217, 255, 0.4)`. Remote cloud processes use `rgba(155, 120, 255, 0.4)`.

## Shapes

The geometric architecture pairs precise curvature with high visual density, meeting desktop ergonomics without feeling clinical or purely rectangular:

- **Primary Application Panes & Dock Containers:** Explicitly constrained to `16px` (spanning `14px` - `18px`).
- **Telemetry Cards, Chat Context Bubbles, Inspector Modules:** Fixed to `14px` (within the `12px` - `16px` range).
- **Command Input Prompts, Parameter Form Fields:** Calibrated to `10px` (within the `10px` - `12px` range).
- **Action Buttons, Segmented Switches, Chip Indicators:** Set to `10px` (within the `9px` - `12px` range).
- **Floating Status Nodes & Micro-Badges:** Fully rounded pills (`9999px`) reserved strictly for machine state tags (e.g., `CUDA: ON`, `LOCAL: 7B`).

## Components

### Buttons & Action Selectors
- **Primary Inference Action:** Background `#367BFF`, text `#E9F4FF`, hover state elevates to bright cyan `#43D9FF` with dark text `#070B14`. Border radius: `10px`.
- **Ghost System Action:** Transparent background, 1px border `#26364D`, text `#91A4BC`. Hover introduces background `#162238` and border `#43D9FF`.
- **Runtime Mode Switcher:** Segmented control container `#0B1220` containing flush `#101A2B` indicator tabs showing active routing (Local vs. Cloud).

### Command Input & Context Entry
- Single-line or auto-expanding multi-line terminal-grade inputs.
- Background: `#101A2B`, border: 1px `#26364D`, text: `#E9F4FF`.
- Focused state replaces the default border with an illuminated `#43D9FF` halo and subtle glow (`0 0 12px rgba(67, 217, 255, 0.2)`).
- Trailing metadata badges display active context budget (e.g., `4,096 / 32,768 tokens`).

### Status Badges & Chips
- Monospaced typography (`JetBrains Mono`, `10px`), height locked to `20px`.
- **Local Engine Active:** Background `rgba(67, 217, 255, 0.1)`, text `#43D9FF`, border `1px solid rgba(67, 217, 255, 0.3)`.
- **Cloud Engine Active:** Background `rgba(155, 120, 255, 0.1)`, text `#9B78FF`, border `1px solid rgba(155, 120, 255, 0.3)`.
- **Warning Alert:** Background `rgba(255, 189, 98, 0.1)`, text `#FFBD62`, border `1px solid rgba(255, 189, 98, 0.3)`.

### Cards & Structured Data Displays
- Standard Card: Surface `#101A2B`, 1px boundary `#26364D`, border-radius `14px`.
- Data tables implement flush border designs with zebra striping between alternating rows: `#101A2B` to `#0B1220`. Active row hovers illuminate with a fine `#367BFF` left-accent indicator.

### Checkboxes, Radios, and Toggles
- Dimension: 16x16px boxes with a 4px corner radius.
- Inactive: Background `#070B14`, border: 1px solid `#26364D`.
- Selected: Background `#367BFF` featuring a crisp white tick (`#E9F4FF`).
- Hardware switch toggles: 32x18px pill enclosure housing a 14px circular slug that shifts from `#64758D` (off) to `#43D9FF` (on).