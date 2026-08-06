JAZZMIN_SETTINGS = {
    "site_title": "UK Portfolio Admin",
    "site_header": "CMS Admin",
    "site_brand": "Portfolio CMS",
    "welcome_sign": "Welcome to the Portfolio CMS",
    "copyright": "UK Portfolio Ltd",
    "search_model": ["products.Product", "blog.Post"],
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
        "home.HomeHero": "fas fa-home",
        "about.AboutHero": "fas fa-info-circle",
        "products.Category": "fas fa-list",
        "products.Product": "fas fa-box",
        "blog.Post": "fas fa-newspaper",
        "contactapp.ContactMessage": "fas fa-envelope",
        "seo.SEOSettings": "fas fa-search",
    },
    "custom_links": {
        "home": [{
            "name": "Homepage Settings", 
            "url": "admin:home_homehero_changelist", 
            "icon": "fas fa-home"
        }]
    },
    "order_with_respect_to": ["navigation", "home", "about", "products", "services", "factory", "certificates", "blog", "contactapp", "seo", "auth"],
}

JAZZMIN_UI_TWEAKS = {
    "theme": "lumen",
    "dark_mode_theme": "darkly",
}
