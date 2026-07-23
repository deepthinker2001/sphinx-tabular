(function () {
  "use strict";

  let sphinxTabularSearchCounter = 0;

  function cssLengthToPx(value) {
    value = (value || "0px").trim();

    if (value === "0") {
      return 0;
    }

    if (value.endsWith("px")) {
      return Number.parseFloat(value) || 0;
    }

    const probe = document.createElement("div");
    probe.style.position = "absolute";
    probe.style.visibility = "hidden";
    probe.style.height = value;
    probe.style.width = "0";
    probe.style.padding = "0";
    probe.style.border = "0";

    document.body.appendChild(probe);
    const px = probe.getBoundingClientRect().height;
    probe.remove();

    return px || 0;
  }

  function updateStickyHeaderOffsets() {
    document
      .querySelectorAll("table.sphinx-tabular-sticky-header")
      .forEach((table) => {
        const thead = table.tHead;

        if (!thead) {
          return;
        }

        table.classList.add("sphinx-tabular-sticky-ready");

        const baseTopValue =
          getComputedStyle(table)
            .getPropertyValue("--sphinx-tabular-sticky-top")
            .trim() || "0px";

        const baseTopPx = cssLengthToPx(baseTopValue);
        let cumulativeOffset = 0;
        const rows = Array.from(thead.rows);

        rows.forEach((row, rowIndex) => {
          const rowTopPx = baseTopPx + cumulativeOffset;
          const cells = Array.from(row.cells);

          cells.forEach((cell) => {
            cell.style.position = "sticky";
            cell.style.top = `${rowTopPx}px`;
            cell.style.zIndex = String(100 - rowIndex);
            cell.style.background =
              "var(--sphinx-tabular-header-bg)";
          });

          cumulativeOffset += row.getBoundingClientRect().height;
        });
      });
  }

  function scheduleStickyHeaderUpdate() {
    updateStickyHeaderOffsets();
    window.requestAnimationFrame(updateStickyHeaderOffsets);
    window.setTimeout(updateStickyHeaderOffsets, 100);
    window.setTimeout(updateStickyHeaderOffsets, 500);
  }

  function initializeSortableTables() {
    document
      .querySelectorAll(
        [
          "table.sphinx-tabular-sortable",
          "table.sphinx-tabular-has-initial-sort",
        ].join(", "))
      .forEach(initializeSortableTable);
  }

  function initializeSortableTable(table) {
  if (table.dataset.sphinxTabularSortInitialized === "true") {
    return;
  }

  const thead = table.tHead;
  const tbody = table.tBodies[0];

  if (!thead || !tbody) {
    return;
  }

  table.dataset.sphinxTabularSortInitialized = "true";

  /*
   * Sorting individual rows is ambiguous when body cells vertically span
   * multiple rows. Disable both initial and interactive sorting until
   * row-group sorting is implemented.
   */
  const hasBodyRowspans = Array.from(tbody.rows).some((row) =>
    Array.from(row.cells).some((cell) => cell.rowSpan > 1)
  );

  if (hasBodyRowspans) {
    table.classList.add("sphinx-tabular-sort-disabled");
    table.dataset.sphinxTabularSortDisabledReason =
      "Body rows contain vertically merged cells.";
    return;
  }

  const bodyRows = Array.from(tbody.rows);

  bodyRows.forEach((row, index) => {
    row.dataset.sphinxTabularOriginalIndex = String(index);
  });

  const leafHeaders = findSortableLeafHeaders(thead);
  const explicitSortTypes = getExplicitSortTypes(table);

  const interactiveSortEnabled =
    table.classList.contains("sphinx-tabular-sortable");

  /*
   * Cache the header path and evaluated body values for every logical
   * leaf column. Initial sorting and interactive sorting resolve their
   * types independently from this shared metadata.
   */
  const columnMetadata = new Map();

  leafHeaders.forEach(({ column, headerText }) => {
    const columnValues = bodyRows.map((row) => {
      const bodyCell = getLogicalCell(row, column);
      return getCellSortValue(bodyCell);
    });

    columnMetadata.set(column, {
      headerText,
      columnValues,
    });
  });

  /*
   * :sort-types: controls interactive sorting only.
   * A column with sort type "none" remains available to :initial-sort:.
   */
  const sortableHeaders = interactiveSortEnabled
    ? leafHeaders.filter(
        ({ column }) => explicitSortTypes.get(column) !== "none"
      )
    : [];

  const textCollator = new Intl.Collator(undefined, {
    sensitivity: "base",
  });

  const naturalCollator = new Intl.Collator(undefined, {
    sensitivity: "base",
    numeric: true,
  });

  /*
   * Interactive state is deliberately independent from the initial sort.
   * The first header click always starts a new ascending interactive sort.
   */
  let activeColumn = null;
  let direction = "none";

  sortableHeaders.forEach(({ cell, column }) => {
    const metadata = columnMetadata.get(column);

    if (!metadata) {
      return;
    }

    const requestedType =
      explicitSortTypes.get(column) ?? "auto";

    const resolvedType =
      requestedType === "auto"
        ? inferSortType(
            metadata.headerText,
            metadata.columnValues
          )
        : requestedType;

    cell.classList.add("sphinx-tabular-sort-header");
    cell.tabIndex = 0;
    cell.setAttribute("aria-sort", "none");
    cell.dataset.sortColumn = String(column);
    cell.dataset.sortType = resolvedType;

    const indicator = document.createElement("span");
    indicator.className = "sphinx-tabular-sort-indicator";
    indicator.setAttribute("aria-hidden", "true");
    indicator.dataset.sortDirection = "none";

    const priorityElement = document.createElement("span");
    priorityElement.className = "sphinx-tabular-sort-priority";

    const iconElement = document.createElement("span");
    iconElement.className = "sphinx-tabular-sort-icon";

    indicator.appendChild(priorityElement);
    indicator.appendChild(iconElement);
    cell.appendChild(indicator);

    const activate = () => {
      if (activeColumn !== column) {
        activeColumn = column;
        direction = "ascending";
      } else if (direction === "ascending") {
        direction = "descending";
      } else if (direction === "descending") {
        direction = "none";
      } else {
        direction = "ascending";
      }

      applyTableSort({
        tbody,
        bodyRows,
        column,
        direction,
        sortType: resolvedType,
        textCollator,
        naturalCollator,
      });

      updateSortHeaders({
        sortableHeaders,
        activeColumn,
        direction,
      });
    };

    cell.addEventListener("click", (event) => {
      /*
       * Preserve links and actual controls placed inside a header.
       */
      if (
        event.target.closest(
          "a, button, input, select, textarea"
        )
      ) {
        return;
      }

      activate();
    });

    cell.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") {
        return;
      }

      event.preventDefault();
      activate();
    });
  });

  /*
   * :initial-sort: contains its own types. These do not affect the types
   * used by later interactive header clicks.
   */
  const initialCriteria = getInitialSort(table)
    .map((criterion) => {
      const metadata = columnMetadata.get(criterion.column);

      if (!metadata) {
        return null;
      }

      const resolvedInitialType =
        criterion.sortType === "auto"
          ? inferSortType(
              metadata.headerText,
              metadata.columnValues
            )
          : criterion.sortType;

      return {
        priority: criterion.priority,
        column: criterion.column,
        direction: criterion.direction,
        sortType: resolvedInitialType,
      };
    })
    .filter((criterion) => criterion !== null);

  if (initialCriteria.length > 0) {
    applyTableSortCriteria({
      tbody,
      bodyRows,
      criteria: initialCriteria,
      textCollator,
      naturalCollator,
    });

    /*
     * Priority indicators are shown only on headers that are also
     * interactively sortable.
     */
    updateInitialSortHeaders({
      sortableHeaders,
      criteria: initialCriteria,
    });
  }
}

  function getExplicitSortTypes(table) {
    const result = new Map();

    for (const className of table.classList) {
      const match = className.match(
        /^sphinx-tabular-sort-col-(\d+)-(auto|text|number|natural|version|percent|date|none)$/
      );

      if (!match) {
        continue;
      }

      /*
       * Directive columns are 1-based.
       * JavaScript logical columns are 0-based.
       */
      const column = Number.parseInt(match[1], 10) - 1;
      const sortType = match[2];

      result.set(column, sortType);
    }

    return result;
  }

  function findSortableLeafHeaders(thead) {
    const rows = Array.from(thead.rows);
    const grid = [];
    const headers = [];

    rows.forEach((row, rowIndex) => {
      grid[rowIndex] ??= [];

      let column = 0;

      Array.from(row.cells).forEach((cell) => {
        while (grid[rowIndex][column]) {
          column += 1;
        }

        const rowSpan = cell.rowSpan || 1;
        const colSpan = cell.colSpan || 1;

        for (
          let targetRow = rowIndex;
          targetRow < rowIndex + rowSpan;
          targetRow += 1
        ) {
          grid[targetRow] ??= [];

          for (
            let targetColumn = column;
            targetColumn < column + colSpan;
            targetColumn += 1
          ) {
            grid[targetRow][targetColumn] = cell;
          }
        }

        headers.push({
          cell,
          column,
          rowIndex,
          rowSpan,
          colSpan,
        });

        column += colSpan;
      });
    });

    const finalHeaderRow = rows.length - 1;

    return headers
      .filter((header) => {
        const finalOccupiedRow =
          header.rowIndex + header.rowSpan - 1;

        return (
          header.colSpan === 1 &&
          finalOccupiedRow === finalHeaderRow
        );
      })
      .map((header) => ({
        ...header,
        headerText: getHeaderPathText(grid, header.column),
      }));
  }

  function getHeaderPathText(grid, column) {
    const labels = [];

    grid.forEach((row) => {
      const cell = row?.[column];

      if (!cell) {
        return;
      }

      const text = getCellSortValue(cell).trim();

      if (text && labels[labels.length - 1] !== text) {
        labels.push(text);
      }
    });

    return labels.join(" ");
  }

  function inferSortType(headerText, values) {
    const header = headerText.trim().toLocaleLowerCase();

    const populated = values
      .map((value) => value.trim())
      .filter((value) => value !== "");

    if (populated.length === 0) {
      return "text";
    }

    /*
     * Identifier-like columns remain text even when every value is numeric,
     * preserving leading zeroes.
     */
    if (
      /\b(id|identifier|code|serial|ticket|reference|ref|part number)\b/.test(
        header
      )
    ) {
      return "text";
    }

    if (
      /\b(version|release|revision|rev)\b/.test(header) &&
      populated.every(isVersionValue)
    ) {
      return "version";
    }

    if (
      /\b(percent|percentage|completion|utilization|rate)\b/.test(
        header
      ) &&
      populated.every(
        (value) => parsePercentValue(value) !== null
      )
    ) {
      return "percent";
    }

    if (
      /\b(date|created|updated|modified|deadline|start date|end date)\b/.test(
        header
      ) &&
      populated.every(
        (value) => parseIsoDateValue(value) !== null
      )
    ) {
      return "date";
    }

    if (
      /\b(count|total|quantity|amount|score|size|number)\b/.test(
        header
      ) &&
      populated.every(
        (value) => parseNumericValue(value) !== null
      )
    ) {
      return "number";
    }

    /* Value-only fallback. */
    if (
      populated.every(
        (value) =>
          value.includes("%") &&
          parsePercentValue(value) !== null
      )
    ) {
      return "percent";
    }

    if (
      populated.every(
        (value) => parseNumericValue(value) !== null
      )
    ) {
      return "number";
    }

    if (
      populated.every(
        (value) => parseIsoDateValue(value) !== null
      )
    ) {
      return "date";
    }

    if (
      populated.every(
        (value) =>
          /[A-Za-z]/.test(value) && /\d/.test(value)
      )
    ) {
      return "natural";
    }

    return "text";
  }

  function isVersionValue(value) {
    return /^v?\d+(?:\.\d+)+(?:[-+][0-9A-Za-z.-]+)?$/i.test(
      value.trim()
    );
  }

  function parsePercentValue(value) {
    let normalized = value.trim();

    if (normalized.endsWith("%")) {
      normalized = normalized.slice(0, -1).trim();
    }

    return parseNumericValue(normalized);
  }

  function parseIsoDateValue(value) {
    const match = value.trim().match(
      /^(\d{4})-(\d{2})-(\d{2})$/
    );

    if (!match) {
      return null;
    }

    const year = Number(match[1]);
    const month = Number(match[2]);
    const day = Number(match[3]);
    const timestamp = Date.UTC(year, month - 1, day);
    const date = new Date(timestamp);

    if (
      date.getUTCFullYear() !== year ||
      date.getUTCMonth() !== month - 1 ||
      date.getUTCDate() !== day
    ) {
      return null;
    }

    return timestamp;
  }

  function parseNumericValue(value) {
    const normalized = value.trim();

    if (
      !/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?$/i.test(
        normalized
      )
    ) {
      return null;
    }

    const number = Number(normalized);
    return Number.isFinite(number) ? number : null;
  }

 function applyTableSort({
  tbody,
  bodyRows,
  column,
  direction,
  sortType,
  textCollator,
  naturalCollator,
}) {
  applyTableSortCriteria({
    tbody,
    bodyRows,
    criteria: [
      {
        column,
        direction,
        sortType,
      },
    ],
    textCollator,
    naturalCollator,
  });
}

