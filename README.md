# sphinx-tabular

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

MD, external file:

```RST
.. rcsv-table:: Title
    :file: table.rcsv
```

MD, inline data.

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




