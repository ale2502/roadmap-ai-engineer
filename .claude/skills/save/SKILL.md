---
name: save
description: Save study progress. Adds a session entry to journal.md and commits all changes.
disable-model-invocation: true
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*)
---

Save the progress of this study session: write a journal entry, then commit.

## 1. Gather what happened

- Review this conversation for what the user studied, built, and struggled with.
- Run `git status` and `git diff` to see which files changed.
- Read the top entry of `journal.md` so the new entry doesn't repeat it.

## 2. Write the journal entry

Insert a new entry in `journal.md` directly below the `<!-- New entries go directly below this line. -->` comment (newest first). Use today's date. If an entry for today already exists, add to it rather than creating a duplicate heading. Use this format, in English:

```markdown
## YYYY-MM-DD

**Step:** <roadmap step, e.g. Step 3: Generative API in practice>
**What I did:** <1-4 bullets: concepts studied, code written, resources used>
**Goal status:** <not started | in progress | met>, with a one-line reason
**Stuck on / questions:** <open problems, or "none">
**Next session:** <the single most useful thing to do next>
```

Base the entry on what actually happened. If something is unclear (e.g. whether the step's goal was met), ask the user instead of guessing. Keep it short.

## 3. Commit

- Stage changes by name (`git add <files>`), not `git add -A`. Never stage `.env`, API keys, virtual environments (`.venv/`), or other secrets and build artifacts. If you see one, warn the user.
- Write a short, imperative, English commit message summarizing the session's work (e.g. `Add streaming script and journal entry for step 3`). Include the `journal.md` update in the same commit. End the message with the Co-Authored-By attribution line Claude Code provides.
- Do not push. Do not amend earlier commits.
- If a pre-commit hook fails, fix the issue and make a new commit.

## 4. Report

Reply with the commit hash and message, plus the "Next session" line from the journal entry. Keep it to a few lines.
