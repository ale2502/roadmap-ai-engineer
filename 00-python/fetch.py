import requests

URL = "https://api.github.com/repos/python/cpython"

def get_repo_info(url):
  response = requests.get(url, timeout=10)
  response.raise_for_status()
  return response.json()

if __name__ == "__main__":
  data = get_repo_info(URL)
  print(data["name"], "has", data["stargazers_count"], "stars")