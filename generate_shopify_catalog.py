import openpyxl, csv, re, os

# Load master workbook
wb = openpyxl.load_workbook('Illume_and_Co_Final_Master_and_SKU_Images(1)/Illume_and_Co_Final_Product_Master.xlsx', data_only=True)
sheet = wb['Final master']

# Load CSV image source index
with open('Illume_and_Co_Final_Master_and_SKU_Images(1)/Image_Source_Index.csv', mode='r', encoding='utf-8') as f:
    img_index = {r['code']: r for r in csv.DictReader(f)}

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

products = []

for r in range(5, 176):
    code = sheet.cell(r, 15).value # Illume ID, e.g. Il_WL_001
    if not code:
        continue
    sku = sheet.cell(r, 2).value
    name = sheet.cell(r, 3).value or ''
    cat = sheet.cell(r, 5).value or 'Decorative Lights'
    qty = sheet.cell(r, 6).value or 10
    colour = sheet.cell(r, 7).value
    material = sheet.cell(r, 8).value
    cct = sheet.cell(r, 9).value
    light_source = sheet.cell(r, 10).value
    use_case = sheet.cell(r, 11).value
    purchase_price = sheet.cell(r, 12).value
    suggested_price = sheet.cell(r, 13).value
    hsn = sheet.cell(r, 14).value or '9405'
    stock = sheet.cell(r, 16).value or 'In Stock'
    
    # Dimensions from Excel
    dim_l = sheet.cell(r, 21).value
    dim_w = sheet.cell(r, 22).value
    dim_h = sheet.cell(r, 23).value
    dim_unit = sheet.cell(r, 24).value or 'in'
    box_wt = sheet.cell(r, 32).value
    
    short_desc = sheet.cell(r, 27).value or ''
    long_desc = sheet.cell(r, 28).value or ''
    
    # Calculate price if suggested price is absent
    if suggested_price is not None and str(suggested_price).strip() != '':
        price = float(suggested_price)
    elif purchase_price is not None and str(purchase_price).strip() != '':
        p = float(purchase_price)
        price = round((p * 2.3) / 100) * 100
        if price < 1500:
            price = 1800
    else:
        price = 12500
    
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
    
    # Build specifications table rows ONLY for fields that have actual data
    specs_rows = []
    
    # SKU / Model
    sku_val = f"{code} ({sku})" if sku else str(code)
    specs_rows.append(f'<tr style="border-bottom: 1px solid #DFD8CC;"><td style="font-weight: 500; padding: 10px 0; width: 42%; color: #8A8175;">SKU / Model</td><td style="padding: 10px 0; font-weight: 600; color: #292929;">{sku_val}</td></tr>')
    
    # Category
    specs_rows.append(f'<tr style="border-bottom: 1px solid #DFD8CC;"><td style="font-weight: 500; padding: 10px 0; width: 42%; color: #8A8175;">Category</td><td style="padding: 10px 0; font-weight: 600; color: #292929;">{cat}</td></tr>')
    
    # Finish & Colour (only if present)
    if colour and str(colour).strip() != '':
        specs_rows.append(f'<tr style="border-bottom: 1px solid #DFD8CC;"><td style="font-weight: 500; padding: 10px 0; width: 42%; color: #8A8175;">Finish &amp; Colour</td><td style="padding: 10px 0; font-weight: 600; color: #292929;">{colour}</td></tr>')
        
    # Primary Material (only if present)
    if material and str(material).strip() != '':
        specs_rows.append(f'<tr style="border-bottom: 1px solid #DFD8CC;"><td style="font-weight: 500; padding: 10px 0; width: 42%; color: #8A8175;">Primary Material</td><td style="padding: 10px 0; font-weight: 600; color: #292929;">{material}</td></tr>')
        
    # Light Source (only if present)
    if light_source and str(light_source).strip() != '':
        specs_rows.append(f'<tr style="border-bottom: 1px solid #DFD8CC;"><td style="font-weight: 500; padding: 10px 0; width: 42%; color: #8A8175;">Light Source</td><td style="padding: 10px 0; font-weight: 600; color: #292929;">{light_source}</td></tr>')
        
    # Color Temperature (CCT) (only if present)
    if cct and str(cct).strip() != '':
        specs_rows.append(f'<tr style="border-bottom: 1px solid #DFD8CC;"><td style="font-weight: 500; padding: 10px 0; width: 42%; color: #8A8175;">Color Temperature (CCT)</td><td style="padding: 10px 0; font-weight: 600; color: #292929;">{cct}</td></tr>')
        
    # Dimensions (only if present)
    dims_parts = []
    if dim_l: dims_parts.append(f"L {dim_l}")
    if dim_w: dims_parts.append(f"W {dim_w}")
    if dim_h: dims_parts.append(f"H {dim_h}")
    if dims_parts:
        dims_str = " × ".join(dims_parts) + f" {dim_unit}"
        specs_rows.append(f'<tr style="border-bottom: 1px solid #DFD8CC;"><td style="font-weight: 500; padding: 10px 0; width: 42%; color: #8A8175;">Fixture Dimensions</td><td style="padding: 10px 0; font-weight: 600; color: #292929;">{dims_str}</td></tr>')
        
    # Recommended Placement (only if present)
    if use_case and str(use_case).strip() != '':
        specs_rows.append(f'<tr style="border-bottom: 1px solid #DFD8CC;"><td style="font-weight: 500; padding: 10px 0; width: 42%; color: #8A8175;">Recommended Placement</td><td style="padding: 10px 0; font-weight: 600; color: #292929;">{use_case}</td></tr>')
        
    # Package Weight (only if present)
    if box_wt and str(box_wt).strip() != '':
        specs_rows.append(f'<tr style="border-bottom: 1px solid #DFD8CC;"><td style="font-weight: 500; padding: 10px 0; width: 42%; color: #8A8175;">Gross Package Weight</td><td style="padding: 10px 0; font-weight: 600; color: #292929;">{box_wt} kg</td></tr>')
        
    # HSN Code
    specs_rows.append(f'<tr style="border-bottom: 1px solid #DFD8CC;"><td style="font-weight: 500; padding: 10px 0; width: 42%; color: #8A8175;">HSN Code (GST)</td><td style="padding: 10px 0; font-weight: 600; color: #292929;">{hsn}</td></tr>')
    
    # Warranty
    specs_rows.append('<tr><td style="font-weight: 500; padding: 10px 0; width: 42%; color: #8A8175;">Warranty Protection</td><td style="padding: 10px 0; font-weight: 600; color: #292929;">2-Year Comprehensive Fixture Coverage</td></tr>')
    
    table_rows_html = "\n      ".join(specs_rows)
    
    # Build clean HTML body
    body_html = f"""<p style="color: #4A443D; font-size: 14.5px; line-height: 1.75; margin-bottom: 20px;">{long_desc or short_desc or name}</p>
<div class="product-specs-wrapper" style="margin-top: 24px;">
  <h4 style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 14px; font-weight: 700; color: #292929;">Technical Specifications</h4>
  <table class="specs-table" style="width: 100%; border-collapse: collapse; font-size: 13px;">
    <tbody>
      {table_rows_html}
    </tbody>
  </table>
</div>"""
    
    # Accurate tags based on authentic Excel data
    tag_list = [cat, 'Illume & Co', '2026 Collection', code]
    if colour and str(colour).strip() != '':
        tag_list.append(str(colour).strip())
    if cct and str(cct).strip() != '':
        cct_lower = str(cct).lower()
        if '3 in 1' in cct_lower or '3iin 1' in cct_lower:
            tag_list.append('3-in-1 CCT')
        elif 'warm white' in cct_lower:
            tag_list.append('Warm White 3000K')
        elif 'natural white' in cct_lower or 'neutral white' in cct_lower:
            tag_list.append('Neutral White 4000K')
            
    # Room and spatial placement tags from Excel Suggested Use Case
    if use_case and str(use_case).strip() != '':
        uc_lower = str(use_case).lower()
        if 'bedroom' in uc_lower:
            tag_list.append('Bedroom')
        if 'dining' in uc_lower:
            tag_list.append('Dining Room')
        if 'living' in uc_lower:
            tag_list.append('Living Room')
        if 'kitchen' in uc_lower:
            tag_list.append('Kitchen Island')
        if 'foyer' in uc_lower or 'passage' in uc_lower or 'entrance' in uc_lower or 'stair' in uc_lower:
            tag_list.append('Staircase & Foyer')
        if 'mirror' in uc_lower or 'dressing' in uc_lower or 'vanity' in uc_lower or 'bath' in uc_lower:
            tag_list.append('Vanity & Bathroom')
            
    tags = ", ".join(tag_list)
    
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
        'raw_sku': sku or '',
        'purchase_price': purchase_price,
        'suggested_price': suggested_price,
        'exact_brochure_model': 'exact model' in img_info.get('status', '')
    })

