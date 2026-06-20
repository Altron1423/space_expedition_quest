// ===== ВИДЕО-ВСТУПЛЕНИЕ (показывается один раз перед всей игрой) =====
//
// Кнопка "Далее" блокируется на фиксированное время (см. INTRO_LOCK_SECONDS),
// независимо от реальной длины видеофайла — это значение задано отдельно
// от длительности самого ролика.

const INTRO_LOCK_SECONDS = 20;

const introVideo = document.getElementById("introVideo");
const introNextBtn = document.getElementById("introNextBtn");
const introHint = document.getElementById("introHint");

// Если команда уже смотрела вступление раньше — сразу пропускаем эту страницу.
if (localStorage.getItem("intro_watched") === "true") {
    window.location.href = "index.html";
}

// Запоминаем, до какого момента видео было честно просмотрено,
// чтобы не дать просто перетащить полосу прокрутки вперёд.
let maxWatchedTime = 0;

introVideo.addEventListener("timeupdate", () => {
    if (introVideo.currentTime > maxWatchedTime + 0.5) {
        introVideo.currentTime = maxWatchedTime;
    } else {
        maxWatchedTime = introVideo.currentTime;
    }
});

// Видео просто доигрывает до конца и останавливается на последнем кадре —
// зацикливание не нужно, ожидание контролируется отдельным таймером ниже.

let secondsLeft = INTRO_LOCK_SECONDS;
introNextBtn.disabled = true;
introHint.textContent = `Подождите ${secondsLeft} секунд, чтобы продолжить...`;

const timerId = setInterval(() => {
    secondsLeft -= 1;

    if (secondsLeft <= 0) {
        clearInterval(timerId);
        introNextBtn.disabled = false;
        introHint.textContent = "Можно продолжать.";
    } else {
        introHint.textContent = `Подождите ${secondsLeft} секунд, чтобы продолжить...`;
    }
}, 1000);

introNextBtn.addEventListener("click", () => {
    if (introNextBtn.disabled) return;

    localStorage.setItem("intro_watched", "true");
    window.location.href = "index.html";
});
