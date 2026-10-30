# j8d.github.io

Source for [j8d.org](https://j8d.org/), a directory of Ryan's small web projects.

- Published by GitHub Pages from the root of `main` (branch publishing). `.nojekyll` serves the
  files as-is; `CNAME` records the custom domain.
- Public Pages projects owned by `j8d` without their own custom domain are served under this
  domain, e.g. `https://j8d.org/nc-trout-stocking/`.
- `python3 scripts/check_site.py` runs the static checks used in CI.
- Design rules: [DESIGN.md](DESIGN.md).

Preview locally with `python3 -m http.server` and open http://localhost:8000/.
