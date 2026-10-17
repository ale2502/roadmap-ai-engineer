# Step 2: LLM Fundamentals

**Goal:** explain in 2 minutes how a word becomes a number and how the model generates text.

**Status:** goal met (2026-10-17). The "Transformer basics" section is written and needs rereading until I can say it without looking. Still to do: complete the two "To do" rows in the experiments log.

## How to run

From the repo root:

```bash
cd 02-llm-fundamentals
python3 -m venv .venv
source .venv/bin/activate
pip install tiktoken sentence-transformers
python tokens.py
python embeddings.py
```

Installed versions when I wrote this: `tiktoken 0.14.0`, `sentence-transformers 6.1.0` (pulls in `torch` and `transformers`, so the install is large). The first run of `embeddings.py` downloads the model, so it needs internet. `requirements.txt` pins every package (45 lines, including dependencies), so `pip install -r requirements.txt` can replace the `pip install` line above.

Files:

- `tokens.py`: encodes a text into token IDs with `tiktoken` (`cl100k_base`) and decodes each ID back to see the pieces.
- `embeddings.py`: encodes texts into vectors with `sentence-transformers` (`all-MiniLM-L6-v2`) and prints the cosine similarity between pairs.

## In my own words

**Tokens.** The model never sees words, only tokens: pieces of text taken from a fixed vocabulary. A tokenizer splits text by statistics, not by grammar (`unbelievably` → `un | belie | vably`). Each piece becomes an ID, which is just a label. ID 5000 isn't "closer" to ID 5001 in any meaningful way. Tokens matter because I pay per token, the context window is measured in tokens, and text gets truncated by tokens.

**Same text, different cost.** The context window is fixed. Text in other languages is split into more tokens, so it fills more of the window and costs more ("Hello my name is Alessandro" is 6 tokens, "Olá meu nome é Alessandro" is 7). Numbers split too (`1234567` → `123 | 456 | 7`).

**Embeddings.** An embedding turns a text into a list of numbers (a vector) where *distance carries meaning*. Texts used in similar contexts end up close together. This is what lets me search by meaning instead of by exact keywords. It's the base for RAG in Step 5.

**Dimensions.** `all-MiniLM-L6-v2` gives every text 384 dimensions. The dimensions are the 384 *positions* in the vector, and each one holds a number. They have no names. Nobody designed them, and training shaped them. The meaning is spread across all of them, so column 17 doesn't mean "animal". The values aren't limited to 0-1 and can be negative. Shape `(3, 384)` means 3 texts (rows) with 384 dimensions (columns).

**Where the closeness comes from.** Training. The model reads a huge amount of text and learns to place texts that appear in similar contexts close together. "Dog" and "puppy" appear around "walk", "bark", "vet". "Invoice" appears around "payment", "due date". Nobody wrote a rule that dogs and puppies are related. The model doesn't know what a dog is, it only knows how the word is used. After training, the model is frozen: `encode` applies what it learned and doesn't learn anything, so the same text always gives the same vector.

**Cosine similarity.** (The number it returns is also called the *similarity score*, or just the *score*. The embedding is the vector, not this number.) It compares two vectors across all 384 dimensions at once:
1. Multiply the two values in each dimension.
2. Add up all 384 products (the dot product, *produto escalar*).
3. Divide by the lengths of the two vectors, so only the direction matters.

The result is between -1 and 1. A high score means the vectors have large values of the same sign in many of the same dimensions, so they point the same way. It's a *sum*, not an average. This model normalizes its vectors to length 1, so the dot product alone already gives the cosine. The score is the combined result of 384 small agreements and disagreements, not a verdict from any single dimension.

## Transformer basics

**Attention.** Each token looks at every other token in the sentence and asks, "which of you help me understand my meaning here?" Each other token gets an attention weight, and the weights add up to 1. In `I sat on the river bank`, `bank` gives most of its weight to `river`. In `I deposited money at the bank`, it gives most to `money`. All tokens do this at the same time, not one after another.

**Attention and the `bank` experiment.** The same word `bank` got different vectors depending on the sentence (0.81 for the money sentence vs 0.15 for the river sentence, both against a money paraphrase). Attention is the reason: the vector for `bank` is adjusted using the words around it. This is why embeddings from a transformer depend on context, and why `all-MiniLM` and the multilingual model (both transformers) can tell the two meanings apart.

**Next-token prediction.** A language model does one job: given all the tokens so far, give every token in the vocabulary (about 100,000) a score for being next. The scores add up to 1. For `The capital of France is`, ` Paris` is on top. `beautiful` gets a small score above zero, because "The capital of France is beautiful" is still a valid sentence. `banana` gets almost nothing.

