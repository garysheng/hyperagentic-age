---
name: make-a-hyperagent-book
description: One-command front door for making an illustrated, narrated picture book in the HYPERAGENTIC AGE universe (hyperagentic-age). A thin cartridge over abu:make-a-book, which owns the chain, the auto-advance policy and every universal render gotcha. This file supplies only what is true of THIS universe. Use when Gary says "make a hyperagent book", "new book in the hyperagent universe", "start a HYPERAGENTIC AGE book about X", or "/make-a-hyperagent-book <idea>". NOT for a brand-new universe (abu:start-new-story-universe) and NOT for editing an existing book (abu:update-book).
---

# Make a HYPERAGENT Book

**Read `abu:make-a-book` FIRST and follow it.** It owns the load-bearing order
(story -> cast -> lock -> render -> cover -> narrate -> deliver -> publish), the auto-advance
policy, the two real gates, the environment, every universal render gotcha, and land-work.

This file is the **cartridge**: only the Hyperagentic Age facts. If you learn something here that
would be true in another universe, promote it to the base skill instead.

## 1. Universe and paths

- **Universe:** `~/Documents/github-repos/hyperagentic-age/universe` (the dir holding
  `universe.json`). Note the `universe/` subdir, unlike Nation of Fire's flat layout.
- Public repo: `github.com/garysheng/hyperagentic-age`.

## 2. Register

**WARM-EDITORIAL**, soft illustrative.

- **Rejected poles:** `neo-comic`, HUD / arc-reactor comic vocabulary, `neon`, 3D / CGI / Pixar,
  glossy plastic. This is NOT a power-armor comic look.
- **Anchor: the CONTENT-NEUTRAL swatch** at `reference/style/warm-editorial-neutral/`, never a
  character portrait. A character-portrait anchor leaks that person's face and clothing into every
  render that does not explicitly feature them; Gary's face and denim jacket once bled across a
  whole book that way. If a book has no recurring human, pass only the neutral anchor plus the
  entity masters it actually needs.
- **Format default:** landscape full-spread `1536x1024`, `layout: "full-spread"`. This is the
  platform's grain (122 of 124 books) and the right register for narrative books. Do NOT default
  to portrait just because the style anchor is a portrait figure; that path-dependence is exactly
  what shipped The Narrow Path portrait the first time. Reserve portrait `art-and-text` for
  genuinely intimate single-character primers, by explicit choice.
- **Full-spread composition:** the caption is a semi-opaque cream card on the bottom of the RIGHT
  half, so keep the bottom-right region calm and set `pos` per spread (`top` when the bottom is
  busy). Avoid the single most important element dead-center, because the gutter splits the image
  at the middle.

## 3. The mark

`A HYPERAGENTIC AGE story`, stamped in back matter by the renderer.

## 4. Universe law

**Real people are stylized editorial likeness, never photoreal.** The subject-approval gate stands
in via the author.

**Public figures ARE publishable. Do NOT hold a book for being about one.** An older form of this
rule said "keep such books private, do not ship a real-person likeness without revisiting it."
That clause invited a revisit, Gary revisited it on 2026-07-25, and it is SUPERSEDED: Nation of
Fire CANON rule 4 governs (public figures depictable by name and likeness, no gate), and The
Narrow Path has shipped publicly with a named, depicted Dario since. The likeness approval itself
is unchanged, and the standing rule stays: **stylized, never photoreal, public professional
persona only, nothing private.** Check the entity's own `realPerson.approval.note` before
inventing a hold.

**Reference matrices for real people are HYPER-REAL by default (Gary, 2026-08-08, SPEC v0.38).**
"Stylized, never photoreal" governs the RENDERED SPREADS, not the reference layer. A realPerson
entity with a photoStack now shoots register-neutral hyper-real automatically (chain_matrix
records `structured.registerNeutral` into canon), because hyper-realism ports down into any
register while a stylized reference cannot recover likeness. Spreads still render warm-editorial;
the neutral plates carry likeness only (compose-spread emits the REGISTER-NEUTRAL MASTER line).
Earned on `david-kobrosky`: his first matrix was shot in-register ink-and-wash and Gary rerolled
it by hand.

