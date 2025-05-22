function updateClasses(selector, classesToAdd = [], classesToRemove = []) {
    const elements = document.querySelectorAll(selector);

    elements.forEach(element => {
    classesToRemove.forEach(cls => element.classList.remove(cls));
    classesToAdd.forEach(cls => element.classList.add(cls));
  });
}


function sendToServer(data, path) {
    return fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    });
}


function checkInputNumber(value) {
    return !isNaN(value);
}


function writeToSessionStorage(obj) {
    Object.keys(obj).forEach(key => {
        const newKey = isNaN(Number(key)) ? key : `${Number(key) + 1}`;
        const value = typeof obj[key] === 'string' ? obj[key] : JSON.stringify(obj[key]);
        sessionStorage.setItem(newKey, value);
    });
}


function getFromSessionStorage22222222() {
    return Object.keys(sessionStorage).reduce((obj, key) => {
        obj[key] = sessionStorage.getItem(key);
        return obj;
    }, {});
}


function getFromSessionStorage() {
    return Object.keys(sessionStorage).reduce((obj, key) => {
        let value = sessionStorage.getItem(key);
        // Try to convert to original type (number, array, object)
        try {
            const parsed = JSON.parse(value);
            obj[key] = parsed;
        } catch (e) {
            // If it's not JSON, keep as string
            obj[key] = value;
        }

        return obj;
    }, {});
}


function cancelOrder() {
    sessionStorage.clear();
    window.location.reload();
}


document.addEventListener('DOMContentLoaded', () => {
    const textareas = document.querySelectorAll('.auto-resize');
    textareas.forEach(textarea => {
        textarea.setAttribute('style', 'height:' + (textarea.scrollHeight) + 'px;overflow-y:hidden;');
        textarea.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
});