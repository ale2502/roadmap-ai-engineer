# Step 2: LLM Fundamentals

**Goal:** explain in 2 minutes how a word becomes a number and how the model generates text.

**Status:** in progress. The first half is done (text → tokens → IDs → vectors). Still to do: more embedding experiments, then transformer basics (attention, next-token prediction).

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

Installed versions when I wrote this: `tiktoken 0.14.0`, `sentence-transformers 6.1.0` (pulls in `torch` and `transformers`, so the install is large). The first run of `embeddings.py` downloads the model, so it needs internet. There is no `requirements.txt` yet: run `pip freeze > requirements.txt` to create it.

Files:

- `tokens.py`: encodes a text into token IDs with `tiktoken` (`cl100k_base`) and decodes each ID back to see the pieces.
- `embeddings.py`: encodes texts into vectors with `sentence-transformers` (`all-MiniLM-L6-v2`) and prints the cosine similarity between pairs.

## In my own words

**Tokens.** The model never sees words, only tokens: pieces of text taken from a fixed vocabulary. A tokenizer splits text by statistics, not by grammar (`unbelievably` → `un | belie | vably`). Each piece becomes an ID, which is just a label. ID 5000 isn't "closer" to ID 5001 in any meaningful way. Tokens matter because I pay per token, the context window is measured in tokens, and text gets truncated by tokens.

**Same text, different cost.** The context window is fixed. Text in other languages is split into more tokens, so it fills more of the window and costs more ("Hello my name is Alessandro" is 6 tokens, "Olá meu nome é Alessandro" is 7). Numbers split too (`1234567` → `123 | 456 | 7`).

**Embeddings.** An embedding turns a text into a list of numbers (a vector) where *distance carries meaning*. Texts used in similar contexts end up close together. This is what lets me search by meaning instead of by exact keywords. It's the base for RAG in Step 5.

**Dimensions.** `all-MiniLM-L6-v2` gives every text 384 dimensions. The dimensions are the 384 *positions* in the vector, and each one holds a number. They have no names. Nobody designed them, and training shaped them. The meaning is spread across all of them, so column 17 doesn't mean "animal". The values aren't limited to 0-1 and can be negative. Shape `(3, 384)` means 3 texts (rows) with 384 dimensions (columns).

**Where the closeness comes from.** Training. The model reads a huge amount of text and learns to place texts that appear in similar contexts close together. "Dog" and "puppy" appear around "walk", "bark", "vet". "Invoice" appears around "payment", "due date". Nobody wrote a rule that dogs and puppies are related. The model doesn't know what a dog is, it only knows how the word is used. After training, the model is frozen: `encode` applies what it learned and doesn't learn anything, so the same text always gives the same vector.

**Cosine similarity.** It compares two vectors across all 384 dimensions at once:
1. Multiply the two values in each dimension.
2. Add up all 384 products (the dot product, *produto escalar*).
3. Divide by the lengths of the two vectors, so only the direction matters.

The result is between -1 and 1. A high score means the vectors have large values of the same sign in many of the same dimensions, so they point the same way. It's a *sum*, not an average. This model normalizes its vectors to length 1, so the dot product alone already gives the cosine. The score is the combined result of 384 small agreements and disagreements, not a verdict from any single dimension.

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
- **Wrong venv in VS Code.** The terminal can show `(.venv)` at the repo root while pointing at `00-python/.venv`, which doesn't have `tiktoken` or `sentence-transformers`. Check with `which python`, or use `Cmd+Shift+P` → `Python: Select Interpreter` and choose `02-llm-fundamentals/.venv`.
- **No `requirements.txt` yet.** `sentence-transformers` pulls in many packages, so pin them with `pip freeze > requirements.txt`.
