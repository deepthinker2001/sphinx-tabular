# sphinx-tabular

## Features

- New plain text CSV file formats that are backwards compatible with CSV: `.rcsv` and `.mcsv`.

    - Spreadsheet applications will not interpret the embedded `sphinx-tabular` commands; they will display as plain text.

- Easily merge cells.

    - `<`  merge this cell with the one to the left of it.
    - `^`  merge this cell with the one above it.

- CSV can be imported from an external file or inline with the directive.
- Interpret text as reStructuredText (`.rcsv`) or Markdown (`.mcsv`) with two new directives:

    - `.. rcsv-table::`
    - `.. mcsv-table::`

- Optional sticky header support for one or more header rows.
- Provides a minimal set of spreadsheet functions with cell referencing.

    - `'Text` literal rendering of text without evaluation.
    - `=CELL` cell refernces.
    * `=CELL1:CELL2` range references.
    - `=ALIGN()` aligns the cell contents in the horizontal and vertical directions.
    - `=CONCAT()` joins text, cell references, icons, and status pills into one rendered cell.
    - `=ICON()` generates a Font Awesome or Bootstrap icon with fallback icons if your theme doesn't support those.
    - `=IF()` conditionally renders one value or another using `==`, `!=`, or `<>` comparisons.
    - `=STATUS()` generates a status pill with text and color.
    - `=SUM()` totals numeric values from cells, ranges, or literal arguments.

## Dependencies

- "python3>3.11"
- "sphinx>=7"
- "docutils>=0.20"
- "myst-parser>=5"

## Installation

    pip install sphinx-tabular

## conf.py setup

Add `"sphinx_tabular",` to your extensions list like this:

    extensions = [
        ...,
        "sphinx_tabular",
        ...,
        ]

Copy and paste this into your extensions in `conf.py`:

    "sphinx_tabular",


## Directives

### rcsv-table

Table values will be rendered as reStructuredText.

#### Inline 

    .. rcsv-table:: Title
        :header-rows: 2
        :width: 100%
        :class: 
        :sticky-header:

        Table, Data, Here
        1, 2, 3

#### From a file

    .. rcsv-table:: Title
        :file: test.rcsv
        :header-rows: 2
        :width: 100%
        :class: 
        :sticky-header:

### mcsv-table

Table values will be rendered as Markdown.

#### Inline

    .. mcsv-table:: Title
        :header-rows: 2
        :width: 100%
        :class: 
        :sticky-header:

        Table, Data, Here
        1, 2, 3

#### From a file

    .. mcsv-table:: Title
        :file: test.mcsv
        :header-rows: 2
        :width: 100%
        :class: 
        :sticky-header:

### Fields

- `:file:` Optional. Path to the `.rcsv` or `.mcsv` file.
- `:header-rows:` Optional. Number of top rows to format as header rows. If `:sticky-header:` is set, these rows become sticky.
- `:width:` Optional. CSS width for the table, such as `100%`.
- `:widths:` Optional. A space-separated list of column widths.
- `:class:` Optional. Additional classes to add to the table.
- `:sticky-header:` Optional. Make the header rows sticky when scrolling long tables.
- `:sticky-offset:` Optional. CSS offset for sticky headers, such as `3.5rem`.
- `:strict:` Optional. Treat ragged rows and malformed input as errors instead of warnings.

## Merge markers

These markers should be in a cell by itself with no other text and unquoted.

- `<` merge this cell with the one to the left.
- `^` merge this cell with the one above it.

### Examples

This will render `Location` as a single cell with two cells beneath it. `Country` will have a vertical span of 2 columns with 2 rows besides it: `Ort/Region/State` and `Postal Code`.

- `Location`,<
- `Country, Ort/Region/State`
- `^,Postal Code`


## Formulas



### Circular References

Circular references will display `#CYCLE!` because they are invalid.

Example:

    A, B
    =B2,=A2



### Alignment

Align a cell's contents horizontally or vertically. Default alignment is `left` and `middle`.

#### Function

- `=ALIGN(VALUE; HORIZONTAL; VERTICAL)`
- `=HALIGN(VALUE; HORIZONTAL)`
- `=VALIGN(VALUE; VERTICAL)`

#### VALUE

The value that will appear in the rendered cell.

#### HORIZONTAL Values

