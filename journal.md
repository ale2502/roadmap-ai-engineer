# Study Journal

Session log for the AI Engineering roadmap. Newest entries first. Claude reads the top entry at the start of each session to pick up where we left off, and `/save` adds a new entry at the end of a session.

<!-- New entries go directly below this line. -->

## 2026-10-21

**Step:** Step 3: Generative API in practice (streaming and tool calling)
**What I did:**
- Set `max_tokens` in `hello.py` back to 300. Wrote `03-raw-api/stream.py` with `client.messages.stream(...)` as a `with` block and a `for` loop over `stream.text_stream`, printing with `end=""` and `flush=True`. Streaming doesn't change how the model generates (always one token at a time). It only sends each chunk as soon as it's ready, so the first words show up much sooner while the total time stays about the same. `flush` pushes buffered output to the screen right away. I didn't see a difference because Haiku is fast, and I skipped the slow-down experiment.
- Wrote `03-raw-api/tool_call.py`: a fake `get_weather(city)` that returns (not prints) a string, a `tools` list with a JSON Schema `input_schema`, and a first call that returned `stop_reason: tool_use` and a `ToolUseBlock` (`id`, `name`, `input={'city': 'Paris'}`). Fixed the tool description, which promised a forecast the function doesn't give.
- Learned that the model never runs the tool. Only the `tools` description is sent, and the Python function stays on my machine. I proved it by commenting out the function and getting the same `tool_use` block. My script runs the function, then a second call sends the history (user question, the assistant's `tool_use` block, a user `tool_result` with `tool_use_id`) and gets the final answer with `end_turn`.
**Goal status:** met for both scripts (streaming and fake tool call work). Structured output is still left in Step 3, and I haven't answered the goal-check question yet.
**Stuck on / questions:** I thought the model ran `get_weather` because the names matched. I passed the whole `input` dict instead of `input["city"]`. I mixed up "three messages" with three variables (it's two API calls, and the second sends a three-entry `messages` list). I predicted `end_turn` for the first tool call. The model added "64°F" and "nice day" that weren't in the tool result. `tool_block = response.content[0]` assumes there's no text block first. The Step 3 summary file doesn't cover streaming or tool calling yet.
**Next session:** Answer the goal-check question in my own words, without reading: what does it mean for a model to "call a tool", who runs the function, and why does it take two API calls? Then add streaming and tool calling to `SUMMARY-step-3-raw-api.md` and start structured output.

## 2026-10-20

**Step:** Step 3: Generative API in practice (first raw API call)
**What I did:**
- Wrote `03-raw-api/hello.py` piece by piece: `load_dotenv()` before `anthropic.Anthropic()` (the client reads the key from the environment), then `client.messages.create(model, max_tokens, messages)`, then printed `response.content[0].text`, `response.usage` and `response.stop_reason`. Fixed the leading space in `.env.example`.
- Predicted token counts before each run. Input is always higher than the message because the API adds a fixed overhead of about 7 tokens (`"hi"` = 8, my 9-token sentence = 16). Output varies between runs of the same prompt because the model samples (temperature). Explaining takes about 30 tokens per sentence, not 20.
- Set `max_tokens = 30` to force truncation: `stop_reason` was `max_tokens` and the text stopped mid-sentence ("word, subword, or"). The cap counts tokens, not sentences. I first guessed it would end after the first sentence.
- Wrote `SUMMARY-step-3-raw-api.md` with the experiments table and mix-ups. Answered the three review questions (overhead, different outputs, `max_tokens`) correctly.
**Goal status:** in progress. `hello.py` works and the response structure is clear, but the streaming script and the fake-tool script are not written yet.
**Stuck on / questions:** Token guesses were low every time (forgot the overhead, underestimated sentence length). I thought `.text` changed the output tokens (it was two different runs). I expected `max_tokens` to end at a sentence boundary. Still open: the Step 2 two-minute explanation without reading, the two "To do" rows in the Step 2 experiments table, `invoice` vs `fatura` (0.58), and the monthly spend limit in the Console.
**Next session:** Set `max_tokens` in `hello.py` back to about 300. Then write `03-raw-api/stream.py` with streaming (`client.messages.stream(...)` and `stream.text_stream`). Before writing it, say what you expect to see on screen compared with `hello.py`, and what happens on the API side.

## 2026-10-19

**Step:** Step 2 wrap-up, then Step 3: Generative API in practice (setup)
**What I did:**
- Temperature: it reshapes the next-token scores before one is picked. Low temperature widens the gaps, so the top token's score goes up and the others go down. High temperature narrows them, so the top goes down and the unlikely ones go up. The scores always add up to 1, so they can't all go down. I first said "all scores go lower" for high temperature, which is wrong.
- Gave the Step 2 two-minute explanation while reading it. Corrections: attention is a step that updates each token's vector from its neighbors (not a token), the word is autoregression (not "outer regression"), the model scores the whole vocabulary (about 100,000 tokens), and a stop token ends the loop.
- Started Step 3 with Anthropic. Differences from the OpenAI-based roadmap: `max_tokens` is required, `system` is its own parameter, and `response.content` is a list of blocks. Current model is `claude-opus-5-5`, which always thinks and rejects `temperature`, `top_p` and `top_k` (400). For the temperature experiment use `claude-haiku-4-5`, which still accepts them.
- Set up `03-raw-api/`: venv created with `python3 -m venv` (macOS has no `python` until the venv is active), installed `anthropic` and `python-dotenv`, added `requirements.txt` and `.env.example`. The Claude subscription and the API are billed separately, so I added $5 of API credits.
**Goal status:** Step 2 met at a basic level. Step 3 in progress: setup done, no script written yet.
**Stuck on / questions:** `python` not found at first (use `python3` outside a venv). Confused the subscription with API credits. Not sure what `.env.example` is for (it lists the variable names without the secret, so it can be committed). The Step 2 two-minute explanation still needs to be said without reading. The two "To do" rows in the Step 2 experiments table are still empty, and so is the `invoice` vs `fatura` (0.58) question.
**Next session:** Write `03-raw-api/hello.py`. Call `load_dotenv()`, create `anthropic.Anthropic()`, send one message and print the text and `response.usage`, after predicting the input and output token counts. Check that `.env.example` has no leading space before `ANTHROPIC_API_KEY=`, and set a monthly spend limit in the Console.

## 2026-10-17

**Step:** Step 2: LLM fundamentals (transformer basics)
**What I did:**
- Attention: predicted that `bank` gets its meaning mostly from `river` in "I sat on the river bank" and from `money` in "I deposited money at the bank". Linked this to last session's `bank` experiment (0.81 vs 0.15): attention makes embeddings depend on context.
- Next-token prediction: the model scores every token in the vocabulary (about 100,000), the scores add up to 1. For `The capital of France is`, I picked `Paris` on top and `beautiful` as a small non-zero score. Then the loop: the picked token is added to the input, the model reads it all again, until a stop token (autoregression).
- Gave the Step 2 goal explanation in my own words. Corrections: name the surrounding-words step "attention", the model scores the whole vocabulary, and the best token isn't always picked (temperature).
- Claude wrote the "Transformer basics" section in `SUMMARY-step-2-llm-fundamentals.md` because I need to read more before I can say it in my own words. Also added two entries to the mix-ups list. Fixed a stale VS Code Markdown preview (the file was fine on disk).
- Review quiz on attention, autoregression and temperature. Attention (`it` → `animal`) was right. Autoregression I didn't know at first, then used it correctly: a long conversation costs more because the whole history is read again on every reply. Temperature: I guessed higher temperature for more similar answers, which is backwards. Low temperature makes the top token win almost every time, so it gives consistent (not necessarily correct) answers, e.g. for invoice extraction.
- Asked how the similarity score (-1 to 1, per pair) differs from the next-token scores (0 to 1, add up to 1 via softmax). Checked it with `Paris` 0.7, `Lyon` 0.5, `banana` 0.1: invalid, since it adds up to 1.3. Added both definitions and two more mix-ups to the Step 2 summary.
**Goal status:** met. I explained text → tokens → vectors → attention → next-token scores → loop → stop token, but only at a basic level. The summary needs rereading until I can say it without looking.
**Stuck on / questions:** I found the first prediction questions too abstract ("what do you think it scores highest compared to what?"), so a concrete example helped. I had temperature backwards at first (now corrected). I added up the invalid distribution correctly (1.3) but first said it "should" add up to 1.3. Open: temperature is understood only as an idea, not tried; some newer models may restrict the setting, to verify in the docs in Step 3. The two "To do" rows in the experiments table of the Step 2 summary are still empty, and so is the `invoice` vs `fatura` (0.58) question.
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
