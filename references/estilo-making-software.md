# Making Software — Style Reference
> blueprint ink on a reading-room page. Set calm serif prose against labelled cobalt line drawings, typewriter mono captions, and almost no chrome at all.

**Theme:** light

Source measurements are normalized; roles and recommendations are interpreted. Font summary lists are independent, not paired by position. HTML examples are reconstructions, not source components.

Making Software is a long-form reference manual laid out like a printed technical book on a near-white Paper #fbfbfb page. One cobalt, Blueprint Blue #103dff, carries the whole identity: the pixel wordmark, the exploded isometric diagrams of floppy disks, CRTs and keyswitches, and every arrowed callout label, shaded through periwinkle and ice tints. Arizona, a bookish serif, sets justified 14px prose with a drop cap at a generous 1.6 line-height, while Departure Mono, a pixel monospace, handles uppercase chapter heads, figure numbers and captions. Chrome is almost absent: 1px hairlines, a 4px bevelled key-cap button and dotted leader lines.

## Colors

| Name | Value | Role |
|------|-------|------|
| Paper | `#fbfbfb` | The single page canvas behind every section, the masthead and the FAQ card; there are no tinted bands |
| Ink | `#000000` | All prose, the Table of Contents rule, chapter heads, button labels and the typewriter footer lines |
| Blueprint Blue | `#103dff` | The pixel wordmark, diagram callout labels, the progress bar and the active WORDS toggle — one cobalt reads as printed blueprint ink, not a UI accent |
| Ash Gray | `#7d7d7d` | Black at 50% for figure numbers, word counts, IN/OUT labels and the button outline — the quiet metadata layer |
| Schematic Blue | `#0043ff` | Line strokes, arrows, dashed guides and solid fills inside the technical illustrations — the working ink of every drawing |
| Periwinkle Fill | `#97acff` | Mid-tone shading on illustrated parts such as the magnetic disk and keyswitch boot — the shadow side of the cobalt |
| Cornflower Tint | `#b6c8ff` | Secondary part shading and hatched cut faces inside diagrams, one step lighter than Periwinkle Fill |
| Ice Wash | `#e6ebff` | The palest blue tint on drawn surfaces, used for lit planes of isometric objects and soft light cones |
| Diagram Mist | `#f4f5f9` | Cool off-white fill for the body of drawn objects, a half-step cooler than the page so parts read as paper cutouts |
| Hairline | `#e1e1e1` | Black at 10% for the FAQ card border and the rule between its rows; the only container edge on the page |
| White | `#ffffff` | Brightest faces of illustrated objects such as disk platters and dust liners, and the bevel highlight on the key button |

## Typography

### arizona — The reading voice for prose, the masthead lede, Table of Contents entries, FAQ answers and the Early Access block. A warm, slightly calligraphic book serif set small at 14px/400 with a 22.4px (1.6) line-height in justified columns and an airy 28px (2.0) in the chapter list; 16px/500 and 14px/600 do the heading work instead of size jumps, so hierarchy stays quiet and literary.
- **Substitute:** EB Garamond
- **Weights:** 400, 500, 600, 700
- **Sizes:** 12px, 14px, 16px
- **Line height:** 1.17, 1.43, 1.50, 1.60, 1.71, 1.80, 2.00
- **Letter spacing:** 0px at 14px and 16px; -0.08px at 12px on the progress-bar glyphs
- **OpenType features:** `"calt"`

### Departure Mono — A pixel-grid monospace for everything mechanical: uppercase chapter heads at 14px/400 with 20px line-height, the 12px/400 uppercase button and footer at 16px, and 10px figure numbers, word counts and stat labels. Zero tracking throughout; its bitmap edges echo the pixel wordmark and make captions read like a typewritten technical drawing.
- **Substitute:** Departure Mono, monospace
- **Weights:** 400
- **Sizes:** 10px, 12px, 14px
- **Line height:** 0.80, 1.33, 1.40, 1.43, 2.24, 2.88
- **Letter spacing:** 0px at 10px, 12px and 14px
- **OpenType features:** `"calt"`

### Type Scale

