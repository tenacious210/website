var user_button = document.getElementById("usersearchbtn");

if (user_button) {
    user_button.onclick = function () {
        var text = document.getElementById("usersearch").value;
        window.location = "/users/" + text;
        return false;
    }
}
