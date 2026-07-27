---
name: make-a-hyperagent-book
description: One-command front door for making an illustrated, narrated picture book in the HYPERAGENTIC AGE universe (hyperagentic-age). Given a book idea, it runs the full agenticstory chain in the correct order — story -> cast -> lock -> render -> cover -> deliver — delegating each step to the generic agenticstory:* skills and adding the hyperagentic-age wiring, the environment, and the gotchas learned by running it. Use when Gary says "make a hyperagent book", "new book in the hyperagent universe", "start a HYPERAGENTIC AGE book about X", or "/make-a-hyperagent-book <idea>". NOT for a brand-new universe (that is agenticstory:start-new-story-universe) and NOT for editing an existing book (agenticstory:update-book).
---

# Make a HYPERAGENT Book

The single door over the agenticstory pipeline, wired for the **hyperagentic-age** universe.
The generic engine is a pipeline, not one skill; `render-book` is deliberately LAST. This
skill runs the whole chain in order and delegates every step to the matching
`agenticstory:*` skill. It never reimplements them; it sequences them and supplies the
universe-specific facts and the hard-won gotchas.

**The order is load-bearing: story -> cast -> lock -> render -> cover -> deliver.**
Invoking `render-book` first cannot work (nothing is cast or locked yet).

## Environment (both are non-obvious, both bit on the first run)

- **The engine is NOT pip-installed.** Run the CLI from the repo via PYTHONPATH:
  ```bash
  ENG=~/Documents/github-repos/agenticstory/engine
  PYTHONPATH=$ENG python3 -m agenticstory.cli <cmd> ...
  ```
- **The universe path is** `~/Documents/github-repos/hyperagentic-age/universe` (the dir that
  holds `universe.json`). Pass THIS to every `agenticstory:*` skill and CLI command.
- **Precheck the style lock:** `universe.json` `identity.register.anchor` must be non-null
  (it is: `reference/style/warm-editorial/refs/figure-anchor.png`). If it were null, STOP.
- **The register is WARM-EDITORIAL**, soft illustrative. It explicitly REJECTS
  `neo-comic`, `HUD/arc-reactor comic vocabulary`, `neon`, `3D/CGI/Pixar`, `glossy plastic`.
  This is NOT the Midas power-armor comic look. Every render passes
  `identity.register.anchor` FIRST and bakes the rejected poles as negatives.
- **The mark is** `A HYPERAGENTIC AGE story` (stamped in back matter by the renderer).

## The chain

### 1. Story  ->  `agenticstory:add-story`
Author `stories/<id>.json`: a one-line logline, the **spine** (a primer explains, a thesis
argues, a testimony recounts; never assume hero-journey), the **refrain** (the line the book
returns to), and the **beats** (each with `text`, `characters`, optional `location`, and
**provenance** — every beat traces to a real source; an unsourced vivid detail does not ship).
Then the **casting sweep**: reuse existing entities wherever possible (this universe already
has `gary`, `chief-of-agents`, `sub-agent`, `maya`, `chrissy`, `engineer`, the `winged-startup`
motif, the plates, the laws). Only genuinely new names become new entities.

### 2. Cast  ->  `agenticstory:add-character` / `add-motif` / `add-setting` / `add-visual-metaphor`
For each NEW entity the story names, scaffold it (no art here). Scaffold via the CLI:
```bash
PYTHONPATH=$ENG python3 -m agenticstory.cli add-entity <universe> character <id> --name "<Name>" --origin <story-id>
```
Then fill `structured.invariants` (the load-bearing likeness rules the read-back checks) and
`prose`. **Schema gotchas that failed validate on the first run:**
- `requiredForRender` may list ONLY sheets that are already LOCKED. Leave it **`[]`** at
  scaffold time; `lock-references` populates the sheets and you set it after.
- A **realPerson** entity needs a `realPerson` block whose `photoStack` is a **non-empty list**
  of on-disk paths under the asset root, and whose `approval.state` is `"gated"` or
  `"approved"`. A string photoStack gets iterated character-by-character (dozens of bogus
  errors). Do NOT add the realPerson block until you have gathered the photo stack; until
  then keep the likeness intent in `prose.rules` + a `stylized-never-photoreal` invariant.

**Real people (e.g. a "Dario" character):** stylized editorial likeness, never photoreal.
The subject-approval gate stands in via the author (Gary). Keep such books **private**;
do not ship a recognizable real-person likeness to a public platform without revisiting it.

