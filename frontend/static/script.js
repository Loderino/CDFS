document.addEventListener('DOMContentLoaded', function() {
    // Элементы UI
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsSlider = document.getElementById('results-count');
    const resultsValue = document.getElementById('results-value');
    const resultsContainer = document.getElementById('results-container');
    const noResults = document.getElementById('no-results');
    const saveChangesBar = document.getElementById('save-changes-bar');
    const saveChangesButton = document.getElementById('save-changes-button');

    // Состояние приложения
    let searchResults = [];
    let changedTags = new Set(); // Хранит индексы результатов с измененными тегами

    // Обновление отображаемого значения слайдера
    resultsSlider.addEventListener('input', function() {
        resultsValue.textContent = this.value;
    });

    // Обработка поискового запроса
    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    // Сохранение изменений в тегах
    saveChangesButton.addEventListener('click', saveTagChanges);

    // Функция выполнения поиска
    function performSearch() {
        const query = searchInput.value.trim();
        const maxResults = parseInt(resultsSlider.value);

        if (!query) {
            alert('Пожалуйста, введите поисковый запрос');
            return;
        }

        // Показываем индикатор загрузки
        resultsContainer.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i><p>Выполняется поиск...</p></div>';

        // Имитация API-запроса (замените на реальный API-вызов)
        fetchSearchResults(query, maxResults)
            .then(data => {
                searchResults = data;
                displayResults(data);

                // Сбрасываем измененные теги
                changedTags.clear();
                saveChangesBar.classList.replace('visible', 'hidden');
            })
            .catch(error => {
                resultsContainer.innerHTML = `
                    <div class="error">
                        <i class="fas fa-exclamation-triangle"></i>
                        <p>Произошла ошибка при выполнении поиска: ${error.message}</p>
                    </div>
                `;
            });
    }

    // Функция для отображения результатов
    function displayResults(results) {
        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-search"></i>
                    <p>По вашему запросу ничего не найдено</p>
                </div>
            `;
            return;
        }

        resultsContainer.innerHTML = '';

        results.forEach((result, index) => {
            const resultElement = document.createElement('div');
            resultElement.className = 'result-item';
            resultElement.dataset.index = index;

            // Создаем HTML для изображения, если оно есть
            const imageHTML = result.image_url ? `
                <div class="result-image">
                    <img src="${result.image_url}" alt="Предпросмотр ${result.path}" />
                </div>
            ` : '';

            resultElement.innerHTML = `
                <div class="result-content">
                    <div class="result-path">${result.path}</div>
                    <div class="result-score">Расстояние: ${result.score}</div>
                    ${imageHTML}
                    <div class="tags-section">
                        <label>Теги:</label>
                        <div class="tags-container" data-index="${index}">
                            ${renderTags(result.tags, index)}
                            <button class="add-tag" data-index="${index}">
                                <i class="fas fa-plus"></i> Добавить тег
                            </button>
                        </div>
                    </div>
                </div>
            `;

            resultsContainer.appendChild(resultElement);
        });

        // Добавляем обработчики событий для тегов
        setupTagEventListeners();
    }

    // Функция для рендеринга тегов
    function renderTags(tags, resultIndex) {
        if (!tags || tags.length === 0) return '';

        return tags.map((tag, tagIndex) => `
            <div class="tag" data-result-index="${resultIndex}" data-tag-index="${tagIndex}">
                <span class="tag-text">${tag}</span>
                                <button class="remove-tag" title="Удалить тег">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');
    }

    // Настройка обработчиков событий для тегов
    function setupTagEventListeners() {
        // Обработчик для кнопки "Добавить тег"
        document.querySelectorAll('.add-tag').forEach(button => {
            button.addEventListener('click', function() {
                const resultIndex = parseInt(this.dataset.index);
                addNewTag(resultIndex, this.parentElement);
            });
        });

        // Обработчик для удаления тега
        document.querySelectorAll('.remove-tag').forEach(button => {
            button.addEventListener('click', function() {
                const tagElement = this.parentElement;
                const resultIndex = parseInt(tagElement.dataset.resultIndex);
                const tagIndex = parseInt(tagElement.dataset.tagIndex);

                // Удаляем тег из данных и из DOM
                searchResults[resultIndex].tags.splice(tagIndex, 1);
                tagElement.remove();

                // Обновляем индексы оставшихся тегов
                updateTagIndices(resultIndex);

                // Отмечаем, что теги были изменены
                changedTags.add(resultIndex);
                showSaveChangesBar();
            });
        });

        // Обработчик для редактирования тега
        document.querySelectorAll('.tag-text').forEach(tagText => {
            tagText.addEventListener('dblclick', function() {
                const tagElement = this.parentElement;
                const resultIndex = parseInt(tagElement.dataset.resultIndex);
                const tagIndex = parseInt(tagElement.dataset.tagIndex);

                // Создаем поле ввода для редактирования
                const currentText = this.textContent;
                tagElement.classList.add('editing');

                this.innerHTML = `<input type="text" class="tag-input" value="${currentText}">`;
                const input = tagElement.querySelector('.tag-input');

                input.focus();
                input.setSelectionRange(0, input.value.length);

                // Обработка завершения редактирования
                function finishEditing() {
                    const newValue = input.value.trim();

                    if (newValue && newValue !== currentText) {
                        searchResults[resultIndex].tags[tagIndex] = newValue;
                        changedTags.add(resultIndex);
                        showSaveChangesBar();
                    }

                    tagElement.classList.remove('editing');
                    tagText.textContent = newValue || currentText;
                }

                input.addEventListener('blur', finishEditing);
                input.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        finishEditing();
                    }
                });
            });
        });
    }

    // Функция для добавления нового тега
    function addNewTag(resultIndex, tagsContainer) {
        // Создаем новый элемент тега
        const newTagElement = document.createElement('div');
        const tagIndex = searchResults[resultIndex].tags ? searchResults[resultIndex].tags.length : 0;

        newTagElement.className = 'tag editing';
        newTagElement.dataset.resultIndex = resultIndex;
        newTagElement.dataset.tagIndex = tagIndex;

        newTagElement.innerHTML = `
            <input type="text" class="tag-input" placeholder="Новый тег">
            <button class="remove-tag" title="Удалить тег">
                <i class="fas fa-times"></i>
            </button>
        `;

        // Вставляем новый тег перед кнопкой "Добавить тег"
        tagsContainer.insertBefore(newTagElement, tagsContainer.querySelector('.add-tag'));

        // Инициализируем массив тегов, если он не существует
        if (!searchResults[resultIndex].tags) {
            searchResults[resultIndex].tags = [];
        }

        // Фокусируемся на поле ввода
        const input = newTagElement.querySelector('.tag-input');
        input.focus();

        // Обработка завершения редактирования
        function finishEditing() {
            const newValue = input.value.trim();

            if (newValue) {
                // Добавляем новый тег в данные
                searchResults[resultIndex].tags.push(newValue);

                // Заменяем поле ввода на текст
                newTagElement.innerHTML = `
                    <span class="tag-text">${newValue}</span>
                    <button class="remove-tag" title="Удалить тег">
                        <i class="fas fa-times"></i>
                    </button>
                `;

                // Добавляем обработчики событий
                newTagElement.querySelector('.tag-text').addEventListener('dblclick', function() {
                    const tagElement = this.parentElement;
                    const resultIndex = parseInt(tagElement.dataset.resultIndex);
                    const tagIndex = parseInt(tagElement.dataset.tagIndex);

                    // Создаем поле ввода для редактирования
                    const currentText = this.textContent;
                    tagElement.classList.add('editing');

                    this.innerHTML = `<input type="text" class="tag-input" value="${currentText}">`;
                    const input = tagElement.querySelector('.tag-input');

                    input.focus();
                    input.setSelectionRange(0, input.value.length);

                    // Обработка завершения редактирования
                    function finishEditing() {
                        const newValue = input.value.trim();

                        if (newValue && newValue !== currentText) {
                            searchResults[resultIndex].tags[tagIndex] = newValue;
                            changedTags.add(resultIndex);
                            showSaveChangesBar();
                        }

                        tagElement.classList.remove('editing');
                        tagText.textContent = newValue || currentText;
                    }

                    input.addEventListener('blur', finishEditing);
                    input.addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') {
                            finishEditing();
                        }
                    });
                });

                newTagElement.querySelector('.remove-tag').addEventListener('click', function() {
                    const tagElement = this.parentElement;
                    const resultIndex = parseInt(tagElement.dataset.resultIndex);
                    const tagIndex = parseInt(tagElement.dataset.tagIndex);

                    // Удаляем тег из данных и из DOM
                    searchResults[resultIndex].tags.splice(tagIndex, 1);
                    tagElement.remove();

                    // Обновляем индексы оставшихся тегов
                    updateTagIndices(resultIndex);

                    // Отмечаем, что теги были изменены
                    changedTags.add(resultIndex);
                    showSaveChangesBar();
                });

                newTagElement.classList.remove('editing');

                // Отмечаем, что теги были изменены
                changedTags.add(resultIndex);
                showSaveChangesBar();
            } else {
                // Если поле пустое, удаляем элемент
                newTagElement.remove();
            }
        }

        input.addEventListener('blur', finishEditing);
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                finishEditing();
            }
        });

        // Обработчик для кнопки удаления
        newTagElement.querySelector('.remove-tag').addEventListener('click', function() {
            newTagElement.remove();
        });
    }

    // Обновление индексов тегов после удаления
    function updateTagIndices(resultIndex) {
        const tagElements = document.querySelectorAll(`.tag[data-result-index="${resultIndex}"]`);
        tagElements.forEach((element, index) => {
            element.dataset.tagIndex = index;
        });
    }

    // Показать панель сохранения изменений
    function showSaveChangesBar() {
        if (changedTags.size > 0) {
            saveChangesBar.classList.replace('hidden', 'visible');
        }
    }

    // Сохранение изменений в тегах
    function saveTagChanges() {
        // Собираем данные для отправки на сервер
        const updatedTags = Array.from(changedTags).map(index => {
            return {
                path: searchResults[index].path,
                tags: searchResults[index].tags
            };
        });

        // Имитация отправки данных на сервер (замените на реальный API-вызов)
        updateTagsOnServer(updatedTags)
            .then(() => {
                // Сбрасываем состояние
                changedTags.clear();
                saveChangesBar.classList.replace('visible', 'hidden');

                // Показываем уведомление об успешном сохранении
                showNotification('Теги успешно сохранены', 'success');
            })
            .catch(error => {
                showNotification(`Ошибка при сохранении тегов: ${error.message}`, 'error');
            });
    }

    // Функция для отображения уведомлений
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
        `;

        document.body.appendChild(notification);

        // Анимация появления
        setTimeout(() => {
            notification.classList.add('visible');
        }, 10);

        // Автоматическое скрытие через 3 секунды
        setTimeout(() => {
            notification.classList.remove('visible');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    // Имитация API-запросов (замените на реальные API-вызовы)

    // Функция для получения результатов поиска
    function fetchSearchResults(query, maxResults) {
        return fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                max_results: maxResults
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Ошибка при выполнении запроса:', error);
            throw error;
        });
    }


    // Функция для обновления тегов на сервере
    function updateTagsOnServer(updatedTags) {
        return fetch('/api/update_tags', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedTags)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.error || `HTTP ошибка: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                return data;
            } else {
                throw new Error(data.error || 'Неизвестная ошибка при обновлении тегов');
            }
        })
        .catch(error => {
            console.error('Ошибка при обновлении тегов:', error);
            throw error;
        });
    }


    // Добавляем стили для уведомлений
    const notificationStyles = document.createElement('style');
    notificationStyles.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: var(--border-radius);
            background-color: white;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            transform: translateX(120%);
            transition: transform 0.3s ease;
            max-width: 350px;
        }

        .notification.visible {
            transform: translateX(0);
        }

        .notification-content {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .notification i {
            font-size: 1.2rem;
        }

        .notification.success {
            border-left: 4px solid var(--success-color);
        }

        .notification.success i {
            color: var(--success-color);
        }

        .notification.error {
            border-left: 4px solid var(--accent-color);
        }

        .notification.error i {
            color: var(--accent-color);
        }

        .loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 4rem 2rem;
            color: var(--dark-gray);
            text-align: center;
        }

        .loading i {
            font-size: 2rem;
            margin-bottom: 1rem;
        }

        .error {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 4rem 2rem;
            color: var(--accent-color);
            text-align: center;
        }

        .error i {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
    `;

    document.head.appendChild(notificationStyles);
});
