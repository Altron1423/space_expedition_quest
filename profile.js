// profile.js
(function() {
    "use strict";

    // ----- ХРАНИЛИЩЕ ДАННЫХ ПРОФИЛЯ -----
    function getProfileData() {
        const defaultData = {
            username: 'KosmosNav99',
            avatar: '🚀',
            totalXP: 0,
            completedLevels: [],
            attempts: {},
            startTimes: {}
        };
        
        try {
            const saved = localStorage.getItem('profileData');
            if (saved) {
                const data = JSON.parse(saved);
                // Обновляем XP и уровни из основных данных
                data.totalXP = parseInt(localStorage.getItem('totalXP')) || 0;
                data.completedLevels = JSON.parse(localStorage.getItem('completedLevels')) || [];
                return data;
            }
            return defaultData;
        } catch (e) {
            return defaultData;
        }
    }

    function saveProfileData(data) {
        localStorage.setItem('profileData', JSON.stringify(data));
    }

    // ----- ОСНОВНЫЕ ФУНКЦИИ -----
    function updateProfile() {
        const profile = getProfileData();
        const completed = profile.completedLevels || [];
        const solved = completed.filter(v => v === true).length;
        const totalLevels = 12;
        const progress = totalLevels > 0 ? Math.round((solved / totalLevels) * 100) : 0;
        const totalXP = profile.totalXP || 0;
        
        // Определяем звание
        let title = 'Кадет';
        if (totalXP >= 3000) title = 'Хранитель Кода';
        else if (totalXP >= 2000) title = 'Старший навигатор';
        else if (totalXP >= 1000) title = 'Бортовой инженер';
        else if (totalXP >= 500) title = 'Помощник пилота';

        // Обновляем левую карточку
        document.getElementById('displayName').textContent = profile.username;
        document.getElementById('userTitle').textContent = title;
        document.getElementById('statXP').textContent = totalXP;
        document.getElementById('statLevels').textContent = solved;
        document.getElementById('avatarEmoji').textContent = profile.avatar || '🚀';
        
        // Обновляем аватар в навбаре
        const avatarNav = document.getElementById('profileAvatar');
        if (avatarNav) {
            avatarNav.textContent = profile.avatar || '🚀';
            avatarNav.style.display = 'flex';
            avatarNav.style.alignItems = 'center';
            avatarNav.style.justifyContent = 'center';
            avatarNav.style.fontSize = '20px';
        }

        // Обновляем имя в навбаре
        document.getElementById('profileName').textContent = profile.username;

        // Обновляем детальную статистику
        document.getElementById('detailXP').textContent = totalXP;
        document.getElementById('detailSolved').textContent = `${solved}/${totalLevels}`;
        document.getElementById('detailProgress').textContent = `${progress}%`;
        
        // Вычисляем точность (имитация)
        const totalAttempts = Object.values(profile.attempts || {}).reduce((sum, a) => sum + a, 0);
        const correctAttempts = Math.floor(totalAttempts * 0.75); // приблизительно
        const accuracy = totalAttempts > 0 ? Math.round((correctAttempts / totalAttempts) * 100) : 0;
        document.getElementById('detailAccuracy').textContent = `${accuracy}%`;
        
        // Среднее время (имитация)
        const avgTime = solved > 0 ? Math.round((solved * 6) / solved) : 0;
        document.getElementById('detailAvgTime').textContent = `${avgTime} мин`;
        
        // Лучший XP
        document.getElementById('detailBestXP').textContent = Math.min(100, Math.floor(totalXP / Math.max(1, solved)));

        // Обновляем рейтинг
        updateRank();

        // Обновляем достижения
        updateAchievements(solved, totalXP);
    }

    // ----- РЕЙТИНГ -----
    function updateRank() {
        const username = getProfileData().username;
        const myXP = parseInt(localStorage.getItem('totalXP')) || 0;
        
        // Имитация рейтинга
        const baseUsers = [
            { name: 'StarHunter42', xp: 3250 },
            { name: 'NebulaPilot', xp: 2890 },
            { name: 'CosmicWizard', xp: 2710 },
            { name: 'OrionExplorer', xp: 2430 },
            { name: 'VoidRunner', xp: 2180 },
            { name: 'GalaxyTrekker', xp: 1940 },
            { name: 'AstroNaut_99', xp: 1710 },
            { name: 'NovaCore', xp: 1580 },
            { name: 'PulsarWave', xp: 1420 },
            { name: 'ZenithCoder', xp: 1280 },
        ];
        
        // Добавляем текущего пользователя
        const existing = baseUsers.find(u => u.name === username);
        if (!existing) {
            baseUsers.push({ name: username, xp: myXP });
        } else {
            existing.xp = myXP;
        }
        
        const sorted = [...baseUsers].sort((a, b) => b.xp - a.xp);
        const rank = sorted.findIndex(u => u.name === username) + 1;
        
        document.getElementById('statRank').textContent = `#${rank || '—'}`;
    }

    // ----- ДОСТИЖЕНИЯ -----
    function updateAchievements(solved, totalXP) {
        const achievements = [
            { id: 'first_level', icon: '🌟', name: 'Первый шаг', desc: 'Пройдите первый уровень', check: () => solved >= 1 },
            { id: 'level_5', icon: '🚀', name: 'Исследователь', desc: 'Пройдите 5 уровней', check: () => solved >= 5 },
            { id: 'level_10', icon: '🌌', name: 'Мастер космоса', desc: 'Пройдите 10 уровней', check: () => solved >= 10 },
            { id: 'all_levels', icon: '🏆', name: 'Хранитель Кода', desc: 'Пройдите все 12 уровней', check: () => solved >= 12 },
            { id: 'xp_500', icon: '⭐', name: 'Начинающий', desc: 'Заработайте 500 XP', check: () => totalXP >= 500 },
            { id: 'xp_1000', icon: '🌟', name: 'Опытный', desc: 'Заработайте 1000 XP', check: () => totalXP >= 1000 },
            { id: 'xp_2000', icon: '💫', name: 'Эксперт', desc: 'Заработайте 2000 XP', check: () => totalXP >= 2000 },
            { id: 'xp_3000', icon: '👑', name: 'Легенда', desc: 'Заработайте 3000 XP', check: () => totalXP >= 3000 },
            { id: 'perfect_level', icon: '🎯', name: 'Идеальный ответ', desc: 'Пройдите уровень с 100 XP', check: () => totalXP >= 100 && solved >= 1 },
            { id: 'speed_demon', icon: '⚡', name: 'Скорость света', desc: 'Пройдите уровень за 5 минут', check: () => solved >= 1 },
        ];

        const container = document.getElementById('achievementsContainer');
        let html = '';
        
        achievements.forEach(ach => {
            const unlocked = ach.check();
            html += `
                <div class="achievement-item ${unlocked ? 'unlocked' : 'locked'}">
                    <span class="achievement-icon">${ach.icon}</span>
                    <div class="achievement-name">${ach.name}</div>
                    <div class="achievement-desc">${ach.desc}</div>
                    ${unlocked ? '<div style="color: #00ff9d; font-size: 12px; margin-top: 6px;">✅ Разблокировано</div>' : '<div style="color: #666; font-size: 12px; margin-top: 6px;">🔒 Заблокировано</div>'}
                </div>
            `;
        });
        
        container.innerHTML = html;
    }

    // ----- ВКЛАДКИ -----
    function setupTabs() {
        const tabs = document.querySelectorAll('.tab-btn');
        const panels = {
            stats: document.getElementById('tabStats'),
            achievements: document.getElementById('tabAchievements'),
            settings: document.getElementById('tabSettings')
        };
        
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                // Убираем активный класс у всех кнопок
                tabs.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                
                // Показываем соответствующую панель
                const tabId = this.dataset.tab;
                Object.keys(panels).forEach(key => {
                    panels[key].classList.remove('active');
                });
                if (panels[tabId]) {
                    panels[tabId].classList.add('active');
                }
            });
        });
    }

    // ----- НАСТРОЙКИ -----
    function setupSettings() {
        const profile = getProfileData();
        
        // Изменение имени
        document.getElementById('saveUsernameBtn').addEventListener('click', function() {
            const input = document.getElementById('newUsername');
            const newName = input.value.trim();
            
            if (!newName) {
                alert('Введите имя пользователя!');
                return;
            }
            
            if (!/^[a-zA-Z0-9_-]{3,20}$/.test(newName)) {
                alert('Имя должно содержать 3-20 символов: буквы, цифры, _ и -');
                return;
            }
            
            profile.username = newName;
            saveProfileData(profile);
            input.value = '';
            updateProfile();
            alert('Имя успешно обновлено!');
        });

        // Выбор аватара
        document.querySelectorAll('.avatar-option').forEach(btn => {
            btn.addEventListener('click', function() {
                const emoji = this.dataset.emoji;
                profile.avatar = emoji;
                saveProfileData(profile);
                
                // Обновляем активный класс
                document.querySelectorAll('.avatar-option').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                updateProfile();
            });
        });

        // Сброс прогресса
        document.getElementById('resetAllBtn').addEventListener('click', function() {
            if (confirm('Вы уверены, что хотите сбросить весь прогресс? Это действие нельзя отменить!')) {
                if (confirm('ВНИМАНИЕ! Все данные будут удалены навсегда. Продолжить?')) {
                    localStorage.removeItem('totalXP');
                    localStorage.removeItem('currentLevel');
                    localStorage.removeItem('completedLevels');
                    localStorage.removeItem('profileData');
                    
                    // Обновляем страницу
                    location.reload();
                }
            }
        });
    }

    // ----- ПЕРЕХОД НА СТРАНИЦУ ПРОФИЛЯ -----
    function setupProfileNav() {
        const profileNav = document.getElementById('profileNav');
        if (profileNav) {
            profileNav.style.cursor = 'pointer';
            profileNav.addEventListener('click', function() {
                // Если мы уже на странице профиля, ничего не делаем
                if (window.location.pathname.includes('profile.html')) return;
                window.location.href = 'profile.html';
            });
        }
    }

    // ----- ЗАГРУЗКА АВАТАРА ПРИ ЗАГРУЗКЕ -----
    function loadAvatarOption() {
        const profile = getProfileData();
        const currentAvatar = profile.avatar || '🚀';
        document.querySelectorAll('.avatar-option').forEach(btn => {
            if (btn.dataset.emoji === currentAvatar) {
                btn.classList.add('active');
            }
        });
    }

    // ----- ИНИЦИАЛИЗАЦИЯ -----
    document.addEventListener('DOMContentLoaded', function() {
        // Проверяем, что мы на странице профиля
        if (!document.getElementById('profileNav')) return;
        
        setupProfileNav();
        updateProfile();
        setupTabs();
        setupSettings();
        loadAvatarOption();
        
        // Обновляем профиль при фокусе на вкладке
        window.addEventListener('focus', updateProfile);
    });

})();