### 3. Lock  ->  `agenticstory:lock-references`
Generate and lock each new entity's reference matrix. Each shot: `identity.register.anchor`
FIRST, rejected poles as negatives, the shot's angle + the entity's invariants, then
`render-readback` (any DEFECT regenerates FROM SCRATCH, never an edit pass). For a real
person, pass the photo stack and re-add the valid `realPerson` block now. Set the entity's
`requiredForRender` to the shots you locked. Idempotent.

### Format: DEFAULT to landscape full-spread (Gary, strong preference 2026-07-24)

**Render interior spreads as landscape `1536x1024`, and set the manifest `layout: "full-spread"`.** This is the platform's grain (122 of 124 books) and the right register for narrative and epic books. Do NOT default to portrait `art-and-text` just because the style anchor is a portrait figure; that path-dependence is the exact mistake that shipped The Narrow Path portrait the first time.

- **Why 1536x1024 is exact:** the reader shows one landscape image across two 3:4 pages (`2 x 3:4 = 3:2`), so a 3:2 image maps perfectly, no padding and no crop. (Portrait books pad to `1152x1536`; full-spread interiors need NO padding.)
- **The cover stays portrait 3:4** (`1152x1536`) and so does the **closing plate** — only the interior spreads are landscape. Conform the cover from its producible 2:3 render with `conform_cover.py --mode pad` (blurred self-bleed, never flat bars — see step 5).
- **Composition rules for full-spread:** the caption is a semi-opaque cream card on the bottom of the RIGHT half of the spread, so keep the bottom-right region calm (no key face/action there) and set `pos` per spread (`bottom` default; `top` when the bottom is busy; `bottom-left`/`bottom-right` corner cards are narrower). Avoid placing the single most important element dead-center, because the book's gutter splits the image at the middle.
- Reserve portrait `art-and-text` for genuinely intimate, single-character primers (e.g. a quiet teaching book), and only by explicit choice.

