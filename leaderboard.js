// leaderboard.js
(function() {
    "use strict";

    // ----- ИНСТРУМЕНТЫ -----
    function getSavedProgress() {
        let totalXP = parseInt(localStorage.getItem('totalXP')) || 0;
        let completed = JSON.parse(localStorage.getItem('completedLevels')) || [];
        let solved = completed.filter(v => v === true).length;
        return { totalXP, solved, completed };
    }

    function getTeamName() {
        try {
            const savedProfile = localStorage.getItem('profileData');
            const profile = savedProfile ? JSON.parse(savedProfile) : {};
            return profile.username || localStorage.getItem('registeredTeamName') || 'KosmosNav99';
        } catch (e) {
            return localStorage.getItem('registeredTeamName') || 'KosmosNav99';
        }
    }

    // ----- ГЕНЕРАЦИЯ ТАБЛИЦЫ -----
    function renderLeaderboard() {
        const container = document.getElementById('leaderboardContainer');
        if (!container) return;

        // 1. Получаем данные текущего пользователя
        const myData = getSavedProgress();
        const myXP = myData.totalXP;
        const mySolved = myData.solved;
        const username = getTeamName();

        // 2. СТАТИЧНЫЙ СПИСОК участников (10 человек + текущий)
        const baseUsers = [
            { name: 'StarHunter42', xp: 3250, solved: 12 },
            { name: 'NebulaPilot', xp: 2890, solved: 11 },
            { name: 'CosmicWizard', xp: 2710, solved: 10 },
            { name: 'OrionExplorer', xp: 2430, solved: 9 },
            { name: 'VoidRunner', xp: 2180, solved: 9 },
            { name: 'GalaxyTrekker', xp: 1940, solved: 8 },
            { name: 'AstroNaut_99', xp: 1710, solved: 7 },
            { name: 'NovaCore', xp: 1580, solved: 6 },
            { name: 'PulsarWave', xp: 1420, solved: 6 },
            { name: 'ZenithCoder', xp: 1280, solved: 5 },
        ];

        // Проверяем, есть ли текущий пользователь в списке, если нет — добавляем
        const existingIdx = baseUsers.findIndex(u => u.name === username);
        if (existingIdx === -1) {
            baseUsers.push({ name: username, xp: myXP, solved: mySolved });
        } else {
            // Обновляем данные существующего
            baseUsers[existingIdx].xp = myXP;
            baseUsers[existingIdx].solved = mySolved;
        }

        // Сортируем по XP (по убыванию)
        const sorted = [...baseUsers].sort((a, b) => b.xp - a.xp);

        // 3. Формируем HTML таблицы
        let html = `<table class="leaderboard">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Пилот</th>
                    <th>🚀 Звание</th>
                    <th>⭐ XP</th>
                    <th>✅ Уровней</th>
                </tr>
            </thead>
            <tbody>`;

        if (sorted.length === 0) {
            html += `<tr><td colspan="5" class="empty-message">Нет данных. Пройдите хотя бы один уровень!</td></tr>`;
        } else {
            sorted.forEach((user, index) => {
                const rank = index + 1;
                let medal = '';
                if (rank === 1) medal = '🥇 ';
                else if (rank === 2) medal = '🥈 ';
                else if (rank === 3) medal = '🥉 ';

                // Определяем звание по XP
                let title = 'Кадет';
                if (user.xp >= 3000) title = 'Хранитель Кода';
                else if (user.xp >= 2000) title = 'Старший навигатор';
                else if (user.xp >= 1000) title = 'Бортовой инженер';
                else if (user.xp >= 500) title = 'Помощник пилота';

                // Если это текущий пользователь — добавляем класс
                const isCurrent = (user.name === username);
                const rowClass = isCurrent ? 'current-user' : '';

                // Бейджи для топ-3
                let badgeClass = '';
                if (rank === 1) badgeClass = 'badge-gold';
                else if (rank === 2) badgeClass = 'badge-silver';
                else if (rank === 3) badgeClass = 'badge-bronze';

                html += `<tr class="${rowClass}">
                    <td class="rank-col"><span class="${badgeClass}">${medal || rank}</span></td>
                    <td><strong>${user.name}</strong> ${isCurrent ? '👈' : ''}</td>
                    <td>${title}</td>
                    <td>${user.xp}</td>
                    <td>${user.solved}</td>
                </tr>`;
            });
        }

        html += `</tbody></table>`;
        container.innerHTML = html;
    }

    // ----- ОБНОВЛЕНИЕ ПРИ ЗАГРУЗКЕ И ПО КЛИКУ -----
    document.addEventListener('DOMContentLoaded', function() {
        renderLeaderboard();

        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', function(e) {
                e.preventDefault();
                renderLeaderboard();
                this.textContent = '✓ Обновлено';
                setTimeout(() => { this.textContent = '⟳ Обновить'; }, 1200);
            });
        }

        // Обновляем имя в профиле
        const profileNameEl = document.getElementById('profileName');
        if (profileNameEl) {
            profileNameEl.textContent = getTeamName();
        }
    });

    // Обновляем таблицу при фокусе на вкладке
    window.addEventListener('focus', function() {
        renderLeaderboard();
    });

})();
