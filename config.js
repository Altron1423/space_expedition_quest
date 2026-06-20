const API_URL = "http://26.239.170.23:8000"; // Адрес бэка


async function apiRequest(path, options = {}) {

    const token = localStorage.getItem("access_token");

    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    // Если есть токен — подставляем его в заголовок запроса
    if (token) {
        headers["Authorization"] = "Bearer " + token;
    }

    let response;

    try {
        response = await fetch(API_URL + path, {
            ...options,
            headers
        });
    } catch (networkError) {
        // Сюда попадаем, если сервер недоступен / нет интернета / CORS блок
        console.error("Сетевая ошибка при запросе к", path, networkError);
        return { ok: false, status: 0, data: null, networkError: true };
    }

    let data = null;

    try {
        data = await response.json();
    } catch {
        // Ответ может быть пустым (например, 204 No Content) — это нормально
    }

    return { ok: response.ok, status: response.status, data };
}


// ===== РАБОТА С ЭТАПАМИ (УРОВНЯМИ) =====
//
// Новая механика прохождения уровня:
//   1) Перед самой первой задачей за игру — один раз показывается видео.
//   2) Перед КАЖДЫМ уровнем — вызываем start_stage, получаем задачу,
//      показываем комикс-картинку 15 секунд, потом саму задачу.
//   3) После ответа команды — вызываем finish_stage (когда бэк выложит).
//
// startStage() и finishStage() — единая точка входа для этой логики,
// чтобы остальной код (script.js) не знал деталей про fetch и пути.

async function startStage() {
    // GET /api/team/start_stage — требует авторизации (токен из localStorage)
    // ⚠️ Метод именно GET, не POST (подтверждено свежей схемой от бэка).
    return apiRequest("/api/team/start_stage", { method: "GET" });
}

async function finishStage(answer, problemsId, dataSetId) {
    // POST /api/team/finish_stage
    // Тело запроса: { answer, problems_id, data_set_id }
    // Ответ: { complete: true/false, comics_png_name: "..." }
    return apiRequest("/api/team/finish_stage", {
        method: "POST",
        body: JSON.stringify({
            answer: answer,
            problems_id: problemsId,
            data_set_id: dataSetId
        })
    });
}


// ===== ПОЛУЧЕНИЕ ID ТЕКУЩЕГО СОБЫТИЯ (event_id) =====
//
// Лидерборд (event/get_leaderbord/{event_id}) требует event_id в пути,
// а на фронте мы его пока никак не храним. Поэтому берём событие
// динамически: запрашиваем список всех событий и берём первое.
//
// ⚠️ Это рабочее решение только пока в системе ОДНО соревнование.
// Если появится несколько активных событий одновременно — нужно будет
// придумать, как команда выбирает/узнаёт "своё" событие (например,
// event_id может прийти в ответе team/register при регистрации,
// и тогда его нужно сохранять в localStorage сразу при регистрации).
//
// ⚠️ ВАЖНО: путь /api/event/... подтверждён живым запросом к бэку
// (curl-пример в документации показал реальный ответ с unique_id события).
// Если снова появится 404 — проверить актуальность event_id в свежей /api/docs,
// событие на бэке может быть пересоздано с новым ID.

async function getCurrentEventId() {

    const { ok, data, networkError } = await apiRequest("/api/event/get_all");

    if (networkError || !ok || !data || !Array.isArray(data.events) || data.events.length === 0) {
        return null;
    }

    return data.events[0].unique_id;
}
