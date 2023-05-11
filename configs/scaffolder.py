import configs.settings as settings
import os

folders = dict(
  goto='goto_acc',
  sap='sap'
)

def define_folder_project_name(item):
  if 'goto' in item:
    return folders.get('goto')
  if 'sap' in item:
    return folders.get('sap')

def create_folder():
  for folder in list(folders.keys()):
    for env in list(settings.DB.keys()):
      os.makedirs(f'out/{folders.get(folder)}/{env}', exist_ok=True)