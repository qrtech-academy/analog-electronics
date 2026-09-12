# The Book
The course typeset as a book with LuaLaTeX: ten chapters, one per lecture, then the two written
papers and their model answers as appendices. The worked solutions to the exercises stay in the
repository.

---

## Building it
```bash
sudo apt -y install make texlive-luatex texlive-latex-extra fonts-texgyre fonts-texgyre-math \
                    fonts-dejavu-core
make book                      # Writes book/analog-electronics.pdf, dated today.
make book VERSION=v1.2.3       # The same, with the version on the title page.
make -C book clean             # Removes book/build/ and the PDF.
```

The build runs LuaLaTeX until the contents and the cross-references stop moving, then prints any
overfull or underfull lines and LaTeX warnings it found, and fails if a reference is left
undefined. A clean build prints nothing after the `lualatex` lines except a couple of mildly
underfull ones.

---

## Where the figures come from
**The book does not have its own figures.** Every one is included straight from the lecture tree,
as `\bookfigure{lectures/LNN/appendix/images/name.png}{caption}{label}`, so the PNG a chapter shows
is the PNG the lecture shows. Redrawing a figure therefore redraws it in the book:

```bash
make diagrams                  # Redraws every figure from diagrams/, into the lecture trees.
make book                      # Picks them up; the PDF depends on the PNGs.
```

That is the same arrangement as the numbers: `make numbers` checks every value the appendices quote
against `diagrams/models.py`, and the book's prose is a typeset copy of those appendices, so a
number that moves is caught in the Markdown before it reaches here.

The captions are the lectures' own alt text, which is written as a full description of the figure
rather than as a label. That is deliberate in the Markdown, for readers who cannot see the image,
and it makes a good printed caption for the same reason.

---

## Releasing a new edition
The PDF is committed, as `book/analog-electronics.pdf`, so the repository always holds a readable
copy; rebuild it with `make book` and commit it along with any change to the book. Each edition is
also published as a GitHub release, with its version on the title page. The book shares the
repository's version namespace, so push a `vx.y.z` tag:

```bash
git tag v1.2.3
git push origin v1.2.3
```

The [Book workflow](../.github/workflows/book.yml) then builds the PDF with the tag on its title
page and attaches it to a release of the same name. Because the namespace is shared, every version
tag publishes an edition of the book, whether or not the book itself changed.

The README's download link points at the committed PDF in `main`, not at a release, so it always
serves the newest build and never needs updating.

---

## What is where
```text
book.tex                The book: front matter, ten chapters, appendices, in order.
aelbook.sty             Every visual decision: page, type, colours, figures, exercises, papers.
aelbook.lua             How \code{...} typesets an inline name (#, \n, and where it may break).
front/                  Title pages and preface.
chapters/NN/            Chapter NN: chapter.tex (the opener), one file per appendix of lecture
                        LNN, summary.tex (the review) and exercises.tex.
back/exam/              Appendices A to E: the papers and their model answers.
```

Every `.tex` file typeset from course material starts with a comment naming its source, for
example:

```tex
% Section 7.2, from lectures/L07/appendix/b_the_emitter_factor.md.
```

---

## Updating the content
**The course material is the source of truth, and the book follows it.** A chapter's text is a
typeset copy of its lecture's Markdown, so when you change a lecture appendix, make the same change
in the `.tex` file whose header names it. The same holds for `exam/*.md` and `back/exam/`.

Three kinds of content behave differently, and only the first looks after itself:
* **The figures update themselves.** They are included from `lectures/`, so `make diagrams` is the
  only command a redrawn figure needs.
* **Prose, tables and the code specifications do not.** Edit the `.tex` beside the `.md`.
* **The chapter openers and the reviews are written for the book.** `chapters/NN/chapter.tex` is a
  book opener rather than a copy of the lecture's agenda, and `summary.tex` is the lecture
  README's objectives, self-test questions and further reading, reshaped. Keep them in step with
  the lecture README in substance rather than word for word.

A few conventions, so an edit reads like the rest of the book:
* **Code blocks:** `cppcode` (C++), `shell`, and `console` (program output, directory trees, plain
  text).
* **Inline code:** `\code{...}`, written exactly as in the source. Inside it, write `\%` for `%`,
  `\{` or `\}` for an unbalanced brace, `\\` for a backslash, and `\#` for `#` in a heading or
  caption. `\file{...}` is for a path, which breaks only at a slash or a dot.
* **References:** `\secref{c7:app:b}` is the section typeset from appendix B of L07,
  `\secref{c7:sec:b3}` is its subsection B.3, `Exercise~\ref{c7:ex:8}` is exercise C.8 of L07, and
  `Chapter~\ref{c7:ch:smallsignal}` is the chapter itself. The book renumbers everything, so always
  refer by label.
* **Exercises:** `\recall{Title}`, `\handcalc{Title}`, `\design{Title}`, `\codeexercise{Title}` and
  `\crosscheck{Title}`, one macro per kind the lectures use; `\task{What to expect}` for a titled
  part, and `\checkyourself{\code{f}, \code{g}}` for the toolkit functions an exercise names.
* **Papers:** `\question{Title}{Marks}` and `\qpart{a}` in a paper, `\answersection{N}{Title}{Marks}`
  and `\answerhead{a}{Title}{Marks}` in its answers, with `\worth{N}` for a plain mark allocation
  and `\credit{...}` for one that carries a comment.
* **Figures:** `\bookfigure{lectures/.../name.png}{caption}{cN:fig:name}`, the path relative to the
  repository root. An optional first argument sets the width, which defaults to the text measure.
* **A new lecture appendix** is a new file in `chapters/NN/`, `\input` from that chapter's
  `chapter.tex`.

The worked solutions are not in the book. Each chapter's exercises say where they are in the
repository (`lectures/LNN/appendix`), so moving or renaming a solutions appendix means updating
that chapter's `exercises.tex`.

---

## License
The book, its text and the PDF built from it, is released under the repository's
[MIT License](../LICENSE), like every other file here.
