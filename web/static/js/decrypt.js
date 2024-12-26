async function importKey(keyString) {
    try {
        const keyBytes = new Uint8Array(keyString.match(/.{2}/g).map(byte => parseInt(byte, 16)));
        return await crypto.subtle.importKey(
            'raw',
            keyBytes,
            { name: 'AES-GCM' },
            false,
            ['decrypt']
        );
    } catch (error) {
        console.error("Error importing key:", error);
        throw new Error("Key import failed.");
    }
}

async function decrypt(encryptedData, key) {
    try {
        const encryptedArray = new Uint8Array(atob(encryptedData).split('').map(char => char.charCodeAt(0)));
        const iv = encryptedArray.slice(0, 12);
        const encryptedText = encryptedArray.slice(12);
        const decrypted = await crypto.subtle.decrypt(
            { name: 'AES-GCM', iv },
            key,
            encryptedText
        );
        return new TextDecoder().decode(decrypted);
    } catch (error) {
        console.error("Decryption error:", error);
        throw new Error("Decryption failed.");
    }
}

async function decryptNoteAndDisplay(encryptedNote, secretKey) {
    try {
        const key = await importKey(secretKey);
        const decryptedNote = await decrypt(encryptedNote, key);
        const noteElement = document.getElementById("decrypted-note");
        noteElement.textContent = decryptedNote;
        window.decryptedNoteContent = decryptedNote;
    } catch (error) {
        const errorMessageElement = document.getElementById("error-message");
        errorMessageElement.classList.remove("d-none");
        errorMessageElement.textContent = "Failed to decrypt the note. Please check the URL or secret key.";
    }
}

function clearNote() {
    const noteElement = document.getElementById("decrypted-note");
    if (noteElement) {
        noteElement.style.opacity = '0';
        setTimeout(() => {
            noteElement.textContent = "";
            noteElement.closest('#note-container').style.display = 'none';
        }, 300);
    }
    window.decryptedNoteContent = null;
}

function handleVisibilityChange() {
    if (document.hidden) {
        clearNote();
    }
}

window.initialize = function(encryptedNote) {
    const secretPart = window.location.pathname.split("/").pop();
    const isNoteViewed = sessionStorage.getItem("noteViewed");

    if (isNoteViewed === encryptedNote) {
        console.warn("Note already viewed in this session.");
        return;
    }

    decryptNoteAndDisplay(encryptedNote, secretPart);

    sessionStorage.setItem("noteViewed", encryptedNote);

    document.addEventListener("visibilitychange", handleVisibilityChange);
    window.addEventListener("beforeunload", clearNote);
    window.addEventListener("unload", clearNote);
};
