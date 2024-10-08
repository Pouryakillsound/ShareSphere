import os

def fetch_type(s: str):
  res = ""
  for i in reversed(s):
    if i == ".":
      break
    res += i
  else:
    return ""
  return "".join([i for i in reversed(res)])

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
