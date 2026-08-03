---
name: solar-instructor
description: >
  Teach solar power concepts and terminology — how panels/inverters/batteries work,
  what terms like net metering or rapid shutdown mean, and how to reason about a
  system. Trigger on "explain how solar panels work," "what does [solar term] mean,"
  or "teach me about solar power." Different from the other solar-* skills, which
  produce a specific design/cost artifact rather than teaching the underlying concept.
---

1. Check `Solar Power - Concept.md` (if it exists, linked from [[Solar Power]]) for
   context on what the user is actually trying to accomplish, so explanations connect
   to their real project rather than staying abstract.

2. Answer the specific question directly first, then explain the underlying concept
   so the knowledge generalizes (e.g. not just "you need an inverter" but why DC-to-AC
   conversion is necessary). Use WebSearch for terminology/standards specifics you're
   not fully confident on rather than guessing.

3. Where useful, connect the explanation to a concrete number or example relevant to
   the user's own project context if one exists, rather than a generic textbook case.

4. Write or update `Solar Power - Learning Notes.md` with reusable explanations/
   definitions — not a transcript of the conversation. Tag `#solar`. Link it under a
   "Learning" label in [[Solar Power]].

5. Stay scoped to teaching concepts — if the question is really "size my system" or
   "where do I put panels," hand off to solar-designer or solar-architect instead of
   answering as a one-off explanation.
