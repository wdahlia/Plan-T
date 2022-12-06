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
    // const progress = setInterval(graph, 40);
    // setTimeout(function () {
    //     clearInterval(progress)
    // }, 6000);

} catch { }

try {

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

    slideBtnClick(".add-btn", slideToggle);


} catch { }


try {
    const tasks = document.querySelectorAll('.today-task-list .task');
    const taskView = document.querySelector('#task-detail');
    const taskDetailForm = document.querySelector('#today-detail-form');
    const detailTit = document.querySelector('#detail-title');
    const detailCont = document.querySelector('#detail-cont');
    const detailBtnDel = document.querySelector('#detail-btn-del');

    const taskMenu = function (e) {
        // console.log(this.dataset.todoPk);
        e.preventDefault();
        taskView.classList.toggle('activate');

        this.classList.toggle('activate');

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
        let delUrl = '/todos/delete/';
        let updateUrl = '/todos/update/';

        axios({
            method: 'POST',
            url: '/todos/today/',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'multipart/form-data'
            },
        })
            .then((res) => {
                const data = res.data.resJson;
                jsonParse = JSON.parse(data);

                const nodes = [...this.parentElement.children];
                const idx = nodes.indexOf(this);

                // todo 수정 업데이트 버튼 actions 속성 부여
                updateUrl = updateUrl + '1';
                taskDetailForm.setAttribute('action', `${updateUrl}`);
                console.log(updateUrl);

                // todo 삭제 버튼 href 속성 부여
                delUrl = delUrl + '1';
                console.log(delUrl);
                detailBtnDel.setAttribute('href', `${delUrl}`);

                detailTit.value = jsonParse[idx].fields.title;
                detailCont.value = jsonParse[idx].fields.content;

                // const todoPK = jsonParse[idx].fields.pk;
                // delUrl = delUrl + `${todoPK}`;
                ;
            })


    }
    tasks.forEach(task => {
        task.addEventListener('click', taskMenu);
    })

} catch { }

try {
    const todayDate = document.querySelector('#id_when');
    const currentDate = new Date().toLocaleString();
    const todayMonth = document.querySelector('.today-date-month');
    const todayDay = document.querySelector('.today-date-day');

    todayDate.value = currentDate.substring(0, 10);
    todayMonth.innerText = currentDate.substring(6, 8);
    todayDay.innerText = currentDate.substring(9, 11);

} catch { }


try {
    // 요일 activate
    const week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',]
    const weekdayNow = week[new Date().getDay()];

    const weekArea = document.querySelector('.week-area');
    const weekdayAll = document.querySelectorAll('.weekday');

    for (i = 0; i < week.length; i++) {
        weekdayAll[i].innerText = week[i];
        if (weekdayAll[i].innerText === weekdayNow) {
            weekdayAll[i].classList.add('activate');
            const boxWidth = document.querySelector('.box').clientWidth;
            const scrollPos = (boxWidth * i);
            weekArea.scrollTo({
                top: 0,
                left: scrollPos,
                behavior: 'smooth'
            });
        }
    }


    // 이전, 다음주 변경 비동기
    const weekBtn = document.querySelectorAll('.week-btn');

    let cnt = 0;
    const weekMove = function (e) {
        e.preventDefault();
        const isPrev = e.target.parentElement.dataset.isPrev;
        let urls = '/todos/week/';
        if (isPrev === 'true') {
            cnt--;
            cnt = String(cnt);
            urls = `${urls}${cnt}`
            e.target.parentElement.setAttribute('data-week-cnt', `${cnt}`)
        } else {
            cnt++;
            cnt = String(cnt);
            urls = `${urls}${cnt}`
            e.target.parentElement.setAttribute('data-week-cnt', `${cnt}`)
        }
        e.target.parentElement.setAttribute('href', `${urls}`);

        for (let i = 0; i < 7; i++) {
            if (cnt != 0) {
                weekdayAll[i].classList.remove('activate');
                weekArea.scrollTo({
                    top: 0,
                    left: 0,
                    behavior: 'smooth'
                });
            } else if (weekdayAll[i].innerText === weekdayNow && cnt == 0) {
                weekdayAll[i].classList.add('activate');
                const boxWidth = document.querySelector('.box').clientWidth;
                const scrollPos = (boxWidth * i);
                weekArea.scrollTo({
                    top: 0,
                    left: scrollPos,
                    behavior: 'smooth'
                });
            }
        }



        axios({
            method: 'get',
            url: `${urls}`,
        })
            .then((res) => {

                let data = res.data.resJson;
                jsonParse = JSON.parse(data[1]);

                const tasklist = document.querySelectorAll('.task-list');
                const tasktest = document.querySelector('.task-cont-test');

                for (let i = 0; i < 7; i++) {

                    while (tasklist[i].hasChildNodes()) {
                        tasklist[i].removeChild(
                            tasklist[i].firstChild
                        )
                    }
                }

                for (let i = 0; i < data.length; i++) {
                    jsonParse = JSON.parse(data[i]);

                    if (jsonParse.length != 0) {

                        for (let j = 0; j < jsonParse.length; j++) {

                            tasklist[i].insertAdjacentHTML("beforeend", `
                            <li class="task">
                                <p class="task-cont">${jsonParse[j].fields.title}</p>
                            </li>
                            `)

                        }
                    }

                    tasklist[i].insertAdjacentHTML("beforeend", `
                            <li class="task deactivate">
                                <p class="task-cont">add task</p>
                            </li>
                            `)
                }
            });
    };

    weekBtn.forEach(btn => {
        btn.addEventListener('click', weekMove)
    });

} catch { }

try {

} catch { }