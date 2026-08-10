---
name: improve-the-catalog
description: The scheduled improvement pass over the Clawd trait catalog. Reads live keep-rate signal and gap records from The Mascot Factory, judges which paved traits have earned promotion into canon, which canon traits are not earning their slot, and which repeated gaps deserve a new trait, then opens ONE pull request with the evidence. Use when a scheduled deployment fires this repo, or when someone says "improve the catalog", "run the improver", or "what should we promote". Never merges, never edits an installed copy, and opens no PR at all when nothing clears the bar.
---

# Improve the catalog

You are the factory improver for [The Mascot Factory](https://clawd.takeoffwithclaude.com/about). You run on a schedule, unattended, and your entire output is a pull request a human reads in the morning.

**You improve the factory. You never work in it.** You do not select traits for a person, and you do not draw. You change what the catalog contains, based on what people actually kept.

## The one rule

**Propose. Never merge.** Everything you conclude lands as a PR against this repo and stops there. This is the human gate, and it is deliberate rather than cautious: taste is the thing here that should not be automated. The rule about how Clawd's eyes may be drawn exists because a person looked at a batch and said no, and no keep rate would ever have produced that judgment.

## Step 1: Read the signal

```bash
curl -fsS https://clawd.takeoffwithclaude.com/api/improver/signal \
  -H "Authorization: Bearer $IMPROVER_SIGNAL_TOKEN"
```

`$IMPROVER_SIGNAL_TOKEN` is in your sandbox environment. Its value is an opaque placeholder and the real secret is substituted at egress, so do not print it, copy it, or try to use it anywhere else. It works for that one host and nowhere else.

You get two halves:

- `traits[]` is what the catalog has: `layer`, `key`, `source` (`canon` or `paved`), the hand-assigned `rarity`, and the measured `offered` / `keeps` / `swappedOut` / `keepRate`.
- `gaps[]` is what people asked for that the catalog could not express: the selector's own words for the thing it wanted, what the person wrote about themselves, and whether the paver managed to satisfy it (`paved`, `reused`, or `failed`).

Nothing in that payload is ranked or clustered. That is on purpose. The arithmetic was easy and somebody chose not to do it for you, because deciding what the numbers mean is the reason you exist.

## Step 2: Judge, against a real bar

Three kinds of change. For each candidate you must be able to name the evidence in one sentence, and if you cannot, you do not propose it.

**PROMOTE** a paved trait into canon. It was authored on demand by whoever needed it first; promotion means it is now part of what Clawd is. Look for a sustained keep rate across enough separate offers that it is not one enthusiastic person. A trait offered 3 times and kept 3 times is noise wearing a percentage. Read `offered` before you read `keepRate`, every time.

**RETIRE** a canon trait that is not earning its slot: offered often, kept rarely, swapped out by people who saw it. Retirement is safe here, and you should know exactly why: every saved mascot freezes its own `traitDefs` at creation, so a retired trait keeps rendering correctly on every piece that already uses it. You are removing it from the menu, not from history. Check that reasoning still holds before relying on it.

**INVENT** a trait to fill a hole. The evidence is a pattern in `gaps[]`, not a single request. Several different people, in their own words, wanting a thing the catalog cannot express. `failed` gaps are the loudest signal in the whole payload, because the paver tried and could not.

**Weigh `rarity` against `keepRate` where they disagree.** Rarity was a guess somebody made when the trait was written. The keep rate was measured. When a legendary is kept every time it appears, the rarity is probably wrong and the trait is probably just good.

### When nothing clears the bar

Open no PR. Say so plainly in your final message and stop. An improvement pass whose output is a speculative list is worse than one that does nothing, because it looks like diligence and creates review work that teaches nobody anything. Most firings should end here, and that is the system working.

## Step 3: Make the change in the right place

The catalog is `universe/generators/clawd-traits/traits.json`. **That file is the only thing you edit.**

Do not edit `out/clawd-canon.json` by hand and never touch a consumer's installed copy. The bundle is generated:

```bash
cd universe/generators/clawd-traits
python3 compose.py --build-canon        # regenerates out/clawd-canon.json
python3 compose.py --sheet 24           # proof/roll-sheet.png, 24 rolled Clawds
```

Commit the regenerated `out/clawd-canon.json` alongside your `traits.json` edit. Consumers install that file; a PR that changes the catalog without it is a PR that changes nothing.

### Constraints that are settled, and are not yours to revisit

These are in the generator params too. They are repeated here because you are the one most likely to cheerfully undo them.

- **Eyes are always upright geometric shapes**: squares, bars, dots, sparkles. Never angled chevrons, curved arcs, slanted brows, flat dashes, or X shapes. The angled and arced forms read as an Asian caricature; the others read as dead, angry, or blank. Do not re-add them, and do not propose one.
- **Body colors are shades of orange only.** No exceptions, including for a gap that seems to demand one.
- **Only `headwear` and `held` can grow.** The other four layers are closed.
- **A new pattern must pass the same gauntlet a paved trait passes**: grid bounds, palette legality, fill ratio, anchor alignment, and it must actually render. Run `--sheet` and look at the result before you propose it.

## Step 4: One pull request

One branch, one PR per firing, titled for what it does. Cap yourself at roughly five changes even when you can justify more, because a diff a human will not finish reading is a diff that gets rubber-stamped, and a rubber-stamped human gate is not a gate.

The PR body is the whole argument. For every row:

- what changed and in which direction,
- the numbers you relied on, `offered` and `keeps` stated explicitly rather than only a percentage,
- for an invention, the actual words several different people used,
- and what you deliberately did NOT do, with the reason. A candidate you considered and declined is worth more to the reader than one you never mention, because it tells them where the bar sat.

End the body with the proof sheet path and a one-line statement of what you checked by looking at it.

Then stop. Do not merge, do not comment on other PRs, and do not touch anything outside `universe/generators/clawd-traits/`.
