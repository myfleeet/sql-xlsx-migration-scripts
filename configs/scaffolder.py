import configs.settings as settings
import os

def create_folder():
  for folder in ['goto', 'accenture']:
    for env in list(settings.DB.keys()):
      os.makedirs(f'out/{folder}/{env}', exist_ok=True)