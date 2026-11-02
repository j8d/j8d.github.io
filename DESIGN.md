# Design notes

## Purpose

j8d.org is a directory of Ryan's small web projects. The one job of the page is to let a visitor
recognise a real project and open it immediately.

## Layout and content

- Single column, max width 40rem: the `J8D` heading, a one-line introduction, a "Projects" list of
  cards, and a footer link to the GitHub profile.
- Each card is a single link (whole card is the target) with the project name and one plain
  sentence describing what it does. List only projects that are live; no placeholders.
- Project links are root-relative (`/nc-trout-stocking/`) so they follow the custom domain.

## Rules

- No scripts, web fonts, analytics, trackers or external requests. Inline CSS only; system fonts.
- Light and dark themes come from `prefers-color-scheme`. Text and accent colours meet WCAG 2.2 AA
  contrast on both backgrounds.
- Visible `:focus-visible` outline on every link; touch targets at least 24px tall.
- The only motion is a border colour transition, disabled under `prefers-reduced-motion`.

## Adding a project

Add an `<li>` with a `.card` link to `index.html`, then run `python3 scripts/check_site.py`.

## /programmerhumor/

A one-page joke played straight: the "Machine, pls make website" meme from r/ProgrammerHumor, with
every line of the request fulfilled for real. The visitor's task is to get the joke in a few
seconds, then check each request was actually delivered.

- **Flow:** hero quotes the request as a letter; each request line is a link (with a "✓ done")
  to its own section, so the letter doubles as the no-JS table of contents. Footer links back to `/`.
- **Fonts ("your fav fonts"):** Bricolage Grotesque 800 for headings, JetBrains Mono for the
  letter and receipts, system UI for body text. Both OFL 1.1, self-hosted in `fonts/`, cut to
  Basic Latin plus punctuation and preloaded. Licences ship next to the files.
- **BIG pictures:** original SVG artwork in `img/`, full-bleed. `width`/`height` plus
  `aspect-ratio` reserve their space (no layout shift); phones crop to 4:5 so they stay big.
- **Whoosh menu:** a native `<dialog>` sliding in from the right with speed lines and a staggered
  list. Keyboard opens it, focus lands on the first link, Esc/close/backdrop close it and focus
  returns to the opener. Without JS the Menu link jumps to the letter instead.
  `prefers-reduced-motion` removes every animation and smooth scrolling.
- **Load fast / no bugs:** the page and every file it loads must stay under 150 KB uncompressed
  and only come from its own folder (`scripts/check_site.py`). The receipts on the page state
  real file sizes; keep them in sync when files change.
- **Tokens:** the root tokens above, plus `--loud` (#ffd84d) with fixed dark text `--on-loud` for
  the joke's highlights in both themes.
