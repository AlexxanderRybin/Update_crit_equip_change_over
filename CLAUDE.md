# CLAUDE.md

Этот файл содержит руководство для Claude Code (claude.ai/code) при работе с кодом в данном репозитории.

## Обзор проекта

Это Python ETL-скрипт, который синхронизирует данные о графике переключений критического оборудования из Excel в базу данных PostgreSQL (ODS). Скрипт читает графики переключений оборудования из Excel-файла на SharePoint и загружает их в таблицу PostgreSQL для инструментов визуализации, таких как Spotfire.

## Архитектура

**Архитектура одного скрипта**: Все приложение содержится в файле `Update_crit_equip_change_over.py` с двумя основными функциями:

1. `update_data()` - Читает листы Excel и загружает в таблицы PostgreSQL используя pandas и SQLAlchemy
2. `grant_sel_permissions()` - Предоставляет права SELECT сервисному пользователю Spotfire (TDM_user)

**Поток данных**:
- Источник: Excel-файл на SharePoint (`Major Equipment changeover.xlsx`)
- Назначение: База данных PostgreSQL (`yuzdc1-n-v70419.sakhalin2.ru:5432/ODS`)
- Схема: `opf_w_db`
- Таблица: `critical_equipment_changeover`

**Конфигурация структуры базы данных**: Словарь `db_struct` определяет маппинг между листами Excel и таблицами базы данных, включая типы колонок. Каждая запись связывает:
- Имя листа Excel → имя таблицы
- Имена колонок → типы SQLAlchemy

## Настройка окружения

```bash
# Создать и активировать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

## Запуск скрипта

```bash
# Сначала активируйте виртуальное окружение
source venv/bin/activate

# Запустите ETL-процесс
python Update_crit_equip_change_over.py
```

Скрипт выполнит:
1. Чтение листа "Visualization" из Excel-файла
2. Замену таблицы `critical_equipment_changeover` в PostgreSQL
3. Предоставление прав SELECT пользователю TDM_user

## Основные зависимости

- **psycopg/psycopg2**: Адаптер PostgreSQL (определяется автоматически)
- **SQLAlchemy**: ORM базы данных и управление подключениями
- **pandas**: Чтение Excel и операции с DataFrame
- **openpyxl**: Поддержка формата файлов Excel

## Учетные данные базы данных

Параметры подключения к базе данных жестко закодированы в скрипте:
- Хост: `yuzdc1-n-v70419.sakhalin2.ru:5432`
- База данных: `ODS`
- Пользователь: `OPF_user`
- Схема: `opf_w_db`
- Пользователь для прав: `TDM_user`

## Расположение Excel-файла

Исходный Excel-файл находится на корпоративном SharePoint:
```
//sakhalin2.ru/SE/OPF/Dept_02/OPF Operations/AU-OP-2 Maintenance - Integrated Planning/Planning Dept Projects/Проект#4 - График переключений критических агрегатов vs ТОиР/Major Equipment changeover.xlsx
```

Для доступа к этому пути требуется сетевое подключение к корпоративной сети Sakhalin2.

## Изменение структуры таблиц

Для добавления или изменения таблиц:

1. Обновите словарь `db_struct` с новыми маппингами лист-таблица
2. Укажите имена колонок и типы SQLAlchemy в `columns_types`
3. Добавьте опциональный словарь `converters` для пользовательской обработки типов данных

Пример:
```python
db_struct = {
    "ИмяЛиста": {
        "name": "имя_таблицы",
        "columns_types": {
            "КолонкаА": types.Text,
            "КолонкаБ": types.Integer,
        },
        "converters": {"КолонкаВ": функция_конвертера}  # Опционально
    }
}
```