**Similarity score vs next-token score.** Two different numbers.
- *Similarity score:* how close in meaning two texts are. It compares one pair of vectors and goes from -1 to 1. Each pair is independent, so `dog` vs `puppy` (0.80) and `dog` vs `invoice` (0.22) don't affect each other.
- *Next-token score:* how likely each token in the vocabulary is to come next. Each goes from 0 to 1 and they all add up to 1, because the tokens compete for 100% of the probability. A final step called softmax makes them add up to 1, and temperature works on it.

Check: `Paris` 0.7, `Lyon` 0.5, `banana` 0.1 is invalid because it adds up to 1.3. With only three options they must add up to 1 (for example 0.7, 0.2, 0.1).

**The generation loop (autoregression).** After a token is picked, it is added to the end of the input, and the model reads the whole sequence again, including the new token. It scores every token again, picks one, and repeats until it picks a special stop token. The model's own output becomes part of its next input, which is what *autoregression* means.

**Temperature.** The picked token is usually a high-scoring one, but not always the top one. A setting called *temperature* controls how much lower-scoring tokens get a chance. Low temperature stays close to the top score. High temperature spreads out. This is why the same prompt can give different answers.

**Why this matters later.**
- **Streaming (Step 3):** tokens arrive one at a time because each one comes from one pass of the loop.
- **Cost:** I pay for every input token and every output token, and each output token is one more trip around the loop.
- **Context window (Step 5):** each pass re-reads everything so far, so a long conversation fills the window and eventually overflows.

**The 2-minute explanation.** The text is split into tokens, and each token gets an ID from a fixed vocabulary. Each ID becomes a vector (an embedding). Attention then adjusts each vector using the surrounding tokens, so `bank` next to `river` differs from `bank` next to `money`. The model uses the result to score every token in the vocabulary for what comes next and picks one, usually a high-scoring one. That token is added to the input and the model repeats the process, until it picks a stop token.

## Foundations, step by step

1. **Tokenize.** `tiktoken.get_encoding("cl100k_base")`, then `enc.encode(text)` gives IDs and `enc.decode([id])` shows the piece for one ID.
2. **Compare languages.** The same sentence in English and Portuguese has a different token count. This is why non-English text costs more.
3. **Taxonomy vs embedding.** A taxonomy tree is built by hand and is rigid. An embedding is learned, and closeness means similar meaning.
4. **Embed.** `SentenceTransformer("all-MiniLM-L6-v2").encode(texts)` returns an array of shape `(number of texts, 384)`.
5. **Compare.** `util.cos_sim(vectors[0], vectors[1])` gives the similarity between two texts.
6. **Make a prediction before every experiment.** Writing down a guess first shows which part of my intuition is wrong.
7. **Look inside.** `vectors[0] * vectors[1]` multiplies dimension by dimension, and `.sum()` gives the dot product, which should be close to the cosine score here.

## Experiments log

| Experiment | My guess | Result | What I learned |
| --- | --- | --- | --- |
| `dog` vs `puppy` (`all-MiniLM-L6-v2`) | 0.7 | 0.80 | Related words in the same language score high. |
| `dog` vs `invoice` | 0.1-0.2 | 0.22 | Unrelated words score low, but not zero. |
| `dog` vs `cachorro` (`all-MiniLM-L6-v2`) | n/a | 0.26 | Barely above unrelated. The model is English-only. |
| `dog` vs `cachorro` (`paraphrase-multilingual-MiniLM-L12-v2`) | | | To do. |
| `bank` (money) vs `bank` (river), each against a money paraphrase | | | To do. |

## Problems and mix-ups (and fixes)

- **"The context window gets bigger."** No: the window is fixed. The same text fills more of it in some languages because it takes more tokens.
- **Dimensions as labeled categories.** They have no names and values aren't limited to 0-1. Only the overall position matters.
- **"Dimension" vs "value".** A dimension is a slot (one of 384). The number in it is the value.
- **Average vs sum.** The similarity score is a sum of the per-dimension products, normalized by vector length. It isn't an average.
- **"It checks the surrounding words" has a name.** That step is attention. Say the word.
- **"The best token" isn't always chosen.** The pick is usually a high-scoring token, but temperature lets lower-scoring ones through. That's why answers vary.
- **Higher temperature for more similar answers.** Backwards: low temperature makes the top token win almost every time, so answers are more similar. It makes them consistent, not correct.
- **Similarity score vs next-token score.** The first is -1 to 1 per pair and doesn't add up to anything. The second is a probability per token and adds up to 1.
- **Wrong venv in VS Code.** The terminal can show `(.venv)` at the repo root while pointing at `00-python/.venv`, which doesn't have `tiktoken` or `sentence-transformers`. Check with `which python`, or use `Cmd+Shift+P` → `Python: Select Interpreter` and choose `02-llm-fundamentals/.venv`.
- **No `requirements.txt`.** `sentence-transformers` pulls in many packages, so I pinned them all with `pip freeze > requirements.txt` (run inside `02-llm-fundamentals` with the right venv active).
