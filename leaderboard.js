// ===== ТАБЛИЦА ЛИДЕРОВ =====
//
// Используем лидерборд от бэка:
//   POST /api/event/get_leaderbord/{event_id}
// Ответ:
//   { "teams": [ { "name": "...", "score": 0, "stage": 0 }, ... ] }
//
// ⚠️ Бэк отдаёт массив команд НЕОТСОРТИРОВАННЫМ — сортировка по очкам
// делается здесь, на фронте (см. .sort() ниже). Это сделано намеренно,
// бэк сам об этом предупреждает в описании ручки.
//
// event_id не хранится на фронте, поэтому сначала получаем его
// динамически через getCurrentEventId() (берёт первое событие из списка).

async function loadLeaderboard() {

    const tbody = document.getElementById("leaderboardBody");

    const eventId = await getCurrentEventId();

    if (!eventId) {
        tbody.innerHTML = `<tr><td colspan="4">Не удалось определить текущее событие.</td></tr>`;
        return;
    }

    const { ok, data, networkError } = await apiRequest(
        `/api/event/get_leaderbord/${eventId}`,
        { method: "POST" }
    );

    if (networkError) {
        tbody.innerHTML = `<tr><td colspan="4">Не удалось подключиться к серверу. Проверьте соединение.</td></tr>`;
        return;
    }

    if (!ok || !data || !Array.isArray(data.teams)) {
        tbody.innerHTML = `<tr><td colspan="4">Не удалось загрузить таблицу лидеров.</td></tr>`;
        return;
    }

    // Ручка возвращает НЕОТСОРТИРОВАННЫЙ массив — сортируем сами по очкам
    const teams = [...data.teams].sort((a, b) => b.score - a.score);

    if (teams.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4">Пока нет ни одной команды.</td></tr>`;
        return;
    }

    tbody.innerHTML = teams.map((team, index) => `
        <tr>
            <td>${index + 1}</td>
            <td>${escapeHtml(team.name)}</td>
            <td>${team.stage}</td>
            <td>${team.score}</td>
        </tr>
    `).join("");
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

loadLeaderboard();
