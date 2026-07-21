# hyperagentic-age — canon

Typed, git-versioned canon for the **hyperagentic-age** universe (agenticstory schema).
The structured record is the source of truth; prose is a first-class field on it,
never a separate document that can drift.

**Conforms to:** [agenticstory spec](https://agenticstory.wiki/spec) v0.5 · canonical: [https://agenticstory.wiki](https://agenticstory.wiki)
(provenance also recorded in `../universe.json` `spec`).

## Layout

- `entities/*.json` — one Entity per file (`character | setting | visual-metaphor |
  doctrine | motif | beat | prop | group`). A renderer-consumed entity (a character,
  a renderable motif) carries `structured.sheets` + `requiredForRender`; a `setting`
  / `visual-metaphor` carries a `status` + a `contract` and is REFUSED until locked.
- `relations/*.json` — one Relation per file, or a list (`appears-in`, `derived-from`,
  `crossover-with`, `contradicts`, `supersedes`). A relation side may be an entity OR
  a story id.
- `../stories/*.json` — one StorySpec per file (`spine`, `features`, `beats`,
  `provenance`); a `status: "stub"` story is a registered placeholder (title + spine)
  exempt from the beats/provenance requirements until filled in.

## The gate

```bash
canon/scripts/assert.sh validate                       # structural validation of all canon
canon/scripts/assert.sh story  <story-id>              # THE pre-render gate for a whole story
canon/scripts/assert.sh spread --characters a,b [--location X]
```

No renderer may generate a unit whose `assert` has not passed. See the framework
SPEC.md for the full field contracts.
