var button = document.getElementById("usersearchbtn");

if(button) {
    button.onclick = function () {
        var text = document.getElementById("usersearch").value;
        console.log(window.location.pathname + "?user=" + text);
        window.location = window.location.pathname + "?user=" + text;
        return false;
    }
}

document.getElementById('light-dark-mode-toggle').addEventListener('click', () => localStorage.setItem('theme', document.body.classList.toggle('dark-mode') ? 'dark' : 'light'));
