#!/usr/bin/env python3
"""Generates the static pages of this site. Standard library only.

    python tools/build.py

Writes:  index.html (English), ru/index.html (Russian), sitemap.xml
All numbers and texts live in this file (DATA section). Edit them, run the script, commit the result.
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://folzy.is-a.dev/llm-bench-2026-11/'
GITHUB = 'https://github.com/folzy1092/llm-bench-2026-11'
DATE = '2026-11-04'
SITE = 'LLM Bench 2026-11'
AUTHOR = {'name': 'Folzy', 'url': 'https://github.com/folzy1092'}
# Paste the verification codes from Google Search Console / Bing Webmaster Tools here, then re-run the script.
VERIFY = {'google-site-verification': '', 'msvalidate.01': ''}

E = lambda s: html.escape(str(s), quote=True)
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def date_s(lang, d):
    if d is None:
        return None
    y, m, dd = d
    return f'{dd:02d}.{m:02d}.{y}' if lang == 'ru' else f'{MONTHS[m - 1]} {dd}, {y}'


# ============================== DATA ==============================
# id, model, vendor, release, price_in, price_out, context_k, aa_index, task_cost, speed_lo, speed_hi, restricted, note_ru, note_en
MODELS = [
    ('opus', 'Claude Opus 5.5', 'Anthropic', (2026, 9, 22), 4, 20, 1000, 58, 10.04, 94, 96, False,
     'Цена задачи и скорость — при max-усилии', 'Task cost and speed measured at max effort'),
    ('astra', 'GPT-6 Astra', 'OpenAI', (2026, 9, 3), 10, 50, 1050, 57, 6.24, 67, 71, False,
     'Самая сильная модель OpenAI', "OpenAI's strongest model"),
    ('sol', 'GPT-6.1 Sol', 'OpenAI', (2026, 9, 29), 2, 10, 1050, 55, 1.27, 51, 74, False,
     'Лучшее соотношение цена/качество', 'Best price-to-quality ratio'),
    ('argon', 'Gemini 4 Argon', 'Google', (2026, 10, 13), 2, 10, 1000, 50, None, 56, 84, False,
     'Промо-цена только до 30.11, дальше 4/20', 'Promo price only until Nov 30, then $4/$20'),
    ('fable', 'Claude Fable 5.1', 'Anthropic', None, 10, 50, 1000, 49, 13.04, 66, 70, False,
     'Самая дорогая задача в индексе AA', 'Most expensive task in the AA index'),
    ('kimi', 'Kimi K3.1 Pro', 'Moonshot', (2026, 10, 23), 2, 10, 1000, 46, 1.98, 31.6, 31.6, False,
     'Есть быстрый вариант Highspeed', 'A faster Highspeed variant exists'),
    ('grok', 'Grok 4.7', 'xAI', (2026, 9, 21), 2, 6, 500, None, 3.74, 71, 80, False,
     'Индекс v5 пока не опубликован; тратит много токенов', 'No v5 index score yet; burns a lot of tokens'),
    ('glm', 'GLM-5.3', 'Z.ai', (2026, 8, 14), 1.4, 4.4, 1000, 32, None, 86, 90, False,
     'Почти все цифры вендорские', 'Almost all figures come from the vendor'),
    ('carbon', 'Gemini 4 Carbon', 'Google', (2026, 10, 28), None, None, None, 59, None, None, None, True,
     'Закрытый доступ (Fairwind Program), даты публичного релиза нет',
     'Restricted access (Fairwind Program), no public release date'),
]

# id, group, unit, opus, fable, astra, argon, (benchmark ru, en), (source ru, en), (note ru, en)
BENCH = [
    ('tb4v', 'code', '%', 66.4, 55.8, 57.9, 57.4, ('Terminal-Bench 4.0 (заявления вендоров)', 'Terminal-Bench 4.0 (vendor claims)'), ('Вендоры', 'Vendors'), ('', '')),
    ('tb4aa', 'code', '%', 60, 55, 59.5, 57, ('Terminal-Bench 4.0 (независимо)', 'Terminal-Bench 4.0 (independent)'), ('AA', 'AA'),
     ('У Opus ≈60, у Astra 59–60 (показана середина)', 'Opus ≈60, Astra 59–60 (midpoint shown)')),
    ('fc11', 'code', '%', 54.4, 50.3, 53.3, None, ('FrontierCode v1.1', 'FrontierCode v1.1'), ('Anthropic', 'Anthropic'), ('', '')),
    ('fc2', 'code', '%', 46, None, 42, None, ('FrontierCode 2.0 (приватный)', 'FrontierCode 2.0 (private)'), ('AA', 'AA'), ('', '')),
    ('cursor', 'code', '%', 57.8, 51.8, None, None, ('CursorBench 4.0', 'CursorBench 4.0'), ('Anthropic', 'Anthropic'), ('', '')),
    ('deepswe', 'code', '%', 74.2, 67.4, 74.1, 77.9, ('DeepSWE v1.1', 'DeepSWE v1.1'), ('Google', 'Google'), ('', '')),
    ('fswe2', 'code', '%', 62.3, 56.3, 65.5, 55.0, ('FrontierSWE v2', 'FrontierSWE v2'), ('Google', 'Google'), ('', '')),
    ('vibe', 'code', '%', 90.3, 90.3, 89.6, 91.9, ('Vibe Code Bench', 'Vibe Code Bench'), ('Google', 'Google'), ('', '')),
    ('arena', 'code', 'Elo', 1810, None, 1773, None, ('Arena WebDev (Elo)', 'Arena WebDev (Elo)'), ('LMArena', 'LMArena'),
     ('У Fable — 6-е место, точного Elo нет', 'Fable ranks 6th, exact Elo unavailable')),
    ('gdpval', 'work', 'Elo', 1846, 1735, 1542, None, ('GDPval-AA v2.1 (Elo)', 'GDPval-AA v2.1 (Elo)'), ('Anthropic', 'Anthropic'), ('', '')),
    ('auto', 'work', '%', 40.0, 31.4, 41.4, 51.3, ('AutomationBench', 'AutomationBench'), ('Anthropic / Google', 'Anthropic / Google'), ('', '')),
    ('vals', 'work', '%', 67.0, 65.8, 63.1, 68.9, ('Vals Index', 'Vals Index'), ('Google', 'Google'), ('', '')),
    ('hle', 'reason', '%', 67.7, 65.6, 57.2, None, ('HLE (с инструментами)', 'HLE (with tools)'), ('Anthropic', 'Anthropic'), ('', '')),
    ('hled', 'reason', '%', 68, 60, 64, None, ('HLE-Diamond', 'HLE-Diamond'), ('AA', 'AA'), ('', '')),
    ('critpt', 'reason', '%', 61, None, 72, None, ('CritPt v2 (физика)', 'CritPt v2 (physics)'), ('AA', 'AA'), ('', '')),
    ('tbsci', 'reason', '%', 59, None, 63, None, ('Terminal-Bench-Science', 'Terminal-Bench-Science'), ('AA', 'AA'), ('', '')),
    ('arc3', 'reason', '%', None, None, 62.7, 49.8, ('ARC-AGI-3 (Standard harness)', 'ARC-AGI-3 (Standard harness)'), ('ARC Prize', 'ARC Prize'),
     ('99.9% у OpenAI — на собственной обвязке, не на нейтральной', "OpenAI's 99.9% comes from its own harness, not the neutral one")),
    ('riemann', 'reason', '%', 69.6, 65.6, 72.0, 76.0, ('RiemannBench (математика)', 'RiemannBench (math)'), ('Google', 'Google'), ('', '')),
    ('fmath', 'reason', '%', None, None, 97.6, None, ('FrontierMath Tier 4', 'FrontierMath Tier 4'), ('OpenAI', 'OpenAI'),
     ('Только заявление вендора', 'Vendor claim only')),
    ('graph', 'context', '%', 66.8, 65.0, 71.8, 84.2, ('GraphWalks 256K–1M', 'GraphWalks 256K–1M'), ('Google', 'Google'), ('', '')),
    ('lvbench', 'context', '%', 83.7, 79.7, 87.5, 91.7, ('LVBench (длинное видео)', 'LVBench (long video)'), ('Google', 'Google'), ('', '')),
    ('chart', 'context', '%', 66.3, 46.2, 71.0, 71.6, ('Chartography (по данным Google)', 'Chartography (per Google)'), ('Google', 'Google'),
     ('В таблице Anthropic тот же тест даёт 89.0 и 88.4 — другая методика',
      "Anthropic's table gives 89.0 and 88.4 for the same test — different methodology")),
    ('osworld', 'context', '%', 81.8, 80.7, None, None, ('OSWorld 2.1 (partial)', 'OSWorld 2.1 (partial)'), ('Anthropic', 'Anthropic'), ('', '')),
]

FABLE_VS_OPUS = [  # id, benchmark, unit, opus, fable   (Anthropic table, Sep 22 2026)
    ('tb4', 'Terminal-Bench 4.0', '%', 66.4, 55.8),
    ('auto', 'AutomationBench', '%', 40.0, 31.4),
    ('gdpval', 'GDPval-AA (Elo)', 'Elo', 1846, 1735),
    ('cursor', 'CursorBench', '%', 57.8, 51.8),
    ('fc', 'FrontierCode', '%', 54.4, 50.3),
    ('hle', 'HLE', '%', 67.7, 65.6),
    ('tbsci', 'Terminal-Bench-Science', '%', 58.7, 52.6),
    ('osworld', 'OSWorld 2.1', '%', 81.8, 80.7),
    ('chart', 'Chartography', '%', 89.0, 88.4),
]

TB4_GAP = [  # id, model, vendor, vendor claim, independent (AA)
    ('opus', 'Opus 5.5', 'Anthropic', 66.4, 60),
    ('fable', 'Fable 5.1', 'Anthropic', 55.8, 55),
    ('astra', 'GPT-6 Astra', 'OpenAI', 57.9, 59.5),
    ('argon', 'Gemini 4 Argon', 'Google', 57.4, 57),
    ('grok', 'Grok 4.7', 'xAI', 37.6, 25.8),
    ('kimi', 'Kimi K3.1 Pro', 'Moonshot', 65.7, 67),
]

STATUS = {'ok': ('верно', 'correct'), 'bad': ('неверно', 'wrong'), 'clarify': ('уточнение', 'clarification'), 'found': ('найдено', 'found')}
NAMING = [  # id, status key, (asked ru, en), (actual ru, en), (detail ru, en)
    ('opus', 'ok', ('Claude Opus 5.5', 'Claude Opus 5.5'),
     ('Claude Opus 5.5 · релиз 22.09.2026', 'Claude Opus 5.5 · released Sep 22, 2026'),
     ('Текущий флагман линейки Opus', 'Current flagship of the Opus line')),
    ('sol', 'clarify', ('ChatGPT 6.1 Sol', 'ChatGPT 6.1 Sol'), ('GPT-6.1 Sol', 'GPT-6.1 Sol'),
     ('ChatGPT — это продукт, модель называется GPT. И это не сильнейшая у OpenAI: выше стоит GPT-6 Astra',
      'ChatGPT is the product; the model is called GPT. It is also not the strongest at OpenAI: GPT-6 Astra ranks above it')),
    ('astra', 'clarify', ('ChatGPT 6 Astra', 'ChatGPT 6 Astra'), ('GPT-6 Astra · запуск 03.09.2026', 'GPT-6 Astra · launched Sep 3, 2026'),
     ('Название верное с поправкой на GPT. Самая сильная модель OpenAI', "Right name once \"ChatGPT\" becomes \"GPT\". OpenAI's strongest model")),
    ('gemini38', 'bad', ('Gemini 3.8 Pro', 'Gemini 3.8 Pro'), ('Такой модели нет', 'No such model'),
     ('Есть Gemini 3.8 Flash и Gemini 3.1 Pro (preview). Флагман Google — Gemini 4 Argon',
      "There are Gemini 3.8 Flash and Gemini 3.1 Pro (preview). Google's flagship is Gemini 4 Argon")),
    ('argon', 'ok', ('Gemini 4 Argon', 'Gemini 4 Argon'), ('Gemini 4 Argon · GA с 13.10.2026', 'Gemini 4 Argon · GA since Oct 13, 2026'),
     ('Но сильнее него закрытый Gemini 4 Carbon, доступный только киберзащитникам',
      'But the closed Gemini 4 Carbon, available only to cyber defenders, is stronger')),
    ('glm', 'ok', ('GLM 5.3', 'GLM 5.3'), ('GLM-5.3 · анонс 14.08.2026', 'GLM-5.3 · announced Aug 14, 2026'),
     ('Последний флагман Z.ai. GLM-5.5 существует только в слухах', "Z.ai's latest flagship. GLM-5.5 exists only as a rumor")),
    ('grok', 'found', ('Последний Grok', 'Latest Grok'), ('Grok 4.7 · 21.09.2026', 'Grok 4.7 · Sep 21, 2026'),
     ('Grok 4.8 анонсирован Маском, но не выпущен. Grok 5 тоже', 'Grok 4.8 was announced by Musk but not released. Neither was Grok 5')),
    ('kimi', 'found', ('Последний Kimi', 'Latest Kimi'), ('Kimi K3.1 Pro · 23.10.2026', 'Kimi K3.1 Pro · Oct 23, 2026'),
     ('Веса обещаны к 4 ноября, лицензия на момент сбора данных не опубликована',
      'Weights were promised by Nov 4; the license was not published at the time of data collection')),
]

SOURCES = [
    ('https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v5', 'Artificial Analysis: Intelligence Index v5'),
    ('https://winbuzzer.com/2026/10/28/artificial-analysis-reweights-ai-rankings-toward-private-tests-xcxwbn/', 'WinBuzzer: AA reweights rankings toward private tests'),
    ('https://arcprize.org/results/openai-gpt-6-astra', 'ARC Prize: GPT-6 Astra results'),
    ('https://www.anthropic.com/claude-opus-5-5', 'Anthropic: Claude Opus 5.5'),
    ('https://openai.com/index/gpt-6-astra-next-generation-work/', 'OpenAI: GPT-6 Astra'),
    ('https://techcrunch.com/2026/09/29/openai-launches-gpt-6-1-sol-says-it-nearly-matches-gpt-6-astra-and-costs-less/', 'TechCrunch: GPT-6.1 Sol launch'),
    ('https://venturebeat.com/technology/google-unveils-gemini-4-carbon-retaking-the-worlds-no-1-spot-on-updated-harder-benchmarks-but-access-is-limited', 'VentureBeat: Gemini 4 Carbon'),
    ('https://venturebeat.com/technology/google-makes-gemini-4-argon-broadly-available-with-limited-time-low-api-pricing-of-2-10-per-1m-token', 'VentureBeat: Gemini 4 Argon pricing'),
    ('https://www.datacamp.com/blog/claude-fable-5-1', 'DataCamp: Claude Fable 5.1'),
    ('https://www.datacamp.com/blog/gemini-4-argon-vs-claude-opus-5-5', 'DataCamp: Gemini 4 Argon vs Claude Opus 5.5'),
    ('https://dev.to/akartit/gemini-4-argon-vs-opus-55-vs-gpt-6-astra-same-prompt-real-bills-1dd9', 'dev.to: Argon vs Opus 5.5 vs Astra, same prompt'),
    ('https://fjdesign.de/en/blog/opus-5-5-vs-gpt-astra-compared-which-ai-model-right-business', 'fjdesign: Opus 5.5 vs GPT Astra in client work'),
    ('https://af.net/realtime/moonshot-ai-details-2-8t-open-weight-model-kimi-k3-1-pro/', 'af.net: Kimi K3.1 Pro details'),
    ('https://github.com/EugeneDraitsev/telegram-bot-app/pull/87', 'GitHub: Opus 5.5 vs Astra in a Telegram bot app (PR #87)'),
]


def datasets(lang):
    i = 0 if lang == 'ru' else 1
    models = [dict(id=m[0], model=m[1], vendor=m[2], release=date_s(lang, m[3]), price_in=m[4], price_out=m[5], context_k=m[6],
                   aa_index=m[7], task_cost=m[8], speed_lo=m[9], speed_hi=m[10], restricted=m[11], note=m[12 + i]) for m in MODELS]
    bench = [dict(id=b[0], group=b[1], unit=b[2], opus=b[3], fable=b[4], astra=b[5], argon=b[6],
                  benchmark=b[7][i], source=b[8][i], note=b[9][i]) for b in BENCH]
    fvo = [dict(id=r[0], benchmark=r[1], unit=r[2], opus=r[3], fable=r[4]) for r in FABLE_VS_OPUS]
    tb4 = [dict(id=r[0], model=r[1], vendor=r[2], claimed=r[3], independent=r[4]) for r in TB4_GAP]
    naming = [dict(id=n[0], status_key=n[1], status=STATUS[n[1]][i], asked=n[2][i], actual=n[3][i], detail=n[4][i]) for n in NAMING]
    return dict(models=models, bench=bench, fable_vs_opus=fvo, tb4_gap=tb4, naming=naming)


# ============================== TEXT ==============================
L_JS = {
    'ru': dict(notLoaded='Не загрузилось', closedSuffix=' · закрыт', vendor='Вендор', indexAA='Индекс AA v5', taskCost='Цена задачи',
               speedTps='Скорость, т/с', leads='Лидирует в строках', of=' из ', gapPp='Разрыв, п.п.', claimed='Заявление вендора',
               aaMeasure='Замер AA', valueX='Цена задачи индекса, $ (логарифмическая шкала)', valueY='Индекс AA v5',
               better='← лучше: дешевле и сильнее'),
    'en': dict(notLoaded='Failed to load', closedSuffix=' · closed', vendor='Vendor', indexAA='AA Index v5', taskCost='Cost per task',
               speedTps='Speed, tok/s', leads='Leads in rows', of=' of ', gapPp='Gap, pp', claimed='Vendor claim',
               aaMeasure='AA measurement', valueX='Cost of an index task, $ (log scale)', valueY='AA Index v5',
               better='← better: cheaper and stronger'),
}

T = {
    'ru': dict(
        htmllang='ru', locale='ru_RU', other_locale='en_US', switch='English version', switch_lang='en',
        title='Бенчмарки ИИ-моделей, ноябрь 2026: Opus 5.5, GPT-6, Gemini 4, Grok, Kimi, GLM',
        desc='Сводка бенчмарков Claude Opus 5.5, GPT-6 Astra, GPT-6.1 Sol, Gemini 4 Argon, Grok 4.7, Kimi K3.1 Pro и GLM-5.3: индекс, цена, скорость, кодинг.',
        keywords='бенчмарки ИИ 2026, сравнение нейросетей, Claude Opus 5.5, GPT-6 Astra, GPT-6.1 Sol, Gemini 4 Argon, Gemini 4 Carbon, Grok 4.7, Kimi K3.1 Pro, GLM-5.3, Claude Fable 5.1, лучшая нейросеть для кодинга, Artificial Analysis Intelligence Index, Terminal-Bench, ARC-AGI-3, цены API LLM',
        eyebrow='Сводка бенчмарков · 4 ноября 2026', h1='Фронтир-модели ИИ: кто сейчас впереди',
        lede='Claude Opus 5.5 — лучшая из доступных моделей: {opus_idx} баллов в индексе Artificial Analysis v5. Claude Fable 5.1 уступает ему в {ahead} из {total} сравнимых тестов Anthropic.',
        chips=[('sec-index', 'Индекс, цена, скорость'), ('sec-trio', 'Тройка лидеров'), ('sec-fable', 'Fable против Opus'),
               ('sec-names', 'Проверка названий'), ('sec-pick', 'Что брать'), ('sec-faq', 'Вопросы и ответы')],
        tile1='Индекс AA v5, лидер среди доступных', tile1n='Claude Opus 5.5',
        tile2='Цена задачи индекса, GPT-6.1 Sol', tile2n='У Opus 5.5 — {opus_cost}',
        tile3='ARC-AGI-3, GPT-6 Astra', tile3n='Нейтральная обвязка ARC Prize',
        tile4='GraphWalks 256K–1M, Gemini 4 Argon', tile4n='Длинный контекст, данные Google',
        tile5='Opus 5.5 впереди Fable 5.1', tile5v='{ahead} из {total}', tile5n='Сравнимые тесты Anthropic',
        idx_h2='Индекс, цена и скорость',
        idx_sub='Независимый индекс Artificial Analysis v5 — главная опора этой сводки: большая часть его тестов закрытая, подогнать под них модель сложнее.',
        c_index='Индекс интеллекта AA v5', c_index_n='Чем выше, тем лучше. Для Grok 4.7 индекс v5 пока не опубликован.',
        c_value='Цена и качество', c_value_n='Стоимость задачи индекса против баллов. Сильнее и дешевле — левее и выше.',
        c_speed='Скорость вывода', c_speed_n='Токенов в секунду, диапазон замеров AA при максимальном усилии. Цифры ориентировочные.',
        c_models='Все модели', c_models_n='Цены за миллион токенов. Закрытая Gemini 4 Carbon в практике недоступна, поэтому сравнивать надо с Argon.',
        col_model='Модель', col_vendor='Вендор', col_release='Релиз', col_in='Вход, $', col_out='Выход, $', col_ctx='Контекст, тыс. токенов',
        col_idx='Индекс AA v5', col_cost='Задача, $', col_speed='Скорость, т/с', col_note='Заметка',
        trio_h2='Тройка лидеров и Fable',
        trio_sub='Opus 5.5, GPT-6 Astra и Gemini 4 Argon, плюс Fable 5.1 для сравнения. Вендоры выбирают тесты, где выглядят лучше, поэтому важна колонка «Источник».',
        c_wins='Сколько строк выиграла каждая модель', c_wins_n='Считаем строки таблиц ниже, где есть хотя бы две цифры. Это не рейтинг, а способ увидеть, где кто силён.',
        c_read='Как читать таблицы',
        read_li=['Жирным и с фоном выделено лучшее значение в строке.', 'Прочерк значит, что данных нет, а не что результат плохой.',
                 'Заявления вендоров и независимые замеры (AA, ARC Prize, LMArena) нельзя считать равными по весу.',
                 'ARC-AGI-3: цифра OpenAI для Astra получена на собственной обвязке, в таблице стоит нейтральный замер.'],
        groups=dict(code='Кодинг и агенты', reason='Рассуждение и наука', work='Knowledge work', context='Длинный контекст и мультимодальность'),
        col_test='Тест', col_source='Источник',
        fable_h2='Fable 5.1 против Opus 5.5, и кому верить',
        fable_sub='Слух, что Fable проигрывает Opus, подтверждается. Заодно видно, как сильно заявления вендоров расходятся с независимыми замерами.',
        c_fvo='Разрыв Opus 5.5 и Fable 5.1', c_fvo_n='Таблица Anthropic, тесты в процентах. Справа — на сколько пунктов Opus впереди.',
        c_tb4='Terminal-Bench 4.0: вендор и независимо', c_tb4_n='Полый круг — заявление вендора, тёмный — замер AA. Справа разница; самый большой разрыв у Grok 4.7.',
        callout='Независимые данные совпадают с таблицей Anthropic: индекс AA — {opus_idx} у Opus против {fable_idx} у Fable. В GDPval-AA разница тоже в пользу Opus: {gd_o} против {gd_f} Elo. При этом Fable дороже за токен: {f_in} / {f_out} против {o_in} / {o_out} долларов за миллион токенов на входе и выходе.',
        callout_note='Две оговорки. Сама Anthropic пишет, что на практике разрыв уже, чем в цифрах, и советует начинать с Opus, а на Fable переходить, только если Opus не справляется с длинной задачей. И Opus тестировали с включёнными safeguards: кибер- и био-задачи уходят на более старую модель, что занижает его баллы.',
        names_h2='Проверка названий', names_sub='В обсуждениях ходит много неточных названий моделей. Вот что существует на самом деле.',
        col_asked='Частое название', col_actual='Как на самом деле', col_status='Статус', col_detail='Подробности',
        pick_h2='Что брать', pick_sub='Для типичных задач разработчика: бэкенд на Python, боты, фронтенд.',
        pick1='Python-бэкенд', pick1t='Claude Opus 5.5 в Claude Code на среднем усилии. Он лидирует в FrontierCode и Terminal-Bench, а практики отмечают меньше доработок на существующем коде. Для рутины подойдёт GPT-6.1 Sol.',
        pick2='Telegram-боты', pick2t='Обычно это простая логика и интеграции, фронтир-интеллект тут лишний. Бери GPT-6.1 Sol, а Opus подключай для сложных хендлеров и архитектуры. Если бот принимает голосовые, учти: у Opus нет аудиовхода. Прямых сравнений трёх моделей именно на ботах найти не удалось.',
        pick3='Фронтенд', pick3t='Opus — первый в WebDev Arena: {a_o} Elo против {a_a} у Astra. Для быстрых новых компонентов практики хвалят Astra. Argon силён на бумаге, но в живых тестах нестабилен.',
        pick4='Цена и качество', pick4t='GPT-6.1 Sol — лучший баланс: {sol_idx} баллов индекса при {sol_cost} за задачу. Kimi K3.1 Pro — если нужны открытые веса. Не стоит брать Fable 5.1 и Grok 4.7: у Grok дешёвые токены съедает их количество.',
        faq_h2='Вопросы и ответы',
        faq=[
            ('Какая ИИ-модель лучшая в ноябре 2026?',
             'Среди общедоступных моделей Claude Opus 5.5 лидирует в независимом индексе Artificial Analysis v5: {opus_idx} баллов, немного впереди GPT-6 Astra ({astra_idx}) и GPT-6.1 Sol ({sol_idx}). У Gemini 4 Carbon {carbon_idx} баллов, но доступ только у киберзащитников.'),
            ('Fable 5.1 хуже, чем Opus 5.5?',
             'В собственной таблице Anthropic Opus 5.5 впереди во всех {total} сравнимых тестах, независимый индекс это подтверждает ({opus_idx} против {fable_idx}). Fable при этом дороже за токен: {f_in} / {f_out} против {o_in} / {o_out} долларов за миллион токенов. Сама Anthropic пишет, что на практике разрыв уже.'),
            ('Какая модель лучшая для кодинга?',
             'Claude Opus 5.5 лидирует в агентном кодинге и фронтенде (Terminal-Bench, FrontierCode, Arena WebDev). GPT-6.1 Sol даёт лучшее соотношение цены и качества: {sol_idx} баллов индекса при {sol_cost} за задачу против {opus_cost} у Opus. Gemini 4 Argon силён на длинном контексте.'),
            ('Существует ли Gemini 3.8 Pro?',
             'Нет. Есть Gemini 3.8 Flash и Gemini 3.1 Pro (preview). Актуальный флагман Google — Gemini 4 Argon, а более сильный Gemini 4 Carbon закрыт для публики.'),
            ('Можно ли верить цифрам вендоров?',
             'Осторожно. Один и тот же тест у вендора и в независимом замере может отличаться больше чем на десять пунктов: Grok 4.7 на Terminal-Bench 4.0 у xAI {grok_v}, а у Artificial Analysis {grok_i}.'),
        ],
        cav_h2='Оговорки',
        cav=['Большинство цифр взято из таблиц самих вендоров с удобными им настройками. Один и тот же тест в разной обвязке расходится больше чем на десять пунктов, это видно на графике про Terminal-Bench.',
             'Индекс AA v5 вышел совсем недавно и заметно сдвинул оценки. Старые сравнения на v4 смешивать с ним нельзя.',
             'Скорость у AA плавает от замера к замеру, для части моделей менялась методика. Считай цифры ориентировочными.',
             'Отзывы практиков — единичные прогоны и блоги, это сигнал, а не статистика.',
             'Не нашлось: ARC-AGI-3 для Opus, Fable, Grok, Kimi и GLM; индекс v5 для Grok 4.7; WebDev Elo для Argon; MMMU и AIME для этого поколения.',
             'Лицензия и фактическая публикация весов Kimi K3.1 Pro на момент сбора данных не подтверждены.',
             'Страница собрана по результатам автоматизированного исследования открытых источников. Ключевые цифры стоит сверить по ссылкам ниже, прежде чем на них опираться.'],
        src_h2='Источники', src_n='Вторичные источники: новости, блоги, лидерборды и таблицы вендоров. Подписи ссылок описательные.',
        foot='Данные на 4 ноября 2026. Исходный код и данные: ', foot_link='GitHub',
        noscript='Графикам нужен JavaScript. Все цифры есть и в таблицах.',
        ld_headline='Фронтир-модели ИИ в ноябре 2026: сводка бенчмарков',
        art_about='Сравнение Claude Opus 5.5, GPT-6 Astra, GPT-6.1 Sol, Gemini 4 Argon, Grok 4.7, Kimi K3.1 Pro и GLM-5.3',
    ),
    'en': dict(
        htmllang='en', locale='en_US', other_locale='ru_RU', switch='Русская версия', switch_lang='ru',
        title='AI Model Benchmarks, Nov 2026: Opus 5.5 vs GPT-6 vs Gemini 4 vs Grok, Kimi, GLM',
        desc='Benchmark roundup of Claude Opus 5.5, GPT-6 Astra, GPT-6.1 Sol, Gemini 4 Argon, Grok 4.7, Kimi K3.1 Pro and GLM-5.3: index, price, speed, coding.',
        keywords='AI model benchmarks 2026, LLM comparison, Claude Opus 5.5, GPT-6 Astra, GPT-6.1 Sol, Gemini 4 Argon, Gemini 4 Carbon, Grok 4.7, Kimi K3.1 Pro, GLM-5.3, Claude Fable 5.1, best AI for coding, Artificial Analysis Intelligence Index, Terminal-Bench, ARC-AGI-3, LLM API pricing',
        eyebrow='Benchmark roundup · November 4, 2026', h1='Frontier AI models: who is ahead in November 2026',
        lede="Claude Opus 5.5 is the best publicly available model: {opus_idx} points on the Artificial Analysis Intelligence Index v5. Claude Fable 5.1 trails it in {ahead} of {total} comparable tests in Anthropic's own table.",
        chips=[('sec-index', 'Index, price, speed'), ('sec-trio', 'Top three'), ('sec-fable', 'Fable vs Opus'),
               ('sec-names', 'Name check'), ('sec-pick', 'What to pick'), ('sec-faq', 'FAQ')],
        tile1='AA Index v5, leader among available models', tile1n='Claude Opus 5.5',
        tile2='Cost per index task, GPT-6.1 Sol', tile2n='Opus 5.5: {opus_cost}',
        tile3='ARC-AGI-3, GPT-6 Astra', tile3n='Neutral ARC Prize harness',
        tile4='GraphWalks 256K–1M, Gemini 4 Argon', tile4n="Long context, Google's numbers",
        tile5='Opus 5.5 ahead of Fable 5.1', tile5v='{ahead} of {total}', tile5n='Comparable Anthropic tests',
        idx_h2='Index, price and speed',
        idx_sub='The independent Artificial Analysis v5 index is the backbone of this roundup: most of its tests are private, so models are harder to tune against them.',
        c_index='Intelligence Index v5 (Artificial Analysis)', c_index_n='Higher is better. Grok 4.7 has no published v5 score yet.',
        c_value='Price vs quality', c_value_n='Cost of an index task versus score. Stronger and cheaper means further up and to the left.',
        c_speed='Output speed', c_speed_n='Tokens per second, range of AA measurements at max effort. Figures are approximate.',
        c_models='All models', c_models_n='Prices per million tokens. The closed Gemini 4 Carbon is not available in practice, so compare against Argon.',
        col_model='Model', col_vendor='Vendor', col_release='Release', col_in='Input, $', col_out='Output, $', col_ctx='Context, K tokens',
        col_idx='AA Index v5', col_cost='Task, $', col_speed='Speed, tok/s', col_note='Note',
        trio_h2='The top three and Fable',
        trio_sub='Opus 5.5, GPT-6 Astra and Gemini 4 Argon, with Fable 5.1 for comparison. Vendors pick tests that flatter them, so the Source column matters.',
        c_wins='How many rows each model wins', c_wins_n='Counts rows in the tables below that have at least two numbers. Not a ranking, just a view of who is strong where.',
        c_read='How to read the tables',
        read_li=['Bold with a background marks the best value in a row.', 'A dash means no data, not a bad result.',
                 'Vendor claims and independent measurements (AA, ARC Prize, LMArena) should not be weighed equally.',
                 "ARC-AGI-3: OpenAI's number for Astra comes from its own harness; the table shows the neutral measurement."],
        groups=dict(code='Coding and agents', reason='Reasoning and science', work='Knowledge work', context='Long context and multimodality'),
        col_test='Test', col_source='Source',
        fable_h2='Fable 5.1 vs Opus 5.5, and whom to trust',
        fable_sub='The rumor that Fable loses to Opus checks out. It also shows how far vendor claims drift from independent measurements.',
        c_fvo='Opus 5.5 vs Fable 5.1 gap', c_fvo_n="Anthropic's table, percentage tests. On the right: how many points Opus leads by.",
        c_tb4='Terminal-Bench 4.0: vendor vs independent', c_tb4_n='Hollow circle is the vendor claim, dark circle the AA measurement. The gap is on the right; the largest is Grok 4.7.',
        callout="Independent data agrees with Anthropic's table: the AA index is {opus_idx} for Opus versus {fable_idx} for Fable. On GDPval-AA Opus also leads: {gd_o} vs {gd_f} Elo. Fable also costs more per token: {f_in} / {f_out} versus {o_in} / {o_out} dollars per million input / output tokens.",
        callout_note='Two caveats. Anthropic itself says the gap is narrower in practice than the numbers suggest and advises starting with Opus, moving to Fable only if Opus cannot finish a long task. And Opus was tested with safeguards on: cyber and bio tasks are routed to an older model, which lowers its scores.',
        names_h2='Model name check', names_sub='Plenty of inexact model names circulate online. Here is what actually exists.',
        col_asked='Name in circulation', col_actual='Actual name', col_status='Status', col_detail='Details',
        pick_h2='What to pick', pick_sub='For typical developer work: Python backend, bots, frontend.',
        pick1='Python backend', pick1t='Claude Opus 5.5 in Claude Code at medium effort. It leads FrontierCode and Terminal-Bench, and practitioners report less rework on existing code. GPT-6.1 Sol is fine for routine work.',
        pick2='Telegram bots', pick2t='Usually simple logic plus integrations, so frontier-level intelligence is overkill. Pick GPT-6.1 Sol and bring in Opus for tricky handlers and architecture. If the bot takes voice messages, note that Opus has no audio input. No head-to-head comparison of the three models on bots specifically could be found.',
        pick3='Frontend', pick3t='Opus is first on WebDev Arena: {a_o} Elo versus {a_a} for Astra. Practitioners praise Astra for quick new components. Argon looks strong on paper but is unstable in hands-on tests.',
        pick4='Price and quality', pick4t="GPT-6.1 Sol is the best balance: {sol_idx} index points at {sol_cost} per task. Kimi K3.1 Pro fits if you need open weights. Skip Fable 5.1 and Grok 4.7: Grok's cheap tokens are eaten up by how many of them it uses.",
        faq_h2='FAQ',
        faq=[
            ('Which AI model is the best in November 2026?',
             'Among publicly available models, Claude Opus 5.5 leads the independent Artificial Analysis Intelligence Index v5 with {opus_idx} points, just ahead of GPT-6 Astra ({astra_idx}) and GPT-6.1 Sol ({sol_idx}). Gemini 4 Carbon scores {carbon_idx}, but only cyber defenders can access it.'),
            ('Is Claude Fable 5.1 worse than Opus 5.5?',
             "In Anthropic's own table Opus 5.5 is ahead in all {total} comparable tests, and the independent index agrees ({opus_idx} vs {fable_idx}). Fable also costs more per token: {f_in} / {f_out} versus {o_in} / {o_out} dollars per million input / output tokens. Anthropic itself says the gap is narrower in practice."),
            ('Which model is best for coding?',
             'Claude Opus 5.5 leads on agentic coding and frontend (Terminal-Bench, FrontierCode, Arena WebDev). GPT-6.1 Sol offers the best price-to-quality ratio: {sol_idx} index points at {sol_cost} per index task versus {opus_cost} for Opus. Gemini 4 Argon is strong at long-context work.'),
            ('Does Gemini 3.8 Pro exist?',
             "No. There are Gemini 3.8 Flash and Gemini 3.1 Pro (preview). Google's current flagship is Gemini 4 Argon; the stronger Gemini 4 Carbon is closed to the public."),
            ('Can I trust vendor benchmark numbers?',
             'Treat them with care. The same test can differ by more than ten points between vendor and independent runs: for Grok 4.7 on Terminal-Bench 4.0, xAI reports {grok_v} while Artificial Analysis measured {grok_i}.'),
        ],
        cav_h2='Caveats',
        cav=["Most numbers come from the vendors' own tables, with settings that suit them. The same test in a different harness differs by more than ten points, as the Terminal-Bench chart shows.",
             'The AA v5 index is brand new and shifted scores noticeably. Do not mix older v4 comparisons with it.',
             'AA speed varies between measurements and the method changed for some models. Treat speed figures as approximate.',
             'Practitioner reviews are single runs and blog posts: a signal, not statistics.',
             'Not found: ARC-AGI-3 for Opus, Fable, Grok, Kimi and GLM; v5 index for Grok 4.7; WebDev Elo for Argon; MMMU and AIME for this generation.',
             'License and actual release of the Kimi K3.1 Pro weights were not confirmed at the time of data collection.',
             'This page was assembled from an automated research pass over public sources. Verify key numbers against the linked sources before relying on them.'],
        src_h2='Sources', src_n='Secondary sources: news, blogs, leaderboards and vendor tables. Link labels are descriptive.',
        foot='Data as of November 4, 2026. Source code and data: ', foot_link='GitHub',
        noscript='Charts need JavaScript. All numbers are also in the tables.',
        ld_headline='Frontier AI models in November 2026: benchmark roundup',
        art_about='Comparison of Claude Opus 5.5, GPT-6 Astra, GPT-6.1 Sol, Gemini 4 Argon, Grok 4.7, Kimi K3.1 Pro and GLM-5.3',
    ),
}

# ============================== RENDERING ==============================
MODEL_KEYS = ['opus', 'fable', 'astra', 'argon']


def numstr(x):
    return str(int(x)) if x == int(x) else str(x)


FMT = {
    'int': lambda v: str(round(v)),
    'pct1': lambda v: f'{v:.1f}%',
    'usd': lambda v: '$' + (numstr(v) if v == int(v) else f'{v:.2f}'),
    'usd2': lambda v: f'${v:.2f}',
    'elo': lambda v: str(round(v)),
    'text': lambda v: numstr(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else str(v),
}


class Ctx:
    """Lookup helpers over the datasets of one language, including the computed ones."""

    def __init__(self, ds):
        self.ds = dict(ds)
        self.ds['fvo_summary'] = [dict(ahead=sum(1 for r in ds['fable_vs_opus'] if r['opus'] > r['fable']), total=len(ds['fable_vs_opus']))]

    def get(self, source, field, where=None, row=None):
        rows = self.ds[source]
        if row is not None:
            return rows[row][field]
        k, v = where.split('=')
        return next(r for r in rows if str(r[k]) == v)[field]

    def val(self, source, field, fmt, where=None, row=None, cls='n', plain=False):
        v = self.get(source, field, where, row)
        text = FMT[fmt](v)
        if plain:
            return text
        sel = f'data-where="{where}"' if where else f'data-row="{row}"'
        c = f' class="{cls}"' if cls else ''
        return f'<span{c} data-draw="val" data-source="{source}" data-field="{field}" {sel} data-fmt="{fmt}">{text}</span>'


def fill(ctx, text, plain=False):
    c = ctx
    v = lambda *a, **k: c.val(*a, plain=plain, **k)
    m = dict(
        opus_idx=v('models', 'aa_index', 'int', where='id=opus'),
        fable_idx=v('models', 'aa_index', 'int', where='id=fable'),
        astra_idx=v('models', 'aa_index', 'int', where='id=astra'),
        sol_idx=v('models', 'aa_index', 'int', where='id=sol'),
        carbon_idx=v('models', 'aa_index', 'int', where='id=carbon'),
        opus_cost=v('models', 'task_cost', 'usd2', where='id=opus'),
        sol_cost=v('models', 'task_cost', 'usd2', where='id=sol'),
        ahead=v('fvo_summary', 'ahead', 'int', row=0),
        total=v('fvo_summary', 'total', 'int', row=0),
        gd_o=v('fable_vs_opus', 'opus', 'elo', where='id=gdpval'),
        gd_f=v('fable_vs_opus', 'fable', 'elo', where='id=gdpval'),
        f_in=v('models', 'price_in', 'usd', where='id=fable'),
        f_out=v('models', 'price_out', 'usd', where='id=fable'),
        o_in=v('models', 'price_in', 'usd', where='id=opus'),
        o_out=v('models', 'price_out', 'usd', where='id=opus'),
        a_o=v('bench', 'opus', 'elo', where='id=arena'),
        a_a=v('bench', 'astra', 'elo', where='id=arena'),
        grok_v=FMT['pct1'](37.6),
        grok_i=FMT['pct1'](25.8),
    )
    # the Grok vendor/independent figures in the FAQ come from the TB4 dataset
    m['grok_v'] = FMT['pct1'](next(r['claimed'] for r in c.ds['tb4_gap'] if r['id'] == 'grok'))
    m['grok_i'] = FMT['pct1'](next(r['independent'] for r in c.ds['tb4_gap'] if r['id'] == 'grok'))
    return text.format(**m)


def cell(kind, f, r, hi):
    v = r.get(f)
    cls, style = [], ''
    if kind == 'range':
        s = '—' if v is None else (numstr(v) if v == r.get(hi) else f'{numstr(v)}–{numstr(r.get(hi))}')
    elif kind == 'val':
        s = '—' if v is None else (FMT['elo'](v) if r['unit'] == 'Elo' else FMT['pct1'](v))
        vals = [r[k] for k in MODEL_KEYS if r.get(k) is not None]
        if len(vals) >= 2 and v is not None and v == max(vals):
            cls.append('best')
    elif kind == 'idx':
        s = '—' if v is None else FMT['int'](v)
        if v is not None:
            cls.append('bar')
            style = f' style="--w:{v / 65 * 100:.2f}%"'
    elif kind == 'status':
        s = str(v)
        cls.append('st-' + r['status_key'])
    else:
        s = '—' if v is None else FMT.get(kind, FMT['text'])(v)
    if f in ('note', 'detail'):
        cls.append('sm')
    return s, cls, style


def table(source, cols, rows, body, group=None):
    ths = ''.join(
        f'<th data-field="{f}" data-fmt="{k}"' + (f' data-hi="{hi}"' if hi else '') + (f' class="{c}"' if c else '') + f'>{E(h)}</th>'
        for f, k, c, h, hi in cols)
    trs = []
    for r in rows:
        tds = []
        for f, k, c, h, hi in cols:
            s, extra, style = cell(k, f, r, hi)
            classes = ' '.join(x for x in [c] + extra if x)
            cattr = ' class="' + classes + '"' if classes else ''
            tds.append('<td' + cattr + style + '>' + E(s) + '</td>')
        dim = ' class="dim"' if r.get('restricted') else ''
        trs.append(f'<tr data-key="{E(r["id"])}"{dim}>{"".join(tds)}</tr>')
    g = f' data-group="{group}"' if group else ''
    return (f'<div class="tbl-wrap"><table class="gt" data-source="{source}" data-row-key="id"><thead><tr>{ths}</tr></thead>'
            f'<tbody data-draw="{body}"{g}>{"".join(trs)}</tbody></table></div>')


def page(lang):
    t = T[lang]
    ds = datasets(lang)
    ctx = Ctx(ds)
    F = lambda s: fill(ctx, s)
    P = lambda s: fill(ctx, s, plain=True)
    ru = lang == 'ru'
    url = BASE + ('ru/' if ru else '')
    rel = '../' if ru else ''
    sw_href = BASE + ('' if ru else 'ru/')

    models_sorted = sorted(ds['models'], key=lambda r: -(r['aa_index'] if r['aa_index'] is not None else -1))
    mcols = [('model', 'text', '', t['col_model'], None), ('vendor', 'text', 'hide-sm', t['col_vendor'], None),
             ('release', 'text', 'hide-sm', t['col_release'], None), ('price_in', 'usd', 'num', t['col_in'], None),
             ('price_out', 'usd', 'num', t['col_out'], None), ('context_k', 'text', 'num hide-sm', t['col_ctx'], None),
             ('aa_index', 'idx', 'num', t['col_idx'], None), ('task_cost', 'usd2', 'num', t['col_cost'], None),
             ('speed_lo', 'range', 'num hide-sm', t['col_speed'], 'speed_hi'), ('note', 'text', 'hide-sm', t['col_note'], None)]
    bcols = [('benchmark', 'text', '', t['col_test'], None), ('source', 'text', 'hide-sm', t['col_source'], None),
             ('opus', 'val', 'num', 'Opus 5.5', None), ('fable', 'val', 'num', 'Fable 5.1', None),
             ('astra', 'val', 'num', 'GPT-6 Astra', None), ('argon', 'val', 'num', 'Gemini 4 Argon', None)]
    ncols = [('asked', 'text', '', t['col_asked'], None), ('actual', 'text', '', t['col_actual'], None),
             ('status', 'status', '', t['col_status'], None), ('detail', 'text', 'hide-sm', t['col_detail'], None)]

    groups_html = ''.join(
        f'<div class="card"><h3>{E(t["groups"][g])}</h3>' +
        table('bench', bcols, [r for r in ds['bench'] if r['group'] == g], 'benchBody', group=g) + '</div>'
        for g in ['code', 'reason', 'work', 'context'])

    faq_pairs = [(q, P(a)) for q, a in t['faq']]
    faq_html = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq_pairs)

    ld_article = {
        '@context': 'https://schema.org', '@type': 'Article', 'headline': t['ld_headline'], 'description': t['desc'],
        'inLanguage': lang, 'datePublished': DATE, 'dateModified': DATE, 'mainEntityOfPage': url, 'url': url,
        'author': {'@type': 'Person', 'name': AUTHOR['name'], 'url': AUTHOR['url']},
        'keywords': t['keywords'], 'about': t['art_about'],
    }
    ld_faq = {
        '@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': lang,
        'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq_pairs],
    }
    ld = lambda o: '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False).replace('</', '<\\/') + '</script>'

    verify = ''.join(f'<meta name="{k}" content="{E(v)}">\n' for k, v in VERIFY.items() if v)
    favicon = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%231f1e1d'/%3E"
               "%3Crect x='6' y='17' width='5' height='9' rx='1.5' fill='%23d97757'/%3E%3Crect x='13.5' y='10' width='5' height='16' rx='1.5' fill='%2310a37f'/%3E"
               "%3Crect x='21' y='5' width='5' height='21' rx='1.5' fill='%234285f4'/%3E%3C/svg%3E")

    head = f'''<!doctype html>
<html lang="{t['htmllang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(t['title'])}</title>
<meta name="description" content="{E(t['desc'])}">
<meta name="keywords" content="{E(t['keywords'])}">
<meta name="author" content="{E(AUTHOR['name'])}">
<meta name="robots" content="index, follow, max-image-preview:large">
{verify}<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{BASE}">
<link rel="alternate" hreflang="ru" href="{BASE}ru/">
<link rel="alternate" hreflang="x-default" href="{BASE}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{E(t['title'])}">
<meta property="og:description" content="{E(t['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:locale:alternate" content="{t['other_locale']}">
<meta property="article:published_time" content="{DATE}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{E(t['title'])}">
<meta name="twitter:description" content="{E(t['desc'])}">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{favicon}">
<link rel="stylesheet" href="{rel}assets/style.css">
{ld(ld_article)}
{ld(ld_faq)}
</head>
'''

    chips = ''.join(f'<button type="button" class="chip" data-go="{i}">{E(n)}</button>' for i, n in t['chips'])
    li = lambda items: ''.join(f'<li>{E(x)}</li>' for x in items)
    srcs = ''.join(f'<li><a href="{E(u)}" rel="noopener" target="_blank">{E(n)}</a></li>' for u, n in SOURCES)
    ds_attr = lambda name: f'data-draw="{name}"'

    body = f'''<body>
<div class="bm">

<nav class="top" aria-label="Language and repository">
<a href="{sw_href}" hreflang="{t['switch_lang']}" lang="{t['switch_lang']}">{E(t['switch'])}</a>
<a href="{GITHUB}" rel="noopener">GitHub</a>
</nav>

<header class="hero" id="top">
<p class="eyebrow">{E(t['eyebrow'])}</p>
<h1>{E(t['h1'])}</h1>
<p class="lede">{F(E(t['lede']))}</p>
<nav class="chips" aria-label="Sections">{chips}</nav>
</header>

<div class="tiles">
<div class="tile"><p class="tl">{E(t['tile1'])}</p><p class="tv">{ctx.val('models', 'aa_index', 'int', where='id=opus', cls='')}</p><p class="tn">{E(t['tile1n'])}</p></div>
<div class="tile"><p class="tl">{E(t['tile2'])}</p><p class="tv">{ctx.val('models', 'task_cost', 'usd2', where='id=sol', cls='')}</p><p class="tn">{F(E(t['tile2n']))}</p></div>
<div class="tile"><p class="tl">{E(t['tile3'])}</p><p class="tv">{ctx.val('bench', 'astra', 'pct1', where='id=arc3', cls='')}</p><p class="tn">{E(t['tile3n'])}</p></div>
<div class="tile"><p class="tl">{E(t['tile4'])}</p><p class="tv">{ctx.val('bench', 'argon', 'pct1', where='id=graph', cls='')}</p><p class="tn">{E(t['tile4n'])}</p></div>
<div class="tile"><p class="tl">{E(t['tile5'])}</p><p class="tv">{F(E(t['tile5v']).replace('{ahead}', '{ahead}').replace('{total}', '{total}')).replace('class="n" ', '')}</p><p class="tn">{E(t['tile5n'])}</p></div>
</div>

<section class="sec" id="sec-index">
<h2>{E(t['idx_h2'])}</h2>
<p class="sub">{E(t['idx_sub'])}</p>
<div class="grid3">
<div class="card" id="c-index"><h3>{E(t['c_index'])}</h3><p class="note">{E(t['c_index_n'])}</p><div class="chart" {ds_attr('indexChart')} data-source="models"></div></div>
<div class="card" id="c-value"><h3>{E(t['c_value'])}</h3><p class="note">{E(t['c_value_n'])}</p><div class="chart" {ds_attr('valueChart')} data-source="models"></div></div>
<div class="card" id="c-speed"><h3>{E(t['c_speed'])}</h3><p class="note">{E(t['c_speed_n'])}</p><div class="chart" {ds_attr('speedChart')} data-source="models"></div></div>
</div>
<noscript><p>{E(t['noscript'])}</p></noscript>
<div class="card" id="c-models"><h3>{E(t['c_models'])}</h3><p class="note">{E(t['c_models_n'])}</p>
{table('models', mcols, models_sorted, 'modelsBody')}
</div>
</section>

<section class="sec" id="sec-trio">
<h2>{E(t['trio_h2'])}</h2>
<p class="sub">{E(t['trio_sub'])}</p>
<div class="grid2">
<div class="card" id="c-wins"><h3>{E(t['c_wins'])}</h3><p class="note">{E(t['c_wins_n'])}</p><div class="chart" {ds_attr('winsChart')} data-source="wins"></div></div>
<div class="card"><h3>{E(t['c_read'])}</h3><ul>{li(t['read_li'])}</ul></div>
</div>
<div class="grid2">
{groups_html}
</div>
</section>

<section class="sec" id="sec-fable">
<h2>{E(t['fable_h2'])}</h2>
<p class="sub">{E(t['fable_sub'])}</p>
<div class="grid2">
<div class="card" id="c-fvo"><h3>{E(t['c_fvo'])}</h3><p class="note">{E(t['c_fvo_n'])}</p><div class="chart" {ds_attr('fvoChart')} data-source="fvo_delta"></div></div>
<div class="card" id="c-tb4"><h3>{E(t['c_tb4'])}</h3><p class="note">{E(t['c_tb4_n'])}</p><div class="chart" {ds_attr('tb4Chart')} data-source="tb4_delta"></div></div>
</div>
<div class="card"><p class="callout">{F(E(t['callout']))}</p><p class="note">{E(t['callout_note'])}</p></div>
</section>

<section class="sec" id="sec-names">
<h2>{E(t['names_h2'])}</h2>
<p class="sub">{E(t['names_sub'])}</p>
<div class="card">{table('naming', ncols, ds['naming'], 'namingBody')}</div>
</section>

<section class="sec" id="sec-pick">
<h2>{E(t['pick_h2'])}</h2>
<p class="sub">{E(t['pick_sub'])}</p>
<div class="picks">
<div class="card"><h3>{E(t['pick1'])}</h3><p>{E(t['pick1t'])}</p></div>
<div class="card"><h3>{E(t['pick2'])}</h3><p>{E(t['pick2t'])}</p></div>
<div class="card"><h3>{E(t['pick3'])}</h3><p>{F(E(t['pick3t']))}</p></div>
<div class="card"><h3>{E(t['pick4'])}</h3><p>{F(E(t['pick4t']))}</p></div>
</div>
</section>

<section class="sec" id="sec-faq">
<h2>{E(t['faq_h2'])}</h2>
<div class="faq">{faq_html}</div>
</section>

<section class="sec" id="sec-caveats">
<h2>{E(t['cav_h2'])}</h2>
<div class="card"><ul>{li(t['cav'])}</ul></div>
</section>

<section class="sec" id="sec-sources">
<h2>{E(t['src_h2'])}</h2>
<p class="sub">{E(t['src_n'])}</p>
<ul class="src">{srcs}</ul>
<p class="foot">{E(t['foot'])}<a href="{GITHUB}" rel="noopener">{E(t['foot_link'])}</a>.</p>
</section>

</div>
<script>window.__L={json.dumps(L_JS[lang], ensure_ascii=False)};window.__DATA={json.dumps(ds, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')};</script>
<script src="{rel}assets/d3.min.js" defer></script>
<script src="{rel}assets/app.js" defer></script>
</body>
</html>
'''
    return head + body


def sitemap():
    def entry(loc):
        return (f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{DATE}</lastmod>\n'
                f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="ru" href="{BASE}ru/"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>\n  </url>\n')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + entry(BASE) + entry(BASE + 'ru/') + '</urlset>\n')


if __name__ == '__main__':
    (ROOT / 'ru').mkdir(exist_ok=True)
    (ROOT / 'index.html').write_text(page('en'), encoding='utf-8')
    (ROOT / 'ru' / 'index.html').write_text(page('ru'), encoding='utf-8')
    (ROOT / 'sitemap.xml').write_text(sitemap(), encoding='utf-8')
    print('built: index.html, ru/index.html, sitemap.xml')