- `l` or `left`
- `c` or `center`
- `r` or `right`
- `j` or `justify`

#### VERTICAL Values

- `t` or `top`
- `m` or `middle`
- `b` or `bottom`

#### Rendered Classes

Rendered class will use the full names.

- `sphinx-tabular-halign-center`
- `sphinx-tabular-valign-middle`

#### Examples

- `=ALIGN(B4; center; middle)` displays the contents of cell `B4` horizontally centered and vertically middle-aligned.
- `=ALIGN(STATUS(Active; green); r; b)` displays a status pill aligned right and bottom.
- `=B4 | ALIGN(c; m)` displays the contents of cell `B4` centered and middle-aligned.

#### Pipe Modifier Example

- `=B4 | ALIGN(c; m)` displays the `B4` cell contents centered and middle.


#### Shortcuts

- `=B4 | CM` displays the contents of cell `B4` center and middle.
- `=B4 | LT` displays the contents of cell `B4` left and top.
- `=B4 | RB` displays the contents of cell `B4` right and bottom.


### Cell References

Place the value from another cell in the current cell.

- `=A1` Place the value of cell `A1` in this cell.
- `=BB12` Place the value of cell `BB12` in this cell.
- `=STATUS(B2;C4)` Place a status pill with the text from `B2` and the color from `C4`.





### Concatenation

`CONCAT()` joins multiple values together in one rendered cell.

#### Function

* `=CONCAT(VALUE; VALUE; ...)`

#### Fields

Each `VALUE` can be:

* Literal text
* A quoted string
* A cell reference
* A rendered value from another formula, such as `ICON()` or `STATUS()`

Formula arguments use semicolons (`;`) instead of commas.

#### Examples

* `=CONCAT("Status: "; B4)` displays `Status: ` followed by the contents of cell `B4`.
* `=CONCAT(A2; ": "; B2)` joins the contents of `A2`, literal text, and the contents of `B2`.
* `=CONCAT(ICON(fa-solid; circle-check); " "; B4)` displays an icon followed by a space and the contents of `B4`.
* `=CONCAT(STATUS(B4; C4); " "; D4)` displays a status pill followed by a space and the contents of `D4`.

`CONCAT()` preserves rich rendered values. For example, an `ICON()` inside `CONCAT()` still renders as an icon, and a `STATUS()` inside `CONCAT()` still renders as a status pill.

#### Pipe modifier example

* `=CONCAT(ICON(fa-solid; circle-check); " "; "Ready") | CM` displays the icon and text centered horizontally and vertically.




### Icons

Renders a class-based icon span.

`ICON()` emits CSS classes only. To use full Font Awesome or Bootstrap Icons, load those icon fonts locally through your Sphinx theme/static assets.

#### Function

- `=ICON(ICON_SET; ICON_NAME)`
- `=ICON(ICON_SET; ICON_NAME; ACCESSIBLE_LABEL)` [Optional]

#### Fields

See the Font Awesome or Bootstrap icon website for the actual names of the icons.

`ICON_SET`:

- `fa-solid` from Font Awesome.
- `fa-regular` from Font Awesome.
- `fa-brands` from Font Awesome.
- `bi` for Bootstrap Icons.


`ICON_NAME` is the name of the Font Awesome or Bootstrap icon.

Font Awesome is similar to `circle-check`, `github`.

Bootstrap is similar to `exclamation-triangle`.

`ACCESSIBLE_LABEL` sets the aria label for accessibility.

### Conditional Rendering

`IF()` conditionally renders one value when a comparison is true and another value when the comparison is false.

#### Function

* `=IF(CONDITION; TRUE_VALUE; FALSE_VALUE)`

#### Condition syntax

Conditions currently support these comparison operators:

- `==` equals
- `!=` not equals
- `<>` not equals
- `>` greater than
- `>=` greater than or equal
- `<` less than
- `<=` less than or equal

Single equals (`=`) is not supported as a comparison operator. Use `==` for equality checks.

Equality comparisons are string-based. Numeric comparisons with `>`, `>=`, `<`, and `<=` require both sides to be numeric.

#### Fields

* `CONDITION` is a comparison between two values.
* `TRUE_VALUE` is rendered when the condition is true.
* `FALSE_VALUE` is rendered when the condition is false.

Each value can be:

