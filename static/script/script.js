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
    console.log($r1, r1);
    function graph() {
        // r1 = r1 + ($r1 - r1) * 0.045;
        r1 = 1.6
        console.log(r1);
        console.log(Math.round((r1 * 180 / Math.PI + 90) / 360 * 100));

        ctx.clearRect(0, 0, 100, 100);
        ctx.strokeStyle = "#3cddaa";
        ctx.lineWidth = 10;
        ctx.lineCap = "round";
        ctx.beginPath();
        ctx.arc(50, 50, 40, -Math.PI / 2, r1, false);
        ctx.stroke();

        // const rateArea = document.querySelector('#progress-per');
        // let achRate = Number(rateArea.dataset.achRate);
        // console.log(achRate);
        // rateArea.innerText = `${achRate}%`;

        document.getElementById('progress-per').innerHTML = Math.round((r1 * 180 / Math.PI + 90) / 360 * 100) + "%";
    }
    graph();
    // const progress = setInterval(graph, 40);
    // setTimeout(function () {
    //     clearInterval(progress)
    // }, 6000);

} catch { }

try {
    //  today 할일 등록 토글 
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
    // 할일 기능 관련 DOM 객체 지정
    const tasks = document.querySelectorAll('.today-task-list .task');
    const taskConts = document.querySelectorAll('.today-task-list .task .task-cont')
    const taskView = document.querySelector('#task-detail');
    const taskDetailForm = document.querySelector('#today-detail-form');
    const detailTit = document.querySelector('#detail-title');
    const detailCont = document.querySelector('#detail-cont');
    const detailST = document.querySelector('#starttime-pick-edit');
    const detailET = document.querySelector('#endtime-pick-edit');
    const detailBtnDel = document.querySelector('#detail-btn-del');
    const detailDelForm = document.querySelector('#detail-del-form');
    const todayStudyArea = document.querySelector('.today-study-area');
    const updateBtn = document.querySelector('#todo-update');

    // 할일 클릭 시 옆에 상세 토글 나오는 기능, json 데이터 비동기, 할일 active 토글 기능
    const taskMenu = function (e) {
        e.preventDefault();

        for (let i = 0; i < tasks.length; i++) {
            if (tasks[i].classList.contains('activate')) {
                tasks[i].classList.remove('activate');
            }
        }
        todayStudyArea.classList.toggle('hide');
        taskView.classList.toggle('activate');
        // this.classList.toggle('activate');
        if (taskView.classList.contains('activate')) {
            this.parentElement.classList.add('activate');
        } else {
            this.parentElement.classList.remove('activate');
        }
        // this.classList.toggle('activate');

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

                // const nodes = [...this.parentElement.children];
                // const idx = nodes.indexOf(this);
                const nodes = [...tasks];
                const idx = nodes.indexOf(this.parentElement);

                // todo 수정 업데이트 버튼 actions 속성 부여
                const todoPK = jsonParse[idx].pk;
                updateUrl = updateUrl + `${todoPK}`;
                // updateUrl = this.dataset.taskUrl;
                taskDetailForm.setAttribute('action', `${updateUrl}`);

                // todo 삭제 버튼 href 속성 부여
                delUrl = delUrl + `${todoPK}`;
                detailDelForm.setAttribute('action', `${delUrl}`);

                // 받아온 todo 데이터  input에 대입
                detailTit.value = jsonParse[idx].fields.title;
                detailCont.value = jsonParse[idx].fields.content;
                detailST.value = jsonParse[idx].fields.started_at;
                detailET.value = jsonParse[idx].fields.expired_at;
                ;
            })
    };

    // 각 할일을 누를 때마다 이벤트 작동하도록 forEach 사용
    taskConts.forEach(taskCont => {
        taskCont.addEventListener('click', taskMenu);
    });

    // today todo 업데이트 비동기
    updateBtn.addEventListener('click', function (e) {
        e.preventDefault();
        const taskDetailForm = document.querySelector('#today-detail-form');

        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
        let urls = taskDetailForm.getAttribute('action');
        console.log(urls);
        axios({
            method: 'POST',
            url: `${urls}`,
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'multipart/form-data'
            },
            data: new FormData(taskDetailForm),
        })
            .then((res) => {
                console.log(res);
                const data2 = res.data;
                console.log(data2);
                for (let i = 0; i < taskConts.length; i++) {
                    if (taskConts[i].parentElement.classList.contains('activate')) {
                        taskConts[i].innerText = data2.todoTitle;
                    }
                }
            })
    });

} catch { }

