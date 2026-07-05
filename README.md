# sphinx-tabular

[![PyPI](https://img.shields.io/pypi/v/sphinx-tabular.svg)](https://pypi.org/project/sphinx-tabular/)
[![Python](https://img.shields.io/pypi/pyversions/sphinx-tabular.svg)](https://pypi.org/project/sphinx-tabular/)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://deepthinker2001.github.io/sphinx-tabular/)

[Full documentation](https://deepthinker2001.github.io/sphinx-tabular/index.html)


## Donations to help support this project...

[Venmo](https://venmo.com/code?user_id=3950053597120230543&created=1783274674)


## Features

- Sphinx extension.
- Uses standard CSV file format.
- Easily merge table cells with `<` and `^`.
- Support reStructuredText and Markdown.
- Support for inline table data and external files.
- Optional sticky header support for one or more header rows.
- Provides a minimal set of spreadsheet formulas.
- Set table cell alignment and per-cell alignment in both horizontal and vertical directions.
- Set custom cell text and background colors.
- Custom status pill.
- Support for Font Awesome and Bootstrip icons if installed by your theme.



# Installation

`pip install sphinx-tabular`


# conf.py

```bash
extensions = [
    ...,
    'sphinx_tabular',
    ...,
]
```

## Directives

RST, external file:

```RST
.. rcsv-table:: Title
    :file: table.rcsv
```

RST, inline data.

```RST
.. rcsv-table:: Title

    Col 1, Row 1
    Col 2, Row 2
```

Markdown, external file:

```RST
.. rcsv-table:: Title
    :file: table.rcsv
```

Markdown, inline data.

```RST
.. rcsv-table:: Title

    Col 1, Row 1
    Col 2, Row 2
```


## Merging Cells

Columns

```RST
.. rcsv-table:: Title

    Merged,<
    Unmerged, Unmerged
```

Rows

```RST
.. rcsv-table:: Title

    Merged,Unmerged
    ^, Unmerged
```


## Additional Capabilities

See [full documentation](https://deepthinker2001.github.io/sphinx-tabular/) for additional capabilities:

### Formatting

* Custom theming.
* `=ALIGN()` horizontal/vertical cell value alignment.
* `=BG()` set the background cell color.
* `=FG()` set text color.
* `=ICON()` use a Font Awesome or Bootstrap icon, or a fallback.
* `=STATUS()` insert a colored status pill.


### Spreadsheet

* `'` interprest as literal text without evaluation.
* `+`,`-`,`*`,`/` arithmetic operations on cells.
* `=C4` cell references.
* `=A4:B4` cell ranges.
* `=AVG()` take the average.
* `=CONCAT()` concatenation of cell values.
* `=COUNT()` count number of numerical values.
* `=IF()` conditional evaluation.
* `=MAX()` find the maximum value.
* `=MIN()` find the minimum value.
* `=ROUND()` round the number to an int or the specified decimal places.
* `=SUM()` sum a set or range of values.


