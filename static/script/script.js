try {
    const inputBox = document.getElementsByTagName('input');

    const loginActivate = function (e) {
        inputArea = e.target.closest('.input-area');
        if (!e.target.value == "") {
            inputArea.classList.add("activate");
        }
        else {
            inputArea.classList.remove("activate");
        }
    };
    for (let i = 0; i < inputBox.length; i++) {
        inputBox[i].addEventListener('keyup', loginActivate);
    }


} catch {

}

try {


    var ctx = document.getElementById('today-progress-crc').getContext("2d");

    // var r = -Math.PI / 2;
    var $r1 = (270 * Math.PI / 180) - Math.PI / 2;
    var r1 = -Math.PI / 2;

    function graph() {
        console.log(ctx);
        r1 = r1 + ($r1 - r1) * 0.045;

        ctx.clearRect(0, 0, 100, 100);

        ctx.strokeStyle = "#3cddaa";
        ctx.lineWidth = 10;
        ctx.lineCap = "round";
        ctx.beginPath();
        ctx.arc(50, 50, 40, -Math.PI / 2, r1, false);
        ctx.stroke();

        document.getElementById('progress-per').innerHTML = Math.round((r1 * 180 / Math.PI + 90) / 360 * 100) + "%";
    }
    const progress = setInterval(graph, 40);
    setTimeout(function () {
        clearInterval(progress)
    }, 6000);

} catch {

}

