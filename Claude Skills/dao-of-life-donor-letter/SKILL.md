---
name: dao-of-life-donor-letter
description: >
  Generate a donor acknowledgment/thank-you letter for a specific Dao of Life gift,
  using the church's actual template library in Drive. Trigger on requests like "write
  a thank-you letter for [donor]'s donation," "acknowledge this gift," or "send a
  year-end summary to a recurring donor."
---

1. Determine the gift type from what the user describes: cash/check/EFT, event
   ticket/quid-pro-quo, non-cash property, in-kind professional services, grant/DAF
   distribution, recurring monthly donor year-end summary, or a restricted/purpose-
   specific gift.

2. Read the real template text fresh from Drive — don't rely on a paraphrase — using the
   Drive connector's read_file_content on `Dao_of_Life_Donor_Acknowledgment_Templates.md`,
   fileId `1OCMmpcKIN1vjuIPtnHpKF_geU5l_gF3h`. Pick the section matching the gift type
   from step 1.

3. Ask for whatever required fields the user hasn't given: donor name, amount, date, and
   — for quid-pro-quo gifts — the fair market value of any goods/services received
   (needed to calculate the deductible portion). Never invent amounts or dates.

4. Apply the built-in rules: written acknowledgment is legally required for any single
   gift ≥$250; quid-pro-quo benefit value must be disclosed for gifts >$75. For non-cash
   property, describe the property only — never state a value — and point the donor to
   Form 8283 for their own appraisal.

5. If the gift sounds unusual or large (real estate, a closely-held business interest,
   tangible property >$5,000, vehicles, art/collectibles, cryptoassets, restricted
   endowments, or naming rights), flag that it needs Board pre-approval per the Gift
   Acceptance Policy and check with the user before drafting the letter as if routine.

6. Save the finished letter as `Dao of Life Donor Letter - <Donor> - YYYY-MM-DD.md`.

7. Add or update the matching row in [[Dao of Life Finances]]' Donations table,
   including the "Ack sent" column, so it's clear the compliance requirement was met.
