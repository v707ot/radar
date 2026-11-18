#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Встраивает разделы «Печатная плата» и «Ссылки/даташиты» в HTML-страницы,
обновляет навигацию и создаёт index.html."""
import pathlib, shutil

root = pathlib.Path(__file__).resolve().parent
hw = root / "hardware"

pcb_svg = (hw / "pcb_layout.svg").read_text(encoding="utf-8")
pcb_svg = pcb_svg.replace('width="1240" height="1010"', 'width="100%" height="auto"', 1)

PCB_SECTION = (
    '<h2>14. Печатная плата: компоновка и трассировка</h2><div class="card">'
    + pcb_svg +
    '<p>Подробно: <b>docs/ПЕЧАТНАЯ_ПЛАТА_ТРАССИРОВКА.md</b>. '
    'Плата-носитель 64×48 мм (4 слоя: сигналы / сплошная земля / питание / сигналы), '
    'платы датчиков 26×26 мм (2 слоя). Под антеннами 60 ГГц — зоны запрета (keepout) без меди. '
    'Трассировка: SPI ≤ 50 мм с согласованием длин, CAN — диффпара 120 Ом с терминатором у разъёма, '
    'питание 0,5…1,0 мм «звездой» с развязкой. Все выходы — только сигнальные.</p></div>'
)

LINKS_SECTION = (
    '<h2>15. Ссылки: даташиты и закупка в России</h2><div class="card">'
    '<p>Полный справочник — <b>docs/ССЫЛКИ_ДАТАШИТЫ_ЗАКУПКА.md</b>.</p>'
    '<h3>Даташиты (официальные)</h3>'
    '<table><tr><th>Поз.</th><th>Компонент</th><th>Даташит</th></tr>'
    '<tr><td>U1…U6</td><td>Acconeer A121 / XM125</td><td><a href="https://developer.acconeer.com/download/a121-datasheet/">A121 datasheet (PDF)</a> · <a href="https://developer.acconeer.com/download/xm125-datasheet/">XM125 datasheet (PDF)</a></td></tr>'
    '<tr><td>U8</td><td>STM32G474RE</td><td><a href="https://www.st.com/resource/en/datasheet/stm32g474re.pdf">STM32G474 datasheet (PDF)</a> · <a href="https://www.st.com/resource/en/user_manual/um2505-stm32g4-nucleo64-boards-mb1367-stmicroelectronics.pdf">UM2505 (Nucleo)</a></td></tr>'
    '<tr><td>U9</td><td>TJA1051 (CAN)</td><td><a href="https://web.archive.org/web/20231128040048/https://www.nxp.com/docs/en/data-sheet/TJA1051.pdf">TJA1051 datasheet (PDF)</a></td></tr>'
    '<tr><td>PS1</td><td>Pololu D24V5F3</td><td><a href="https://www.pololu.com/product/2842/resources">D24V5F3 (схема, ресурсы)</a></td></tr>'
    '<tr><td>Q1</td><td>2N7002</td><td><a href="https://www.onsemi.com/download/data-sheet/pdf/2n7002-d.pdf">2N7002 datasheet (PDF)</a></td></tr>'
    '<tr><td>D1</td><td>1N4148</td><td><a href="https://www.vishay.com/docs/81857/1n4148.pdf">1N4148 datasheet (PDF)</a></td></tr>'
    '<tr><td>D2</td><td>TVS SMBJ5.0A</td><td><a href="https://www.vishay.com/docs/88392/smbj.pdf">SMBJ series datasheet (PDF)</a></td></tr>'
    '</table>'
    '<h3>Закупка в РФ: прямые карточки ChipDip</h3>'
    '<p>ChipDip закрыт антибот-защитой (DDoS-Guard) для автоматического доступа, но ссылки ниже открываются в браузере. '
    'Способ получения ссылок — публичный веб-архив (Wayback CDX API), см. docs/ССЫЛКИ_ДАТАШИТЫ_ЗАКУПКА.md, п.0.</p>'
    '<table><tr><th>Компонент</th><th>Ссылка ChipDip</th></tr>'
    '<tr><td>TJA1051T/3</td><td><a href="https://www.chipdip.ru/product/tja1051tk-3-1j">chipdip.ru/product/tja1051tk-3-1j</a></td></tr>'
    '<tr><td>STM32G474VET6</td><td><a href="https://www.chipdip.ru/product/stm32g474vet6-2">chipdip.ru/product/stm32g474vet6-2</a></td></tr>'
    '<tr><td>2N7002</td><td><a href="https://www.chipdip.ru/product/2n7002-tp-tranzistor-mosfet-n-kanal-60v-0.115a-sot-23-mcc-9000542509">2N7002 (SOT-23)</a></td></tr>'
    '<tr><td>1N4148</td><td><a href="https://www.chipdip.ru/product/1n4148-diod-impulsnyy-0.15a-100v-do-35-yj-9000497880">1N4148 (DO-35)</a></td></tr>'
    '<tr><td>TVS SMBJ5.0A</td><td><a href="https://www.chipdip.ru/product/smbj5.0a-zaschitnyy-diod-600vt-5v-smb-do-214aa-sunmate-9001052837">SMBJ5.0A</a></td></tr>'
    '<tr><td>LED АЛ307КМ5</td><td><a href="https://www.chipdip.ru/product/al307km5-svetodiod-krasnyy-45-d-5mm-2.5mkd-660nm-proton-202246162">АЛ307КМ5</a></td></tr>'
    '<tr><td>Зуммер (активный)</td><td><a href="https://www.chipdip.ru/product/zummer-b2pb-b1d-pezoel-y-22-25-98-8db-0.1m-zelenyy-autonics-8045901851">зуммер пьезо, со встроенным генератором</a></td></tr>'
    '</table>'
    '<h3>Поиск по партномеру в магазинах РФ</h3>'
    '<table><tr><th>Магазин</th><th>Ссылка (пример: TJA1051)</th></tr>'
    '<tr><td>ChipDip</td><td><a href="https://www.chipdip.ru/search?searchtext=TJA1051">chipdip.ru/search?searchtext=TJA1051</a></td></tr>'
    '<tr><td>Промэлектроника</td><td><a href="https://www.promelec.ru/search/?q=TJA1051">promelec.ru/search/?q=TJA1051</a></td></tr>'
    '<tr><td>Платан</td><td><a href="https://www.platan.ru/cgi-bin/qwery_i.pl?code=TJA1051">platan.ru/cgi-bin/qwery_i.pl?code=TJA1051</a></td></tr>'
    '<tr><td>Кварц (Quartz1)</td><td><a href="https://www.quartz1.com/price/search.php?word=TJA1051">quartz1.com/price/search.php?word=TJA1051</a></td></tr>'
    '<tr><td>Ozon</td><td><a href="https://www.ozon.ru/search/?text=TJA1051">ozon.ru/search/?text=TJA1051</a></td></tr>'
    '</table></div>'
)

TAIL = '</div>\n</body></html>'

# --- preview.html ---
pv = root / "preview.html"
html = pv.read_text(encoding="utf-8")
if "14. Печатная плата" in html:
    print("preview.html: разделы уже встроены, пропуск")
else:
    assert TAIL in html, "хвост preview.html не найден"
    html = html.replace(TAIL, PCB_SECTION + LINKS_SECTION + TAIL)
    pv.write_text(html, encoding="utf-8")
    print("preview.html обновлён:", len(html), "байт")

# --- index.html = копия preview.html ---
shutil.copyfile(pv, root / "index.html")
print("index.html создан")

# --- навигация ---
nav_old = '<a href="sim/detection3d.html">3D-демо</a> · <a href="sim/detection.html">2D-демо</a>'
nav_new = (nav_old + ' ·\n<a href="docs/ПЕЧАТНАЯ_ПЛАТА_ТРАССИРОВКА.md">Плата</a> · '
           '<a href="docs/ССЫЛКИ_ДАТАШИТЫ_ЗАКУПКА.md">Даташиты и закупка</a>')
for f in ("project.html", "sensors.html"):
    p = root / f
    h = p.read_text(encoding="utf-8")
    if "ПЕЧАТНАЯ_ПЛАТА_ТРАССИРОВКА.md" in h:
        print(f, "навигация уже обновлена, пропуск")
    elif nav_old in h:
        p.write_text(h.replace(nav_old, nav_new), encoding="utf-8")
        print(f, "навигация обновлена")
    else:
        print(f, "!! шаблон навигации не найден")

# верхняя панель preview/index
pn_old = ('🎮 <b>Визуализации</b>: <a href="sim/principle.html" style="color:#7fb8ff"><b>Принцип дальности</b></a> · '
          '<a href="sim/detection3d.html" style="color:#7fb8ff">3D (два БПЛА)</a> · '
          '<a href="sim/detection.html" style="color:#7fb8ff">2D (гонка дронов)</a>')
pn_new = (pn_old + '<br>🧩 <a href="docs/ПЕЧАТНАЯ_ПЛАТА_ТРАССИРОВКА.md" style="color:#7fb8ff"><b>Печатная плата</b> (трассировка)</a> · '
          '🔗 <a href="docs/ССЫЛКИ_ДАТАШИТЫ_ЗАКУПКА.md" style="color:#7fb8ff"><b>Даташиты и закупка в РФ</b></a>')
for f in ("preview.html", "index.html"):
    p = root / f
    h = p.read_text(encoding="utf-8")
    if "ПЕЧАТНАЯ_ПЛАТА_ТРАССИРОВКА.md" in h:
        print(f, "верхняя панель уже обновлена, пропуск")
    elif pn_old in h:
        p.write_text(h.replace(pn_old, pn_new), encoding="utf-8")
        print(f, "верхняя панель обновлена")
    else:
        print(f, "!! шаблон верхней панели не найден")
