# Ambika Lights — Premium Luxury Shopify OS 2.0 Theme

A bespoke, ultra-luxury Shopify Online Store 2.0 theme crafted for **Ambika Lights** (Pune, India).

Benchmarked against:
- **`axnine.net`**: Interactive PDP light illumination switch (ON / OFF), CCT Kelvin switcher (3000K, 4000K, 6000K), technical architectural dimensions.
- **`thedecorkart.com`**: Visual mega-menu, high-conversion Indian e-commerce UX, fragile transit guarantee, Pincode delivery checker.
- **`whiteteak.com`**: Comprehensive luxury lighting taxonomy (Decorative, Commercial/Architectural, Designer Fans, Artifacts), "Shop by Space / Room", B2B Architect Trade Program (BoQ submission), Pune showroom booking.

---

## 📁 Theme Architecture

```
ambika_lights/
├── assets/
│   ├── theme.css                  # Master luxury styling system (Tokens, Gold glow, Megamenu, Cart)
│   └── theme.js                   # Zero-dependency JS (On/Off Switch, CCT, Pincode checker, Cart Drawer)
├── config/
│   ├── settings_schema.json       # Shopify Theme Editor customizer schema
│   └── settings_data.json         # Ambika Lights color tokens, contact details & defaults
├── layout/
│   └── theme.liquid               # Master layout with LocalBusiness Schema & Google Fonts
├── locales/
│   └── en.default.json            # English translations & Indian commerce copy
├── sections/
│   ├── announcement-bar.liquid    # Insured fragile transit & Pune showroom banner
│   ├── header.liquid              # Luxury header with 5-column visual mega-menu & thumbnails
│   ├── hero-slideshow.liquid      # Hero with dual CTA ("Explore Decorative" / "Commercial Solutions")
│   ├── shop-by-category.liquid    # Chandeliers, Pendants, Wall Lights, Ceiling & Fans
│   ├── shop-by-room.liquid        # Spatial illumination (Living, Dining, Foyer, Bedroom, Office, etc.)
│   ├── featured-collections.liquid# Statement Chandeliers, Crystal Chandeliers, Modern Pendants
│   ├── bestsellers-grid.liquid    # Signature bestselling lights with INR pricing
│   ├── commercial-b2b.liquid      # Architectural dark showcase (Magnetic tracks, COBs, Profiles)
│   ├── services-grid.liquid       # Consultation, Project orders, Installation, Custom fabrication
│   ├── project-gallery.liquid     # Pune Villa, Fine Dining & Corporate HQ case studies
│   ├── showroom-booking.liquid    # Budhwar Peth, Pune flagship appointment & Google Maps
│   ├── main-product.liquid        # Interactive PDP (Light On/Off, CCT, Pincode, Specs Accordion)
│   ├── main-collection.liquid     # Filterable collection grid with sorting
│   ├── trade-inquiry-form.liquid  # Architect & Interior Designer BoQ submission portal
│   └── footer.liquid              # Brand story, Pune showroom coordinates, Indian payment badges
├── snippets/
│   ├── icon.liquid                # Inline lightweight SVG icons
│   ├── product-card.liquid        # Product card with hover image swap, badge, quick add
│   ├── light-toggle.liquid        # Interactive Light ON / OFF toggle component
│   ├── pincode-checker.liquid     # Indian Pincode checker with Pune local delivery logic
│   ├── specs-table.liquid         # Technical lighting specifications table (Wattage, CCT, CRI, etc.)
│   └── whatsapp-button.liquid     # Floating WhatsApp concierge (+91 74994 65163)
├── templates/
│   ├── index.json                 # Homepage configuration
│   ├── product.json               # Product detail page configuration
│   ├── collection.json            # Collection listing page configuration
│   ├── page.commercial-projects.json # Dedicated B2B & Commercial landing page
│   ├── page.showroom.json         # Dedicated Pune showroom visit page
│   ├── cart.json                  # Shopping bag page
│   └── 404.json                   # Luxury 404 page
└── preview_theme_showcase.html     # Standalone local interactive preview file
```

---

## 🌟 Key Luxury Features Implemented

### 1. Interactive Fixture Light Switch (ON / OFF)
- Modeled after `axnine.net` and `incommonwith.com`.
- Allows customers to preview fixtures in their illuminated state against a deep ambient background or unlit state with a single click.

### 2. CCT Color Temperature Selector
- Choose between:
  - **3000K Warm White / Amber** (ideal for living & dining rooms)
  - **4000K Neutral White** (daylight balance)
  - **6000K Cool White** (crisp architectural clarity)
- Automatically updates form submission properties.

### 3. Indian Pincode Delivery & Showroom Installation Checker
- Built specifically for high-value Indian e-commerce.
- Detects **Pune postal codes (starting with `411`)** to offer same-day showroom demo and technician installation support at Budhwar Peth.
- Confirms insured fragile wooden crate transit for other Indian pincodes.

### 4. Technical Lighting Engineering Specifications
Displays architectural-grade metrics expected by interior designers and discerning buyers:
- Wattage / Consumption
- Color Rendering Index (CRI Ra ≥ 90 / 95)
- Luminous Flux (Lumens)
- Operating Voltage (220V - 240V Indian standard)
- Triac / DALI / 0-10V Dimmer Compatibility
- Dimensions & Suspension Drop Length

### 5. Floating WhatsApp Concierge
- Direct link pre-filled with inquiry context connecting to Ambika Lights' helpline: `+91 74994 65163`.

---

## 🚀 How to Run & Deploy

### A. Local Standalone Preview (No Shopify Account Required)
Simply double click or open [preview_theme_showcase.html](file:///Users/akshay/Documents/GitHub/ambika_lights/preview_theme_showcase.html) in any browser. It demonstrates the complete design system, the header mega-menu, product cards, and the interactive PDP light switch.

### B. Previewing Live on Shopify via Shopify CLI
```bash
# Login to your Shopify partner or development store
shopify auth login

# Start local development server with hot-reload
shopify theme dev --store your-store-name.myshopify.com

# Push theme to Shopify store
shopify theme push --store your-store-name.myshopify.com
```

### C. Theme Quality & Linting
The theme has been tested with Shopify's official theme linter:
```bash
shopify theme check --fail-level error
```
Result: **0 Errors**.
