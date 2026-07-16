# The Hyperagentic Age

The story universe behind Gary Sheng's Anthropic wikis, explainers, and decks — the shared
canon (characters, metaphors, visual laws) that every one of those properties renders from.

Built on the [Agentic Story](https://agenticstory.wiki) framework (spec v0.2): a typed,
git-versioned canon with load-bearing references and quality wired as gates. This repo is the
**canon**; the wiki / decks / explainers are **properties** (projections) over it.

## Layout

```
universe/
  universe.json                 # provenance: names the spec version + framework wiki
  canon/
    entities/                   # typed records (characters, doctrines)
    relations/                  # the graph edges (appears-in, embodies)
    scripts/assert.sh           # the LOAD-BEARING pre-render gate
    README.md                   # engine-generated canon notes
  reference/                    # the universe's own locked art (master + state refs)
  stories/                      # properties: one stub/full record each
CANON.md                        # prose companion (the human-readable tour)
```

## The world in one breath

An agent (a small blocky clay-coral Anthropic-orange mascot) lives in the **digital world** —
translucent, glowing, casting light not shadow. The **Chief of Agents** (grand gold admiral hat)
is the layer a person talks to: it *listens* to one human input, *commands* many sub-agents who do
the hands-on work, and *delivers* the finished work by crossing — once — the hard threshold from the
digital world into the real one (peeking out of a MacBook to hand it over). Rendered warm and
editorial, not comic.

## Working in this repo

- **Validate the canon:** `python3 -m agenticstory.cli validate universe` (from the engine dir), or
  `universe/canon/scripts/assert.sh validate`.
- **Gate a render:** `universe/canon/scripts/assert.sh spread --characters chief-of-agents` — it exits
  non-zero and refuses if any required reference is missing. No renderer may draw a unit whose assert
  has not passed.
- **Grow the universe by making properties:** add a `stories/<id>.json` (stub → full), lock new
  character/setting references, commit. Every canon change is a commit; the diff is the changelog.

Engine + spec: `~/Documents/github-repos/agenticstory` · https://agenticstory.wiki
