---
name: az-practice-quiz
description: >
  Quiz the user on Azure AZ-104/AZ-204 material and track weak spots over time.
  Trigger on requests like "quiz me on AZ-104 networking," "test me on Azure Functions,"
  or "how am I doing on AZ-204 prep." Different from az-study-guide, which writes
  reference notes rather than interactive practice.
---

1. Figure out scope: a specific topic, a full exam domain, or "whatever I'm weakest on."
   For the last case, read [[Azure Study Log]] for previously logged weak areas and
   prioritize those.

2. Pull from existing practice-question material first rather than inventing everything
   fresh: `Practice Number 1.md`, `AZ 204 Practice questions.md`,
   `AZ-204_Practice_Questions.md`, and `AZ-204 Practice Questions by Exam Objective` (or
   its sibling files) already contain hundreds of real questions organized by exam
   objective. Generate new questions in that same by-objective style only for gaps these
   don't cover.

3. Administer one question at a time, not a dump — wait for the user's answer before
   revealing the correct one and rationale, the way a real practice exam works.

4. At the end of the session, log a dated entry to [[Azure Study Log]] (create it if it
   doesn't exist): date, cert (AZ-104/AZ-204), topics covered, score (X/Y), and which
   specific topics were missed — these become next session's priority.

5. Don't overwrite prior log entries — this note is an append-only history, oldest or
   newest first is fine but stay consistent with however the note is already ordered.
