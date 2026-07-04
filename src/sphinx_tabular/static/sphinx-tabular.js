(function () {
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
            cell.style.background = "var(--sphinx-tabular-header-bg)";
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

  document.addEventListener("DOMContentLoaded", scheduleStickyHeaderUpdate);
  window.addEventListener("load", scheduleStickyHeaderUpdate);
  window.addEventListener("resize", scheduleStickyHeaderUpdate);

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(scheduleStickyHeaderUpdate);
  }
})();