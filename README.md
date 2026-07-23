# HYPERAGENTIC AGE

A **brand universe**: a brand held as version-controlled canon plus locked golden assets, in a form an
agent can load and render deliverables from. Built on the
[Agentic Brand Universe](https://github.com/garysheng/agentic-brand-universe) standard (spec v0.6).

> **Third-party material.** The style pack in `universe/reference/style/anthropic-plate/refs/` mirrors
> Anthropic's own published brand illustrations, used as style references so this standard can be
> demonstrated against a real visual language. All rights remain Anthropic's; this project is
> unaffiliated with them. See [NOTICE.md](./NOTICE.md).

## What is here

| Path | What it holds |
|---|---|
| `universe/canon/entities/` | typed records of what is true: characters, motifs, doctrines |
| `universe/reference/` | the **goldens**, the locked assets that are the visual answer of record |
| `universe/reference/style/` | **style packs**: refs, palette, rejected poles, and a read-back gate |
| `universe/projections/` | six typed contracts for six unlike kinds of deliverable |
| `examples/` | real output, produced by the composer from those contracts |

## Start here

**[PROJECTIONS.md](./PROJECTIONS.md)** is the tour: all six projections, what each one stresses, and the
actual artifacts they produced. Read it before the JSON.

## Why six, and why unlike

A framework that produced one kind of thing a hundred times is still unproven. Each new *kind* of
deliverable is what exposes a structural hole. These six were chosen to be deliberately unlike each
other, and executing them produced **twelve distinct design failures** in the standard, none of which
were found by reviewing it:

- a slot type that named nothing capable of producing it
- a declared surface no generator could physically make
- a cross-slot rule written as one gestalt question instead of an itemized checklist
- verification comparing outputs to each other rather than to the golden
- the verifier modelled as an external service instead of a role
- resume logic that restored failures, freezing artifacts permanently broken
- registers bound per composition, so a book could only speak one visual language
- a register that rejects the cast still being handed the cast
- provider quirks bound to a pin, leaving the deliberately portable path unguarded
- an exception that killed a whole run the failure model promised to survive

Each one is now a normative rule in the spec, and most are a free static check in the linter.

## The mark

The universe's own motif is the **winged startup**: a hand-stacked tower of cream blocks with wings,
locked at `universe/reference/winged-startup/`. Every use of it, at every size, derives from that one
master rather than being redrawn, which is the whole point of a golden.

## Related

- [agentic-brand-universe](https://github.com/garysheng/agentic-brand-universe): the standard, the
  engine, the linter, and the composer.
- [Frameworks Are Proven by Variety, Not Volume](https://appliedai.wiki/perspectives/frameworks-are-proven-by-variety-not-volume):
  the write-up of what executing these six taught.
