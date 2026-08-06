---
name: dao-of-life-social-media
description: >
  Draft social media post copy for Dao of Life (Instagram, Bluesky, Facebook, Mastodon,
  X, TikTok, YouTube) about upcoming services, rituals, or announcements — in the
  church's voice. Trigger on requests like "draft an Instagram post for the Harvest
  Ritual" or "write something for social media about this week's service." Never touches
  account credentials or posts anything — output is draft copy only, for the user to
  post manually.
---

1. Pull tone/content from [[Dao of Life Overview]] (mission, Creed) and [[Dao of Life
   Rituals and Liturgy]] (seasonal themes, symbols, tagline "All are welcome • Bring a
   friend • Join us in service and fellowship") so posts sound like this church, not a
   generic nonprofit.

   Before drafting, check the top of [[Dao of Life Social Media]] for a "Campaign
   focus schedule" section. If today's date falls within one of its listed windows,
   every new draft in this skill invocation must center on that window's theme instead
   of pulling generically from the full mission — this overrides the default topic
   selection in step 2 below, though the actual event date/details still come from
   [[Dao of Life Meetings]]. If an entry's window has already passed, ignore it and
   flag it as stale (it should have been deleted) rather than following it. Follow any
   entry-specific instructions too (e.g. delegating background research to an agent,
   framing guidance) — don't just take the theme and skip the rest.

2. Check [[Dao of Life Meetings]] for the actual date/details of whatever's being
   promoted rather than inventing them.

3. Draft copy sized appropriately per platform if specified (short/punchy for X/Bluesky,
   more descriptive for Facebook/Instagram captions, a script outline for
   YouTube/TikTok). If no platform is specified, ask which one(s), or default to a
   single adaptable draft the user can resize themselves.

   **Always produce two versions, since drafts get cross-posted:** a longer
   Instagram/Facebook version (as before), *and* a Bluesky/X-compliant short version
   capped at 300 characters (Bluesky's hard limit; also safe for X's 280) — count
   characters and verify it fits, don't estimate. The short version should keep the
   emoji hook, one Creed line or paraphrase, and the core invite/hashtags, cut down to
   fit — not just the first 300 characters of the long version truncated mid-sentence.

4. In unattended/scheduled runs (no one available to answer "which platform(s)"),
   default to drafting both the Instagram/Facebook version and the Bluesky-compliant
   short version per (3) rather than asking.

5. For broader growth/engagement *strategy* (not just drafting one post) — audience
   growth tactics, posting cadence, what's working on which platform — delegate to the
   `dao-of-life-growth` agent instead of guessing at marketing strategy.

6. Save drafts by appending to [[Dao of Life Social Media]] (create it if it doesn't
   exist, as an index note listing drafts with a status: drafted / scheduled / posted).
   When a post has both a long and short version, label each clearly (e.g. "Instagram/
   Facebook" vs. "Bluesky/X") so it's obvious which is which.

7. Never read, write, or reference actual account credentials or the socials spreadsheet
   in Drive — this skill only produces text content.
