# Study Journal

Session log for the AI Engineering roadmap. Newest entries first. Claude reads the top entry at the start of each session to pick up where we left off, and `/save` adds a new entry at the end of a session.

<!-- New entries go directly below this line. -->

## 2026-10-14

**Step:** Step 0 review, then Step 2: LLM fundamentals (tokens, embeddings intuition)
**What I did:**
- Reviewed Step 0: venv activation (`which python`, `pip show`), why `requirements.txt` fixes "works on my machine", how to read a traceback (last line first, then scroll up when it's vague), and `if __name__ == "__main__":` (an unguarded LLM call would fire on every import).
- Tokens: wrote `02-llm-fundamentals/tokens.py` with `tiktoken` (`cl100k_base`). `unbelievably` splits into `un | belie | vably`, so tokenizers split by statistics, not grammar. Tokens are IDs from a fixed vocabulary, and the ID itself carries no meaning.
- Compared English and Portuguese: "Hello my name is Alessandro" is 6 tokens, "Olá meu nome é Alessandro" is 7. Non-English text costs more tokens and fills more of the fixed context window. Numbers split too (`1234567` is `123 | 456 | 7`).
- Embeddings (intuition only, no code yet): a taxonomy tree is hand-built and rigid; an embedding is a learned vector where closeness means similar meaning. This is the base for RAG in Step 5.
**Goal status:** in progress. Step 0 is met. Step 2 goal (explain in 2 minutes how a word becomes a number and how the model generates text) has the first half (text → tokens → IDs → vectors); still to do: embeddings experiment, then transformer basics (attention, next-token prediction).
**Stuck on / questions:** Context window stays fixed, but the same text fills more of it (I first said it "gets bigger"). Embedding dimensions aren't labeled categories and values aren't limited to 0-1. Still need practice reading tracebacks. Make a concrete prediction before each experiment.
**Next session:** Install `sentence-transformers` in the `02-llm-fundamentals` venv, write `embeddings.py`, and predict the vector shape and the dog-puppy vs dog-invoice similarity before running it.

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