**The register anchor must be CONTENT-NEUTRAL, never a character portrait (earned 2026-07-25).** The universe register anchor is a content-neutral warm-editorial swatch (`reference/style/warm-editorial-neutral/`), NOT any character's portrait. A character-portrait anchor leaks that person's face and clothing into every render that does not explicitly feature them (Gary's face + denim jacket bled across a whole book). If a book has NO recurring human, pass only the neutral anchor + the needed entity masters.

**Cast by POSITIVE description; never name the thing you are trying to exclude (earned 2026-07-25).** Negative prompts backfire: "do NOT include a man in a denim jacket, NOBODY wears denim" makes the model render a man in a denim jacket, because naming it plants it. Instead describe who IS in frame concretely (ages, a headscarf, a child, seen-from-behind) and, for a no-humans scene, say only "the little helper alone, no people." Do not mention the excluded look at all.

**Identity fidelity (earned 2026-07-24): put EVERY locked invariant of each featured character into the prompt; do not abbreviate the identity.** Hand-driving the render (rather than letting `canon-resolve` assemble the block) is where signature details silently drop: Gary shipped across a whole book with a PLAIN denim jacket because the prompt said "denim jacket over a white tee" and omitted his locked **yellow smiley patch (left chest)** and **orange pixel-mascot patch (right chest)**. Small invariants (patches, glasses, a pendant) vanish when unstated. Read the entity's `structured.invariants` and name each one, especially the tiny distinguishing ones.

**Motif note (Gary, 2026-07-24): do NOT reach for the winged-startup block-stack ("startup stack flying") as the hopeful-rising motif.** It renders as awkward flying block-towers. Prefer a motif NATIVE to the story: for a lantern/fire book, rising **sky-lanterns** (the carefully-carried fire lifting into the dawn) are far stronger and cohere with the book's own imagery. Pick the rising/hope motif from what the story is already made of, not a reused universe prop.

### 4. Validate + render  ->  `agenticstory:render-book`
```bash
PYTHONPATH=$ENG python3 -m agenticstory.cli validate <universe>            # must be OK
PYTHONPATH=$ENG python3 -m agenticstory.cli assert-story <universe> <id>   # deeper render gate
```
`validate` OK means the ids resolve; it can pass while an entity is an unlocked stub (empty
`requiredForRender`), which would render an INCONSISTENT character. Only proceed to render
once each featured new entity has a locked master in `requiredForRender`. Then
`render-book`: per spread, `canon-resolve` -> generate (register-anchor-first) -> `render-readback`.
Words-before-art holds: run `voice-gate` on the manuscript first.

### 5. Cover  ->  `agenticstory:cover`
Portrait, register anchor first. **BAKE the title, subtitle, and the `A HYPERAGENTIC AGE story` mark INTO the render as integrated hand-painted storybook lettering, not a flat PIL overlay (Gary, 2026-07-25: "make sure the covers are generated so the text isn't just overlaid").** A generated, painted title reads as a real book cover; a font composited on top reads as a slide. Quote the EXACT strings in the prompt ("render the title AS PART OF THE ART, hand-painted integrated lettering... spell every word exactly"). Then READ THE COVER BACK and check the spelling of every line letter by letter; on any misspelling, regenerate FROM SCRATCH (this is the render-readback discipline, and it is what makes baked text safe). PIL-composited type is only a FALLBACK if the model cannot hold the spelling after ~3 tries.

**Cover aspect: NEVER hand-roll the pad. Use the framework tool (earned 2026-07-25, Gary: "very not a fan of the white left-right padding").** Image models emit the cover at a producible tall aspect (2:3, `1024x1536`); the reader wants 3:4 (`1152x1536`). Do NOT pad the width with a flat color: flat bars seam visibly against the art's textured/vignetted background. Run the framework's conform tool, which fills the side panels with a blurred self-bleed (a soft continuation of the art's own colors, so the padding vanishes):

```bash
uv run --with pillow python3 ~/Documents/github-repos/agenticstory/skills/cover/scripts/conform_cover.py \
  <baked-title-cover.png> <out/spread-00-cover.webp> --aspect 3:4 --mode pad
```

`--mode pad` (blurred self-bleed, no keyline) is the DEFAULT cover fill (SPEC §cover-conform). Flat-color side bars are banned.

**The BACK COVER (closing plate, `spread-<N+1>.webp`) needs its OWN title-free art; do NOT reuse the titled front cover (earned 2026-07-25, Gary: "we're missing a back cover").** The reader shows the closing plate BEHIND the overlaid closing verse + note, so it must be clean atmospheric art with generous empty lower space and NO baked title. When the front cover has the title baked in (the default now), there is no untitled version to fall back on, so generate a dedicated title-free back-cover plate (a quiet, tender closing vignette, "no text or lettering anywhere, leave the lower half calm and open"), conform it to portrait 3:4 the same way, and ship it as `spread-<N+1>.webp`. (Older books that composited the title with PIL kept an untitled `cover-art.png` usable as the plate; a baked-title book does not.)

### 6. Deliver  ->  the platform-delivery skill
Ship to books.garysheng.com when the book is blessed and Gary asks.

## Gates honored (inherited from the pipeline)
- Words-before-art + voice-gate; casting reuse-first; register-anchor-first every render;
  read-back-from-scratch on any defect; spine declared not assumed; provenance per beat;
  subject-approval for a real person; render only against locked references.

## First worked example (the reference instance)
`stories/ai-safety-primer.json` — a 5-spread primer of Anthropic's AI-safety worldview,
beats traced to `garyinparadise/.../culture-interview/sources/`, casting reuses
`chief-of-agents` + `gary` + `winged-startup`, one new character `dario` (stylized,
real-person gate via author). Setup is authored, scaffolded, and `validate`-green; the art
run (lock dario -> render 5 spreads -> cover) is the remaining step this skill drives.

## Skill improvement
If the engine's schema or CLI changes (a new required field, a renamed command, a new
`add-*` skill), fix this SKILL.md in the same session per the AGENTS.md skill-improvement rule.

## Land the work -> `agenticstory:land-work` (ALWAYS, never "parked")

**The run is not over until every branch it opened is merged or queued.** Never end
a report with "the branch is committed but parked, main is checked out elsewhere".
Gary has no opinion about merging and never will; that sentence costs a round trip
whose answer is always "use your judgment". Parking is an unfinished job and it
compounds into a pile of stale worktrees.

```bash
ENG=~/Documents/github-repos/agenticstory/engine
# FIRST thing in a run: finish what a previous run could not.
(cd "$ENG" && python3 -m agenticstory.cli land ~/Documents/github-repos/hyperagentic-age --drain-only)
# LAST thing, once per repo the run touched:
(cd "$ENG" && python3 -m agenticstory.cli land ~/Documents/github-repos/hyperagentic-age --branch <work-branch>)
# Housekeeping when worktrees pile up:
(cd "$ENG" && python3 -m agenticstory.cli land ~/Documents/github-repos/hyperagentic-age --prune-stale)
```

Safe by construction: merges only when the target is checked out nowhere or held by
a CLEAN worktree, QUEUES when a live session holds it dirty (the next run drains
it), and never uses `git update-ref` or `git branch -f`. A queued merge is a
SUCCESS worth one line. **Surface only a genuine merge CONFLICT.**
