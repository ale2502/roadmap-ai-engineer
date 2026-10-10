# AI Engineering Study Repo

This repo is a personal study space for **AI Engineering (product)**: building products on top of existing models, not training models from scratch. The curriculum follows the "Roadmap AI Engineering 2026" by @matheusolivsilv (originally in Portuguese, July 2026). The full roadmap is reproduced in English below.

## Ground rules

- **Everything in this repo is in English**: lessons, notes, code comments, commit messages, READMEs, and all conversation with Claude. The source roadmap is Portuguese, so translate anything taken from it.
- **Follow the roadmap order.** Skipping steps is the most common mistake. Don't jump ahead (e.g. build an agent before understanding tokens, tool calls and context) unless the user explicitly asks, and say what they'd be skipping.
- **Raw API before frameworks.** Call the provider API by hand before using LangChain/LangGraph, so failures can be debugged. Likewise, learn embeddings before RAG.
- **Intuition over proofs.** Explain concepts the way an engineer needs them, not as a mathematician would.
- Classical software engineering (databases, auth, observability, deploy) is assumed known. Don't re-teach it unless asked.

## How Claude should act in this repo

Claude is a **study partner and tutor**, not just a code generator.

- When the user starts or continues a step, state which step it is and what its **Goal** is (see roadmap below).
- Prefer guiding the user to write the code themselves (hints, small scaffolds, review) over handing over finished solutions. Give full solutions when asked, or after the user has tried.
- Keep explanations short and concrete. Connect each concept to the later step that depends on it (e.g. tokens → cost, truncation, context windows).
- End each lesson by checking the step's **Goal**: ask the user to explain it in their own words or demonstrate it with working code.
- If the user asks something that belongs to a later step, answer briefly and point to where it's covered.
- Tell the user when something in the roadmap may be outdated (APIs, model names, library versions) and verify against the current official docs before teaching it.
- Never commit API keys. Keep secrets in `.env` (git-ignored) and provide `.env.example`.

## Session continuity

- At the start of every session, read the top (most recent) entry of `journal.md`. Greet the user with a one- or two-line recap of the last session (step, what was done, "Next session" item) and ask whether to continue from there.
- `journal.md` is written by the `/save` skill (`.claude/skills/save/SKILL.md`), which adds a session entry and commits. Suggest `/save` when the user wraps up a session or finishes a meaningful chunk of work. Don't write journal entries or commit unless the user runs `/save` or asks.

## Suggested repo layout

Create folders as the user reaches each step. Don't scaffold everything upfront.

```
00-python/              # Step 0
02-llm-fundamentals/    # Step 2: notes + small experiments (tokenizers, embeddings)
03-raw-api/             # Step 3: streaming script, fake tool call script
04-langchain-langgraph/ # Step 4: chatbot with 1 tool, agent graph
05-context-rag/         # Step 5: context, RAG, memory, MCP notes
notes/                  # Free-form notes, glossary, resources
```

Each step folder should have a `README.md` with: what was learned, how to run the code, and whether the step's **Goal** was met.

## Lesson/code conventions

- Python is the main language. Use a virtual environment (`python -m venv .venv`) and a `requirements.txt` (or `pyproject.toml`) per step or at the root.
- Scripts should run locally with a single command documented in the step README.
- Comments explain *why*, not *what*. Keep scripts small and readable. They are for learning.
- Commit messages: short, imperative, English (e.g. `Add streaming script for step 3`).

---

# Roadmap: AI Engineering 2026 (English translation)

**Profile:** @matheusolivsilv
**Focus:** AI Engineering (product): build products with ready-made models, not train models from scratch.

## How to use this roadmap

1. Follow the **order**. Skipping steps is the most common mistake.
2. Each block has **what to study** plus **where to start**.
3. The from-scratch project (chatbot → RAG → production) is separate content. This is the map.

## Step 0: Language

**Python** is the standard in AI Engineering job postings.

| If you are… | Start with |
| --- | --- |
| New to programming | Learn Python (interactive) |
| Already program in another language | Official Python Tutorial |
| Web / full-stack dev working with AI | TypeScript Handbook as a second language |
| Aiming at model training | Python + C++ later (not a priority now) |

**Goal:** read Python code, install a package with `pip`, run a local script.

## Step 1: Choose your path

| Path | Day-to-day work |
| --- | --- |
| **AI Engineering** ← this roadmap | APIs, RAG, agents, context, shipping LLM products |
| ML Engineer | Train/fine-tune models, data, experiments |
| Full stack with AI | App + back end + model integration |

