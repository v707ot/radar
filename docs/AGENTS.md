# AGENTS.md — uav_lowalt_warning

Автономное **сигнальное** устройство предупреждения о малой высоте БПЛА.
Изделие гражданское: выходы — зуммер, светодиод, дискретный флаг «LOW ALT», CAN-телеметрия.
**Исполнительных/инициирующих цепей в изделии нет.** Не смешивать с посторонними
документами репозитория (например, «Гресс») — проект полностью самостоятелен.

## Структура

- `README.md`, `ПРОЕКТ.md` — обзор и пояснительная записка.
- `docs/` — документы: датчики, закупка, подключение/сборка, круговой обзор,
  `ПЕЧАТНАЯ_ПЛАТА_ТРАССИРОВКА.md`, `ССЫЛКИ_ДАТАШИТЫ_ЗАКУПКА.md`.
- `hardware/` — `BOM.csv`, `ЗАКУПКА_RU.csv`, `ЗАКУПКА_CN.csv`,
  генератор `gen_diagrams.py` и готовые `*.svg` (block, schematic, mounting,
  coverage, timing, work_algorithm, **pcb_layout**).
- `sim/` — HTML-демонстрации: `principle.html`, `detection.html`, `detection3d.html`.
- `index.html` / `preview.html` / `project.html` / `sensors.html` — сайт.
- `build_pages.py` — сборка страниц (см. ниже).

## Сборка

```bash
python3 hardware/gen_diagrams.py   # перегенерировать все SVG (в т.ч. pcb_layout.svg)
python3 build_pages.py             # собрать index.html и обновить навигацию
```

`build_pages.py` **идемпотентен**: встраивает разделы 14 (печатная плата) и 15
(ссылки) в `preview.html` только если их ещё нет, и обновляет верхнюю панель /
навигацию один раз. `index.html` — точная копия `preview.html`.

## Ключевые решения

- Датчик: 6× Acconeer A121 (XM125, 60 ГГц PCR) на общей SPI: 1 вниз,
  4 в кольцо (360°), 1 вверх. Реакция ≤ 1 мс, погрешность ≤ 1 м, масса ~97 г.
- Порог срабатывания H_ср = 2…10 м, регулируется с БПЛА (демо: ползунок «Порог H_ср»).
- Плата-носитель 64×48 мм, 4 слоя (сигналы / земля / питание / сигналы),
  зона запрета под антеннами датчиков (keepout) — трассы туда не заводить.

## Проверка ссылок

Внешние ссылки периодически ломаются. Быстрая проверка:

```bash
python3 - <<'PY'
import re,subprocess
h=open('index.html',encoding='utf-8').read()
for u in sorted(set(re.findall(r'href="(https?://[^"]+)"',h))):
    c=subprocess.run(["curl","-sL","-o","/dev/null","--max-time","25",
                      "-w","%{http_code}","-A","Mozilla/5.0",u],
                     capture_output=True,text=True).stdout
    print(c,u)
PY
```

Известные особенности:
- `chipdip.ru`, `ozon.ru`, `aliexpress.ru` отдают 403/307 на скриптовые запросы —
  это норма, ссылки рабочие в браузере.
- `st.com` блокирует автозапросы PDF (код `000`); в
  `docs/ССЫЛКИ_ДАТАШИТЫ_ЗАКУПКА.md` добавлены зеркала в веб-архиве.
- NXP перенесла документацию: прямой `nxp.com/docs/en/data-sheet/TJA1051.pdf` → 404;
  используется архивная копия.
- Платан: поиск по `platan.ru/cgi-bin/qwery_i.pl?code=<ПАРТНОМЕР>` (не `qwery.pl`).

## Публикация

Сайт публикуется на GitHub Pages из репозитория `v707ot/radar`
(branch `main`, workflow `.github/workflows/pages.yml`):
<https://v707ot.github.io/radar/>.
Локальная рабочая копия — этот каталог; для публикации синхронизировать файлы в
клон `v707ot/radar` и запушить в `main`.