try {
    // 타임테이블 생성
    const timetableAreaL = document.querySelector('.timetable-left');
    const timetableAreaR = document.querySelector('.timetable-right');
    const timetableHourL = document.querySelector('.hour-left');
    const timetableHourR = document.querySelector('.hour-right');
    let num = 54

    while (timetableAreaL.children.length < 54) {
        const timeMinBox = document.createElement('p');
        timeMinBox.classList.add('timetable-min');
        timetableAreaL.appendChild(timeMinBox);
    }
    while (timetableAreaR.children.length < 54) {
        const timeMinBox = document.createElement('p');
        timeMinBox.classList.add('timetable-min');
        timetableAreaR.appendChild(timeMinBox);
    }
    for (let i = 0; i < 9; i++) {
        const hourTimeL = document.createElement('p');
        hourTimeL.innerText = i + 6;
        timetableHourL.appendChild(hourTimeL);

        const hourTimeR = document.createElement('p');
        hourTimeR.innerText = i + 15;
        timetableHourR.appendChild(hourTimeR);
    }

    // 장고 템플릿으로 time_list 값 넣어둔 DOM 가져오기
    const testBox = document.querySelectorAll('.testbox');

    for (let i = 0; i < testBox.length; i++) {
        // dataset으로 time_list 값 가져옴
        let lng = testBox[i].dataset.timeArray.length - 1;
        let arr = testBox[i].dataset.timeArray.substring(1, lng);

        // str 을 num 으로 변경 > for 문 활용하기 위해서 변경함
        arr = arr.split(', ')
        let startAt = Number(arr[0]);
        let minCnt = Number(arr[1]);

        if (startAt > 54) {
            startAt -= 54;
            for (let j = startAt; j < startAt + minCnt; j++) {
                timetableAreaR.children[j].classList.add('activate');
            }
        } else {
            for (let j = startAt; j < startAt + minCnt; j++) {
                timetableAreaL.children[j].classList.add('activate');
            }
        }
    }


} catch { }

try {
    const todayDate = document.querySelector('#id_when');
    const currentDate = new Date().toLocaleString();
    const todayMonth = document.querySelector('.today-date-month');
    const todayDay = document.querySelector('.today-date-day');

    // 오늘 날짜 구해서 todos-today 에 date인풋 value 값으로 바로 넣어주기
    todayDate.value = currentDate.substring(0, 10);

    // todos-today 메인에 현재날짜 표시
    todayMonth.innerText = currentDate.split('. ')[1];
    todayDay.innerText = currentDate.split('. ')[2];

} catch { }


