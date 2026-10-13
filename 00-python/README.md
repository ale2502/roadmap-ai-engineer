# Step 0: Language (Python)

**Goal:** read Python code, install a package with `pip`, run a local script.

**Status:** met. Created a venv, installed `requests` with `pip`, read `fetch.py` before running it, and ran it locally.

## How to run

From the repo root:

```bash
cd 00-python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python fetch.py
```

Expected output: `cpython has <N> stars` (needs internet).

Files:

- `fetch.py`: calls the GitHub API with `requests` and prints a repo's star count.
- `use_fetch.py`: imports `fetch` and calls `get_repo_info`. Shows that the `__main__` check keeps the import free of side effects.
- `demo.py`: prints `__name__`. Compare `python demo.py` with `python -c "import demo"`.
- `requirements.txt`: pinned dependencies (`pip freeze > requirements.txt`).

## In my own words

**Why I activate the virtual environment.** If I don't activate it and I `pip install` something, the package goes into the shared (global) Python, and different projects can end up with conflicting versions. Activating puts `.venv/bin` at the front of `PATH`, so `python` and `pip` point to the copies inside `.venv`, and the project only gets the dependencies it needs. I activate once per terminal window, not once per repository. VS Code can do it for me in new terminals, but I still check for `(.venv)` in the prompt before any `pip install`.

**The sequence.**
1. Create the project folder (`00-python`).
2. Create the venv once: `python3 -m venv .venv`. It makes a folder with its own Python and an empty place for packages.
3. Activate it in each new terminal: `source .venv/bin/activate`.
4. Install what the project needs: `pip install requests`.

**What `import requests` does.** Python finds the package in the `site-packages` of the active environment and runs its code, which makes its functions available in my script (e.g. `requests.get(...)`). Importing any file or module runs it from top to bottom, and only once per program. Defining a function (`def`) doesn't call it.

**What I installed.** I ran `pip install` once, for `requests`. pip also installed its 4 dependencies (`certifi`, `charset_normalizer`, `idna`, `urllib3`), so `requirements.txt` has 5 packages. `pip` itself comes with every venv and isn't listed by `pip freeze`.

**`__name__` and `if __name__ == "__main__":`.** Every file has a `__name__` that Python sets automatically. It's `"__main__"` when I run the file directly, and the file's own name (e.g. `"fetch"`) when another file imports it. The `if` runs its body only when the file is started directly. So `use_fetch.py` can `import fetch` to borrow `get_repo_info` without firing the request.

**`.json()`** returns a Python dict (not a string), which is why `data["name"]` works.

## Foundations, step by step

1. **Terminal vs shell.** The terminal is the window that shows text. The shell (`zsh`) is the program inside it that reads and runs my commands.
2. **Virtual environment.** A project-local folder with its own Python and packages. Like `node_modules` in JavaScript, but it also contains the interpreter. Dot folders (`.venv`, `.git`) are hidden by convention; `ls -a` shows them.
3. **`PATH`.** The shell looks for `python` in the folders listed in `PATH`, in order. Activation puts `.venv/bin` first; `deactivate` removes it. `which python` shows which one wins.
4. **Create and activate.** `python3 -m venv .venv`, then `source .venv/bin/activate`. `(.venv)` appears in the prompt.
5. **Install and inspect.** `pip install requests`, then `pip show requests`. `Location:` shows the `site-packages` folder inside `.venv`, and `Requires:` shows the dependencies.
6. **Isolation test.** With the venv active, `import requests` loads the copy under `.venv/`. After `deactivate`, the same import loads the shared copy under `/Library/Frameworks/...`. A package only in the shared Python (`pydantic`) raises `ModuleNotFoundError` inside the venv. That error means "wrong interpreter, or not installed here".
7. **`.gitignore`** at the repo root: `.venv/`, `.env`, `__pycache__/`, so the environment, secrets and caches are never committed.
8. **Read, predict, run.** Read `fetch.py`, predict the output, then run `python fetch.py`.
9. **Imports and `__name__`.** `demo.py` and `use_fetch.py` showed that importing runs a file, and that the `__main__` check keeps imports free of side effects.
10. **Pin dependencies.** `pip freeze > requirements.txt` records exact versions (`requests==2.34.2`) so the environment can be rebuilt with `pip install -r requirements.txt`. This matters later because LLM libraries change fast and updates often break things.

## Problems I hit (and fixes)

- **`python3 -m venv` failed** with `ensurepip ... non-zero exit status 1`. Cause: the Homebrew Python 3.14.7 had a broken XML module (`pyexpat` couldn't load), so `platform.mac_ver()` was empty and pip crashed. Fix: `brew upgrade python@3.14 expat`. Lesson: read the real error, not only the last line.
- **Re-running `venv` over a broken `.venv`** left a mix of two Python versions (`python` linked to 3.14, pip from 3.12). Fix: `rm -rf .venv` and create it again. Never layer a new venv on a broken one.
- **`can't open file 'demo.py'`**: I had created the files inside `.venv`. Code goes next to `.venv`, never inside it (the venv gets deleted and rebuilt). Use `pwd` and `ls` to check where I am. A script can be run from anywhere with its path, but `import` looks in the current folder.
- **VS Code "invalid Python interpreter" popup**: it remembered the deleted venv. Fix: `Cmd+Shift+P` → `Python: Select Interpreter` → choose `00-python/.venv/bin/python`.
- **Terminal beeping in VS Code**: turn off `terminal.integrated.enableBell` and the terminal accessibility signals in Settings.
