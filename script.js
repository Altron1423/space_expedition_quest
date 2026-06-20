// ===== СТРАНИЦА ЗАДАЧИ: КОМИКС → ЗАДАЧА → ОТВЕТ =====
//
// Логика уровня:
//   1) Если команда ещё не смотрела видео-вступление — отправляем на intro.html
//   2) Вызываем start_stage — получаем задачу текущего этапа
//   3) Показываем комикс-картинку (15 секунд, кнопка "Далее" заблокирована)
//   4) Показываем саму задачу и поле для ответа
//   5) При отправке ответа — вызываем finish_stage,
//      получаем complete (true/false) и comics_png_name для следующего шага

const COMIC_DURATION_SECONDS = 15;

// ⚠️ ВРЕМЕННАЯ ЗАГЛУШКА: у бэка пока нет эндпоинта раздачи картинок комиксов,
// поэтому показываем одну статичную картинку на все уровни.
// Когда бэк выложит эндпоинт — заменить функцию getComicImageHtml() ниже.
const PLACEHOLDER_COMIC_IMAGE_URL = "https://placehold.co/700x260/0b1a33/33d6ff?text=Комикс+квеста";

function getComicImageHtml(pngName) {
    // pngName сейчас не используется — ждём эндпоинт раздачи файлов от бэка.
    return `<img src="${PLACEHOLDER_COMIC_IMAGE_URL}" alt="Комикс" style="max-width:100%;border-radius:18px;">`;
}

// Элементы слайда с комиксом
const comicStage = document.getElementById("comicStage");
const comicTitle = document.getElementById("comicTitle");
const comicImage = document.getElementById("comicImage");
const comicNextCard = document.getElementById("comicNextCard");
const comicNextBtn = document.getElementById("comicNextBtn");

// Элементы слайда с задачей
const taskStage = document.getElementById("taskStage");
const taskTitle = document.getElementById("taskTitle");
const taskText = document.getElementById("taskText");
const taskImage = document.getElementById("taskImage");
const answerCard = document.getElementById("answerCard");
const helpCard = document.getElementById("helpCard");
const answerInput = document.getElementById("answer");
const submitBtn = document.getElementById("submitBtn");
const result = document.getElementById("result");

// Верхняя плашка с XP/уровнем
const topXP = document.getElementById("topXP");
const topLevel = document.getElementById("topLevel");

let currentStage = null; // данные текущего этапа, пришедшие от start_stage

init();

async function init() {

    // Шаг 0 — без регистрации/входа команды дальше идти нет смысла
    if (localStorage.getItem("access_token") === null) {
        window.location.href = "register.html";
        return;
    }

    // Шаг 1 — видео-вступление показывается один раз за всю игру
    if (localStorage.getItem("intro_watched") !== "true") {
        window.location.href = "intro.html";
        return;
    }

    await loadStage();
}

// Запрашивает у бэка текущий этап команды и запускает показ комикса
async function loadStage() {

    const { ok, data, networkError } = await startStage();

    if (networkError) {
        comicTitle.textContent = "Не удалось подключиться к серверу.";
        return;
    }

    if (!ok || !data) {
        comicTitle.textContent = "Не удалось загрузить этап. Попробуйте обновить страницу.";
        return;
    }

    currentStage = data;

    topLevel.textContent = `Уровень ${currentStage.stage}`;
    topXP.textContent = "— XP";

    showComicSlide();
}

// ===== СЛАЙД КОМИКСА (15 секунд) =====
function showComicSlide() {

    comicStage.style.display = "block";
    taskStage.style.display = "none";
    comicNextCard.style.display = "block";
    answerCard.style.display = "none";
    helpCard.style.display = "none";

    comicTitle.textContent = currentStage.name;
    comicImage.innerHTML = getComicImageHtml(currentStage.png_name);

    let secondsLeft = COMIC_DURATION_SECONDS;
    comicNextBtn.disabled = true;
    comicNextBtn.textContent = `ДАЛЕЕ (${secondsLeft})`;

    const timerId = setInterval(() => {
        secondsLeft -= 1;

        if (secondsLeft <= 0) {
            clearInterval(timerId);
            comicNextBtn.disabled = false;
            comicNextBtn.textContent = "ДАЛЕЕ";
        } else {
            comicNextBtn.textContent = `ДАЛЕЕ (${secondsLeft})`;
        }
    }, 1000);
}

comicNextBtn.addEventListener("click", () => {
    if (comicNextBtn.disabled) return;
    showTaskSlide();
});

// ===== СЛАЙД ЗАДАЧИ =====
function showTaskSlide() {

    comicStage.style.display = "none";
    comicNextCard.style.display = "none";

    taskStage.style.display = "block";
    answerCard.style.display = "block";
    helpCard.style.display = "block";

    taskTitle.textContent = currentStage.name;
    taskText.textContent = currentStage.text;
    taskImage.innerHTML = getComicImageHtml(currentStage.png_name);

    answerInput.value = "";
    result.textContent = "";
}

submitBtn.addEventListener("click", handleSubmit);

async function handleSubmit() {

    const value = answerInput.value.trim();

    if (!value) {
        result.textContent = "Введите ответ.";
        return;
    }

    if (!currentStage) {
        result.textContent = "Этап ещё не загружен, подождите.";
        return;
    }

    submitBtn.disabled = true;
    result.textContent = "Проверяем ответ...";

    const { ok, data, networkError } = await finishStage(
        value,
        currentStage.problem_id,
        currentStage.data_set_id
    );

    submitBtn.disabled = false;

    if (networkError) {
        result.textContent = "Не удалось подключиться к серверу.";
        return;
    }

    if (!ok || !data) {
        result.textContent = "Не удалось отправить ответ. Попробуйте снова.";
        return;
    }

    if (data.complete) {
        result.textContent = "Правильно! 🚀 Переходим к следующему этапу...";
        setTimeout(loadStage, 1500);
    } else {
        result.textContent = "Неверно, попробуйте снова.";
    }
}
