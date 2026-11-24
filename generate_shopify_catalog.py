import openpyxl, csv, re, os

# Load master workbook
wb = openpyxl.load_workbook('Illume_and_Co_Final_Master_and_SKU_Images(1)/Illume_and_Co_Final_Product_Master.xlsx', data_only=True)
sheet = wb['Final master']

# Load CSV image source index
with open('Illume_and_Co_Final_Master_and_SKU_Images(1)/Image_Source_Index.csv', mode='r', encoding='utf-8') as f:
    img_index = {r['code']: r for r in csv.DictReader(f)}

products = []

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text.lower())
    return re.sub(r'[-\s]+', '-', text).strip('-')

SHOPIFY_TAXONOMY_MAP = {
    'Chandeliers': 'Home & Garden > Lighting > Lighting Fixtures > Chandeliers',
    'Pendant Lights': 'Home & Garden > Lighting > Lighting Fixtures > Pendant Light Fixtures',
    'Ceiling Lights': 'Home & Garden > Lighting > Lighting Fixtures > Ceiling Light Fixtures',
    'Wall Lights': 'Home & Garden > Lighting > Lighting Fixtures > Wall Light Fixtures',
    'Table Lamps': 'Home & Garden > Lighting > Lamps > Table Lamps',
    'Fandelier': 'Home & Garden > Household Appliances > Climate Control Appliances > Fans > Ceiling Fans',
    'Fans': 'Home & Garden > Household Appliances > Climate Control Appliances > Fans > Ceiling Fans',
    'Fan': 'Home & Garden > Household Appliances > Climate Control Appliances > Fans > Ceiling Fans',
    'Decorative Lights': 'Home & Garden > Lighting > Lighting Fixtures',
}

for r in range(5, 176):
    code = sheet.cell(r, 15).value # Illume ID, e.g. Il_WL_001
    if not code:
        continue
    sku = sheet.cell(r, 2).value or ''
    name = sheet.cell(r, 3).value or ''
    cat = sheet.cell(r, 5).value or 'Decorative Lights'
    qty = sheet.cell(r, 6).value or 10
    colour = sheet.cell(r, 7).value or 'Brushed Gold / Brass'
    material = sheet.cell(r, 8).value or 'Metal & Optical Crystal'
    cct = sheet.cell(r, 9).value or '3 in 1 Tri-Color Switchable (3000K / 4000K / 6000K)'
    light_source = sheet.cell(r, 10).value or 'Integrated Architectural LED'
    use_case = sheet.cell(r, 11).value or 'Living Salons, Dining Galleries, Foyers'
    purchase_price = sheet.cell(r, 12).value
    suggested_price = sheet.cell(r, 13).value
    hsn = sheet.cell(r, 14).value or '9405'
    stock = sheet.cell(r, 16).value or 'In Stock'
    short_desc = sheet.cell(r, 27).value or ''
    long_desc = sheet.cell(r, 28).value or ''
    
    # Calculate price if suggested price is absent
    if suggested_price is not None and suggested_price != '':
        price = float(suggested_price)
    elif purchase_price is not None and purchase_price != '':
        # Default luxury retail markup ~2.2x - 2.5x
        p = float(purchase_price)
        price = round((p * 2.3) / 100) * 100
        if price < 1500:
            price = 1800
    else:
        price = 12500 # fallback default for high-end statement piece
    
    # Compare at price (MSRP / Catalogue listing price ~ 20-30% higher for perceived value)
    compare_at_price = round((price * 1.25) / 100) * 100
    
    # Image filenames
    img_info = img_index.get(code, {})
    primary_rel = img_info.get('primary', '')
    usecase_rel = img_info.get('usecase', '')
    wide_rel = img_info.get('wide', '')
    
    images = []
    if primary_rel:
        images.append(os.path.basename(primary_rel))
    if usecase_rel:
        images.append(os.path.basename(usecase_rel))
    if wide_rel:
        images.append(os.path.basename(wide_rel))
    
    handle = slugify(f"{name}-{code}")
    
    # Build rich HTML body matching theme specs table
    body_html = f"""<p>{long_desc or short_desc or name}</p>
<div class="product-specs-wrapper" style="margin-top: 20px;">
  <h4 style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 12px; font-weight: 700;">Technical Specifications</h4>
  <table class="specs-table" style="width: 100%; border-collapse: collapse; font-size: 13px;">
    <tbody>
      <tr style="border-bottom: 1px solid #E8E2D8; padding: 8px 0;"><td style="font-weight: 600; padding: 6px 0; width: 40%;">SKU / Model</td><td style="padding: 6px 0;">{code} ({sku or 'Illume & Co'})</td></tr>
      <tr style="border-bottom: 1px solid #E8E2D8; padding: 8px 0;"><td style="font-weight: 600; padding: 6px 0;">Finish & Colour</td><td style="padding: 6px 0;">{colour}</td></tr>
      <tr style="border-bottom: 1px solid #E8E2D8; padding: 8px 0;"><td style="font-weight: 600; padding: 6px 0;">Primary Material</td><td style="padding: 6px 0;">{material}</td></tr>
      <tr style="border-bottom: 1px solid #E8E2D8; padding: 8px 0;"><td style="font-weight: 600; padding: 6px 0;">Color Temperature (CCT)</td><td style="padding: 6px 0;">{cct}</td></tr>
      <tr style="border-bottom: 1px solid #E8E2D8; padding: 8px 0;"><td style="font-weight: 600; padding: 6px 0;">Light Source</td><td style="padding: 6px 0;">{light_source}</td></tr>
      <tr style="border-bottom: 1px solid #E8E2D8; padding: 8px 0;"><td style="font-weight: 600; padding: 6px 0;">Recommended Placement</td><td style="padding: 6px 0;">{use_case}</td></tr>
      <tr style="border-bottom: 1px solid #E8E2D8; padding: 8px 0;"><td style="font-weight: 600; padding: 6px 0;">HSN Code (GST)</td><td style="padding: 6px 0;">{hsn}</td></tr>
      <tr><td style="font-weight: 600; padding: 6px 0;">Warranty Protection</td><td style="padding: 6px 0;">2-Year Complete Fixture Coverage</td></tr>
    </tbody>
  </table>
</div>"""
    
    tags = f"{cat}, {colour}, Illume & Co, 2026 Collection, {code}"
    
    products.append({
        'handle': handle,
        'title': name,
        'body_html': body_html,
        'vendor': 'Illume & Co',
        'category': cat,
        'taxonomy_category': SHOPIFY_TAXONOMY_MAP.get(cat, 'Home & Garden > Lighting > Lighting Fixtures'),
        'tags': tags,
        'published': 'TRUE',
        'sku': code,
        'qty': qty,
        'price': f"{price:.2f}",
        'compare_at_price': f"{compare_at_price:.2f}",
        'images': images,
        'code': code,
        'raw_sku': sku,
        'purchase_price': purchase_price,
        'suggested_price': suggested_price,
        'exact_brochure_model': 'exact model' in img_info.get('status', '')
    })

