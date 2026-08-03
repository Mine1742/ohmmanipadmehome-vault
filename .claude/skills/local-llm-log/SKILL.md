---
name: local-llm-log
description: >
  Log progress on the Local LLM project — what was installed, run, tuned, or decided,
  and any issues hit. Trigger on requests like "log that I got Ollama running," "note
  that I upgraded my GPU," or "update my local LLM project progress." Different from
  editing the static reference notes (system_requirements, installation_guide, etc.),
  which document how things generally work rather than what you specifically did.
---

1. Append a dated entry to `local_llm_project_notes/Local LLM Project Log.md` (create it
   if it doesn't exist, linked from [[Local LLM Project Overview]]) with: date, what was
   done, what worked/didn't, and any decisions made (model choice, hardware, config).

2. If the session surfaced a durable fact that belongs in one of the static reference
   notes (e.g. a corrected command in `running_llm.md`, a new GPU option in
   `gpu_upgrade.md`), update that reference note too — but keep the dated narrative in
   the log, don't just silently fold it into the reference note and lose the history.

3. Don't invent hardware specs, model names, or outcomes the user didn't actually state.

4. This is an append-only running log — add new entries, don't rewrite or reorganize
   past ones unless asked.
