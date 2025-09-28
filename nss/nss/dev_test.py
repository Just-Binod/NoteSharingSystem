# dev_test.py - Save this in your project root for testing
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nss.settings')
django.setup()

from django.conf import settings

print("=== Google OAuth2 Configuration Check ===")
print(f"DEBUG Mode: {settings.DEBUG}")
print(f"Client ID: {settings.GOOGLE_OAUTH2_CLIENT_ID}")
print(f"Redirect URI: {settings.GOOGLE_OAUTH2_REDIRECT_URI}")
print(f"Allowed Hosts: {settings.ALLOWED_HOSTS}")

# Test the URLs
if settings.DEBUG:
    test_url = "http://127.0.0.1:8000/note/auth/google/"
else:
    test_url = "https://iwasbinod.pythonanywhere.com/note/auth/google/"

print(f"\nTest URL: {test_url}")
print("=== Configuration Check Complete ===")