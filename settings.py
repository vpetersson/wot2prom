import os


def str2bool(v):
    return v.lower() in ("yes", "true")


# Should be something like 'https://192.168.1.10:8484',
# or 'https://192.168.1.10:8484, https://192.168.1.11:8484"
WOT_ENDPOINTS = os.getenv('WOT_ENDPOINTS', False)

# Set to to to verify SSL certificate.
WOT_VERIFY_SSL = str2bool(os.getenv('WOT_VERIFY_SSL', 'False'))

# Your WoT token. The default token is the example token.
WOT_TOKEN = os.getenv('WOT_TOKEN', 'cKXRTaRylYWQiF3MICaKndG4WJMcVLFz')