* Literal text
* A quoted string
* A cell reference
* A rendered value from another formula, such as `STATUS()`, `ICON()`, or `CONCAT()`

#### Examples

* `=IF(B2 == "Active"; STATUS(B2; green); STATUS(B2; gray))` displays a green status pill when `B2` is `Active`; otherwise it displays a gray status pill.
* `=IF(B3 != "Blocked"; ICON(fa-solid; circle-check); ICON(fa-solid; triangle-exclamation))` displays a check icon unless `B3` is `Blocked`.
* `=IF(B4 <> ""; CONCAT(ICON(fa-solid; circle-check); " "; B4); "")` displays an icon and text when `B4` is not empty.
- `=IF(C2 >= 90; STATUS(Passing; green); STATUS(Failing; red))` displays a green status when `C2` is 90 or higher.
- `=IF(D2 < 1; STATUS(Blocked; red); STATUS(Ready; green))` displays a red status when `D2` is less than 1.

`IF()` evaluates only the selected branch. If the condition is true, the false branch is not evaluated. If the condition is false, the true branch is not evaluated.




### Literal Cell Rendering

Add a leading single quote `'` to render a formula literally instead of evaluating it.

- `'=STATUS(Active; green)` displays `=STATUS(Active; green)`.


### Range References

Range references select multiple cells using spreadsheet-style coordinates.

#### Syntax

* `=A2:A4`
* `=A2:C4`
* `=CONCAT(A2:A4)`

Ranges are resolved row by row from the top-left cell to the bottom-right cell.

#### Behavior

A range reference can be used anywhere a formula argument is accepted.

Standalone ranges render as comma-separated values:

```csv
Name,State,Rendered
A,Active,
B,Blocked,
C,Ready,=B2:B4
```

Rendered result:

```text
Active, Blocked, Ready
```

Rectangular ranges are resolved in row-major order:

```csv
A2,B2
A3,B3
```

`=A2:B3` resolves as:

```text
A2, B2, A3, B3
```

Reversed ranges are normalized automatically. For example, `=A4:A2` resolves the same cells as `=A2:A4`.

#### Ranges with merged cells

If a range includes a cell hidden by a merge marker, the hidden cell resolves to its visible parent cell.

Example:

```csv
System,Rendered
Ground,
^,=A2:A3
```

The range resolves as:

```text
Ground, Ground
```

#### Ranges with `CONCAT()`

`CONCAT()` flattens ranges.

```csv
=CONCAT("States: "; A2:A4)
```

This joins the values directly:

```text
States: ActiveBlockedReady
```

`CONCAT()` does not automatically add separators. Add separators explicitly when needed:

```csv
=CONCAT(A2; ", "; A3; ", "; A4)
```

#### Notes

Range references provide the foundation for aggregate formulas such as `SUM()`, `AVG()`, `MIN()`, and `MAX()`, but those aggregate functions are not implemented yet.


### Status pills

Renders a status pill.

#### Function

- `=STATUS(LABEL; COLOR)`

#### Fields

- `LABEL` is any text or a cell reference.
- `COLOR` can be:

    - `green` or `success`
    - `yellow` or `warning`
    - `red` or `danger` or `error`
    - `blue` or `info`
    - `gray` (default) or `grey` or `neutral` \
    - `purple`




#### Pipe Modifier Example

- `=B4 | STATUS(C4)` is equivalent to `=STATUS(B4; C4)`.
- `=D4 | STATUS(E4) | CM` displays the `D4` cell contents in a status pill with color from cell `E4` center and middle.

### Summation

`SUM()` totals numeric values from cells, ranges, or literal arguments.

#### Function

* `=SUM(VALUE; VALUE; ...)`

#### Fields

Each `VALUE` can be:

* A literal number
* A cell reference
* A range reference
* Another formula that renders a numeric value

Blank values are ignored.

Non-numeric values are ignored and produce a warning.

If no numeric values are found, `SUM()` returns `0`.

#### Examples

* `=SUM(B2:B4)` totals the numeric values in cells `B2` through `B4`.
* `=SUM(B2; B3; B4)` totals separate cell references.
* `=SUM(B2:B4; 10)` totals a range and a literal number.
* `=IF(SUM(B2:B4) >= 100; STATUS(Passing; green); STATUS(Failing; red))` uses a sum inside a conditional formula.

#### Example table