**A `realPerson` block needs a `photoStack` that is a NON-EMPTY LIST** of on-disk paths under the
asset root, and an `approval.state` of `gated` or `approved`. A string photoStack gets iterated
character by character and produces dozens of bogus validation errors. Do not add the block until
the photo stack exists; until then keep the likeness intent in `prose.rules` plus a
`stylized-never-photoreal` invariant.

## 4b. In-art text is welcome (Gary, 2026-07-28: "you can put text in the images")

There is no universe-wide no-text law and there should not be one. Baked, readable lettering is a
first-class design element here: a promise on a door, a posted notice, a plaque, a sign.

- **Quote the exact string in the prompt, then spell-check it at crop-zoom on read-back and
  regenerate from scratch on any error.** Short strings spell reliably; long ones garble.
- **`the-constitution` is the exception and keeps its rule:** its pages carry abstract
  principle-marks, NEVER readable text. That distinction is meaningful rather than annoying. The
  internal principles stay unreadable; the thing a lab PUBLISHES is legible on purpose, because
  legibility is what makes it copyable.
- **A repeated exact string across two spreads is how you SHOW a standard spreading.** One door
  carrying the promise, then every door carrying the same words, is an argument no caption can
  make. Both spreads must bake the identical string, and both get spell-checked.

## 5. Entity calibrations

- **Reuse first:** `gary`, `chief-of-agents`, `sub-agent`, `maya`, `chrissy`, `engineer`, the
  `winged-startup` motif, the plates, the laws.
- **`gary`'s locked invariants include a yellow smiley patch (left chest) and an orange
  pixel-mascot patch (right chest).** A prompt saying "denim jacket over a white tee" drops both,
  and he shipped across an entire book in a plain jacket. Name every small invariant, especially
  the tiny distinguishing ones.
- **Do NOT reach for the winged-startup block-stack as the generic hopeful-rising motif.** It
  renders as awkward flying block-towers. Pick the rising motif from what the story is already
  made of; for a lantern book, rising sky-lanterns beat it and cohere with the book's own imagery.

## 6. Delivery

Ships to books.garysheng.com via the platform-delivery skill when the book is blessed and Gary
asks. Private-by-default for real-person books, per the universe law above.

## 6b. Editing a shipped book: know the one-command route first

Edits route to `abu:update-book`. But if the edit is ART-ONLY on one slot — "re-roll the
closing plate", "same cover, warmer light" — the whole reproduction context already sits in
the `.recipe.json` beside the asset, and the route is ONE command with ZERO canon reads:

```bash
python3 <abu>/skills/reroll-slot/scripts/reroll_from_recipe.py \
  books/<book>/closing-plate.png --note "<the one delta>"
```

It replays the recorded generate + conform + publish chain and prints the readback
reminder. Earned in THIS universe: the 2026-08-07 closing-plate edit on
nobody-labeled-the-door took 85 tool calls (71 before the first generation) with the
answer sitting in the recipe the whole time; the reroll verb replays it in one call.

## 7. Worked examples

- **`stories/the-introducer.json` — THE real-person reference instance** (2026-08-08): a
  22-spread ODE spine (subject never arcs; one craft lands on ever-larger objects; the refrain
  changes OBJECTS not mouths), a commissioned private person (david-kobrosky, ships unlisted), a
  spouse cameo (mikaela), a public-figure cameo (gary-vee, photo-stack + single master, the
  dario pattern), and an AGE ERA (`david-kobrosky@college`, anchored on a real young photo).
  Backstory beats carry public receipts (107 brunches, @thebrunchguy, MeetSunday, Forbes) in
  their provenance. ERA CASTING RULE learned here: when a book spans a life, sweep EVERY beat
  for which era it belongs to when the look is created — spreads 5 and 6 shipped in the adult
  shirt during the Brunch Club years and Gary caught it in the reader.
- `stories/ai-safety-primer.json` — a 5-spread primer of Anthropic's AI-safety worldview, beats
  traced to the culture-interview corpus.
- The published trilogy: The Narrow Path, A Book to Live By, Machines of Loving Grace.

## Skill improvement
A lesson true of any universe goes in `abu:make-a-book`, not here. Only Hyperagentic Age
facts live in this file.
