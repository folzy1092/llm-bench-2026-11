# LLM Bench 2026-11

**AI model benchmarks, November 2026** — Claude Opus 5.5, GPT-6 Astra, GPT-6.1 Sol, Gemini 4 Argon, Grok 4.7, Kimi K3.1 Pro, GLM-5.3 and more: the Artificial Analysis index, price per task, speed, coding and reasoning benchmarks, and a check of which model names actually exist.

**Бенчмарки ИИ-моделей, ноябрь 2026** — сводка по Claude Opus 5.5, GPT-6 Astra, GPT-6.1 Sol, Gemini 4 Argon, Grok 4.7, Kimi K3.1 Pro, GLM-5.3 и другим: индекс Artificial Analysis, цена задачи, скорость, кодинг и рассуждение, проверка существующих названий моделей.

| | |
|---|---|
| 🇬🇧 English | https://folzy.is-a.dev/llm-bench-2026-11/ |
| 🇷🇺 Русский | https://folzy.is-a.dev/llm-bench-2026-11/ru/ |

Data as of **November 4, 2026** · Данные на **4 ноября 2026**.

---

## English

### What is in the page

- Intelligence Index v5 (Artificial Analysis), cost per index task, output speed, API prices, context windows.
- The top three (Opus 5.5, GPT-6 Astra, Gemini 4 Argon) plus Fable 5.1, across coding, reasoning, knowledge-work and long-context tests, with the source of every number.
- Fable 5.1 vs Opus 5.5, and vendor claims vs independent measurements on Terminal-Bench 4.0.
- A name check: which of the commonly cited model names exist (for example, there is no Gemini 3.8 Pro).
- Recommendations for typical developer work, an FAQ, caveats and a list of sources.

### Honest caveat

The numbers come from vendor tables, independent leaderboards and news coverage, collected in an automated research pass. Most vendor figures use settings that suit the vendor. Verify the numbers you rely on against the linked sources. Some values could not be found and are shown as a dash.

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

### Publish on GitHub Pages

1. Put the files in the repository root (keep the folder structure).
2. Repository **Settings → Pages → Build and deployment → Deploy from a branch**, branch `main`, folder `/ (root)`.
3. After a minute the site is live at `https://folzy.is-a.dev/llm-bench-2026-11/`.

If you rename the repository, change `BASE` and `GITHUB` at the top of `tools/build.py` and rebuild.

### Update the data

Edit the data and texts in `tools/build.py`, then run from the repository root:

```bash
python tools/build.py
```

Python 3.8+, standard library only. The script rewrites `index.html`, `ru/index.html` and `sitemap.xml`. Commit and push the result.

### Search engines (SEO)

The pages are plain static HTML: tables, numbers and the FAQ are in the markup, so crawlers read them without running JavaScript. Each page has a title, description, canonical link, `hreflang` for en/ru/x-default, Open Graph and Twitter tags, and JSON-LD (`Article`, `FAQPage`).

To get indexed faster:

1. **Google:** add the site in [Search Console](https://search.google.com/search-console) as a *URL prefix* property (`https://folzy.is-a.dev/llm-bench-2026-11/`), then submit `sitemap.xml` and request indexing of both pages.
2. **Bing and DuckDuckGo** (DuckDuckGo uses Bing's index): add the site in [Bing Webmaster Tools](https://www.bing.com/webmasters) and submit the sitemap.
3. If a service asks for a verification meta tag, paste the code into `VERIFY` in `tools/build.py` and rebuild.

Indexing takes days to weeks, and ranking is not guaranteed. `robots.txt` is not included on purpose: crawlers only read it from the domain root, and a project site lives under a subpath.

### Licenses

d3 is distributed under the ISC license (see the banner in `assets/d3.min.js`). The repository has no license file yet; add one if you want others to reuse the code or data.

---

## Русский

### Что на странице

- Индекс интеллекта v5 (Artificial Analysis), цена задачи индекса, скорость вывода, цены API, контекст.
- Тройка лидеров (Opus 5.5, GPT-6 Astra, Gemini 4 Argon) и Fable 5.1 по кодингу, рассуждению, knowledge work и длинному контексту, у каждой цифры указан источник.
- Fable 5.1 против Opus 5.5 и заявления вендоров против независимых замеров на Terminal-Bench 4.0.
- Проверка названий: какие из часто упоминаемых моделей существуют (например, Gemini 3.8 Pro не существует).
- Рекомендации для типичных задач разработчика, вопросы и ответы, оговорки и список источников.

### Честная оговорка

Цифры взяты из таблиц вендоров, независимых лидербордов и новостей и собраны автоматизированным исследованием. Большинство цифр вендоров получено на удобных им настройках. Ключевые числа стоит сверить по ссылкам. Часть значений найти не удалось, они показаны прочерком.

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

### Публикация на GitHub Pages

1. Положи файлы в корень репозитория, сохранив структуру папок.
2. **Settings → Pages → Build and deployment → Deploy from a branch**, ветка `main`, папка `/ (root)`.
3. Через минуту сайт откроется по адресу `https://folzy.is-a.dev/llm-bench-2026-11/`.

Если переименуешь репозиторий, поменяй `BASE` и `GITHUB` в начале `tools/build.py` и пересобери.

### Обновление данных

Поправь данные и тексты в `tools/build.py` и запусти из корня репозитория:

```bash
python tools/build.py
```

Нужен Python 3.8+, только стандартная библиотека. Скрипт перезапишет `index.html`, `ru/index.html` и `sitemap.xml`. Закоммить и запушь результат.

### Поисковики (SEO)

Страницы — обычный статический HTML: таблицы, цифры и FAQ лежат прямо в разметке, поэтому поисковики читают их без JavaScript. У каждой страницы есть title, description, canonical, `hreflang` для en/ru/x-default, теги Open Graph и Twitter, JSON-LD (`Article`, `FAQPage`).

Чтобы проиндексировали быстрее:

1. **Google:** добавь сайт в [Search Console](https://search.google.com/search-console) как ресурс с префиксом URL (`https://folzy.is-a.dev/llm-bench-2026-11/`), отправь `sitemap.xml` и запроси индексацию обеих страниц.
2. **Bing и DuckDuckGo** (DuckDuckGo использует индекс Bing): добавь сайт в [Bing Webmaster Tools](https://www.bing.com/webmasters) и отправь sitemap.
3. Если сервис просит мета-тег подтверждения, вставь код в `VERIFY` в `tools/build.py` и пересобери.

Индексация занимает от нескольких дней до недель, место в выдаче не гарантировано. `robots.txt` не добавлен намеренно: поисковики читают его только в корне домена, а проектный сайт живёт в подпапке.

### Лицензии

d3 распространяется по лицензии ISC (см. шапку `assets/d3.min.js`). Файла лицензии для самого репозитория пока нет; добавь его, если хочешь, чтобы код и данные можно было переиспользовать.
