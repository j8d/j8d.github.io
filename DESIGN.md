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
