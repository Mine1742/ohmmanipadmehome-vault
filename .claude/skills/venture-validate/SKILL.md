---
name: venture-validate
description: >
  Move a venture idea from Raw to Researching/Validated — market size, competition,
  feasibility, and a go/no-go recommendation. Trigger on requests like "validate this
  idea," "research the market for X," or "is [idea] worth pursuing." Different from
  venture-idea-capture, which just logs an idea cheaply without research.
---

1. Find the idea's card in [[App Ideas]]. If it doesn't have one yet, create it first
   (see venture-idea-capture) before validating.

2. Delegate market/competitor/feasibility research to the `venture-research` agent
   rather than guessing — give it the idea's problem/audience/differentiation as
   context so its research is targeted, not generic.

3. Create a dedicated deep-dive note `Venture Idea - <name>.md`, tagged
   `#entrepreneur`, linked from [[App Ideas]] and [[Entrepreneur Hub]], with sections:
   Problem & audience (recap), Market size & trends, Competitive landscape,
   Differentiation / unfair advantage, Risks & open questions, Recommendation
   (go / no-go / needs more research).

4. Update the idea's status in [[App Ideas]] to Researching or Validated — or Shelved,
   if the research surfaces a clear reason not to pursue it. Don't sugarcoat a bad
   signal just to keep momentum.

5. Log the validation decision and reasoning in [[Venture Search Log]].