try {
    // 요일 activate
    const week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',]
    const weekdayNow = week[new Date().getDay()];
    const prevWeekValue = document.querySelector('.prev-week');
    const nextWeekValue = document.querySelector('.next-week');
    const weekUpdate = function (days) {
        let datumP = new Date();
        // console.log(weekSun);
        datumP.setDate(datumP.getDate() - datumP.getDay() + days);
        let prevWeek = datumP.toLocaleString().split('. ').slice(0, 3);
        // console.log(prevWeek);
        prevWeekValue.innerText = `~ ${prevWeek[0]}.${prevWeek[1]}.${prevWeek[2]}`;
        datumP.setDate(datumP.getDate() + 6);
        console.log(datumP);
        let nextWeek = datumP.toLocaleString().split('. ').slice(0, 3);
        // console.log(nextWeek);
        nextWeekValue.innerText = `${nextWeek[0]}.${nextWeek[1]}.${nextWeek[2]} ~`;
    };
    weekUpdate(0);

    // console.log(datumP.toLocaleString().split('. ')[2]);


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
    let weekCnt = 0;
    const weekMove = function (e) {
        e.preventDefault();
        // 주차 날짜 업데이트

        const isPrev = e.target.parentElement.dataset.isPrev;
        let urls = '/todos/week/';
        if (isPrev === 'true') {
            cnt--;
            weekCnt -= 7;
            console.log(weekCnt);
            cnt = String(cnt);
            urls = `${urls}${cnt}`
            e.target.parentElement.setAttribute('data-week-cnt', `${cnt}`)
        } else {
            cnt++;
            weekCnt += 7;
            cnt = String(cnt);
            urls = `${urls}${cnt}`
            e.target.parentElement.setAttribute('data-week-cnt', `${cnt}`)
        }
        e.target.parentElement.setAttribute('href', `${urls}`);

        weekUpdate(weekCnt);

        for (let i = 0; i < 7; i++) {
            // 이번주가 아니면 요일에 activate 표시 제거
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

        //  todo 데이터 불러오는 axios
        axios({
            method: 'get',
            url: `${urls}`,
        })
            .then((res) => {
                let data = res.data.resJson;
                jsonParse = JSON.parse(data[1]);

                const tasklist = document.querySelectorAll('.task-list');

                // 새 데이터 채우기 전 기존 html 삭제하기
                for (let i = 0; i < 7; i++) {
                    while (tasklist[i].hasChildNodes()) {
                        tasklist[i].removeChild(
                            tasklist[i].firstChild
                        )
                    }
                }

                for (let i = 0; i < data.length; i++) {
                    jsonParse = JSON.parse(data[i]);

                    // 받아온 json에 데이터가 있으면 새 데이터로 채워넣기
                    if (jsonParse.length != 0) {
                        for (let j = 0; j < jsonParse.length; j++) {
                            if (jsonParse[j].fields.is_completed) {
                                tasklist[i].insertAdjacentHTML("beforeend", `
                                <li class="task deactivate">
                                <p class="task-cont">${jsonParse[j].fields.title}</p>
                                <input type="checkbox" name="task-chb${jsonParse[j].pk}" id="task-chb${jsonParse[j].pk}" checked="checked">
                                <label for="task-chb${jsonParse[j].pk}" class="task-chb"></label>
                                </li>
                                `)
                            } else {
                                tasklist[i].insertAdjacentHTML("beforeend", `
                                <li class="task">
                                <p class="task-cont">${jsonParse[j].fields.title}</p>
                                <input type="checkbox" name="task-chb${jsonParse[j].pk}" id="task-chb${jsonParse[j].pk}" >
                                <label for="task-chb${jsonParse[j].pk}" class="task-chb"></label>
                                </li>
                                `)
                            }

                        }
                    } else {
                        // 받아오는 데이터 없으면 비어있는 표시 넣기
                        tasklist[i].insertAdjacentHTML("beforeend", `
                        <li class="task-empty">
                        <p class="task-cont"> 작성된 할일이 없어요 :(</p>
                        </li>
                        `)
                    }
                }
            });
    };

    weekBtn.forEach(btn => {
        btn.addEventListener('click', weekMove)
    });

} catch { }

// Todo is_completed 비동기
try {
    // Axios POST method csrf token setting
    // link : https://velog.io/@corner3499/Django-9-CSRF-Token-%EC%B2%98%EB%A6%AC-Todo%EC%9D%98-%EB%A7%88%EC%A7%80%EB%A7%89
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';

    // 실제 데이터가 들어있는 input tags 들을 담을 변수
    let inputTags = [];
    // task 클래스를 가진 녀석들을 다 찾아냄
    document.querySelectorAll(".task").forEach(
        function (v, i, o) {
            // 자식들 중 input 태그를 지정함
            inputTags.push(o[i].children[1]);
        }
    );

    inputTags.forEach(function (v, i, o) {
        // 렌더링 되고나서 초기 상태에 따른 활성화 클래스 추가 
        if (v.checked)
            v.parentElement.classList.add("deactivate");
        else
            v.parentElement.classList.remove("deactivate");

        v.addEventListener("click", () => {
            // 현재 체크 값 및 todo id 값 추출 
            is_completed = (v.checked) ? true : false;
            todoId = v.id.split("task-chb")[1];

            // axios post arguments 설정
            url = "/todos/is_completed/";
            data = {
                is_completed,
                todoId,
            };

            // axios 비동기 통신
            axios.post(
                url,
                data
            ).then((res) => {
                // 결과값이 잘 나오는지 출력
                // console.log(res.data.is_completed);

                // 결과값에 따른 활성화 클래스 추가 
                if (res.data.is_completed)
                    v.parentElement.classList.add("deactivate");
                else
                    v.parentElement.classList.remove("deactivate");
            });
        });
    });

} catch { }