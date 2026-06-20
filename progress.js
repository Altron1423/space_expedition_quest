

async function loadProgress() {

    const teamName = localStorage.getItem("team_name");

    const statLevel = document.getElementById("statLevel");
    const statSolved = document.getElementById("statSolved");
    const statTeamName = document.getElementById("statTeamName");
    const stagesList = document.getElementById("stagesList");

    if (!teamName) {
        stagesList.innerHTML = `<p>Команда не определена. Сначала нужно войти в систему (страница входа в разработке).</p>`;
        return;
    }

    const { ok, data, networkError } = await apiRequest("/api/team/get_all");

    if (networkError) {
        stagesList.innerHTML = `<p>Не удалось подключиться к серверу.</p>`;
        return;
    }

    if (!ok || !data || !Array.isArray(data.teams)) {
        stagesList.innerHTML = `<p>Не удалось загрузить данные прогресса.</p>`;
        return;
    }

    const myTeam = data.teams.find(team => team.name === teamName);

    if (!myTeam) {
        stagesList.innerHTML = `<p>Команда «${teamName}» не найдена среди зарегистрированных.</p>`;
        return;
    }

    const stages = Array.isArray(myTeam.stages) ? myTeam.stages : [];

    statTeamName.textContent = myTeam.name;
    statLevel.textContent = stages.length;
    statSolved.textContent = stages.length;

    if (stages.length === 0) {
        stagesList.innerHTML = `<p>Пока нет пройденных этапов.</p>`;
        return;
    }

    stagesList.innerHTML = stages.map(stage => `
        <div class="stat-box" style="text-align:left; margin-bottom:15px;">
            <div><strong>Этап ${stage.stage}</strong></div>
            <div>Задача: ${stage.problem ? escapeHtml(stage.problem.name) : "—"}</div>
            <div>Ответ команды: ${escapeHtml(stage.answer ?? "—")}</div>
        </div>
    `).join("");
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = String(str);
    return div.innerHTML;
}

loadProgress();
