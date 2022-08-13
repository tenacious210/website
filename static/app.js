var emotes_button = document.getElementById("emotesearchbtn");
var user_button = document.getElementById("usersearchbtn");

if (emotes_button) {
    emotes_button.onclick = function () {
        var text = document.getElementById("usersearch").value;
        window.location = window.location.pathname + "?user=" + text;
        return false;
    }
}

if (user_button) {
    user_button.onclick = function () {
        var text = document.getElementById("usersearch").value;
        window.location = "/users/" + text;
        return false;
    }
}

document.getElementById('light-dark-mode-toggle').addEventListener('click', () => localStorage.setItem('theme', document.body.classList.toggle('dark-mode') ? 'dark' : 'light'));
