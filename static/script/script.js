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


} catch { }

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

} catch { }

try {
    // const toggleBtn = document.querySelector('.btn-plus');
    // const todaySection = document.querySelector('.today-section');
    // toggleBtn.addEventListener('click', function () {
    //     todaySection.classList.toggle('show');
    // });

    let slideUp = (target, duration = 500) => {
        target.style.transitionProperty = "height, margin, padding";
        target.style.transitionDuration = duration + "ms";
        target.style.boxSizing = "border-box";
        target.style.height = target.offsetHeight + "px";
        target.offsetHeight;
        target.style.overflow = "hidden";
        target.style.height = 0;
        target.style.paddingTop = 0;
        target.style.paddingBottom = 0;
        target.style.marginTop = 0;
        target.style.marginBottom = 0;
        window.setTimeout(() => {
            target.style.display = "none";
            target.style.removeProperty("height");
            target.style.removeProperty("padding-top");
            target.style.removeProperty("padding-bottom");
            target.style.removeProperty("margin-top");
            target.style.removeProperty("margin-bottom");
            target.style.removeProperty("overflow");
            target.style.removeProperty("transition-duration");
            target.style.removeProperty("transition-property");
            //alert("!");
        }, duration);
    };
    let slideDown = (target, duration = 500) => {
        target.style.removeProperty("display");
        let display = window.getComputedStyle(target).display;

        if (display === "none") display = "block";

        target.style.display = display;
        let height = target.offsetHeight;
        target.style.overflow = "hidden";
        target.style.height = 0;
        target.style.paddingTop = 0;
        target.style.paddingBottom = 0;
        target.style.marginTop = 0;
        target.style.marginBottom = 0;
        target.offsetHeight;
        target.style.boxSizing = "border-box";
        target.style.transitionProperty = "height, margin, padding";
        target.style.transitionDuration = duration + "ms";
        target.style.height = height + "px";
        target.style.removeProperty("padding-top");
        target.style.removeProperty("padding-bottom");
        target.style.removeProperty("margin-top");
        target.style.removeProperty("margin-bottom");
        window.setTimeout(() => {
            target.style.removeProperty("height");
            target.style.removeProperty("overflow");
            target.style.removeProperty("transition-duration");
            target.style.removeProperty("transition-property");
        }, duration);
    };
    let slideToggle = (target, duration = 500) => {
        if (window.getComputedStyle(target).display === "none") {
            return slideDown(target, duration);
        } else {
            return slideUp(target, duration);
        }
    };

    // ====

    let speedAnimation = 400;
    let target = document.querySelector('.today-section');

    let slideBtnClick = (cl, sl) =>
        document
            .querySelector(cl)
            .addEventListener("click", () => sl(target, speedAnimation));

    slideBtnClick(".btn-plus", slideToggle);


} catch { }
try {
    const tasks = document.querySelectorAll('.task');
    const taskMenu = function (e) {
        e.preventDefault();
        // console.log(this.childNodes[1]);
        // console.log(this.childNodes[3]);
        this.childNodes[1].classList.toggle('activate');
        this.childNodes[3].classList.toggle('activate');

    }
    tasks.forEach(task => {
        task.addEventListener('click', taskMenu);
    })

} catch { }

try {
    const todayDate = document.querySelector('#id_when');
    const currentDate = new Date().toISOString();

    const todayMonth = document.querySelector('.today-date-month');
    const todayDay = document.querySelector('.today-date-day');

    todayDate.value = currentDate.substring(0, 10);

    todayMonth.innerText = currentDate.substring(5, 7);
    todayDay.innerText = currentDate.substring(8, 10);

} catch { }