| Role | Family | Weight | Size | Line Height | Letter Spacing |
|------|--------|--------|------|-------------|----------------|
| caption | Departure Mono | 400 | 10px | 1.4 | 0px |
| label | Departure Mono | 400 | 12px | 1.33 | 0px |
| body | arizona | 400 | 14px | 1.6 | 0px |
| list | arizona | 400 | 14px | 2 | 0px |
| eyebrow | Departure Mono | 400 | 14px | 1.43 | 0px |
| heading | arizona | 500 | 16px | 1.5 | 0px |
| lede | arizona | 400 | 16px | 1.8 | 0px |

## Spacing & Layout

**Base unit:** 4px

**Density:** spacious

- **Page max-width:** 1536px
- **Section gap:** 256px
- **Card padding:** 16px
- **Element gap:** 16px

### Border Radius

- **buttons:** 4px
- **cards:** 4px
- **images:** 0px

## Components

### Pixel Masthead Bar
**Role:** Book title and author header

A 128px-high transparent band on Paper with the Blueprint Blue #103dff pixel-bitmap MAKING SOFTWARE wordmark at left and two right-aligned arizona lines at 16px with 28.8px line-height: the lede at 400 and the author credit at 500, both Ink. No nav links, no border, no shadow.

### Glyph Divider Strip
**Role:** Section break rule

A full-width row of repeated double-dash glyphs in Ash Gray #7d7d7d spanning the 72px-inset content width, optionally broken in the centre by a Departure Mono 12px/400 uppercase MAKING SOFTWARE label at 16px line-height. Replaces a solid rule between major blocks.

### Drop Cap Prose Column
**Role:** Long-form reading text

Justified Ink arizona 14px/400 at 22.4px line-height and 0px tracking in a column about 427px wide, opened by a two-line serif drop cap. Paragraphs separate with 32px margins; small figures interleave directly between paragraphs with no frame.

### Blueprint Figure Panel
**Role:** Labelled technical illustration

A square-cornered 0px figure on a faint dotted grid with no border or shadow. Ash Gray #7d7d7d Departure Mono 10px/400 uppercase FIG_001 rotated at the left edge, a bracketed object name and year rotated at right, and Blueprint Blue mono callouts with arrowed leader lines.

### Bevelled Key Button
**Role:** Primary purchase action

A 28px-high button with rgba(255,255,255,0.502) fill, 1px solid rgba(0,0,0,0.502) border, 4px radius and 0 8px padding. Ink Departure Mono 12px/400 uppercase label at 16px line-height; inset bevel rgba(255,255,255,0.75) 1px 1px 0 2px plus rgba(0,0,0,0.1) -1px -1px 0 2px. No outer shadow.

### Ruled Section Header
**Role:** Table of Contents heading line

Ink arizona 16px/400 title with a trailing period at left, a 1px solid #000000 horizontal rule filling the row, and a Departure Mono 12px/400 uppercase PROGRESS · WORDS toggle at right where the active option turns Blueprint Blue #103dff.

### Chapter Index List
**Role:** Three-column table of contents

Numbered Departure Mono 14px/400 uppercase chapter heads at 20px line-height, then bulleted arizona 14px/400 entries at 28px line-height joined by a dotted leader to an Ash Gray #7d7d7d Departure Mono 10px word count such as 3.6K WORDS. Three equal columns, 64px gaps.

### Dithered Progress Meter
**Role:** Book completion status

A centred block under a 1px Ink rule: arizona 16px/400 Current Progress label at left, a Blueprint Blue #103dff bar of arizona 12px block glyphs at -0.08px tracking fading into a dithered tail at right, then a two-column grid of Ash Gray Departure Mono 10px/400 labels with Ink values at 14px line-height.

### IN/OUT FAQ Card
**Role:** Question and answer reader

A Paper #fbfbfb card with 1px solid rgba(0,0,0,0.102) border, 4px radius and 0px outer padding; rows split by a Hairline #e1e1e1 rule. Ash Gray Departure Mono IN: and OUT: labels, the question in Ink uppercase mono, the answer in arizona 14px/400 at 24px line-height.

### Blurred Question Rail
**Role:** FAQ question picker

A left list of arizona 14px/600 questions at 24px line-height; the active one is sharp Ink with Departure Mono 14px up and down arrow buttons (24px square, transparent, 0px radius), while neighbours fade out under progressive blur.

### Early Access Block
**Role:** Centred purchase call to action

Centred stack on Paper: arizona 16px/500 heading at 24px line-height, two lines of arizona 14px/400 copy at 24px, a Bevelled Key Button, then an arizona 14px line ending in an underlined Join the mailing list link. 16px gaps; no card behind it.

