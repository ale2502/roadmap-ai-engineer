# Study Journal

Session log for the AI Engineering roadmap. Newest entries first. Claude reads the top entry at the start of each session to pick up where we left off, and `/save` adds a new entry at the end of a session.

<!-- New entries go directly below this line. -->

## 2026-10-14

**Step:** Step 0: Language (Python basics), review before starting Step 2
**What I did:**
- Reflected on the Step 0 step-by-step: what happens without venv activation (`which python`, `pip show` to find where a package landed), why `requirements.txt` fixes "works on my machine", and how to debug a failed `pip install`.
- Learned what a traceback is: read the last line for the error type, then scroll up for the real cause when it's vague (like `non-zero exit status 1`).
- Re-explained `if __name__ == "__main__":` and checked `fetch.py`: only the `import`, `URL` and `def` sit outside the `if`, so importing it has no side effects. Connected it to cost: an unguarded LLM call would fire on every import.
**Goal status:** met (Step 0). The review confirmed it; no new code this session.
**Stuck on / questions:** Mixed up why `pydantic` failed in the venv while `requests` worked in both places (`pydantic` was only in the shared Python, `requests` was in both). Not yet retried. Also need to practise reading tracebacks.
**Next session:** Retry the `pydantic` vs `requests` question in two sentences, then start Step 2 (LLM fundamentals): tokens first, with a tokenizer experiment in the venv.

## 2026-10-13

**Step:** Step 0: Language (Python basics)
**What I did:**
- Fixed a broken `venv` (Homebrew Python's `pyexpat` was failing, so pip crashed) and rebuilt a clean `.venv`. Learned the terminal vs shell difference, what a venv is (like `node_modules` plus its own interpreter), and how activation works through `PATH`.
- Ran `pip install requests`, traced where it landed with `pip show`, and used an isolation test to see the venv copy vs the shared copy. Created `.gitignore` and `requirements.txt`.
- Read `fetch.py` before running it, then ran it (`cpython has 77630 stars`). Worked through how `import` runs a file and what `if __name__ == "__main__":` does, using `demo.py` and `use_fetch.py`.
- Wrote `00-python/README.md` with my own summary, the step-by-step foundations, and the problems I hit.
**Goal status:** met. Created a venv, installed a package with `pip`, and read and ran a local script.
**Stuck on / questions:** none. `__name__` took several explanations to click, so worth a quick recap if it comes up again.
**Next session:** Start Step 2 (LLM fundamentals): tokens first, with a tokenizer experiment in the venv.

## 2026-10-12

**Step:** Step 0: Language (Python basics)
**What I did:**
- Finished the Input and Output lesson on learnpython.org.
- Learned that `input()` reads one line as a string, `.split()` turns it into a list, and `map(int, ...)` converts the items. Input ends when Enter is pressed, and the loop ends when the list runs out.
- Solved the "sum three integers" exercise; fixed a missing `total = 0` initialisation, and compared the loop version with `a, b, c = map(int, input().split())`.
**Goal status:** in progress. Still to do: `pip` install and running a local script.
**Stuck on / questions:** none
**Next session:** Confirm the last classes and objects exercise is done, then do the Step 0 goal: create a venv, `pip install` a package, and run a local script.

## 2026-10-11

**Step:** Step 0: Language (Python basics)
**What I did:**
- Practised loops with `break` and `continue` (guard clauses), and fixed a `SyntaxError` from missing colons on `if`/`elif`.
- Worked through classes and objects on learnpython.org; only the final exercise is left.
**Goal status:** in progress. Still to do: `pip` install and running a local script.
**Stuck on / questions:** none
**Next session:** Finish the classes and objects exercise, then do the Step 0 goal: create a venv, `pip install` a package, and run a local script.

## 2026-10-10

**Step:** Step 0: Language (Python basics)
**What I did:**
- Set up the study repo: `CLAUDE.md` with the English roadmap, `journal.md`, and the `/save` skill.
- Practised Python lists (indexing, slicing, mutation, iteration, comprehensions, a messages-style list of dicts).
- Finished practising conditions (`if`/`elif`/`else`).
**Goal status:** in progress. Still to do: `pip` install and running a local script.
**Stuck on / questions:** none
**Next session:** Continue the Python practice, then do the Step 0 goal: create a venv, `pip install` a package, and run a local script.
