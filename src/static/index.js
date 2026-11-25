const citationCheckboxes = document.querySelectorAll(".source-card-checkbox");
const selectionButton = document.querySelector("#toggle-citation-selection");
const deleteButton = document.querySelector("#delete-citations-button");
const deleteForm = document.querySelector("#delete-citations-form");

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

if (deleteForm) {
  deleteForm.addEventListener("submit", (event) => {
    const selectedCount = deleteForm.querySelectorAll(
      ".source-card-checkbox:checked"
    ).length;
    if (selectedCount === 0) {
      event.preventDefault();
      return;
    }

    const confirmed = window.confirm(
      `Haluatko varmasti poistaa ${selectedCount} lähdettä?`
    );
    if (!confirmed) {
      event.preventDefault();
    }
  });
}
