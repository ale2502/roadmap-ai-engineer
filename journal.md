# Study Journal

Session log for the AI Engineering roadmap. Newest entries first. Claude reads the top entry at the start of each session to pick up where we left off, and `/save` adds a new entry at the end of a session.

<!-- New entries go directly below this line. -->

## 2026-10-17

**Step:** Step 2: LLM fundamentals (transformer basics)
**What I did:**
- Attention: predicted that `bank` gets its meaning mostly from `river` in "I sat on the river bank" and from `money` in "I deposited money at the bank". Linked this to last session's `bank` experiment (0.81 vs 0.15): attention makes embeddings depend on context.
- Next-token prediction: the model scores every token in the vocabulary (about 100,000), the scores add up to 1. For `The capital of France is`, I picked `Paris` on top and `beautiful` as a small non-zero score. Then the loop: the picked token is added to the input, the model reads it all again, until a stop token (autoregression).
- Gave the Step 2 goal explanation in my own words. Corrections: name the surrounding-words step "attention", the model scores the whole vocabulary, and the best token isn't always picked (temperature).
- Claude wrote the "Transformer basics" section in `SUMMARY-step-2-llm-fundamentals.md` because I need to read more before I can say it in my own words. Also added two entries to the mix-ups list. Fixed a stale VS Code Markdown preview (the file was fine on disk).
**Goal status:** met. I explained text → tokens → vectors → attention → next-token scores → loop → stop token, but only at a basic level. The summary needs rereading until I can say it without looking.
**Stuck on / questions:** I found the first prediction questions too abstract ("what do you think it scores highest compared to what?"), so a concrete example helped. Open: temperature is understood only as an idea, not tried. The two "To do" rows in the experiments table of the Step 2 summary are still empty, and so is the `invoice` vs `fatura` (0.58) question.
**Next session:** Reread the "2-minute explanation" in the Step 2 summary and say it out loud without looking. Then start Step 3: call the provider API by hand and write a streaming script, so the token loop shows up live.

## 2026-10-16

**Step:** Step 2: LLM fundamentals (embeddings wrap-up)
**What I did:**
- Created `02-llm-fundamentals/requirements.txt` with `pip freeze` (45 lines, mostly dependencies of `sentence-transformers`), and updated the two outdated mentions in the Step 2 summary. Added "similarity score" as another name for the cosine similarity number (the embedding is the vector, not the number).
- Explained the `dog` vs `cachorro` jump (0.26 → 0.98): the multilingual model was trained on many languages, so translations land close together.
- `bank` experiment with the multilingual model, comparing each sentence against a money paraphrase. My guesses were 0.8 and 0.3. Results: money sentence vs paraphrase 0.81, river sentence vs paraphrase 0.15, money vs river 0.34. The same word `bank` gets a different pull depending on the other words in the sentence. That is what attention does, and it is the first topic of transformer basics.
**Goal status:** in progress. The embeddings half is done (word → tokens → IDs → context-aware vectors → similarity score). Still to do: how the model generates text (attention in more detail, next-token prediction).
**Stuck on / questions:** I forgot the name of the number (cosine similarity / similarity score). I explained the `bank` result as "the context decides", which is right, but the mechanism (tokens attend to the neighboring words) is still new. Open: why `invoice` vs `fatura` is only 0.58 (is `fatura` as clean a translation of `invoice` as `cachorro` is of `dog`?). I skipped the prediction first, and ran only one pair, before the proper experiment.
**Next session:** Start transformer basics: attention (how `bank` gets its meaning from neighboring words), then next-token prediction (how the model generates text). End by explaining the Step 2 goal in 2 minutes.

## 2026-10-15

