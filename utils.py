import os

def fetch_type(s: str):
  s = s.rsplit('.')
  return s[-1] if len(s) > 1 else ''

def fetch_size(address: str):
  size = os.stat(address).st_size
  if size > 1024 ** 3:
    return f"{size // (1024 ** 3)} GB"
  elif size > 1024 ** 2:
    return f"{size // (1024 ** 2)} MB"
  elif size > 1024:
    return f"{size // (1024)} KB"

def fetch_files(dir):
  return [(i.name, fetch_type(i.name), fetch_size(os.path.abspath(dir) + "/" + i.name)) for i in os.scandir(dir) if i.is_file()]
