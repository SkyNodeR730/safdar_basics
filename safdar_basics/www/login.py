import frappe

no_cache = 1


def get_context(context):
    context.no_breadcrumbs = 1
    context.no_header = 1
    context.no_footer = 1
    context.no_sidebar = 1

    try:
        company = frappe.defaults.get_global_default("company")
        if company:
            company_doc = frappe.get_doc("Company", company)
            context.company_name = company_doc.company_name
            context.company_logo = company_doc.company_logo
        else:
            context.company_name = "Derma Shine"
            context.company_logo = None
    except Exception:
        context.company_name = "Derma Shine"
        context.company_logo = None

    context.is_logged_in = frappe.session.user != "Guest"
    context.year = frappe.utils.now_datetime().year

    # CSRF token — retrieve safely; guest sessions may not have one yet
    try:
        token = frappe.local.session.data.get("csrf_token", "")
    except Exception:
        token = ""
    context.csrf_token = token or ""

    context.products = [
        {"id": 1, "src": "/assets/safdar_basics/images/products/1.jpeg", "alt": "Sweet Almond Liposoluble Wax", "category": "Waxing"},
        {"id": 2, "src": "/assets/safdar_basics/images/products/2.jpeg", "alt": "Pure Pout Lip Treatment", "category": "Makeup"},
        {"id": 3, "src": "/assets/safdar_basics/images/products/3.jpeg", "alt": "Derma Shine Glow Collection", "category": "Collection"},
        {"id": 4, "src": "/assets/safdar_basics/images/products/4.jpeg", "alt": "Rice Face Scrub", "category": "Skincare"},
        {"id": 5, "src": "/assets/safdar_basics/images/products/5.jpeg", "alt": "Brightening Beauty Fluid", "category": "Skincare"},
        {"id": 6, "src": "/assets/safdar_basics/images/products/6.jpeg", "alt": "Green Apple Liposoluble Wax", "category": "Waxing"},
        {"id": 7, "src": "/assets/safdar_basics/images/products/7.jpeg", "alt": "Softening Bleach Mask", "category": "Face"},
        {"id": 8, "src": "/assets/safdar_basics/images/products/8.jpeg", "alt": "Gluta Bright Serum", "category": "Serum"},
        {"id": 9, "src": "/assets/safdar_basics/images/products/9.jpeg", "alt": "Hand & Feet Lightening Cream", "category": "Body"},
        {"id": 10, "src": "/assets/safdar_basics/images/products/10.jpeg", "alt": "Derma Shine Skincare Set", "category": "Set"},
        {"id": 11, "src": "/assets/safdar_basics/images/products/11.jpeg", "alt": "Walnut Face Polish", "category": "Skincare"},
        {"id": 12, "src": "/assets/safdar_basics/images/products/12.jpeg", "alt": "Skin Whitening Cream", "category": "Skincare"},
        {"id": 13, "src": "/assets/safdar_basics/images/products/13.jpeg", "alt": "Vitamin C Brightening Serum", "category": "Serum"},
        {"id": 14, "src": "/assets/safdar_basics/images/products/14.jpeg", "alt": "Rose Water Facial Toner", "category": "Toner"},
        {"id": 15, "src": "/assets/safdar_basics/images/products/15.jpeg", "alt": "Anti-Aging Night Cream", "category": "Skincare"},
        {"id": 16, "src": "/assets/safdar_basics/images/products/16.jpeg", "alt": "Derma Shine Luxury Bundle", "category": "Bundle"},
    ]

    context.features = [
        {
            "icon": "fas fa-boxes-stacked",
            "title": "Inventory Management",
            "desc": "Real-time stock tracking with intelligent reorder alerts and multi-warehouse support.",
        },
        {
            "icon": "fas fa-cart-shopping",
            "title": "Sales & Orders",
            "desc": "Streamline order processing from quotation to delivery with one-click workflows.",
        },
        {
            "icon": "fas fa-users",
            "title": "Customer Management",
            "desc": "360° customer profiles with purchase history, preferences, and loyalty tracking.",
        },
        {
            "icon": "fas fa-file-invoice-dollar",
            "title": "Billing & Invoicing",
            "desc": "Automated invoicing, tax calculation, and seamless payment reconciliation.",
        },
        {
            "icon": "fas fa-chart-line",
            "title": "Analytics & Reports",
            "desc": "Deep business insights with customisable dashboards and exportable reports.",
        },
        {
            "icon": "fas fa-store",
            "title": "Multi-Branch",
            "desc": "Manage unlimited locations from a single unified cloud platform with ease.",
        },
        {
            "icon": "fas fa-globe",
            "title": "Multi-Language",
            "desc": "Full support for multiple languages, currencies, and regional tax configurations.",
        },
        {
            "icon": "fas fa-mobile-screen-button",
            "title": "Mobile Ready",
            "desc": "Full-featured mobile experience for on-the-go business management anytime.",
        },
    ]

    context.stats = [
        {"number": "10K+", "label": "Products Managed"},
        {"number": "500+", "label": "Happy Clients"},
        {"number": "50+", "label": "Cities Covered"},
        {"number": "99.9%", "label": "Uptime"},
    ]

    context.testimonials = [
        {
            "name": "Sarah Ahmed",
            "role": "CEO, Glow Beauty Co.",
            "text": "Derma Shine ERP completely transformed our operations. We reduced stockouts by 80% and our entire team loves the intuitive interface.",
            "avatar": "SA",
            "rating": 5,
        },
        {
            "name": "Aisha Khan",
            "role": "Operations Manager, Luxe Cosmetics",
            "text": "The multi-branch management feature is a true game-changer. We now manage all 12 locations seamlessly from one beautiful dashboard.",
            "avatar": "AK",
            "rating": 5,
        },
        {
            "name": "Fatima Malik",
            "role": "Founder, Bloom Salon Group",
            "text": "Analytics and reports gave us insights we never had before. Our revenue grew by 35% within just 6 months of using the platform.",
            "avatar": "FM",
            "rating": 5,
        },
    ]

    return context
