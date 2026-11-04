# LLM Bench 2026-11

**AI model benchmarks, November 2026** — a static page comparing Claude Opus 5.5, GPT-6 Astra, GPT-6.1 Sol, Gemini 4 Argon, Grok 4.7, Kimi K3.1 Pro, GLM-5.3 and more: the Artificial Analysis index, cost per task, speed, coding and reasoning benchmarks, and a check of which model names actually exist.

**Бенчмарки ИИ-моделей, ноябрь 2026** — статическая страница со сравнением Claude Opus 5.5, GPT-6 Astra, GPT-6.1 Sol, Gemini 4 Argon, Grok 4.7, Kimi K3.1 Pro, GLM-5.3 и других: индекс Artificial Analysis, цена задачи, скорость, кодинг и рассуждение, проверка существующих названий моделей.

| | |
|---|---|
| English | https://folzy.is-a.dev/llm-bench-2026-11/ |
| Русский | https://folzy.is-a.dev/llm-bench-2026-11/ru/ |

Data as of **November 4, 2026** · Данные на **4 ноября 2026**.

---

## English

### What is in the page

- Intelligence Index v5 (Artificial Analysis), cost per index task, output speed, API prices, context windows.
- The top three (Opus 5.5, GPT-6 Astra, Gemini 4 Argon) plus Fable 5.1 across coding, reasoning, knowledge-work and long-context tests, with the source of every number.
- Fable 5.1 vs Opus 5.5, and vendor claims vs independent measurements on Terminal-Bench 4.0.
- A name check: which of the commonly cited model names exist (for example, there is no Gemini 3.8 Pro).
- Recommendations for typical developer work, an FAQ, caveats and a list of sources.

### About the data

The numbers come from vendor tables, independent leaderboards and news coverage, collected in an automated research pass over public sources. Most vendor figures use settings that suit the vendor, so the page marks the source of each value. Verify the numbers you rely on against the linked sources. Values that could not be found are shown as a dash.

### Repository layout

```
index.html          English page (generated)
ru/index.html       Russian page (generated)
sitemap.xml         sitemap with hreflang alternates (generated)
assets/style.css    styles, light and dark theme
assets/app.js       charts and tables (d3), reads the data embedded in each page
assets/d3.min.js    d3 v7 (ISC license, https://d3js.org)
tools/build.py      generator: all data and all texts live here
```

### Rebuilding the pages

The pages are generated. Edit the data or texts in `tools/build.py` and run it from the repository root:

```bash
python tools/build.py
```

Python 3.8+, standard library only. The script rewrites `index.html`, `ru/index.html` and `sitemap.xml`.

The tables, numbers and FAQ are written into the HTML itself, so the page is readable without JavaScript; `assets/app.js` only draws the charts and re-renders the tables.

---

## Русский

### Что на странице

- Индекс интеллекта v5 (Artificial Analysis), цена задачи индекса, скорость вывода, цены API, контекст.
- Тройка лидеров (Opus 5.5, GPT-6 Astra, Gemini 4 Argon) и Fable 5.1 по кодингу, рассуждению, knowledge work и длинному контексту; у каждой цифры указан источник.
- Fable 5.1 против Opus 5.5 и заявления вендоров против независимых замеров на Terminal-Bench 4.0.
- Проверка названий: какие из часто упоминаемых моделей существуют (например, Gemini 3.8 Pro не существует).
- Рекомендации для типичных задач разработчика, вопросы и ответы, оговорки и список источников.

### О данных

Цифры взяты из таблиц вендоров, независимых лидербордов и новостей и собраны автоматизированным исследованием открытых источников. Большинство цифр вендоров получено на удобных им настройках, поэтому у каждого значения на странице указан источник. Ключевые числа стоит сверить по ссылкам. Значения, которые найти не удалось, показаны прочерком.

### Структура репозитория

```
index.html          английская страница (генерируется)
ru/index.html       русская страница (генерируется)
sitemap.xml         карта сайта с hreflang (генерируется)
assets/style.css    стили, светлая и тёмная тема
assets/app.js       графики и таблицы (d3), читает данные, встроенные в страницу
assets/d3.min.js    d3 v7 (лицензия ISC, https://d3js.org)
tools/build.py      генератор: все данные и тексты лежат здесь
```

### Пересборка страниц

Страницы генерируются. Поправь данные или тексты в `tools/build.py` и запусти его из корня репозитория:

```bash
python tools/build.py
```

Нужен Python 3.8+, только стандартная библиотека. Скрипт перезапишет `index.html`, `ru/index.html` и `sitemap.xml`.

Таблицы, цифры и FAQ записаны прямо в HTML, поэтому страница читается и без JavaScript; `assets/app.js` только рисует графики и перерисовывает таблицы.