**Step:** Step 2: LLM fundamentals (embeddings review)
**What I did:**
- Fixed the VS Code venv mix-up: the terminal can show `(.venv)` at the repo root while pointing at `00-python/.venv`. Check with `which python` or `Python: Select Interpreter`, and use `02-llm-fundamentals/.venv` for Step 2.
- Reviewed embeddings: the 384 dimensions are positions in the vector with no names, and each holds a value. Closeness comes from training on usage patterns, and the model is frozen at `encode` time. Cosine similarity multiplies per dimension and sums, then divides by the vector lengths. It's a sum, not an average. `produto escalar` is the Portuguese for dot product.
- Experiment: `dog` vs `cachorro` scored 0.26 with `all-MiniLM-L6-v2`, barely above `dog` vs `invoice` (0.22). The model is English-only, so it silently gives bad results for Portuguese, which matters for RAG in Step 5.
- Renamed `00-python/README.md` to `00-python/SUMMARY-step-0-python.md`, wrote `02-llm-fundamentals/SUMMARY-step-2-llm-fundamentals.md` as a manual in my own words, and updated the `CLAUDE.md` naming convention for step summaries.
- Multilingual model (`paraphrase-multilingual-MiniLM-L12-v2`): `dog` vs `cachorro` jumped to 0.98 (I guessed 0.6), `dog` vs `invoice` stayed 0.23. The embedding is the whole vector; the number I predict is the similarity score between two embeddings.
- Tested my hypothesis that `fatura` scores low against `invoice` (0.58) because it's ambiguous. Adding context made it worse: `fatura de energia` scored 0.21, while `cobrança` (0.60) and `boleto` (0.56) were close to `fatura`. A longer phrase gets its own meaning instead of clarifying the word, so the hypothesis was refuted. Also learned to build print labels from `texts` after two stale labels misled me, and what `range(1, len(texts))` does (start included, end excluded).
**Goal status:** in progress. The first half (text → tokens → IDs → vectors, plus how similarity is scored and why the model's language matters) is solid. Still to do: the `bank` experiment, then transformer basics (attention, next-token prediction).
**Stuck on / questions:** Mixed up dimension vs value and sum vs average (both cleared up). Still need to make a prediction before each experiment, since I skipped the guess for `cachorro`. Open: a revised explanation for why `invoice` vs `fatura` is only 0.58 while `dog` vs `cachorro` is 0.98, and the `range(2, 4)` check question went unanswered.
**Next session:** Run `pip freeze > requirements.txt` in `02-llm-fundamentals`, and fill in the experiments table in the Step 2 summary (the multilingual rows are still "To do"). Then predict and run the two `bank` sentences (money vs river) against a money paraphrase.

## 2026-10-14

**Step:** Step 0 review, then Step 2: LLM fundamentals (tokens, embeddings intuition)
**What I did:**
- Reviewed Step 0: venv activation (`which python`, `pip show`), why `requirements.txt` fixes "works on my machine", how to read a traceback (last line first, then scroll up when it's vague), and `if __name__ == "__main__":` (an unguarded LLM call would fire on every import).
- Tokens: wrote `02-llm-fundamentals/tokens.py` with `tiktoken` (`cl100k_base`). `unbelievably` splits into `un | belie | vably`, so tokenizers split by statistics, not grammar. Tokens are IDs from a fixed vocabulary, and the ID itself carries no meaning.
- Compared English and Portuguese: "Hello my name is Alessandro" is 6 tokens, "Olá meu nome é Alessandro" is 7. Non-English text costs more tokens and fills more of the fixed context window. Numbers split too (`1234567` is `123 | 456 | 7`).
- Embeddings: a taxonomy tree is hand-built and rigid; an embedding is a learned vector where closeness means similar meaning. Wrote `02-llm-fundamentals/embeddings.py` with `sentence-transformers` (`all-MiniLM-L6-v2`). Shape `(3, 384)` (rows = texts, columns = dimensions), dog-puppy similarity 0.80, dog-invoice 0.22 (my guesses were 0.7 and 0.1-0.2). Scores only mean something when compared within one model. This is the base for RAG in Step 5.
**Goal status:** in progress. Step 0 is met. Step 2 goal (explain in 2 minutes how a word becomes a number and how the model generates text) has the first half (text → tokens → IDs → vectors); still to do: more embedding experiments, then transformer basics (attention, next-token prediction).
**Stuck on / questions:** Context window stays fixed, but the same text fills more of it (I first said it "gets bigger"). Embedding dimensions aren't labeled categories and values aren't limited to 0-1. Still need practice reading tracebacks. Make a concrete prediction before each experiment. No `requirements.txt` yet in `02-llm-fundamentals` (`sentence-transformers` pulls in many packages).
**Next session:** Run `pip freeze > requirements.txt` in `02-llm-fundamentals`, then try two more embedding experiments with predictions first: `"dog"` vs `"cachorro"`, and the two `bank` sentences (money vs river, compared with a money paraphrase).

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