function applyTableSortCriteria({
  tbody,
  bodyRows,
  criteria,
  textCollator,
  naturalCollator,
}) {
  const activeCriteria = criteria.filter(
    ({ direction }) => direction !== "none"
  );

  if (activeCriteria.length === 0) {
    const originalRows = [...bodyRows].sort(
      (left, right) =>
        getOriginalIndex(left) - getOriginalIndex(right)
    );

    originalRows.forEach((row) => {
      tbody.appendChild(row);
    });

    return;
  }

  /*
   * Cache each criterion's value once per row. This avoids repeatedly
   * reading DOM cells from inside the sort comparator.
   */
  const records = bodyRows.map((row) => ({
    row,
    originalIndex: getOriginalIndex(row),

    values: activeCriteria.map(({ column }) => {
      const cell = getLogicalCell(row, column);
      return getCellSortValue(cell);
    }),
  }));

  records.sort((left, right) => {
    /*
     * Criteria are evaluated in source order. The first entry is dominant,
     * the second entry resolves ties, and so on.
     */
    for (
      let index = 0;
      index < activeCriteria.length;
      index += 1
    ) {
      const criterion = activeCriteria[index];
      const leftValue = left.values[index];
      const rightValue = right.values[index];

      /*
       * Blank values remain at the bottom regardless of normal or reverse
       * ordering.
       */
      if (leftValue === "" && rightValue !== "") {
        return 1;
      }

      if (leftValue !== "" && rightValue === "") {
        return -1;
      }

      if (leftValue === "" && rightValue === "") {
        continue;
      }

      const leftValid = isSortValueValid(
        leftValue,
        criterion.sortType
      );

      const rightValid = isSortValueValid(
        rightValue,
        criterion.sortType
      );

      /*
       * Invalid typed values remain below valid values regardless of order.
       */
      if (!leftValid && rightValid) {
        return 1;
      }

      if (leftValid && !rightValid) {
        return -1;
      }

      let comparison = compareSortValues(
        leftValue,
        rightValue,
        criterion.sortType,
        textCollator,
        naturalCollator
      );

      if (comparison === 0) {
        continue;
      }

      if (criterion.direction === "descending") {
        comparison *= -1;
      }

      return comparison;
    }

    /*
     * Preserve source order when all configured criteria compare equally.
     */
    return left.originalIndex - right.originalIndex;
  });

  records.forEach(({ row }) => {
    tbody.appendChild(row);
  });
}


  function isSortValueValid(value, sortType) {
    switch (sortType) {
      case "number":
        return parseNumericValue(value) !== null;

      case "percent":
        return parsePercentValue(value) !== null;

      case "date":
        return parseIsoDateValue(value) !== null;

      default:
        return true;
    }
  }

  function compareSortValues(
    left,
    right,
    sortType,
    textCollator,
    naturalCollator
  ) {
    switch (sortType) {
      case "number":
        return compareParsedValues(
          left,
          right,
          parseNumericValue,
          textCollator
        );

      case "percent":
        return compareParsedValues(
          left,
          right,
          parsePercentValue,
          textCollator
        );

      case "date":
        return compareParsedValues(
          left,
          right,
          parseIsoDateValue,
          textCollator
        );

      case "version":
        return naturalCollator.compare(
          left.replace(/^v/i, ""),
          right.replace(/^v/i, "")
        );

      case "natural":
        return naturalCollator.compare(left, right);

      case "text":
      default:
        return textCollator.compare(left, right);
    }
  }

  function compareParsedValues(
    left,
    right,
    parser,
    fallbackCollator
  ) {
    const leftValue = parser(left);
    const rightValue = parser(right);

    if (leftValue === null && rightValue === null) {
      return fallbackCollator.compare(left, right);
    }

    if (leftValue === null) {
      return 1;
    }

    if (rightValue === null) {
      return -1;
    }

    return leftValue - rightValue;
  }

  function getLogicalCell(row, targetColumn) {
    let logicalColumn = 0;

    for (const cell of Array.from(row.cells)) {
      const colSpan = cell.colSpan || 1;
      const finalColumn = logicalColumn + colSpan;

      if (
        targetColumn >= logicalColumn &&
        targetColumn < finalColumn
      ) {
        return cell;
      }

      logicalColumn = finalColumn;
    }

    return null;
  }

  function getCellSortValue(cell) {
    if (!cell) {
      return "";
    }

    const explicitValue = cell.dataset.sortValue;

    if (explicitValue !== undefined) {
      return explicitValue.trim();
    }

    return cell.textContent.trim();
  }

  function getOriginalIndex(row) {
    return Number.parseInt(
      row.dataset.sphinxTabularOriginalIndex,
      10
    );
  }


  function updateInitialSortHeaders({
    sortableHeaders,
    criteria,
  }) {
    const criteriaByColumn = new Map();

    criteria.forEach((criterion, index) => {
      criteriaByColumn.set(criterion.column, {
        ...criterion,
        priority: index + 1,
      });
    });

    sortableHeaders.forEach(({ cell, column }) => {
      const indicator = cell.querySelector(
        ".sphinx-tabular-sort-indicator"
      );

      const priorityElement = indicator?.querySelector(
        ".sphinx-tabular-sort-priority"
      );

      const criterion = criteriaByColumn.get(column);

      delete cell.dataset.sortPriority;
      delete cell.dataset.sortDirection;

      if (!criterion) {
        cell.setAttribute("aria-sort", "none");

        if (indicator) {
          indicator.dataset.sortDirection = "none";
        }

        if (priorityElement) {
          priorityElement.textContent = "";
        }

        return;
      }

      cell.dataset.sortPriority = String(
        criterion.priority
      );

      cell.dataset.sortDirection =
        criterion.direction;

      cell.setAttribute(
        "aria-sort",
        criterion.priority === 1
          ? criterion.direction
          : "none"
      );

      if (indicator) {
        indicator.dataset.sortDirection =
          criterion.direction;
      }

      if (priorityElement) {
        priorityElement.textContent = String(
          criterion.priority
        );
      }
    });
  }


  function updateSortHeaders({
    sortableHeaders,
    activeColumn,
    direction,
  }) {
    sortableHeaders.forEach(({ cell, column }) => {
      delete cell.dataset.sortPriority;
      delete cell.dataset.sortDirection;

      const indicator = cell.querySelector(
        ".sphinx-tabular-sort-indicator"
      );

      const priorityElement = indicator?.querySelector(
        ".sphinx-tabular-sort-priority"
      );

      if (priorityElement) {
        priorityElement.textContent = "";
      }

      const isActive =
        column === activeColumn &&
        direction !== "none";

      if (!isActive) {
        cell.setAttribute("aria-sort", "none");

        if (indicator) {
          indicator.dataset.sortDirection = "none";
        }

        return;
      }

      cell.setAttribute("aria-sort", direction);

      if (indicator) {
        indicator.dataset.sortDirection = direction;
      }
    });
  }

  function initializeSearchableTables() {
    document
      .querySelectorAll("table.sphinx-tabular-searchable")
      .forEach(initializeSearchableTable);
  }

  function initializeSearchableTable(table) {
    if (table.dataset.sphinxTabularSearchInitialized === "true") {
      return;
    }

    const tbody = table.tBodies[0];

    if (!tbody) {
      return;
    }

    /*
     * Hiding individual rows is ambiguous when a body cell spans multiple
     * rows. Disable search until body row-group support is implemented.
     */
    const hasBodyRowspans = Array.from(tbody.rows).some((row) =>
      Array.from(row.cells).some((cell) => cell.rowSpan > 1)
    );

    if (hasBodyRowspans) {
      table.classList.add("sphinx-tabular-search-disabled");
      table.dataset.sphinxTabularSearchDisabledReason =
        "Body rows contain vertically merged cells.";
      return;
    }

    table.dataset.sphinxTabularSearchInitialized = "true";

    const rows = Array.from(tbody.rows);
    sphinxTabularSearchCounter += 1;

    if (!table.id) {
      table.id =
        `sphinx-tabular-table-${sphinxTabularSearchCounter}`;
    }

    const toolbar = document.createElement("div");
    toolbar.className = "sphinx-tabular-controls";

    const searchGroup = document.createElement("div");
    searchGroup.className = "sphinx-tabular-search";

    const label = document.createElement("label");
    label.className = "sphinx-tabular-visually-hidden";

    const inputId = `${table.id}-search`;
    label.htmlFor = inputId;
    label.textContent = "Search table";

    const input = document.createElement("input");
    input.id = inputId;
    input.className = "sphinx-tabular-search-input";
    input.type = "search";
    input.placeholder = "Search table\u2026";
    input.autocomplete = "off";
    input.setAttribute("aria-controls", table.id);
    input.setAttribute("aria-label", "Search table");

    const count = document.createElement("span");
    count.className = "sphinx-tabular-search-count";
    count.setAttribute("aria-live", "polite");

    searchGroup.appendChild(label);
    searchGroup.appendChild(input);
    searchGroup.appendChild(count);
    toolbar.appendChild(searchGroup);

    table.insertAdjacentElement("beforebegin", toolbar);

    /*
     * Cache searchable row text once. Search uses data-sort-value, which
     * contains evaluated plain values instead of formula source or HTML.
     */
    const searchRecords = rows.map((row) => ({
      row,
      text: getRowSearchText(row),
    }));

    function applySearch() {
      const query = input.value.trim().toLocaleLowerCase();
      let visibleRows = 0;

      searchRecords.forEach((record) => {
        const matches =
          query === "" || record.text.includes(query);

        record.row.hidden = !matches;

        if (matches) {
          visibleRows += 1;
        }
      });

      count.textContent = `${visibleRows} of ${rows.length} rows`;

      table.classList.toggle(
        "sphinx-tabular-search-active",
        query !== ""
      );
    }

    input.addEventListener("input", applySearch);

    input.addEventListener("keydown", (event) => {
      if (event.key !== "Escape") {
        return;
      }

      input.value = "";
      applySearch();
      input.focus();
    });

    applySearch();
  }

  function getRowSearchText(row) {
    return Array.from(row.cells)
      .map((cell) => getCellSortValue(cell))
      .join("\u0000")
      .toLocaleLowerCase();
  }
  function getInitialSort(table) {
    const result = [];

    for (const className of table.classList) {
      const match = className.match(
        /^sphinx-tabular-initial-sort-(\d+)-col-(\d+)-(auto|text|number|natural|version|percent|date)(-reverse)?$/
      );

      if (!match) {
        continue;
      }

      result.push({
        priority: Number.parseInt(
          match[1],
          10
        ),

        /*
        * Directive columns are one-based.
        * JavaScript logical columns are zero-based.
        */
        column:
          Number.parseInt(
            match[2],
            10
          ) - 1,

        sortType: match[3],

        direction:
          match[4] === "-reverse"
            ? "descending"
            : "ascending",
      });
    }

    result.sort(
      (left, right) =>
        left.priority - right.priority
    );

    return result;
  }
  document.addEventListener(
    "DOMContentLoaded",
    scheduleStickyHeaderUpdate
  );

  document.addEventListener(
    "DOMContentLoaded",
    initializeSortableTables
  );

  document.addEventListener(
    "DOMContentLoaded",
    initializeSearchableTables
  );

  window.addEventListener("load", scheduleStickyHeaderUpdate);
  window.addEventListener("resize", scheduleStickyHeaderUpdate);

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(scheduleStickyHeaderUpdate);
  }
})();

