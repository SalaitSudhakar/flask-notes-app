/*
  Client-side JavaScript for the Notes App.

  This file handles simple UI interactions:
  - toggling the visibility of password fields
  - editing notes (populate form and change behavior)
  - deleting notes via an AJAX call

  Comments are intentionally descriptive to help beginners learn
  how the front-end connects with the Flask back-end.
*/

// --- Defensive element queries: select elements if they exist on the page
const showPasswordCheckbox = document.querySelector("#show-password");
const passwordInputs = document.querySelectorAll('input[type="password"]');
const noteTextarea = document.querySelector("#note");
const noteForm = document.querySelector("#noteForm");
const submitButton = document.querySelector("#submitButton");
const cancelButton = document.querySelector("#cancelButton");
const notesList = document.getElementById('notes-list');

// Password toggle: show/hide password when checkbox is changed
if (showPasswordCheckbox) {
  showPasswordCheckbox.addEventListener("change", (e) => {
    const inputType = e.target.checked ? "text" : "password";
    // Update all password inputs on the page
    passwordInputs.forEach((passwordInput) => {
      passwordInput.type = inputType;
    });
  });
}


// ===== EVENT DELEGATION FOR NOTES LIST =====
// Instead of attaching handlers to each button, we listen on the
// parent `ul` and determine which button was clicked. This is more
// efficient and works for dynamically generated list items.
if (notesList) {
  notesList.addEventListener('click', (e) => {
    // Find the clicked button (handles clicks on the button or icon)
    const button = e.target.closest('button');

    // If no button was clicked, ignore the event
    if (!button) return;

    // Find the parent <li> that contains data attributes for the note
    const listItem = button.closest('li[data-note-id]');
    if (!listItem) return; // not inside a note item

    // Extract the note id and content from data attributes
    const noteId = listItem.dataset.noteId;
    const noteContent = listItem.dataset.noteContent;

    // Route actions by button CSS class
    if (button.classList.contains('btn-edit')) {
      editNote(noteId, noteContent);
    } else if (button.classList.contains('btn-delete')) {
      if (confirm('Are you sure you want to delete this note?')) {
        deleteNote(noteId);
      }
    }
  });
}


// ===== EDIT NOTE FUNCTION =====
function editNote(id, data) {
  // Fill the note form with the existing note data so the user
  // can edit it. Change the form action to the edit endpoint.
  console.log("Editing note:", id);

  if (!noteTextarea || !noteForm || !submitButton) {
    console.error("Required form elements missing.");
    return;
  }

  // Put the current note text into the textarea
  noteTextarea.value = data;

  // Change the submit button text so the user knows they will update
  submitButton.innerText = "Update Note";

  // Show a cancel button (if present) so the user can abort editing
  if (cancelButton) {
    cancelButton.style.display = "block";
  }

  // Ensure there is a hidden input containing the note id so the server
  // knows which note to update when the form is submitted.
  let hiddenInput = document.querySelector("#editNoteId");
  if (!hiddenInput) {
    hiddenInput = document.createElement("input");
    hiddenInput.type = "hidden";
    hiddenInput.id = "editNoteId";
    hiddenInput.name = "noteId";
    noteForm.appendChild(hiddenInput);
  }
  hiddenInput.value = id;

  // Change the form action to point to the editing route
  noteForm.setAttribute("action", "/edit-note");

  // Focus the textarea and scroll it into view for better UX
  noteTextarea.focus();
  noteTextarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
}


// ===== DELETE NOTE FUNCTION =====
function deleteNote(noteId) {
  // Send the note id to the server using fetch (AJAX). The server
  // expects JSON with a `noteId` field.
  fetch("/delete-note", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ noteId: noteId }),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Delete failed");
      // On success, reload the app root to show updated notes
      window.location.href = "/";
    })
    .catch((err) => {
      console.error(err);
      alert("Could not delete note. See console for details.");
    });
}


// ===== CANCEL EDIT FUNCTION =====
function cancelEdit() {
  // Reset the note form back to the "Add Note" state
  if (!noteTextarea || !noteForm || !submitButton) return;

  const hiddenInput = document.querySelector("#editNoteId");

  // Clear textarea
  noteTextarea.value = "";

  // Reset button text
  submitButton.innerText = "Add Note";

  // Hide cancel button if present
  if (cancelButton) {
    cancelButton.style.display = "none";
  }

  // Remove hidden input with note id if it exists
  if (hiddenInput) {
    hiddenInput.remove();
  }

  // Reset the form action back to the default create route
  noteForm.setAttribute("action", "/");
}