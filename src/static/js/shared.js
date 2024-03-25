function toggleNavbar() {
    var x = document.getElementById("navbarLinks");
    if (x.style.display === "block") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    }
}

window.addEventListener('DOMContentLoaded', function() {
    var image = document.getElementById('video_feed');
    var systemLog = document.querySelector('.system-log');
    function setSystemLogDimensions() {
        systemLog.style.height = image.clientHeight + 'px';
        systemLog.style.width = image.clientWidth + 'px';
    }
    setSystemLogDimensions();
    window.addEventListener('resize', setSystemLogDimensions);
});