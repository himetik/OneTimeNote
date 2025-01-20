async function generateTemporaryKey() {
    const randomBytes = crypto.getRandomValues(new Uint8Array(16));
    return Array.from(randomBytes).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function generateEncryptionKey() {
    const randomBytes = crypto.getRandomValues(new Uint8Array(32));
    return Array.from(randomBytes).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function importKey(keyString) {
    const keyBytes = new Uint8Array(keyString.match(/.{2}/g).map(byte => parseInt(byte, 16)));
    return await crypto.subtle.importKey('raw', keyBytes, { name: 'AES-GCM' }, false, ['encrypt']);
}

async function encrypt(text, key) {
    const encoder = new TextEncoder();
    const encoded = encoder.encode(text);

    const iv = crypto.getRandomValues(new Uint8Array(12));
    const encrypted = await crypto.subtle.encrypt({ name: 'AES-GCM', iv: iv }, key, encoded);

    const encryptedArray = new Uint8Array(iv.length + encrypted.byteLength);
    encryptedArray.set(iv);
    encryptedArray.set(new Uint8Array(encrypted), iv.length);

    return btoa(String.fromCharCode(...encryptedArray));
}

function copyLink() {
    const linkInput = document.getElementById('noteLinkDisplay');
    linkInput.select();
    document.execCommand('copy');
}

function showKeyModal(url) {
    document.getElementById('noteLinkDisplay').value = url;
    const modal = new bootstrap.Modal(document.getElementById('keyModal'));
    modal.show();
}

document.addEventListener('DOMContentLoaded', function () {
    const noteTextarea = document.getElementById('note');
    const maxNoteLength = 1200; // Temporary solution
    window.addEventListener('beforeunload', function () {
        noteTextarea.value = '';
    });

    noteTextarea.addEventListener('keydown', function (event) {
        if (event.key === 'Tab') {
            event.preventDefault();

            const start = this.selectionStart;
            const end = this.selectionEnd;

            this.value = this.value.substring(0, start) + '\t' + this.value.substring(end);

            this.selectionStart = this.selectionEnd = start + 1;
        }
    });

    document.getElementById('save-button').addEventListener('click', async function () {
        const originalNote = noteTextarea.value;
        if (!originalNote.trim()) {
            alert("Note cannot be empty!");
            return;
        }
        if (originalNote.length > maxNoteLength) {
            alert(`Note is too long! Maximum length is ${maxNoteLength} characters.`);
            return;
        }
        try {
            const temporaryKey = await generateTemporaryKey();
            const secretPart = await generateEncryptionKey();
            const key = await importKey(secretPart);
            const encryptedNote = await encrypt(originalNote, key);
            const response = await fetch('/creation', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    note: encryptedNote,
                    secret_part: secretPart,
                    temporary_key: temporaryKey,
                }),
            });
            if (!response.ok) {
                const errorData = await response.json();
                if (errorData.error) {
                    alert(`Error: ${errorData.error}`);
                } else {
                    alert(`HTTP error! Status: ${response.status}`);
                }
                return;
            }
            const result = await response.json();
            if (result.success) {
                const baseUrl = "https://onetimenote.duckdns.org/view";
                const fullUrl = `${baseUrl}/${temporaryKey}/${secretPart}`;
                showKeyModal(fullUrl);
                noteTextarea.value = '';
            } else {
                alert('Error saving note: ' + (result.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Произошла ошибка: ' + error.message);
        }
    });

    function showKeyModal(link) {
        const modal = new bootstrap.Modal(document.getElementById('keyModal'));
        const linkInput = document.getElementById('noteLinkDisplay');
        linkInput.value = link;
        modal.show();
    }

});
