# the-lit-index — generation prompts

Register anchor (`reference/style/warm-editorial-neutral/refs/warm-editorial-swatch.png`) is passed FIRST as the style anchor on every shot. warm editorial ink-and-wash; never neon, 3D/CGI/Pixar, glossy plastic, HUD/arc-reactor comic vocabulary, neo-comic.

## The chain, and why it is shaped this way

`blueprint` is CODE-DRAWN (`generators/lit-index-blueprint/`) and is never generated. It carries the geometry and, deliberately, nothing else: no surface, colour, material or lighting, so no paint can be inherited from it.

**`master` is the seed, and it carries the ROOM.** It conditions on the blueprint for geometry AND on the locked `marcus-study@livingroom` plate for the environment, so the room this object stands in traces to canon instead of being invented. Every state then chains off `master`, which is how the room reaches all four plates.

The first shoot got this wrong and is worth recording. Every state was seeded off the blueprint ALONE, on the reasoning that a state seeded off a sibling state inherits that sibling's light. That reasoning is right about the LIGHT and wrong as a blanket rule: the blueprint is line-only, so seed-only conditioning left nothing at all to carry the environment, and four plates came back in four different rooms (a bookcase and wood floor, an open doorway onto a valley, a bare wall, a third floor). **A shared seed is the only channel a chain has for anything the seed does not draw.** The narrow rule it came from still stands and is handled by negatives instead: `state-dark` is defined by ABSENCE, so its own prompt kills the coral it would otherwise inherit from `master`.

Shots are 1024x1024 because the grid is very nearly square; a landscape plate would be mostly empty room.

## blueprint  -> reference/the-lit-index/blueprint.png
CODE-DRAWN, DO NOT GENERATE. Produced by `generators/lit-index-blueprint/generate.py` and installed here.

## master (1024x1024)  -> reference/the-lit-index/master.png
REFS: marcus-study@livingroom

Warm editorial ink-and-wash illustration. EXACTLY 7 PANELS ACROSS AND 5 HIGH, 35 IN TOTAL: count them.

THE ROOM IS THE ROOM IN THE SECOND REFERENCE IMAGE and must match it: the same family living room at the quiet end of a house, the same soft sofa with its draped blanket, the same shaded table lamp, the same built-in bookshelf, the same window onto a valley at sunset, the same patterned rug with children's picture books and wooden toys left on it. Keep its furniture, its colours and its warm gold lamplight.

Standing against the room's wall is a wall of small upright panels in a complete, regular grid, seven across and five high, following the geometry of the line drawing EXACTLY: every panel the same tall rounded rectangle at the same size, equal gutters in both directions, no gaps and no missing cells, the plane seen straight on and slightly from the left. It is bookcase-sized, about two metres wide, and sits in the room at the scale of the furniture around it. The wall is translucent clay-coral orange (#D97757), glows softly from within, and casts LIGHT rather than shadow onto the rug and the furniture in front of it. Every panel is lit, and the panels hold a warm density of light and nothing else.

NEGATIVES: a different room, an empty room, a bare or featureless wall, a room without furniture; eight columns, six columns, any column count other than seven; readable text, names, numbers, letters, glyphs, labels; any screen, monitor, display, window pane rendered as a screen, dashboard, chart, graph, counter, percentage or progress bar; housing, frame, casing, cabling, wires, pedestal, plinth, stand, floor markings or interface furniture; a control room, operations centre, server room or data centre; architectural or hall-sized scale; neon; 3D, CGI or Pixar rendering; glossy plastic; HUD or arc-reactor comic vocabulary; neo-comic; photorealism; any human figure.

## state-dark (1024x1024)  -> reference/the-lit-index/state-dark.png
Warm editorial ink-and-wash illustration. EXACTLY 7 PANELS ACROSS AND 5 HIGH, 35 IN TOTAL: count them.

THE SAME ROOM AND THE SAME WALL OF PANELS AS THE REFERENCE IMAGE, from the same viewpoint: the same sofa, lamp, bookshelf, window, rug and toys, unchanged. The one difference is the panels. Every panel is UNLIT: ash grey, matte and inert, giving off no light and no colour at all. The grid is complete and undamaged and the panels are simply empty. The only light in the room is the warm gold lamplight and the sunset through the window, and it falls ON the panels from outside rather than coming out of them.

NEGATIVES: coral, orange, any glow or emitted light from the panels, lit panels, warm light coming from the panels; a different room, a bare or featureless wall, missing furniture; cracks, breakage, missing panels, gaps in the grid, rubble, ruin; eight columns, six columns, any column count other than seven; readable text, names, numbers, letters, glyphs, labels; any screen, monitor, display, dashboard, chart or progress bar; housing, frame, cabling, pedestal or interface furniture; a control room or data centre; architectural scale; neon; 3D, CGI or Pixar rendering; glossy plastic; HUD or arc-reactor comic vocabulary; neo-comic; photorealism; any human figure.

## state-filling (1024x1024)  -> reference/the-lit-index/state-filling.png
Warm editorial ink-and-wash illustration. EXACTLY 7 PANELS ACROSS AND 5 HIGH, 35 IN TOTAL: count them.

THE SAME ROOM AND THE SAME WALL OF PANELS AS THE REFERENCE IMAGES, from the same viewpoint, with the same sofa, lamp, bookshelf, window, rug and toys. Roughly a third of the panels are lit translucent clay-coral orange (#D97757) and glowing; the rest are still ash grey and inert. The lit panels are SCATTERED irregularly through the grid, singly and in twos, spread across all five rows and all seven columns, never forming a filled row, a filled column, a solid block, or any shape that could read as a measurement.

NEGATIVES: a filled row, a filled column, a solid lit block, a progress bar, a percentage, a gauge, any chart or measurement; a different room, a bare or featureless wall, missing furniture; eight columns, six columns, any column count other than seven; readable text, names, numbers, letters, glyphs, labels; any screen, monitor, display, dashboard or counter; housing, frame, cabling, pedestal or interface furniture; a control room or data centre; architectural scale; neon; 3D, CGI or Pixar rendering; glossy plastic; HUD or arc-reactor comic vocabulary; neo-comic; photorealism; any human figure.

## state-answering (1024x1024)  -> reference/the-lit-index/state-answering.png
Warm editorial ink-and-wash illustration. EXACTLY 7 PANELS ACROSS AND 5 HIGH, 35 IN TOTAL: count them.

THE SAME ROOM AND THE SAME WALL OF PANELS AS THE REFERENCE IMAGES, from the same viewpoint, with the same sofa, lamp, bookshelf, window, rug and toys. Most panels are lit translucent clay-coral orange (#D97757) and glowing. EXACTLY ONE panel has come out of the grid and floats forward toward the viewer, and the empty gap it left behind is clearly visible in the wall. That single forward panel throws warm coral light down onto ONE open human hand, which is solid, warm gold, unmistakably real, and casting a soft shadow onto the rug. The hand stays out in the room and never touches or enters the wall.

NEGATIVES: two or more panels forward, a closed gapless grid with nothing missing, a hand rendered translucent or coral or glowing, a hand inside or behind the wall, a whole figure, a face; a different room, a bare or featureless wall, missing furniture; eight columns, six columns, any column count other than seven; readable text, names, numbers, letters, glyphs, labels; any screen, monitor, display, dashboard, chart or progress bar; housing, frame, cabling, pedestal or interface furniture; a control room or data centre; architectural scale; neon; 3D, CGI or Pixar rendering; glossy plastic; HUD or arc-reactor comic vocabulary; neo-comic; photorealism.