### Typewriter Footer
**Role:** Colophon and closing

A 508px-high transparent footer: a centred *** ornament, then centred Ink Departure Mono 12px/400 uppercase lines at 16px line-height framed with pipes, ending in a full-width dithered gray pixel band along the bottom edge. No links grid, no border.

## Do's and Don'ts

### Do
- Use Paper #fbfbfb as the only page canvas and let every section sit on it with roughly 256px of empty space between blocks.
- Set reading prose in arizona 14px/400 with 22.4px line-height, justified, in a column about 427px wide, opening with a two-line serif drop cap.
- Reserve Blueprint Blue #103dff for the pixel wordmark, diagram callout labels and active toggles; body text stays Ink #000000.
- Set chapter heads, captions and buttons in Departure Mono uppercase: 14px/400 for chapter heads, 12px/400 at 16px line-height for buttons and footer.
- Keep metadata such as FIG_001 numbers, word counts and IN/OUT labels in Ash Gray #7d7d7d Departure Mono at 10px.
- Build illustrations as isometric line drawings in Schematic Blue #0043ff shaded with Periwinkle Fill #97acff, Ice Wash #e6ebff and White, labelled with arrowed mono callouts.
- Apply the 4px radius with a 1px border only to the key button and FAQ card; leave figures and rules square at 0px.

### Don't
- Do not introduce a second brand hue; every colourful pixel on the page is a tint of Blueprint Blue #103dff.
- Do not use photography, gradients or product screenshots; imagery is hand-drawn blue technical illustration only.
- Do not set large display headings in the serif; the only big type is the pixel wordmark and headings stay at 16px/500.
- Do not fill buttons with blue; the Early Access control is a translucent white key with a 1px Ash Gray #7d7d7d border and inset bevel.
- Do not add drop shadows, cards with fills or tinted section bands; separation comes from Hairline #e1e1e1 borders and 1px Ink rules.
- Do not track Departure Mono or arizona; both run at 0px letter-spacing at every measured size.
- Do not tighten the prose leading below 22.4px at 14px or the chapter list below 28px; the airy rhythm is part of the book feel.

## Elevation

- **Bevelled Key:** `rgba(255, 255, 255, 0.75) 1px 1px 0px 2px inset, rgba(0, 0, 0, 0.1) -1px -1px 0px 2px inset`

## Surfaces

- **Paper** (`#fbfbfb`) — The whole page canvas, masthead, figure grounds and FAQ card.
- **Diagram Mist** (`#f4f5f9`) — Body fill of drawn objects inside the technical figures.
- **Ice Wash** (`#e6ebff`) — Pale blue lit faces and light cones inside illustrations.

## Imagery

All imagery is original isometric and cutaway technical illustration drawn as SVG in a single blue family: exploded floppy disks, a cathode ray tube, a hard disk drive, a mechanical keyswitch, a pixel Aa glyph and a Gaussian surface. Strokes are thin Schematic Blue lines with dashed construction guides; volumes are shaded flatly with Periwinkle Fill, Cornflower Tint, Ice Wash and White, with diagonal hatching on cut faces. Each figure sits on a faint dotted grid with no frame or radius, a rotated FIG_00N number at its left edge and a bracketed object name and year on its right. Labels are uppercase Departure Mono with arrowed leader lines. There is no photography and no icon set; a dithered gray pixel band closes the footer.

## Layout

A single long, near-white page within a 1536px max width and 72px side margins, composed like a spread from a technical book. The masthead is a 128px band with the blue pixel wordmark at left and a two-line right-aligned serif lede, closed by a full-width row of double-dash glyphs. The opening spread is asymmetric: a narrow left column of justified prose interleaved with small figures beside one large exploded diagram filling the right two-thirds. Later blocks alternate between wide diagrams and short text columns, separated by about 256px of empty space and a centred mono MAKING SOFTWARE divider. The Table of Contents runs three columns under a 1px Ink rule, followed by a centred progress meter, a two-column FAQ, a centred Early Access block and a typewritten footer.

## Similar Brands

- **Bartosz Ciechanowski** — Uses long-form explanatory essays built around precise, labelled technical illustrations of how physical objects and machines work.
- **The Pudding** — Shares an editorial reading layout where custom explanatory graphics, not photography, carry each story.
- **Stripe Press** — Same book-first presentation, treating a website as a carefully typeset print object with serif reading text.
