---
name: job-search-resume-tailor
description: >
  Generate a tailored resume and cover letter for a specific job application, from the
  user's current/master resume plus a target job description. Trigger on requests like
  "tailor my resume for this job," "write a cover letter for this posting," "create a
  resume for [company/role]," or when the user pastes a job description and asks for
  application materials. Keeps a reusable master resume in the vault so each application
  only requires the new job description.
---

1. **Get the master resume.**
   - Check for an existing `Resume - Master.md` in the vault root first.
   - If it exists, use it as the source of truth for the user's real experience —
     don't ask them to re-paste it unless they say it's out of date.
   - If it doesn't exist, ask the user to paste their current resume text (or point to
     a file). Save it verbatim as `Resume - Master.md` at the vault root so future
     applications can skip this step. Note at the top of the file when it was captured.

2. **Get the job description.**
   - Ask for the job description text, or a link to it, if not already provided in the
     request.
   - Check [[Job links]] for a saved posting matching the role/company if the user
     references one already logged there rather than pasting fresh text.
   - If given a URL, fetch it (WebFetch) rather than asking the user to paste the text.

3. **Extract the target's key requirements** from the job description: required
   skills/tools, years of experience, key responsibilities, and any repeated keywords
   (these matter for ATS keyword matching). Note this analysis briefly to the user —
   don't write it to a separate vault file, it's working context for this pass only.

4. **Draft the tailored resume.**
   - Start from `Resume - Master.md`. Reorder, re-emphasize, and rephrase existing
     bullets to foreground what's relevant to this posting, and mirror the job
     description's terminology where the underlying experience genuinely matches.
   - **Never fabricate or inflate** experience, titles, dates, tools, or metrics that
     aren't in the master resume. Tailoring means selection and framing, not invention.
     If the posting wants something the user's master resume doesn't support, flag the
     gap to the user rather than papering over it.
   - Save as `Resume - <Company> - <Role>.md` at the vault root.

5. **Draft the cover letter.**
   - Address the specific company and role. Reference 2-3 concrete points of genuine
     overlap between the master resume and the job description — specific, not
     generic ("I'm a great fit for X" without evidence is filler).
   - Keep it to one page equivalent (roughly 250-400 words).
   - Save as `Cover Letter - <Company> - <Role>.md` at the vault root.

6. **Link both into [[Job Search Hub]]** (create it if it doesn't exist, matching the
   flat-list Hub style used elsewhere in this vault — see [[Greenhouse]] or
   [[Solar Power]] for the pattern). Include [[Job links]] in the hub if not already
   linked there. Add `[[Job Search Hub]]` to [[Personal Hub]] near the existing
   `[[Job links]]` entry if it isn't linked yet.

7. **Offer a submission-ready format.** Ask if the user wants the resume and/or cover
   letter converted to `.docx` for actual submission — if yes, use the `anthropic-skills:docx`
   skill to produce formatted Word versions from the markdown drafts.