```csv id="1hkm74"
Name,Value,Rendered
A,1,
B,2,
C,3,
Total,,=SUM(B2:B4)
```

Rendered result:

```text id="bxqh7k"
6
```


## Theme support

`sphinx-tabular` is designed to work with standard Sphinx HTML themes and theme-aware color systems.

The generated tables use semantic CSS classes and CSS custom properties instead of hard-coded theme colors wherever possible. The default stylesheet supports light and dark themes by using `--pst-*` variables when they are available, which makes the extension work well with themes such as `pydata-sphinx-theme` and `sphinx-book-theme`.

For themes that do not provide `--pst-*` variables, `sphinx-tabular` includes fallback colors so tables still render correctly.

The extension supports:

* Light and dark theme styling
* Theme-aware table backgrounds, text colors, borders, and hover states
* Sticky headers
* Header row styling
* Status pill colors
* Alignment classes
* Class-based icons

Projects can override the default appearance by redefining the `--sphinx-tabular-*` CSS variables in their own Sphinx static CSS file.

Example:

```css
:root {
  --sphinx-tabular-border-color: #d0d7de;
  --sphinx-tabular-header-bg: #f6f8fa;
  --sphinx-tabular-header-fg: #24292f;
  --sphinx-tabular-row-hover-bg: #f6f8fa;
}

html[data-theme="dark"] {
  --sphinx-tabular-border-color: #30363d;
  --sphinx-tabular-header-bg: #161b22;
  --sphinx-tabular-header-fg: #f0f6fc;
  --sphinx-tabular-row-hover-bg: #21262d;
}
```

Icon formulas emit CSS classes only. To use the full Font Awesome or Bootstrap Icons icon sets, load those icon styles locally through your Sphinx theme or `_static` directory. `sphinx-tabular` includes small fallback glyphs for a few common icons so tables remain usable in offline/static builds.



## Known limitations

`sphinx-tabular` is intended for documentation tables, not as a full spreadsheet engine.

Current limitations:

* Formula support is intentionally small. The extension currently supports cell references, `STATUS()`, `ICON()`, `ALIGN()`, `HALIGN()`, `VALIGN()`, and pipe modifiers. It does not yet support `AVG()`, `MIN()`, or `MAX()`.

* Formula arguments use semicolons (`;`) instead of commas. This is intentional so formulas can be written naturally inside comma-separated table rows without extra quoting.

* Merge markers are fixed. An unquoted `<` merges with the cell to the left, and an unquoted `^` merges with the cell above. Quoted `"<"` and `"^"` render as literal text. These markers are not currently configurable.

* Complex or invalid merge layouts may produce warnings or unexpected output. The extension is designed for simple horizontal and vertical merges, not arbitrary spreadsheet-like merge regions.

* `.rcsv` cells are parsed as reStructuredText. `.mcsv` cells are parsed with MyST Markdown. Mixing both markup syntaxes in the same table is not supported.

* `.mcsv` support requires `myst-parser`. The extension loads it automatically, but projects should still include `myst-parser` as an installed dependency.

* `ICON()` emits CSS classes only. Full Font Awesome or Bootstrap Icons support requires the project to load those icon styles and fonts locally. `sphinx-tabular` includes fallback glyphs for a small set of common icons, but it does not bundle full icon font libraries.

* Sticky headers use a small JavaScript helper to support multi-row headers. If JavaScript is disabled, tables still render normally, but multi-row sticky header offsets may not work.

* Sticky headers may require theme-specific CSS adjustments in heavily customized Sphinx themes, especially themes that apply unusual table wrappers, overflow rules, or custom table border behavior.

* Tables are normalized to the longest row. Shorter rows are padded with empty cells. In non-strict mode this produces warnings; in strict mode it raises an error.

* The extension does not currently provide an interactive editor. Tables are authored as inline directive content or external `.rcsv` / `.mcsv` files.

* The extension does not bundle DataTables, sorting, filtering, pagination, or other interactive table libraries. Additional classes such as `datatables` are passed through so projects can integrate their own local JavaScript if needed.

* `IF()` numeric comparisons support simple numeric values only. Full arithmetic expressions such as `A2 + B2 > 10` are not currently supported.

* Range references are supported. `SUM()` is implemented, but `AVG()`, `MIN()`, and `MAX()` are not currently implemented.