This repo follows **AI Engineering**. Other paths still benefit from Python and the fundamentals, but the order changes.

## Step 2: LLM fundamentals (high level)

No need to become a mathematician. Build **intuition**, not proofs.

### Master

- **Tokens**: why you pay, truncate, and break per token
- **Embeddings**: text becomes a vector; semantic similarity
- **Transformer (basics)**: attention, autoregression; the model predicts the next token
- **Prompt**: a consequence of the fundamentals, not loose "prompt engineering"

### Resources

| Resource | Source |
| --- | --- |
| LLMs for developers (short, free) | DeepLearning.AI: Generative AI for Everyone |
| NLP / embeddings (free) | Hugging Face: NLP Course |
| Visual map of the field | roadmap.sh: AI Engineer |
| Long-term reference book | *AI Engineering* by Chip Huyen |

**Goal:** explain in 2 minutes how a word becomes a number and how the model generates text.

## Step 3: Generative API in practice

Before any framework, call the API **by hand** at least once.

### Master

- Requests with and without **streaming** (watch tokens arrive)
- Response structure (human vs assistant messages)
- **Tool calling**: what it means for the model to "call a tool"
- Structured output (JSON / schema)
- Audio and image (just know they exist; no need to master them now)

### Resources

| Resource | Link |
| --- | --- |
| OpenAI quickstart | platform.openai.com/docs/quickstart |
| Streaming | OpenAI docs: Streaming |
| Function / tool calling | OpenAI docs: Function calling |
| Anthropic (alternative) | docs.anthropic.com: Get started |

**Goal:** one local script that streams a response, and one that calls a fake tool (e.g. `get_weather`).

## Step 4: LangChain + LangGraph

> This is the step that separates people who have only "used ChatGPT" from people who build products.

After understanding the raw API, use a framework so you don't reinvent the wheel: swapping providers, tools, memory, streaming to the front end.

### Master

- Swap provider (GPT ↔ Claude ↔ Gemini) with the same code
- The contract: input → output → tool calls → tool results
- **LangGraph**: state graph, a simple ReAct agent
- Streaming events and their impact on UI/UX
- Why framework first, internals later

### Resources (free)

| Resource | Link |
| --- | --- |
| **LangChain Academy** (start here) | academy.langchain.com |
| Intro to LangChain + agents | Introduction to LangChain: Python |
| Intro to LangGraph | Introduction to LangGraph: Python |
| Official notebooks (clone locally) | github.com/langchain-ai/langchain-academy |
| LangChain docs | docs.langchain.com |
| LangGraph docs | docs.langchain.com/oss/python/langgraph/overview |

**Suggested order:** Academy "Introduction to LangChain" → "Introduction to LangGraph" → GitHub notebooks.

**Goal:** a chatbot with 1 working tool running locally, and understand the agent's graph.

## Step 5: Context, RAG, and product patterns

### Master

- **Context window**: what fits, what overflows, compaction
- **RAG (high level)**: ingestion vs retrieval; chunking; when to use RAG vs a plain prompt
- **Memory**: short term (thread) vs long term (user profile)
- **Patterns that show up in job postings and interviews:** MCP, Skills, multi-agent

### Resources

| Topic | Link |
| --- | --- |
| RAG concepts (short) | DeepLearning.AI: LangChain for LLM Application Development |
| MCP: what it is | modelcontextprotocol.io |
| Vector DB (concept) | pgvector on GitHub |

**Goal:** explain how you'd deliver an 80-page PDF to the model without sending all of it in the prompt.

## Step 6: The order most people get wrong

```
Python → LLM fundamentals → Raw API → LangChain/LangGraph → Context/RAG → Production
```

| Common mistake | Why it blocks you |
| --- | --- |
| Jumping straight to "build an agent" | You don't understand tokens, tool calls, or context |
| Only prompt tutorials | You don't know what happens when context overflows |
| Framework without the raw API | You can't debug when it breaks in prod |
| RAG before embeddings | Chunking and scores become black magic |

**Classical software engineering** (databases, auth, observability, deploy) is probably already known. It's the same back end as always. The differentiator is mastering steps 2–5.

## Next

A guided from-scratch project (chatbot → documents → retrieval → eval) is published separately by the author. Production (the last item in the order above) is covered there, not in this roadmap.
