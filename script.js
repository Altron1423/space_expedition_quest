// ---------- ДАННЫЕ УРОВНЕЙ (согласно сценарию) ----------
const levels = [
  { // 1. Отборочный: Кодовые замки
    title: "УРОВЕНЬ 1: КОДОВЫЕ ЗАМКИ (Системы счисления)",
    comic: "Исследователи стоят полукругом перед циклопическими вратами руин – они кажутся совсем маленькими по сравнению с гигантскими постройками Протонов. Тео уже подключил свой кабель к панели замка, на экране горят примеры.",
    task: "Вход в руины заблокирован! Рядом с каждым замком высечены примеры в непривычных для нас системах счисления. Чтобы открыть дверь, переведите ответы в десятичную систему и введите коды! Первый замок: двоичное число 101101. Введите десятичный код.",
    answer: "45",
    answerType: "number",
    hint: "Каждая позиция – степень двойки: 1·2⁵ + 0·2⁴ + 1·2³ + 1·2² + 0·2¹ + 1·2⁰ = 45.",
    maxMinutes: 8
  },
  { // 2. Программируемый робот
    title: "УРОВЕНЬ 2: ПРОГРАММИРУЕМЫЙ РОБОТ (Алгоритмы)",
    comic: "Внутри коридора руин происходит внезапный обвал. Путь вперёд полностью завален каменными глыбами. Тео испуганно прикрывает робота «Байта» от падающих камней.",
    task: "Внимание, обвал прохода! Самим нам эти глыбы не разобрать. Придётся запустить нашего маленького робота-черепашку. Напишите для него оптимальный алгоритм: робот находится в левом нижнем углу (1,1) поля 5×5, ему нужно добраться до правого верхнего угла (5,5), двигаясь только вверх и вправо. Камни лежат в клетках (3,3) и (3,4). Сколько минимально шагов потребуется?",
    answer: "8",
    answerType: "number",
    hint: "Без камней нужно 8 шагов (4 вверх + 4 вправо). Камни не мешают, если идти сначала все шаги вверх, потом вправо.",
    maxMinutes: 8
  },
  { // 3. Лабиринт истины
    title: "УРОВЕНЬ 3: ЛАБИРИНТ ИСТИНЫ (Булева логика)",
    comic: "Команда оказывается в круглом зале, от которого во все стороны расходятся коридоры-развилки. Над каждым проходом горят логические выражения. Астра светит фонариком в тёмный коридор Лабиринта Истины.",
    task: "Перед нами Лабиринт Истины! Чтобы дойти до выхода, нужно проверять логические условия на каждой развилке. Если выражение истинно — наш путь налево, если ложно — направо. Вычислите: (¬(A ∧ B) ∨ C) при A = Истина, B = Ложь, C = Истина. Введите 1 (истина/налево) или 0 (ложь/направо).",
    answer: "1",
    answerType: "number",
    hint: "A∧B = Ложь, отрицание = Истина, Истина ∨ Истина = Истина → 1.",
    maxMinutes: 8
  },
  { // 4. Дешифратор
    title: "УРОВЕНЬ 4: ДЕШИФРАТОР (Кодирование информации)",
    comic: "Капитан Лео настраивает бортовую рацию. Из динамиков доносятся странные зашифрованные звуки.",
    task: "Чтобы защитить наши находки от космических пиратов, штаб перевёл общение с базой на шифрованный канал! Примите сигнал, расшифруйте его с помощью шифра Цезаря. Слово «Вжёуп» зашифровано со сдвигом 3 (А→Г, Б→Д…). Введите расшифрованное слово строчными буквами.",
    answer: "ветер",
    answerType: "string",
    hint: "Каждая буква сдвигается назад на 3 позиции в русском алфавите.",
    maxMinutes: 8
  },
  { // 5. Отправка данных
    title: "УРОВЕНЬ 5: ОТПРАВКА ДАННЫХ (Измерение информации)",
    comic: "Исследователи стоят в высокой комнате-шахте, где под самым потолком сквозь трещину ловит спутниковый сигнал.",
    task: "Связь ловит только под самым потолком! Чтобы отправить научные файлы, мы поднимем туда зонд. Рассчитайте время отправки: файл отчёта имеет размер 2 Мбайта, скорость передачи – 512 Кбит/с. Сколько секунд потребуется? (1 байт = 8 бит)",
    answer: "32",
    answerType: "number",
    hint: "2 Мбайта = 2·1024·1024·8 бит. Делим на 512·1024 бит/с = 32 секунды.",
    maxMinutes: 8
  },
  { // 6. Портал-сеть
    title: "УРОВЕНЬ 6: ПОРТАЛ-СЕТЬ (Графы и маршруты)",
    comic: "Финал миссии. Древние руины вокруг начинают дрожать. Перед командой активируется огромный эвакуационный портал.",
    task: "Исследование завершено, руины нестабильны! Пора возвращаться на «Аргус». Карманный компьютер записал схему комнат и расстояния: A–B=4, A–C=2, B–D=5, B–E=1, C–E=3, C–F=6, D–F=2, E–F=4. Найдите кратчайший путь от A до F. Введите длину пути числом.",
    answer: "8",
    answerType: "number",
    hint: "Самый короткий маршрут A→C→F: 2+6 = 8.",
    maxMinutes: 8
  },
  // ФИНАЛЬНЫЙ ЭТАП (усложнённые задания, время 15 минут)
  { // 7. Главные шлюзы Архива
    title: "ФИНАЛ: ГЛАВНЫЕ ШЛЮЗЫ АРХИВА (Системы счисления)",
    comic: "Астра светит мощным прожектором на ледяные ворота башни. На замёрзшем металле пульсируют огромные ряды цифр.",
    task: "Эти шлюзы заперты куда надёжнее, чем на Ксероне-7! Защита Архива требует ввести целую серию кодов. Переведите шестнадцатеричное число 1A3 в десятичную систему.",
    answer: "419",
    answerType: "number",
    hint: "1·16² + 10·16¹ + 3·16⁰ = 256 + 160 + 3 = 419.",
    maxMinutes: 15
  },
  { // 8. Робот в ледяном плену
    title: "ФИНАЛ: РОБОТ В ЛЕДЯНОМ ПЛЕНУ (Алгоритмы)",
    comic: "Из-за резкого перепада температур сверху срываются огромные замёрзшие глыбы, намертво блокируя проход. Тео обнимает дрона.",
    task: "Проход заморожен и завален! «Байт», тебе придётся расчистить путь, но батарея разряжается вдвое быстрее. На поле 10×10 старт (1,1), финиш (10,10). Стены в клетках (3,3),(3,4),(4,3),(4,4). Найдите длину кратчайшего пути (шаги вверх/вниз/влево/вправо).",
    answer: "20",
    answerType: "number",
    hint: "Манхэттенское расстояние 18, но из-за квадрата стен нужно сделать 2 лишних шага: итого 20.",
    maxMinutes: 15
  },
  { // 9. Залы Квантового Разума
    title: "ФИНАЛ: ЗАЛЫ КВАНТОВОГО РАЗУМА (Булева логика)",
    comic: "Команда заходит в гигантский многоуровневый зал, где коридоры парят в воздухе на магнитных подушках. Над развилками сложные формулы.",
    task: "Мы в главном процессоре Архива! На развилках тройные логические цепочки. Вычислите: ¬( (A ∨ B) ∧ (¬C) ) при A = Ложь, B = Истина, C = Ложь. Ответ: 1 (истина/налево) или 0 (ложь/направо).",
    answer: "0",
    answerType: "number",
    hint: "A∨B = 1, ¬C = 1, (1∧1)=1, ¬1 = 0.",
    maxMinutes: 15
  },
  { // 10. Перехват пиратского крейсера
    title: "ФИНАЛ: ПЕРЕХВАТ ПИРАТСКОГО КРЕЙСЕРА (Шифры)",
    comic: "Экран скафандра капитана Лео загорается красным. В небе кружит огромный боевой корабль пиратов.",
    task: "Пираты глушат основную частоту! База шлёт инструкции, но они зашифрованы. Расшифруйте сообщение «Gur cerfbagny vf pbzvat» (ROT13, английский). Введите строчными латиницей.",
    answer: "the presidential is coming",
    answerType: "string",
    hint: "ROT13 заменяет каждую букву на букву через 13 позиций: a→n, b→o и т.д.",
    maxMinutes: 15
  },
  { // 11. Гипер-излучатель Архива
    title: "ФИНАЛ: ГИПЕР-ИЗЛУЧАТЕЛЬ АРХИВА (Большие данные)",
    comic: "Тео подключает кабели к центральному ядру Архива – гигантскому светящемуся кристаллу. Вокруг кристалла вращаются огромные кластеры данных.",
    task: "Здесь терабайты информации! Нужно задействовать планетарный гипер-излучатель. Отправить 5 файлов по 700 Мбайт каждый со скоростью 100 Мбит/с. Сколько минут потребуется? (1 байт=8 бит, округлите до целых).",
    answer: "5",
    answerType: "number",
    hint: "Объём = 5·700·8 = 28000 Мбит. Время = 28000/100 = 280 сек = 4,67 мин ≈ 5 мин.",
    maxMinutes: 15
  },
  { // 12. Финальный прыжок
    title: "ФИНАЛ: ПОРТАЛ-СЕТЬ (Сложнейший граф)",
    comic: "Башня Архива вибрирует, ледяные стены рушатся. В центре зала открывается ослепительный Портал Перехода.",
    task: "Архив перезагружается! Защитный компьютер выдал финальную карту: A–B=5, A–C=3, B–D=4, B–E=2, C–E=1, C–F=6, D–G=7, E–G=3, F–G=2. Найдите кратчайшее расстояние от A до G.",
    answer: "7",
    answerType: "number",
    hint: "Путь A→C→E→G: 3+1+3 = 7.",
    maxMinutes: 15
  }
];

