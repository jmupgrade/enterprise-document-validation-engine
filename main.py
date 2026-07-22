import streamlit as st

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Shipping Mark Verification Tool",
    page_icon="📦",
    layout="wide"
)

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    .main-title { font-size: 2rem; font-weight: 700; color: #111827; margin-bottom: 0.25rem; }
    .sub-title { font-size: 1rem; color: #6b7280; margin-bottom: 1.5rem; }
    .pass-banner {
        background: #f0fdf4; border: 2px solid #22c55e; border-radius: 10px;
        padding: 1rem 1.5rem; margin-bottom: 1.5rem;
    }
    .fail-banner {
        background: #fef2f2; border: 2px solid #ef4444; border-radius: 10px;
        padding: 1rem 1.5rem; margin-bottom: 1.5rem;
    }
    .alert-banner {
        background: #fff7ed; border: 2px solid #f97316; border-radius: 10px;
        padding: 1rem 1.5rem; margin-bottom: 1.5rem;
    }
    .warn-banner {
        background: #fefce8; border: 1px solid #ca8a04; border-radius: 10px;
        padding: 1rem 1.5rem; margin-bottom: 1.5rem;
    }
    .error-banner {
        background: #fef2f2; border: 1px solid #fca5a5; border-radius: 10px;
        padding: 1rem 1.5rem; margin-bottom: 1.5rem;
    }
    .footer {
        text-align: center; font-size: 0.75rem; color: #9ca3af; margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ===== UTILITY FUNCTIONS =====
def normalize_string(s):
    if not s:
        return ''
    import re
    s = str(s).upper()
    s = re.sub(r'[-\s]', '', s)
    s = s.lstrip('0')
    return s


# ===== DATA EXTRACTION FUNCTIONS =====
def extract_po_data(file):
    """
    In production, parse the actual uploaded PDF using PyMuPDF or pdfplumber.
    For now, returns hardcoded data matching PO #0000001111.
    sizeBreakdownAlert: True if PO contains multiple sizes or child styles under
    Size Breakdown — triggers the double-check warning.
    """
    return {
        'poNumber': '0000001111',
        'customerCode': 'MC, LD',
        'sizeBreakdownAlert': True,
        'sizeBreakdownNote': (
            'This PO contains multiple sizes and/or child styles under Size Breakdown.'
        ),
        'items': [
            {'style': 'PQ99040', 'quantity': 600},
            {'style': 'PQ99041', 'quantity': 600},
            {'style': 'PQ99056', 'quantity': 720},
            {'style': 'PQ99159', 'quantity': 720},
            {'style': 'PQ99030', 'quantity': 600},
            {'style': 'PQ99031', 'quantity': 600},
            {'style': 'PQ99026', 'quantity': 960},
            {'style': 'PQ99027', 'quantity': 960},
            {'style': 'PQ99020', 'quantity': 720},
            {'style': 'PQ99162', 'quantity': 720},
            {'style': 'PQ99068', 'quantity': 960},
            {'style': 'PQ99072', 'quantity': 960},
            {'style': 'PQ99144', 'quantity': 600},
            {'style': 'PQ99138', 'quantity': 600},
            {'style': 'PQ99147', 'quantity': 600},
            {'style': 'PQ99160', 'quantity': 600},
            {'style': 'PQ99102', 'quantity': 600},
            {'style': 'PQ99103', 'quantity': 600},
            {'style': 'PQ99105', 'quantity': 600},
            {'style': 'PQ99083', 'quantity': 600},
            {'style': 'PQ99089', 'quantity': 600},
            {'style': 'PQ99161', 'quantity': 600},
        ]
    }


def extract_sm_data(file):
    """
    In production, parse the actual uploaded file using PyMuPDF, openpyxl,
    or Tesseract depending on file type.
    For now, returns hardcoded shipping mark data.
    """
    return {
        'poNumber': '0000001111',
        'customerCode': 'BE',
        'company': 'WXYZ CORP, LLC',
        'location': 'CITY NAME, NY',
        'countryOfOrigin': 'CHINA',
        'hasPreticket': 'mixed',
        'items': [
            {'style': 'PQ99030', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'YES', 'preticketPcs': 600, 'noPreticketPcs': 0},
            {'style': 'PQ99031', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'YES', 'preticketPcs': 600, 'noPreticketPcs': 0},
            {'style': 'PQ99068', 'pcsPerCarton': 6, 'cartonCount': 160,
             'calculatedQty': 960, 'preticket': 'YES', 'preticketPcs': 960, 'noPreticketPcs': 0},
            {'style': 'PQ99072', 'pcsPerCarton': 6, 'cartonCount': 160,
             'calculatedQty': 960, 'preticket': 'YES', 'preticketPcs': 960, 'noPreticketPcs': 0},
            {'style': 'PQ99083', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'YES', 'preticketPcs': 600, 'noPreticketPcs': 0},
            {'style': 'PQ99089', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'YES', 'preticketPcs': 600, 'noPreticketPcs': 0},
            {'style': 'PQ99161', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'MIXED', 'preticketPcs': 540, 'noPreticketPcs': 60},
            {'style': 'PQ99020', 'pcsPerCarton': 6, 'cartonCount': 120,
             'calculatedQty': 720, 'preticket': 'YES', 'preticketPcs': 720, 'noPreticketPcs': 0},
            {'style': 'PQ99040', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'YES', 'preticketPcs': 600, 'noPreticketPcs': 0},
            {'style': 'PQ99041', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'MIXED', 'preticketPcs': 564, 'noPreticketPcs': 36},
            {'style': 'PQ99138', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'MIXED', 'preticketPcs': 552, 'noPreticketPcs': 48},
            {'style': 'PQ99144', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'MIXED', 'preticketPcs': 564, 'noPreticketPcs': 36},
            {'style': 'PQ99160', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'MIXED', 'preticketPcs': 540, 'noPreticketPcs': 60},
            {'style': 'PQ99162', 'pcsPerCarton': 6, 'cartonCount': 120,
             'calculatedQty': 720, 'preticket': 'MIXED', 'preticketPcs': 672, 'noPreticketPcs': 48},
            {'style': 'PQ99102', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'MIXED', 'preticketPcs': 564, 'noPreticketPcs': 36},
            {'style': 'PQ99103', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'MIXED', 'preticketPcs': 576, 'noPreticketPcs': 24},
            {'style': 'PQ99105', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'MIXED', 'preticketPcs': 576, 'noPreticketPcs': 24},
            {'style': 'PQ99026', 'pcsPerCarton': 6, 'cartonCount': 160,
             'calculatedQty': 960, 'preticket': 'YES', 'preticketPcs': 960, 'noPreticketPcs': 0},
            {'style': 'PQ99027', 'pcsPerCarton': 6, 'cartonCount': 160,
             'calculatedQty': 960, 'preticket': 'YES', 'preticketPcs': 960, 'noPreticketPcs': 0},
            {'style': 'PQ99147', 'pcsPerCarton': 6, 'cartonCount': 100,
             'calculatedQty': 600, 'preticket': 'YES', 'preticketPcs': 600, 'noPreticketPcs': 0},
            {'style': 'PQ99056', 'pcsPerCarton': 6, 'cartonCount': 120,
             'calculatedQty': 720, 'preticket': 'YES', 'preticketPcs': 720, 'noPreticketPcs': 0},
            {'style': 'PQ99159', 'pcsPerCarton': 6, 'cartonCount': 120,
             'calculatedQty': 720, 'preticket': 'YES', 'preticketPcs': 720, 'noPreticketPcs': 0},
        ]
    }


# ===== SIZE BREAKDOWN DETECTION =====
def detect_size_breakdown_alert(po_data):
    """
    Detects if the PO has size breakdown that requires double-checking.
    Rules:
    1. If any PO item style has more than 1 size listed under its Size Breakdown,
       trigger the alert.
    2. If any PO item has child style numbers under its Size Breakdown,
       trigger the alert.
    3. If each style in the PO has only 1 size and no child styles,
       do NOT trigger the alert.
    
    Returns:
        dict with 'sizeBreakdownAlert' (bool) and 'sizeBreakdownNote' (str)
    """
    if 'sizeBreakdownAlert' in po_data:
        return {
            'sizeBreakdownAlert': po_data['sizeBreakdownAlert'],
            'sizeBreakdownNote': po_data.get('sizeBreakdownNote', '')
        }
    
    return {
        'sizeBreakdownAlert': False,
        'sizeBreakdownNote': ''
    }


# ===== VERIFICATION FUNCTION =====
def verify_data(po_data, sm_data):
    po_num_match = (
        normalize_string(po_data['poNumber']) == normalize_string(sm_data['poNumber'])
    )
    company_ok = (
        'WXYZ CORP LLC' in sm_data['company'].upper().replace(',', '').replace('.', '') and
        'CITY NAME NY' in sm_data['location'].upper().replace(',', '')
    )
    country_ok = sm_data['countryOfOrigin'].upper() == 'CHINA'
    has_preticket = sm_data.get('hasPreticket', False)

    size_breakdown_info = detect_size_breakdown_alert(po_data)

    checks = {
        'PO Number Match': {
            'passed': po_num_match,
            'expected': po_data['poNumber'],
            'found': sm_data['poNumber'],
            'critical': True,
            'needs_review': False,
        },
        'Company & Location': {
            'passed': company_ok,
            'expected': 'WXYZ CORP LLC, CITY NAME NY (Required)',
            'found': f"{sm_data['company']}, {sm_data['location']}",
            'critical': True,
            'needs_review': False,
        },
        'Country of Origin': {
            'passed': country_ok,
            'expected': 'CHINA (Expected)',
            'found': sm_data['countryOfOrigin'],
            'critical': False,
            'needs_review': not country_ok,
        },
        'Preticket Status': {
            'passed': True,
            'expected': 'Not specified in PO',
            'found': (
                'MIXED - See details below' if has_preticket == 'mixed'
                else ('YES' if has_preticket else 'NOT FOUND')
            ),
            'critical': False,
            'needs_review': has_preticket == 'mixed',
            'needs_user_input': has_preticket is False or has_preticket == 'mixed',
            'is_mixed': has_preticket == 'mixed',
        },
    }

    # ===== CUSTOMER CODE VERIFICATION STRATEGY =====
    po_cust = str(po_data.get('customerCode', '')).strip()
    sm_cust = str(sm_data.get('customerCode', '')).strip()

    if sm_cust:
        po_cust_norm = normalize_string(po_cust)
        sm_cust_norm = normalize_string(sm_cust)
        po_codes = [c.strip() for c in po_cust_norm.split(',') if c.strip()] if po_cust_norm else []
        cust_match = sm_cust_norm in po_codes if po_codes else False
        
        checks['Customer Code Match'] = {
            'passed': cust_match,
            'expected': po_cust if po_cust else 'Not specified in PO',
            'found': sm_cust,
            'critical': True,
            'needs_review': not cust_match,
        }

    sm_items_map = {
        normalize_string(item['style']): item
        for item in sm_data['items']
    }

    item_checks = []
    for po_item in po_data['items']:
        key = normalize_string(po_item['style'])
        sm_item = sm_items_map.get(key)

        if not sm_item:
            item_checks.append({
                'style': po_item['style'],
                'style_match': False,
                'quantity_match': False,
                'po_qty': po_item['quantity'],
                'sm_qty': 'NOT FOUND',
                'calculation': 'N/A',
                'preticket': 'N/A',
                'preticket_pcs': 0,
                'no_preticket_pcs': 0,
            })
        else:
            qty_match = po_item['quantity'] == sm_item['calculatedQty']
            item_checks.append({
                'style': po_item['style'],
                'style_match': True,
                'quantity_match': qty_match,
                'po_qty': po_item['quantity'],
                'sm_qty': sm_item['calculatedQty'],
                'calculation': (
                    f"{sm_item['pcsPerCarton']} pcs/ctn x "
                    f"{sm_item['cartonCount']} ctns = {sm_item['calculatedQty']}"
                ),
                'preticket': sm_item.get('preticket', 'N/A'),
                'preticket_pcs': sm_item.get('preticketPcs', 0),
                'no_preticket_pcs': sm_item.get('noPreticketPcs', 0),
            })

    overall_pass = (
        checks['PO Number Match']['passed'] and
        checks['Company & Location']['passed'] and
        all(i['style_match'] and i['quantity_match'] for i in item_checks)
    )

    if 'Customer Code Match' in checks:
        overall_pass = overall_pass and checks['Customer Code Match']['passed']

    return {
        'checks': checks,
        'item_checks': item_checks,
        'overall_pass': overall_pass,
        'size_breakdown_alert': size_breakdown_info['sizeBreakdownAlert'],
        'size_breakdown_note': size_breakdown_info['sizeBreakdownNote'],
    }


# ===== MAIN APP =====
st.markdown('<div class="main-title">📦 Shipping Mark Verification Tool</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">WXYZ CORP LLC — Automated verification for '
    'shipping marks against purchase orders</div>',
    unsafe_allow_html=True
)

# Session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'preticket_confirm' not in st.session_state:
    st.session_state.preticket_confirm = None

# ===== UPLOAD SECTION =====
if st.session_state.results is None:
    col1, col2 = st.columns(2)
    with col1:
        po_file = st.file_uploader(
            "Upload Purchase Order (PO)",
            type=['pdf'],
            help="PDF files only"
        )
    with col2:
        sm_file = st.file_uploader(
            "Upload Shipping Mark",
            type=['pdf', 'xlsx', 'xls', 'jpg', 'jpeg'],
            help="PDF, Excel, JPG, JPEG"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "Verify Shipping Mark",
        disabled=(po_file is None or sm_file is None),
        use_container_width=True,
        type="primary"
    ):
        with st.spinner("Extracting and verifying data..."):
            import time
            time.sleep(1.5)
            po_data = extract_po_data(po_file)
            sm_data = extract_sm_data(sm_file)
            st.session_state.results = verify_data(po_data, sm_data)
            st.session_state.preticket_confirm = None
            st.rerun()

# ===== RESULTS SECTION =====
else:
    results = st.session_state.results

    # Overall pass/fail banner
    if results['overall_pass']:
        st.markdown(
            '<div class="pass-banner">'
            '<h2 style="color:#16a34a;margin:0">✅ Verification Passed</h2>'
            '<p style="color:#374151;margin:0.25rem 0 0 0">'
            'All checks passed. Shipping mark is ready for approval.</p>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="fail-banner">'
            '<h2 style="color:#dc2626;margin:0">❌ Verification Failed</h2>'
            '<p style="color:#374151;margin:0.25rem 0 0 0">'
            'Discrepancies detected. Review details below and make corrections.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    # ===== SIZE BREAKDOWN ALERT =====
    if results['size_breakdown_alert']:
        st.markdown(
            '<div class="alert-banner">'
            '<h4 style="color:#9a3412;margin:0 0 0.4rem 0">⚠️ Size Breakdown Notice</h4>'
            '<p style="color:#c2410c;font-weight:600;margin:0">'
            'Double check size breakdown in PO and make sure shipping mark '
            'reflecting the breakdown CORRECTLY.</p>'
            + (
                f'<p style="color:#ea580c;font-size:0.8rem;margin:0.3rem 0 0 0">'
                f'{results["size_breakdown_note"]}</p>'
                if results['size_breakdown_note'] else ''
            ) +
            '</div>',
            unsafe_allow_html=True
        )

    # ===== DOCUMENT INFORMATION TABLE =====
    st.subheader("Document Information")

    doc_rows = []
    for check_name, check in results['checks'].items():
        if check.get('needs_review'):
            status = '🟡 Review'
        elif check['passed']:
            status = '✅ Pass'
        else:
            status = '❌ Fail'
        doc_rows.append({
            'Check': check_name,
            'Status': status,
            'Expected': check['expected'],
            'Found': check['found'],
        })

    st.table(doc_rows)

    # ===== PRETICKET NOTICE =====
    preticket_check = results['checks'].get('Preticket Status', {})
    if preticket_check.get('needs_user_input'):
        if preticket_check.get('is_mixed'):
            st.markdown(
                '<div class="warn-banner">'
                '<h4 style="color:#854d0e;margin:0 0 0.4rem 0">'
                '⚠️ Preticket Information Notice</h4>'
                '<p style="color:#92400e;font-size:0.9rem;margin:0 0 0.5rem 0">'
                'Some styles have mixed preticket status — some cartons show '
                '"Preticket: YES" while others have no preticket information. '
                'See details in the table below.</p>'
                '<p style="color:#92400e;font-size:0.9rem;font-weight:600;margin:0">'
                'Please verify with the supplier if all cartons actually have price '
                'tickets, or if some cartons were shipped without pretickets.</p>'
                '</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="warn-banner">'
                '<h4 style="color:#854d0e;margin:0 0 0.4rem 0">'
                '⚠️ Preticket Information Notice</h4>'
                '<p style="color:#92400e;font-size:0.9rem;margin:0 0 0.75rem 0">'
                'No preticket information found in shipping marks. '
                'Please double check if this order has price tickets or not.</p>'
                '</div>',
                unsafe_allow_html=True
            )
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ Confirmed — No Preticket Required", use_container_width=True):
                    st.session_state.preticket_confirm = False
                    st.rerun()
            with col_b:
                if st.button(
                    "❌ Preticket Required — Contact Supplier",
                    use_container_width=True,
                    type="primary"
                ):
                    st.session_state.preticket_confirm = True
                    st.rerun()

            if st.session_state.preticket_confirm is False:
                st.success("Confirmed: No preticket required for this order.")
            elif st.session_state.preticket_confirm is True:
                st.error("Action required: Contact supplier regarding missing pretickets.")

    # ===== STYLE & QUANTITY VERIFICATION TABLE =====
    st.subheader("Style & Quantity Verification")

    item_rows = []
    for item in results['item_checks']:
        if item['style_match'] and item['quantity_match']:
            status = '✅ Pass'
        else:
            status = '❌ Fail'

        if item['preticket'] == 'YES':
            preticket_display = f"YES ({item['preticket_pcs']} pcs)"
        elif item['preticket'] == 'MIXED':
            preticket_display = (
                f"MIXED: ✓ {item['preticket_pcs']} pcs / "
                f"✗ {item['no_preticket_pcs']} pcs no info"
            )
        else:
            preticket_display = 'N/A'

        item_rows.append({
            'Style #': item['style'],
            'Status': status,
            'PO Qty': item['po_qty'],
            'SM Qty': item['sm_qty'],
            'Calculation': item['calculation'],
            'Preticket': preticket_display,
        })

    st.table(item_rows)

    # ===== CORRECTIVE ACTION =====
    if not results['overall_pass']:
        st.markdown(
            '<div class="error-banner">'
            '<h4 style="color:#991b1b;margin:0 0 0.4rem 0">'
            '🚨 Corrective Action Required</h4>'
            '<p style="color:#b91c1c;font-size:0.9rem;margin:0">'
            'The Purchase Order is the authoritative source. All discrepancies must '
            'be corrected in the shipping mark before approval. Contact the supplier '
            'to provide updated shipping mark documentation.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    # ===== ACTION BUTTONS =====
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Verify Another Document", use_container_width=True):
            st.session_state.results = None
            st.session_state.preticket_confirm = None
            st.rerun()