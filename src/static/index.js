const citationCheckboxes = document.querySelectorAll(".source-card-checkbox");
const selectionButton = document.querySelector("#toggle-citation-selection");

function updateSelectionButton() {
  const hasSelection = Array.from(citationCheckboxes).some(
    (checkbox) => checkbox.checked
  );
  selectionButton.textContent = hasSelection
    ? "Tyhjennä valinnat"
    : "Valitse kaikki";
}

if (selectionButton) {
  selectionButton.addEventListener("click", () => {
    const hasSelection = Array.from(citationCheckboxes).some(
      (checkbox) => checkbox.checked
    );
    citationCheckboxes.forEach((checkbox) => {
      checkbox.checked = !hasSelection;
    });
    updateSelectionButton();
  });

  citationCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", updateSelectionButton);
  });
}
