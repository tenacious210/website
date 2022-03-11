var button = document.getElementById("usersearchbtn");

button.onclick = function () {
    var text = document.getElementById("usersearch").value;
    console.log(window.location.pathname + "?user=" + text);
    window.location = window.location.pathname + "?user=" + text;
    return false;
}