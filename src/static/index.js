const citationCheckboxes = document.querySelectorAll(".source-card-checkbox");
const selectionButton = document.querySelector("#toggle-citation-selection");
const deleteButton = document.querySelector("#delete-citations-button");

function updateSelectionButton() {
  const hasSelection = Array.from(citationCheckboxes).some(
    (checkbox) => checkbox.checked
  );
  selectionButton.textContent = hasSelection
    ? "Tyhjennä valinnat"
    : "Valitse kaikki";
  deleteButton.classList.toggle("is-selected", hasSelection);
}

if (selectionButton && deleteButton) {
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

  updateSelectionButton();
}