# Export standard Shopify Product CSV
fieldnames = [
    'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type', 'Tags', 'Published',
    'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value',
    'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty',
    'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price',
    'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Position',
    'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description', 'Status'
]

def write_shopify_csv(filename, prod_list, base_image_url=""):
    """
    Writes a Shopify-compliant product CSV.
    If base_image_url is empty, Image Src is left blank so Shopify imports
    all products with zero errors (no 'Invalid Image URL' / 'Invalid File URL').
    If base_image_url is provided, Image Src contains full https:// URLs.
    """
    with open(filename, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        
        for p in prod_list:
            if base_image_url and p['images']:
                # First row with image URL
                first_img = f"{base_image_url.rstrip('/')}/{p['images'][0]}"
                writer.writerow([
                    p['handle'],
                    p['title'],
                    p['body_html'],
                    p['vendor'],
                    p['taxonomy_category'],
                    p['category'],
                    p['tags'],
                    'TRUE',
                    'Title',
                    'Default Title',
                    '', '', '', '',
                    p['sku'],
                    '2500',
                    'shopify',
                    p['qty'],
                    'deny',
                    'manual',
                    p['price'],
                    p['compare_at_price'],
                    'TRUE',
                    'TRUE',
                    '',
                    first_img,
                    '1',
                    f"{p['title']} - Illume & Co Pune",
                    'FALSE',
                    f"{p['title']} | Illume & Co Pune Luxury Lighting",
                    f"Curated {p['title']} by Illume & Co Pune. Premium architectural and decorative lighting with 100% insured transit across India.",
                    'active'
                ])
                # Additional image rows
                for idx, img in enumerate(p['images'][1:], start=2):
                    writer.writerow([
                        p['handle'], '', '', '', '', '', '', '',
                        '', '', '', '', '', '',
                        '', '', '', '', '', '', '', '', '', '', '',
                        f"{base_image_url.rstrip('/')}/{img}",
                        str(idx),
                        f"{p['title']} Use Case Image {idx}",
                        '', '', '', ''
                    ])
            else:
                # Clean single-row product import (Image Src is empty so Shopify never throws Invalid URL error)
                writer.writerow([
                    p['handle'],
                    p['title'],
                    p['body_html'],
                    p['vendor'],
                    p['taxonomy_category'],
                    p['category'],
                    p['tags'],
                    'TRUE',
                    'Title',
                    'Default Title',
                    '', '', '', '',
                    p['sku'],
                    '2500',
                    'shopify',
                    p['qty'],
                    'deny',
                    'manual',
                    p['price'],
                    p['compare_at_price'],
                    'TRUE',
                    'TRUE',
                    '',
                    '', # Image Src left empty
                    '', # Image Position left empty
                    '', # Image Alt Text left empty
                    'FALSE',
                    f"{p['title']} | Illume & Co Pune Luxury Lighting",
                    f"Curated {p['title']} by Illume & Co Pune. Premium architectural and decorative lighting with 100% insured transit across India.",
                    'active'
                ])

# 1. Generate Clean CSVs (Image Src empty - 100% Guaranteed Error-Free for Shopify CSV Importer)
write_shopify_csv('illume_all_171_products_shopify.csv', products, base_image_url="")

brochure_chandeliers = [p for p in products if p['category'] == 'Chandeliers' and p['exact_brochure_model']]
brochure_pendants = [p for p in products if p['category'] == 'Pendant Lights' and p['exact_brochure_model']]
brochure_wall = [p for p in products if p['category'] == 'Wall Lights' and p['exact_brochure_model']]
brochure_ceiling = [p for p in products if p['category'] == 'Ceiling Lights' and p['exact_brochure_model']]

top_40 = (brochure_chandeliers[:12] + brochure_pendants[:14] + brochure_wall[:10] + brochure_ceiling[:4])[:40]
write_shopify_csv('illume_top_40_flagship_products_shopify.csv', top_40, base_image_url="")

print(f"Generated clean illume_all_171_products_shopify.csv ({len(products)} products)")
print(f"Generated clean illume_top_40_flagship_products_shopify.csv ({len(top_40)} products)")
