---
name: venture-ideate
description: >
  Generate new venture ideas from scratch — grounded in real, independently-verified
  market research, not brainstormed from stale knowledge or vendor/platform marketing.
  Defaults to the user's standing criteria (updated 2026-07-31): genuinely viable (real,
  checkable evidence of demand — not "how I made $10K/month" blog content), operable
  with truly ZERO other humans in any capacity (no employees, no contractors, no
  fractional experts — the founder plus AI agents/tools only), remote, no
  warehouse/physical-fulfillment requirement. Start at a real, verified scale and grow
  rather than demanding a big number from day one — a small, genuinely zero-human,
  evidence-backed business beats an unverified "$1M+" or "$1K/week" claim. Trigger on
  requests like "generate some venture ideas," "what businesses could I start solo with
  AI agents," or "find me a real zero-employee business." Different from
  venture-idea-capture (logs an idea the user already has) and venture-validate
  (researches one specific, already-named idea).
---

1. Confirm the generation criteria before researching, defaulting to the standing
   profile if the user doesn't override it: genuinely viable with independently
   checkable evidence, zero other humans in any capacity (not just no payroll — no
   subcontractors or fractional experts either, unless the user explicitly says
   otherwise), remote, no warehouse/large team. Default income framing is "start real
   and grow," not a fixed $1M or $1K/week bar — ask only if the user implies a specific
   target or a willingness to relax the zero-human rule.

2. Delegate market-scanning to the `venture-research` agent rather than brainstorming
   from training knowledge alone. Explicitly instruct it to prioritize independently
   checkable evidence — acquisition-marketplace disclosures, detailed first-person
   accounts specific enough to verify, real journalism — and to explicitly exclude
   platform/vendor marketing pages and generic "how I made $X" listicle content as
   evidence, per the 2026-07-31 finding that this genre produced confidently-wrong
   numbers (the voice-agent-reselling and initial zero-human sweeps both had to walk
   back "High confidence" claims once checked against primary sources).

3. Apply the zero-human test explicitly to every candidate: does it genuinely run with
   no other person touching delivery at all, or does the real-world version (check the
   actual operator's own account, not a vendor's description of the category) turn out
   to use a contractor, freelancer, or unpaid partner for at least one function (support,
   security, localization, quality review)? Treat that as disqualifying under the
   default profile, and say so plainly rather than soft-pedaling it — the most-cited
   "solo, zero-employee" success stories in this space (Pieter Levels, Tony Dinh, Japan
   Dev) all turned out to fail this test on inspection.

4. Filter hard. A short list of real, evidence-checked candidates beats a long list of
   padded ones — including reporting zero candidates plainly if nothing survives both
   the demand-evidence check and the zero-human test, rather than manufacturing a
   plausible-sounding one to fill the list.

5. Capture each surviving candidate as a new Raw card in [[App Ideas]], matching the
   existing card format (Status: Raw, Problem, Target audience, Why now / unfair
   advantage, Effort estimate, Confidence, Next step), with a source/date note citing
   this ideation session.

6. Log the session in [[Venture Search Log]]: what criteria were used, how many
   candidates were checked vs. captured, and why the dropped ones didn't make it.

7. Don't deep-validate any candidate here — that's still `venture-validate`'s job once
   the user picks one to pursue further.
