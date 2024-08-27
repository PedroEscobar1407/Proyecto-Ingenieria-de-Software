// emoji picker functionalities
const emojiPicker = document.querySelector('emoji-picker');
const hiddenEmojiInput = document.querySelector('.hidden-emoji-input');
const emotionDisplay = document.querySelector('.entry-emotion-add');


function updateEmojiSelection(event) {
    const selectedEmoji = event.detail.emoji.unicode;
    hiddenEmojiInput.value = selectedEmoji;
    emotionDisplay.textContent = `Emoción: ${selectedEmoji}`;
    emojiPicker.hidden = true;
    validateForm()
}

if (emojiPicker) {
    emojiPicker.addEventListener('emoji-click', updateEmojiSelection);
}

function toggleEmojiPicker() {
    emojiPicker.hidden = !emojiPicker.hidden;
}

const emojiSelectButton = document.querySelector('.emoji-select');
if (emojiSelectButton) {
    emojiSelectButton.addEventListener('click', toggleEmojiPicker);
}

// theme setup
function toggleTheme() {
    const body = document.body;
    body.classList.toggle('dark-mode');

    localStorage.setItem('theme', body.classList.contains('dark-mode') ? 'dark' : 'light');
}

document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
});

// button handling
const buttons = document.querySelectorAll('.chrono-button');

buttons.forEach(button => {
    button.addEventListener('click', function() {
        buttons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
    });
});

function toggleModal() {
    const modal = document.getElementById('new-diary-modal')
    const modalContainer = document.getElementById('new-diary-modal-container');
    modal.hidden = !modal.hidden;
    modalContainer.hidden = !modalContainer.hidden;
    emojiPicker.hidden = true;

    const titleInput = document.getElementById('title-input');
    if (!modalContainer.hidden) {
        titleInput.focus();
    }
    validateForm()
}

function addPsychToggle() {
    const modal = document.getElementById('add-psych-modal')
    const modalContainer = document.getElementById('add-psych-modal-container')
    modal.hidden = !modal.hidden;
    modalContainer.hidden = !modalContainer.hidden;
}

const addButton = document.getElementById('agregar-diario-button');
if (addButton) {
    addButton.addEventListener('click', toggleModal);
    document.getElementById('new-diary-modal').addEventListener('click', toggleModal);
    document.getElementById('new-diary-close').addEventListener('click', toggleModal);
}

const addPsychButton = document.getElementById('add-psych-button');
if (addPsychButton) {
    addPsychButton.addEventListener('click', addPsychToggle);
    document.getElementById('add-psych-modal').addEventListener('click', addPsychToggle);
    document.getElementById('add-psych-close').addEventListener('click', addPsychToggle);
}

const panicButton = document.getElementById('panic-button');

function panicToggle() {
    const modal = document.getElementById('panic-modal')
    const modalContainer = document.getElementById('panic-modal-container')
    modal.hidden = !modal.hidden;
    modalContainer.hidden = !modalContainer.hidden;
}

if (panicButton) {
    panicButton.addEventListener('click', panicToggle);
    document.getElementById('panic-modal').addEventListener('click', panicToggle);
    document.getElementById('panic-close').addEventListener('click', panicToggle);
}

const deleteButton = document.getElementById('delete-diary-button');

function toggleDelete() {
    const modal = document.getElementById('delete-modal')
    const modalContainer = document.getElementById('delete-modal-container')
    modal.hidden = !modal.hidden;
    modalContainer.hidden = !modalContainer.hidden;
}

if (deleteButton) {
    deleteButton.addEventListener('click', toggleDelete);
    document.getElementById('delete-modal').addEventListener('click', toggleDelete);
    document.getElementById('delete-close').addEventListener('click', toggleDelete);
}

function validateForm() {
    const title = $('#title-input').val();
    const text = $('#text-input').val();
    const emotion = $('#hidden-emoji-input').val();

    if (title && title.length <= 25 && text && text.length >= 1 && text.length <= 500 && emotion.length >= 1) {
        $('#publicar-button').removeClass('disabled').prop('disabled', false);
    } else {
        $('#publicar-button').addClass('disabled').prop('disabled', true);
    }
}

$('#title-input, #text-input').on('keyup change', validateForm);
validateForm();
if (document.getElementById('new-diary-modal-container')) {
    $('#new-diary-modal-container')[0].reset();
}
