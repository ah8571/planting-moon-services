# Directory Edits Audit

Date: 2026-03-15

## Status

- `public/data/directories.json` parses successfully.
- No duplicate `id` values remain.
- Most of the plan has been represented in the dataset.
- A smaller set of entries are still partial, ambiguous, or contradicted by the plan itself.

## Well Represented

These plan items are already reflected in `directories.json` closely enough to archive the original request without losing intent:

- Callupcontact
- Onepagelove
- Viesearch
- Startus
- Land Book
- Webdesign Inspiration
- Dynamicbusiness
- Addon Biz
- Pitchwall pricing note
- Ideakiln URL correction and pricing note
- Curated
- Nocodefounders
- Nocodelist
- Resource FYI URL correction
- SubmitMySaaS pricing note
- Startup88 URL and pricing note
- Uneed submission URL and pricing note
- BetaList pricing note and duplicate consolidation
- Startup Ranking consolidation
- SoMuch type update
- Marketing Internet Directory type update
- Toolpilot URL consolidation
- Startupslab.site consolidation
- Launching Next consolidation
- Paggu URL, description, and type update
- Startup Base consolidation
- SoftwareWorld consolidation
- SaaSHunt consolidation
- AITOOLS consolidation to the `aitools.inc` record
- FoundrList entry exists
- Killer Startups entry exists with `Guest Posting`

## Still Partial Or Ambiguous

These items exist, but the current JSON does not fully match the plan notes:

### Type mismatches or incomplete categorization

- Webdesignernews: still typed as `SaaS Directory` instead of `Guest Posting`.
- Devhunt: present as `SaaS Directory`, but the plan also asked for an `Open-Source` angle.
- Brouseai: present, but still looks like a generic imported record and is not yet clearly AI-only.
- Shno: present, but still typed as `SaaS Directory`; the plan explicitly marked this item uncertain as a no-code directory.
- FoundrList: present, but currently typed as `Launch Platform` and `SaaS Directory`; the plan also called for AI and Startup positioning.
- OpenHunts: pricing note was added, but `submissionType` still reads `free`.
- Launching Next: consolidated correctly, but it still uses the existing `Launch Platform` taxonomy instead of a separate `Launchpad` label from the plan wording.

### Ambiguous source decisions still visible in the data

- AITOOLS: the plan called out multiple possible sites. The JSON now keeps `https://aitools.inc`, but the plan never definitively resolved that ambiguity.
- Supertools: represented as The Rundown's Supertools, but the plan note about `supertools` vs `rundown.ai` is still only implicitly handled, not explicitly documented in the entry.

## Contradictions Inside The Plan

These are the main reasons the plan is not fully archive-ready as a pure completed checklist:

- `openlaunch.ai` is listed as a new entry to add, but `Open Launch` also appears in the remove list.
- `ShipyardHQ` appears in the remove list, but both `shipyardhq` and the launchdirectories-style Shipyard entry remain represented in the dataset lineage.
- `Ben's Bites` is called out for removal in one place, but the main `bens-bites` entry still exists.
- `Submission Web Directory` is in the remove list, but the entry still exists.
- `Scoutforge` is in the remove list, but the entry still exists.

## Missing Or Not Clearly Represented

These plan items still look unresolved or absent as stated:

- `startupspotlight` does not appear to be present.
- `openlaunch.ai` specifically does not appear; the current record is `open-launch.com`.
- The plan's explicit remove instructions for `Open Launch`, `ShipyardHQ`, `Scoutforge`, `Submission Web Directory`, and the Ben's Bites removal note have not been reflected yet.

## Archive Recommendation

The plan is close to archive-ready, but not fully clean yet.

Recommended before archiving:

1. Decide whether to keep or remove `Open Launch`.
2. Decide whether the remove-list items should actually be removed from `directories.json`.
3. Resolve the remaining type mismatches for Webdesignernews, Devhunt, Brouseai, Shno, and FoundrList.
4. Either mark the unresolved AITOOLS and Supertools notes as intentionally decided, or make one more small cleanup pass.

After those decisions, the plan can be archived with much less risk of losing unfinished work.
