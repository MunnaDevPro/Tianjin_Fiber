JAZZMIN_SETTINGS = {
    "site_title": "UK Portfolio Admin",
    "site_header": "CMS Admin",
    "site_brand": "Portfolio CMS",
    "site_logo": "core/images/logo.webp",
    "login_logo": "core/images/logo.webp",
    "welcome_sign": "Welcome to the Portfolio CMS",
    "copyright": "UK Portfolio Ltd",
    "search_model": ["products.Product"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "navigation.Navbar": "fas fa-compass",
        "navigation.Footer": "fas fa-shoe-prints",
        "navigation.SocialLink": "fas fa-share-alt",
        "home.HomeHero": "fas fa-home",
        "home.HomeFactory": "fas fa-industry",
        "home.HomeMission": "fas fa-bullseye",
        "home.HomeValues": "fas fa-gem",
        "about.AboutHeader": "fas fa-heading",
        "about.AboutStory": "fas fa-book-open",
        "about.AboutExcellence": "fas fa-award",
        "about.TeamMember": "fas fa-user-tie",
        "about.Testimonial": "fas fa-quote-left",
        "products.Category": "fas fa-list",
        "products.Product": "fas fa-box",

        "contactapp.ContactMessage": "fas fa-envelope",
        "contactapp.ContactPageSettings": "fas fa-cog",
        
        # Services
        "services.ServicesHeader": "fas fa-heading",
        "services.ServiceItem": "fas fa-hand-holding-heart",
        "services.ProcessSection": "fas fa-cogs",
        "services.ProcessStep": "fas fa-step-forward",
        "services.ServicesCTA": "fas fa-bullhorn",
        
        # Factory
        "factory.FactoryHeader": "fas fa-heading",
        "factory.FactoryGallerySection": "fas fa-images",
        "factory.FactoryImage": "fas fa-image",
        "factory.FactoryVideoSection": "fas fa-video",
        "factory.FactoryVideo": "fas fa-play-circle",
        "factory.FactoryCTA": "fas fa-bullhorn",
        
        # Certificates
        "certificates.CertificatesHeader": "fas fa-heading",
        "certificates.Certificate": "fas fa-certificate",
        "certificates.CertificatesCTA": "fas fa-bullhorn",

        # Security
        "activitylog.UserSession": "fas fa-user-shield",
    },
    "custom_links": {
        "home": [{
            "name": "Homepage Settings", 
            "url": "admin:home_homehero_changelist", 
            "icon": "fas fa-home"
        }]
    },
    "order_with_respect_to": ["navigation", "home", "about", "products", "services", "factory", "certificates", "contactapp", "activitylog", "seo", "auth"],
    "custom_css": "core/css/custom_admin.css",
    "custom_js": "core/js/custom_admin.js",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "lumen",
    "dark_mode_theme": "darkly",
}