fieldnames = [
    'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type', 'Tags', 'Published',
    'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value',
    'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty',
    'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price',
    'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Position',
    'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description', 'Status'
]

def write_shopify_csv(filename, prod_list, base_image_url=""):
    with open(filename, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        
        for p in prod_list:
            if base_image_url and p['images']:
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
                for idx, img in enumerate(p['images'][1:], start=2):
                    writer.writerow([
                        p['handle'], '', '', '', '', '', '', '',
                        '', '', '', '', '', '',
                        '', '', '', '', '', '', '', '', '', '', '',
                        f"{base_image_url.rstrip('/')}/{img}",
                        str(idx),
                        f"{p['title']} Ambient Detail {idx}",
                        '', '', '', ''
                    ])
            else:
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
                    '', '', '',
                    'FALSE',
                    f"{p['title']} | Illume & Co Pune Luxury Lighting",
                    f"Curated {p['title']} by Illume & Co Pune. Premium architectural and decorative lighting with 100% insured transit across India.",
                    'active'
                ])

# Base URL for public GitHub image CDN
CDN_BASE = "https://raw.githubusercontent.com/techmitram26/illume_and_co/main/assets"

top_40_codes = {
    'Il_CH_001', 'Il_CH_002', 'Il_CH_005', 'Il_CH_006', 'Il_CH_007', 'Il_CH_008',
    'Il_CH_009', 'Il_CH_010', 'Il_CH_011', 'Il_CH_012', 'Il_CH_013', 'Il_CH_015',
    'Il_PL_001', 'Il_PL_002', 'Il_PL_003', 'Il_PL_004', 'Il_PL_005', 'Il_PL_006',
    'Il_PL_007', 'Il_PL_008', 'Il_PL_009', 'Il_PL_011', 'Il_PL_012', 'Il_PL_013',
    'Il_PL_014', 'Il_PL_015', 'Il_WL_001', 'Il_WL_002', 'Il_WL_003', 'Il_WL_004',
    'Il_WL_005', 'Il_WL_006', 'Il_WL_007', 'Il_WL_008', 'Il_WL_009', 'Il_WL_010',
    'Il_CL_001', 'Il_CL_002', 'Il_CL_003', 'Il_CL_004'
}

remaining_131 = [p for p in products if p['code'] not in top_40_codes]

# Generate CSVs with verified CDN URLs
write_shopify_csv('illume_products_41_to_171_shopify.csv', remaining_131, base_image_url=CDN_BASE)
write_shopify_csv('illume_all_171_products_with_images_shopify.csv', products, base_image_url=CDN_BASE)

print(f"Generated illume_products_41_to_171_shopify.csv ({len(remaining_131)} products)")
print(f"Generated illume_all_171_products_with_images_shopify.csv ({len(products)} products)")
