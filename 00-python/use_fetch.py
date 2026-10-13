import fetch

print("imported fetch, nothing was requested yet")

data = fetch.get_repo_info("https://api.github.com/repos/python/cpython")

print(data["name"])