// Глобальные переменные
let currentLevel = 0;
let totalXP = 0;
let completedLevels = [];      // boolean
let timerInterval = null;
let startTime = null;
let maxMinutesCurrent = 8;
let isLevelCompleted = false;
let taskRevealed = false;      // показано ли задание (таймер запущен)

// DOM элементы
const levelTitleEl = document.getElementById("levelTitle");
const comicPlaceholder = document.getElementById("comicPlaceholder");
const comicTextEl = document.getElementById("comicText");
const showTaskBtn = document.getElementById("showTaskBtn");
const taskSection = document.getElementById("taskSection");
const taskTextEl = document.getElementById("taskText");
const answerInput = document.getElementById("answer");
const submitBtn = document.getElementById("submitBtn");
const resultDiv = document.getElementById("result");
const xpDisplay = document.getElementById("xpDisplay");
const xpProgressFill = document.getElementById("xpProgressFill");
const timerDisplay = document.getElementById("timerDisplay");
const potentialXPSpan = document.getElementById("potentialXP");
const hintBtn = document.getElementById("hintBtn");
const resetBtn = document.getElementById("resetBtn");

// Функции
function updateXPUI() {
    xpDisplay.textContent = `${totalXP} XP`;
    let percent = Math.min(100, (totalXP % 1000) / 10);
    xpProgressFill.style.width = `${percent}%`;
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

function startTimer(maxMinutes) {
    stopTimer();
    startTime = Date.now();
    maxMinutesCurrent = maxMinutes;
    timerInterval = setInterval(() => {
        if (isLevelCompleted) return;
        const elapsedSeconds = (Date.now() - startTime) / 1000;
        const elapsedMinutes = elapsedSeconds / 60;
        const remainingSeconds = Math.max(0, maxMinutesCurrent * 60 - elapsedSeconds);
        const mins = Math.floor(remainingSeconds / 60);
        const secs = Math.floor(remainingSeconds % 60);
        timerDisplay.textContent = `${mins.toString().padStart(2,'0')}:${secs.toString().padStart(2,'0')}`;
        let xpPotential = Math.max(0, Math.floor(100 * (1 - elapsedMinutes / maxMinutesCurrent)));
        if (xpPotential > 100) xpPotential = 100;
        potentialXPSpan.textContent = `⭐ Возможные XP: ${xpPotential}`;
    }, 200);
}

function calculateXP() {
    if (!startTime) return 0;
    const elapsedSeconds = (Date.now() - startTime) / 1000;
    const elapsedMinutes = elapsedSeconds / 60;
    let xp = Math.floor(100 * (1 - elapsedMinutes / maxMinutesCurrent));
    if (xp < 0) xp = 0;
    if (xp > 100) xp = 100;
    return xp;
}

function resetUIBeforeTask() {
    taskSection.classList.add("hidden");
    showTaskBtn.classList.remove("hidden");
    answerInput.disabled = true;
    submitBtn.disabled = true;
    taskRevealed = false;
    stopTimer();
    timerDisplay.textContent = "--:--";
    potentialXPSpan.textContent = "⏳ Нажмите \"Показать задание\"";
    resultDiv.textContent = "";
    answerInput.value = "";
}

function revealTask() {
    if (isLevelCompleted) {
        resultDiv.textContent = "Этот уровень уже пройден. Переходите к следующему.";
        return;
    }
    if (taskRevealed) return;
    taskSection.classList.remove("hidden");
    showTaskBtn.classList.add("hidden");
    answerInput.disabled = false;
    submitBtn.disabled = false;
    taskRevealed = true;
    startTimer(levels[currentLevel].maxMinutes);
}

function loadLevel(levelIndex) {
    if (levelIndex >= levels.length) {
        // Игра пройдена
        levelTitleEl.textContent = "ПОЗДРАВЛЯЕМ! МИССИЯ ВЫПОЛНЕНА";
        comicTextEl.textContent = "Экипаж «Аргуса» спасён, данные Протонов доставлены на Землю. Вы – Хранитель Кода!";
        comicPlaceholder.innerHTML = "🏆 ПОБЕДА! 🏆";
        taskSection.classList.add("hidden");
        showTaskBtn.classList.add("hidden");
        answerInput.disabled = true;
        submitBtn.disabled = true;
        resultDiv.textContent = "Игра пройдена. Сбросьте прогресс, чтобы начать заново.";
        stopTimer();
        isLevelCompleted = true;
        return;
    }
    isLevelCompleted = false;
    const lvl = levels[levelIndex];
    levelTitleEl.textContent = lvl.title;
    comicTextEl.textContent = lvl.comic;
    comicPlaceholder.innerHTML = `🎬 [КАДР КОМИКСА] ${lvl.comic.substring(0, 70)}...`;
    taskTextEl.textContent = lvl.task;
    resetUIBeforeTask();

    if (completedLevels[levelIndex]) {
        // Уровень уже пройден – показываем задание, но не даём отвечать
        taskSection.classList.remove("hidden");
        showTaskBtn.classList.add("hidden");
        answerInput.disabled = true;
        submitBtn.disabled = true;
        taskRevealed = true;
        timerDisplay.textContent = "00:00";
        potentialXPSpan.textContent = "✅ Уровень уже пройден";
        resultDiv.textContent = "Вы уже получили XP за этот уровень. Переходите к следующему.";
    }
}

function checkAnswer() {
    if (isLevelCompleted) {
        resultDiv.textContent = "Этот уровень уже пройден.";
        return;
    }
    if (!taskRevealed) {
        resultDiv.textContent = "Сначала нажмите «Показать задание»!";
        return;
    }
    if (currentLevel >= levels.length) {
        resultDiv.textContent = "Игра завершена.";
        return;
    }
    const lvl = levels[currentLevel];
    let userAnswer = answerInput.value.trim();
    if (userAnswer === "") {
        resultDiv.textContent = "Введите ответ!";
        return;
    }
    let isCorrect = false;
    if (lvl.answerType === "number") {
        let numUser = parseFloat(userAnswer);
        let numCorrect = parseFloat(lvl.answer);
        isCorrect = (numUser === numCorrect);
    } else {
        isCorrect = (userAnswer.toLowerCase() === lvl.answer.toLowerCase());
    }
    if (isCorrect) {
        if (completedLevels[currentLevel]) {
            resultDiv.textContent = "Вы уже получали XP за этот уровень! Переходите к следующему.";
            goToNextLevel();
            return;
        }
        stopTimer();
        const earnedXP = calculateXP();
        totalXP += earnedXP;
        completedLevels[currentLevel] = true;
        updateXPUI();
        const timeSpent = ((Date.now() - startTime) / 1000 / 60).toFixed(2);
        resultDiv.innerHTML = `✅ Правильно! +${earnedXP} XP (за ${timeSpent} мин). Переход к следующему заданию...`;
        localStorage.setItem("totalXP", totalXP);
        localStorage.setItem("currentLevel", currentLevel + 1);
        localStorage.setItem("completedLevels", JSON.stringify(completedLevels));
        setTimeout(() => {
            goToNextLevel();
        }, 2000);
    } else {
        resultDiv.textContent = "❌ Неправильный ответ. Попробуйте ещё раз. Время продолжает идти.";
    }
}

function goToNextLevel() {
    currentLevel++;
    localStorage.setItem("currentLevel", currentLevel);
    loadLevel(currentLevel);
}

function showHint() {
    if (currentLevel < levels.length && taskRevealed) {
        resultDiv.innerHTML = `💡 Подсказка: ${levels[currentLevel].hint}`;
    } else if (currentLevel < levels.length && !taskRevealed) {
        resultDiv.textContent = "Сначала откройте задание!";
    } else {
        resultDiv.textContent = "Игра пройдена.";
    }
}

function resetProgress() {
    if (confirm("Сбросить весь прогресс? Все XP и пройденные уровни будут удалены.")) {
        totalXP = 0;
        currentLevel = 0;
        completedLevels = new Array(levels.length).fill(false);
        updateXPUI();
        loadLevel(0);
        localStorage.setItem("totalXP", totalXP);
        localStorage.setItem("currentLevel", currentLevel);
        localStorage.setItem("completedLevels", JSON.stringify(completedLevels));
    }
}

function loadSavedProgress() {
    const savedXP = localStorage.getItem("totalXP");
    const savedLevel = localStorage.getItem("currentLevel");
    const savedCompleted = localStorage.getItem("completedLevels");
    if (savedXP !== null) totalXP = parseInt(savedXP);
    if (savedLevel !== null) currentLevel = parseInt(savedLevel);
    if (savedCompleted !== null) completedLevels = JSON.parse(savedCompleted);
    else completedLevels = new Array(levels.length).fill(false);
    updateXPUI();
    loadLevel(currentLevel);
}

function updateRegisteredTeamName() {
    const savedProfile = localStorage.getItem("profileData");
    const profile = savedProfile ? JSON.parse(savedProfile) : {};
    const teamName = profile.username || localStorage.getItem("registeredTeamName") || "KosmosNav99";
    const profileName = document.getElementById("profileName");

    if (profileName) {
        profileName.textContent = teamName;
    }
}

// Инициализация
loadSavedProgress();
updateRegisteredTeamName();
showTaskBtn.addEventListener("click", revealTask);
submitBtn.addEventListener("click", checkAnswer);
hintBtn.addEventListener("click", showHint);
resetBtn.addEventListener("click", resetProgress);
