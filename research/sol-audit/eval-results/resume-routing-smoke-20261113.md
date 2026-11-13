# Paused-case skill routing smoke

**Date:** 2026-11-13  
**Task duration:** 18.1s in a fresh OMP task context; not human-active time. Model/provider, tokens and cost: `UNKNOWN`.

Root `AGENTS.md` now requires reading `.agents/skills/resume-revise/SKILL.md` before modifying an existing paused/continuing case. A fresh task read only `AGENTS.md`, the F9 case brief/state, and the explicitly routed canonical skill. It identified the procedure and repeated the exact human-review/criteria next action from state. It did not read the key, decision, ledgers or revision snapshots, and performed no edits. Tool trace confirms this read set.

This validates instruction routing in a task context only. No Cursor/Codex discovery or IDE/new-chat acceptance; no case continuation was performed.