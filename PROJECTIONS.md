# The projections

This universe declares **six projections**: typed contracts for six genuinely different *kinds* of
deliverable. They exist to prove the [Agentic Brand Universe](https://github.com/garysheng/agentic-brand-universe)
standard generalizes past storybooks, which is the thing it was previously unable to demonstrate.

Every image below was produced by the composer from these contracts. None was hand-assembled.

---

## The ladder

Complexity in this standard is not a matter of taste. It is a **count**: how many invariants span more
than one slot. A cross-slot invariant is one that cannot be checked against a single output in
isolation, and it is the expensive class.

| Projection | Slots | Generators | Cross-slot | What it stresses |
|---|---|---|---|---|
| [explanatory-plate](#explanatory-plate) | 1 | **0** | 0 | whether "deterministic" means anything |
| [artful-plate](#artful-plate) | 1 | 1 | 0 | a style pack with no locked subject |
| [thank-you-card](#thank-you-card) | 2 | 1 | 0 | whether `extends` actually resolves |
| [share-card](#share-card) | 2 | 1 | 1 | code output and model output in one artifact |
| [flyer](#flyer) | 4 | 2 | 1 | one visual voice across several parts |
| [storybook](#storybook) | 2+ | 3 | 1 | identity holding across every page |
| [microbiography](#microbiography) | 2 | 2 | 0 | a text-dominant deliverable, no image at all |
| [plate-book](#plate-book) | 1x N | 1 | **2** | a book with no cast, and a fork that INHERITS |

A meme has zero cross-slot invariants. A picture book has the hardest one there is. That is the whole
axis, and a team can read it off a contract before committing to build anything.

---

## explanatory-plate

**Zero generators.** No model touches this. It is emitted as SVG, because a diagram whose entire value
is that its labels are correct cannot survive a model that silently drops letters, and only vector
follows the reader's light or dark theme.

![The altitudes plate](./examples/explanatory-plate.svg)

Emitter: `agenticstory:explanatory-plate`. Its gate is entirely **computed**, so it costs nothing and
runs on every render: palette-only, content fits the viewBox, column headers fit their column, title
and role present. Two real defects were caught by that gate alone, a clipped viewBox and two colliding
headers, both of which look fine in code and are obvious the moment they render.

It emits **two files from one source**: a theme-aware plate for the wiki and a light-locked copy for
an always-cream surface. That duplication used to be a manual step, which is exactly how a dark plate
once shipped onto a cream slide.

---

## artful-plate

One generated image, no recurring subject, no text ever.

![An ink-line artful plate](./examples/artful-plate.webp)

This projection **pins its provider**, and the reasoning is the interesting part. Where a locked
golden carries the look, any competent model works. Here there is no golden: the model's own hand
*is* the register, so swapping the provider changes the brand. Pinning is correct precisely because
nothing else holds the style.

Its gate is entirely **judged**: no text anywhere, hands loopy and non-anatomical, at most four
elements, ground is one flat palette colour.

---

## plate-book

A short explanatory book told entirely in wordless plates, one per idea, page text set beside them.

It is a **fork of `artful-plate` via `extends`**, and unlike the other fork in this universe it
overrides almost nothing: it inherits the register, the pinned provider, the quirk, and all five
per-slot invariants, and adds only sequence. Fix the hand rule on the parent and both get it.

That inheriting fork is what exposed two holes nothing else had:

1. **The linter never merged `extends` before checking**, so a fork that inherits a generator
   false-failed with `SLOT-NO-GENERATOR`. The field was absent from the file and present at run time.
   The other fork overrode every field it used, which is why this survived until now.
2. **The composer computed the contract's judged invariants and then discarded them**, reading its
   checklist from a bound entity instead. A projection with no cast therefore had no checkable rules
   at all. Every earlier characterless deliverable was a *single* plate, with nothing to judge across.

**Its interesting property is an absence.** With no character bound it carries zero identity
invariants, which makes it the cheapest book this universe can compose. Complexity is a property of
the contract, and this contract says plainly that it is a simple one. Its two cross-slot rules are
about the set rather than a subject: one visual voice across every plate, judged against the pack
anchor and never plate-to-plate, and every plate reading as a distinct idea rather than a restatement
of another.

---

## thank-you-card

`extends: share-card`. It forks the two-panel structure rather than copying it, changing only the
surface and the text schema.

![A thank-you card](./examples/thank-you-card.webp)

This is the projection that proved the contract was **not executable**. Its text panel declared
`{recipient, body, signoff}` and named nothing capable of laying that out, because field names are not
a layout. That is how the standard learned that a slot typed `deterministic` must name an emitter or
the type is decoration.

It also declared a 1200x1200 surface, which makes its art panel aspect **0.333**. No image generator
emits 0.333. The contract was internally coherent, reviewed, and undeliverable, which is how
`producibleAspects` and plan-time feasibility got into the standard.

---

## share-card

**The composite.** A text panel laid out by code, beside an art panel produced by a model, in one
artifact.

![A share card](./examples/share-card.webp)

Systems that model rendering as a single template engine cannot express this, which is why composite
assets are almost always assembled by hand, twice, slightly differently.

Its one cross-slot invariant is **computed**: the art must be generated *at* the panel's aspect, never
cropped from a square. Cropping a square into a tall panel costs about 35 percent and takes exactly the
edges the composition needed, the wings and the outstretched hands. Generating at the panel's ratio
costs 2.4 percent.

---

## flyer

Four slots, three deterministic and one generated, with the first genuinely *judged* cross-slot rule:
one visual voice across the hero and the mark.

Nothing here is new mechanically. It exists in the ladder because it sits between "a card" and "a
book", and a standard that skips the middle of its own range has not been tested across it.

---

## storybook

The hard case, and the reason the rest of the standard looks the way it does.

| | |
|---|---|
| ![Storybook cover](./examples/storybook-cover.webp) | ![Storybook spread](./examples/storybook-spread-01.webp) |

Its cross-slot invariant is identity holding across every page, and getting it right took two
corrections that only execution revealed:

**Itemized, not gestalt.** The first version declared one rule: "character identity holds across every
spread." The bound character carried **fourteen** specific declared properties. Across six generated
spreads, twelve held and one failed in every single one. A judge asked *"is this the same person?"*
says yes and ships it. A judge walking the declared list catches it. Collapsing fourteen checkable
properties into one holistic question throws away all the resolution.

**Against the golden, never pairwise.** All spreads drifted the *same* way, because each inherited the
same drift in the same master-to-generation step. Compared with one another they are perfectly
consistent and uniformly wrong. **Consistency is not fidelity.**

Unlike `artful-plate`, this projection deliberately does **not** pin a provider: a locked character
golden carries identity, so any competent model can hold it. The same rule, applied honestly, lands in
opposite directions on two projections.

---

## Two registers in one composition

A book is not written in one visual language. The narrative pages are painterly and carry the
character; a diagram woven between them is flat, characterless, and belongs to a different register
entirely.

| Narrative register | Plate register |
|---|---|
| ![Narrative spread](./examples/two-registers-narrative.webp) | ![Plate](./examples/two-registers-plate.webp) |

Both came out of **one composition**. Registers bind per slot, not per artifact.

The guard that matters: the plate register lists the storybook cast among its rejected poles, so
handing a character's locked golden into a plate slot is two parts of canon contradicting each other.
The compiler **refuses** it, rather than passing the model a reference image that argues against its own
instructions and hoping it resists.

---

## Running any of this

```bash
# free, instant, no API: catches the failure classes above before you pay for anything
python3 <agenticstory>/skills/lint-universe/scripts/lint.py universe

# compose one artifact from a contract
python3 <agenticstory>/skills/compose/scripts/compose.py composition.json
```

The linter earned itself on its first run by finding a generated slot with no generator declared for
it, a bug that had been silently parking every cover as a defect.
