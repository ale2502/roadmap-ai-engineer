# Step 3: Generative API in Practice

**Goal:** one local script that streams a response, and one that calls a fake tool (e.g. `get_weather`).

**Status:** in progress (2026-10-20). `hello.py` is done: a plain request, the response structure, `usage`, token counts and truncation. Still to do: the streaming script, the fake tool-call script, structured output.

## How to run

From the repo root:

```bash
cd 03-raw-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then paste the real key after ANTHROPIC_API_KEY=
python hello.py
```

Installed versions when I wrote this: `anthropic 1.15.0`, `python-dotenv 1.2.4`. Needs internet and API credits. The Claude subscription and the API are billed separately, so the API needs its own credits (and a monthly spend limit in the Console).

Files:

- `hello.py`: sends one message to `claude-haiku-4-5` and prints the reply text, `response.usage` and `response.stop_reason`.
- `.env`: holds `ANTHROPIC_API_KEY=...`. Git-ignored, never committed.
- `.env.example`: the same variable name with no value, so it can be committed. It shows what `.env` needs. No space before the name.
- `requirements.txt`: pinned dependencies.

## In my own words

**The client.** `anthropic.Anthropic()` creates an object that holds the API key and knows how to send requests. It doesn't send anything by itself. It reads `ANTHROPIC_API_KEY` from the environment, so `load_dotenv()` must run first: it copies the value from `.env` into the environment, and without it the client has no key.

**The request.** `client.messages.create(...)` takes keyword arguments (`name=value`), not a bare string:
- `model`: which model answers. I use `claude-haiku-4-5` for experiments because it's cheap.
- `max_tokens`: required by Anthropic. A hard cap on the reply length, not a target.
- `messages`: a list of `{"role": ..., "content": ...}` dicts. I am `"user"`, the model is `"assistant"`. The list can hold a whole conversation with the roles alternating.

**The response.** `response.content` is a list of blocks, so the text is `response.content[0].text`. Printing `response.content[0]` shows the whole block (`TextBlock(...)`). `response.usage` has `input_tokens` and `output_tokens`. `response.stop_reason` says why the model stopped.

**Why `input_tokens` is higher than my message.** The model only reads one flat sequence of tokens, so the API turns my structured messages into that sequence and adds special marker tokens around it (where each turn starts and ends, and where the assistant's turn begins). I never type them, but I pay for them. Anthropic doesn't publish the exact format, so I measured it: `"hi"` gave 8 input tokens and my 9-token sentence gave 16, so the overhead is a fixed cost of about 7 tokens per request. Short prompts feel more expensive than their word count suggests. In a long conversation each turn adds its own markers.

**Why two runs of the same prompt give different `output_tokens`.** The model doesn't always pick the top-scoring token. It samples from the next-token scores, and temperature controls how spread out that sampling is (Step 2). At the default setting the same prompt can give a different reply with a different length. `input_tokens` stays the same because the prompt didn't change. For a very short reply the same text can repeat. For a long reply it's very unlikely.

**What `stop_reason` tells me.**
- `end_turn`: the model picked the stop token and finished by itself.
- `max_tokens`: the cap was reached, so the reply may be cut off. The model doesn't plan for the cap. The API stops counting at the limit, even in the middle of a sentence. In code: `if response.stop_reason == "max_tokens": ...`.

**`.text` doesn't change the cost.** The request is already sent and the tokens already counted. `.text` only changes what `print` shows. If `output_tokens` differs between two runs, it's the sampling and not my code.

## Foundations, step by step

1. **Set up.** A venv in `03-raw-api/`, `pip install anthropic python-dotenv`, `.env` with the key, `.env.example` without it.
2. **Load the key, then create the client.** `load_dotenv()`, then `client = anthropic.Anthropic()`. Keep the client in a variable.
3. **Send one message.** `client.messages.create(model=..., max_tokens=..., messages=[...])`.
4. **Print the results.** `response.content[0].text`, `response.usage`, `response.stop_reason`.
5. **Predict before running.** Write two token counts (input, output) first, then compare.
6. **Vary one thing at a time.** Message `"hi"`, a longer prompt, then `max_tokens = 30`, each time comparing a guess with the real numbers.

## Experiments log

| Experiment | My guess | Result | What I learned |
| --- | --- | --- | --- |
| `"Say hello in one sentence"` | 6 in, 6 out | 12 in, 16 out | The API adds overhead tokens. Replies are longer than I expect, and the emoji or punctuation cost tokens too. |
| Same prompt, second run | n/a | 12 in, 14 out | Same input, different output: sampling. |
| `"hi"` | 5 in, 12 out | 8 in, 16 out | Overhead is a fixed cost of about 7 tokens. |
| `"Explain what a token is in three sentences"`, `max_tokens = 100` | 18 in, 68 out | 16 in, 92 and 97 out, `end_turn` | Explaining takes longer sentences than a greeting (about 30 tokens each, not 20). The model also added a heading I didn't ask for. 97 is only 3 under the cap. |
| Same prompt, `max_tokens = 30` | Ends after the first sentence, 30 out | 16 in, 30 out, `max_tokens`, cut off after "word, subword, or" | The cap doesn't respect sentences. The reply was cut mid-sentence. |

## Problems and mix-ups (and fixes)

- **`python` not found.** On macOS use `python3` outside a venv. Inside an active venv `python` works. Check with `which python`.
- **Subscription vs API.** They are billed separately. The API needs its own credits.
- **Not knowing what `.env.example` is for.** It lists the variable names without the secret, so it can be committed. A leading space before the name is a bug. I fixed it.
- **`anthropic.Anthropic()` not stored.** The client was created and thrown away. Assign it: `client = anthropic.Anthropic()`.
- **`create("hello")`.** `create` takes keyword arguments, not a bare string. My message goes inside `messages=[{"role": "user", "content": ...}]`.
- **Printing `response.content[0]` shows a `TextBlock(...)`.** Add `.text` to get the text.
- **"Adding `.text` changed the output tokens from 16 to 14."** No: those were two different runs, and the model samples. `.text` only changes the print.
- **Token guesses came out too low.** Input: I forgot the overhead of about 7 tokens. Output: I assumed about 20 tokens per sentence, but explanations need about 30, and headings and emoji cost tokens too.
- **"Max tokens ends at the end of the first sentence."** Wrong. The cap counts tokens, not sentences, so the text can stop anywhere.
- **"It will break the sentence" for `max_tokens`.** It *may* cut mid-sentence. A reply that happens to end at the cap still shows `max_tokens`, so I check `stop_reason` instead of looking at the text.
- **Reset `max_tokens` after the experiment.** `hello.py` still has `max_tokens = 30`. Use a comfortable value like 300 for normal runs.

## Why this matters later

- **Streaming (next in this step):** tokens arrive one at a time because each one is one trip around the generation loop.
- **Cost and limits:** I pay for input, output and the overhead. `max_tokens` is a real limit, and `stop_reason` is how I notice truncation.
- **Frameworks (Step 4):** LangChain wraps this same call. Truncation then shows up as strange half answers unless I check `stop_reason`.
- **Context window (Step 5):** the same cut-off happens on the input side when a conversation grows too long.
