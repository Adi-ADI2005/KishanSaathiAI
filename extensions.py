from flask_wtf import CSRFProtect

csrf = CSRFProtect()

def disable_csrf(app):
    app.config['WTF_CSRF_ENABLED'] = False
    csrf._exempt_views = set()  # reset protection