# -*- coding: utf-8 -*-
"""Генератор SVG-схем проекта (единый датчик — радар Acconeer A121)."""
import math, pathlib

OUT = pathlib.Path(__file__).resolve().parent

HEAD = '<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="DejaVu Sans, Arial, sans-serif">\n'
DEFS = '''  <defs>
    <marker id="arw" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L9,3 L0,6 z" fill="#334"/></marker>
    <style>
      .box{fill:#eef4fb;stroke:#2b5f9e;stroke-width:2}
      .box2{fill:#fdf1e6;stroke:#c07a2b;stroke-width:2}
      .box3{fill:#eafaf0;stroke:#2f8f52;stroke-width:2}
      .box4{fill:#fdeaea;stroke:#b33;stroke-width:2}
      .t{font-size:14px;fill:#1a2330;text-anchor:middle;font-weight:bold}
      .ts{font-size:11px;fill:#556;text-anchor:middle}
      .wire{stroke:#334;stroke-width:2;fill:none;marker-end:url(#arw)}
      .title{font-size:21px;font-weight:bold;fill:#12283f;text-anchor:middle}
      .sub{font-size:12.5px;fill:#556;text-anchor:middle}
      .lbl{font-size:11px;fill:#334;text-anchor:middle}
    </style>
  </defs>
'''


def txt(x, y, s, cls='ts', extra=''):
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return f'  <text x="{x}" y="{y}" class="{cls}"{extra}>{s}</text>\n'


def rect(x, y, w, h, cls='box'):
    return f'  <rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>\n'


def path(d, cls='wire', extra=''):
    return f'  <path class="{cls}" d="{d}"{extra}/>\n'


def pol(cx, cy, r, az_deg):
    a = math.radians(az_deg)
    return (cx + r * math.sin(a), cy - r * math.cos(a))


def petal(cx, cy, r, az, fov):
    x1, y1 = pol(cx, cy, r, az - fov / 2)
    x2, y2 = pol(cx, cy, r, az + fov / 2)
    large = 1 if fov > 180 else 0
    return f'M{cx:.1f},{cy:.1f} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large} 1 {x2:.1f},{y2:.1f} Z'


def block_diagram():
    W, H = 1260, 780
    s = HEAD.format(w=W, h=H) + DEFS
    s += txt(630, 34, 'Автономное сигнальное устройство малой высоты БПЛА — структурная схема', 'title')
    s += txt(630, 56, 'Единый тип датчика: 6× радар Acconeer A121 (60 ГГц PCR, SPI) · порог 2…10 м от СУ БПЛА · только сигнальные выходы', 'sub')
    sensors = [('U1 · A121 (вниз)', 'с линзой, узкий луч', 'высота 2…10 м, ≤ 1 мс'),
               ('U2 · A121 (кольцо 0°)', 'широкий FoV, SPI', 'наклон 10°↓ · стены/земля'),
               ('U3 · A121 (кольцо 90°)', 'широкий FoV, SPI', 'наклон 10°↓ · стены/земля'),
               ('U4 · A121 (кольцо 180°)', 'широкий FoV, SPI', 'наклон 10°↓ · стены/земля'),
               ('U5 · A121 (кольцо 270°)', 'широкий FoV, SPI', 'наклон 10°↓ · стены/земля'),
               ('U6 · A121 (вверх)', 'широкий FoV, SPI', 'потолок / препятствия')]
    y0, bh, gap = 88, 70, 11
    for i, (t1, t2, t3) in enumerate(sensors):
        y = y0 + i * (bh + gap)
        s += rect(28, y, 244, bh, 'box3')
        s += txt(150, y + 24, t1, 't')
        s += txt(150, y + 44, t2, 'ts')
        s += txt(150, y + 62, t3, 'ts')
    s += rect(388, y0 + 70, 252, 300, 'box')
    s += txt(514, y0 + 104, 'Микроконтроллер', 't')
    s += txt(514, y0 + 126, 'STM32G474', 't')
    lines = ['SPI-приём сырых данных A121', '6× CS (выбор датчика) + 6× INT', 'фильтр (медиана / Калман)',
             'сравнение с порогом H_ср', 'формирование флага', 'телеметрия в СУ БПЛА',
             'таймаут-контроль (Fail-Safe)', 'приём уставки H_ср по CAN']
    for i, l in enumerate(lines):
        s += txt(514, y0 + 150 + i * 20, l, 'ts')
    s += rect(388, y0 + 392, 252, 78, 'box2')
    s += txt(514, y0 + 422, 'Питание', 't')
    s += txt(514, y0 + 444, 'BEC +5 В → DC-DC +3,3 В', 'ts')
    s += rect(752, y0 + 0, 226, 80, 'box4')
    s += txt(865, y0 + 30, 'Оповещение', 't')
    s += txt(865, y0 + 50, 'зуммер + LED (на борту)', 'ts')
    s += txt(865, y0 + 68, 'пилот слышит / видит', 'ts')
    s += rect(752, y0 + 110, 226, 80, 'box4')
    s += txt(865, y0 + 140, 'Дискретный выход', 't')
    s += txt(865, y0 + 160, '«LOW ALT» (откр. сток /', 'ts')
    s += txt(865, y0 + 178, 'оптопара) — флаг', 'ts')
    s += rect(752, y0 + 250, 226, 80, 'box')
    s += txt(865, y0 + 280, 'CAN-трансивер', 't')
    s += txt(865, y0 + 300, 'TJA1051', 'ts')
    s += txt(865, y0 + 318, 'телеметрия + уставка', 'ts')
    s += rect(1040, y0 + 250, 188, 80, 'box')
    s += txt(1134, y0 + 282, 'СУ БПЛА', 't')
    s += txt(1134, y0 + 302, 'полётный контроллер', 'ts')
    s += txt(1134, y0 + 320, 'пилот / автопилот', 'ts')
    for i in range(6):
        y = y0 + i * (bh + gap) + bh / 2
        ty = y0 + 120 + i * 30
        s += path(f'M272,{y:.0f} C330,{y:.0f} 340,{ty:.0f} 388,{ty:.0f}')
    s += path(f'M514,{y0+392} L514,{y0+370}')
    s += path(f'M640,{y0+40} C700,{y0+40} 700,{y0+40} 752,{y0+40}')
    s += path(f'M640,{y0+150} C700,{y0+150} 700,{y0+150} 752,{y0+150}')
    s += path(f'M640,{y0+290} C700,{y0+290} 700,{y0+290} 752,{y0+290}')
    s += path(f'M978,{y0+150} C1010,{y0+150} 1010,{y0+280} 1040,{y0+280}')
    s += path(f'M978,{y0+290} C1010,{y0+290} 1010,{y0+300} 1040,{y0+300}')
    s += path(f'M1134,{y0+330} C1134,{y0+560} 514,{y0+560} 514,{y0+470}', 'wire', ' stroke-dasharray="6 4"')
    s += txt(630, 700, 'Штриховая линия — питание +5 В от бортовой сети БПЛА (BEC). Сплошные — сигнальные связи (SPI, CAN).', 'lbl')
    s += txt(630, 722, 'Порог H_ср (2…10 м) задаётся из СУ БПЛА по CAN; при потере связи сохраняется последнее значение.', 'lbl')
    s += txt(630, 744, 'Выходы «LOW ALT» и «зуммер/LED» — только сигнальные; исполнительных (инициирующих) цепей нет.', 'lbl')
    s += '</svg>\n'
    (OUT / 'block_diagram.svg').write_text(s, encoding='utf-8')


def schematic():
    W, H = 1300, 960
    s = HEAD.format(w=W, h=H) + DEFS
    s += txt(650, 32, 'Схема электрическая принципиальная (макет, модульная сборка)', 'title')
    s += txt(650, 54, 'Питание 5 В от BEC · MCU STM32G474 · 6× A121 на общем SPI · оповещение и CAN-выход', 'sub')
    s += rect(40, 92, 150, 66, 'box2')
    s += txt(115, 120, 'BEC +5 В', 't')
    s += txt(115, 140, 'бортовая сеть', 'ts')
    s += rect(240, 92, 190, 66, 'box2')
    s += txt(335, 118, 'D24V5F3', 't')
    s += txt(335, 138, '+3,3 В, 500 мА', 'ts')
    s += path('M190,125 L240,125')
    s += rect(40, 196, 150, 60, 'box2')
    s += txt(115, 220, 'TVS + предохр.', 't')
    s += txt(115, 240, 'защита питания', 'ts')
    s += path('M115,158 L115,196')
    s += rect(500, 150, 360, 430, 'box')
    s += txt(680, 184, 'STM32G474 (Nucleo или своя PCB)', 't')
    s += txt(680, 204, 'SPI1 — все A121 · CAN — СУ БПЛА', 'ts')
    pins = [('PA5  SPI1_SCK', 'общий такт SPI'),
            ('PA6  SPI1_MISO', 'данные от A121'),
            ('PA7  SPI1_MOSI', 'данные к A121'),
            ('PA4/PC4..PC8  CS1..CS6', 'выбор датчика (6 линий)'),
            ('PB0..PB5  INT1..INT6', 'готовность данных'),
            ('PA11 CAN_RX / PA12 CAN_TX', 'к TJA1051'),
            ('PB6  GPIO → зуммер', 'через 2N7002'),
            ('PB7  GPIO → LED', 'через R 1 кОм'),
            ('PB8  GPIO → «LOW ALT»', 'откр. сток / оптопара'),
            ('3V3 / GND', 'питание логики')]
    for i, (a, b) in enumerate(pins):
        s += txt(516, 250 + i * 32, a, 'ts', ' text-anchor="start" font-weight="bold"')
        s += txt(844, 250 + i * 32, b, 'ts', ' text-anchor="end"')
    s += rect(40, 320, 330, 250, 'box3')
    s += txt(205, 348, '6× радар Acconeer A121 (модуль XM125)', 't')
    for i in range(6):
        s += txt(205, 372 + i * 30, f'U{i+1}: SCK/MISO/MOSI — общая шина SPI · CS{i+1} — отдельная', 'ts', ' text-anchor="start"')
    s += txt(205, 556, 'Питание +3,3 В, GND · INT — прерывание готовности', 'ts', ' text-anchor="start"')
    s += path('M370,430 C440,430 440,282 500,282')
    s += path('M500,346 C440,346 430,430 370,430')
    s += rect(940, 230, 180, 120, 'box')
    s += txt(1030, 262, 'TJA1051', 't')
    s += txt(1030, 284, 'CAN-трансивер', 'ts')
    s += txt(1030, 304, '120 Ом терминатор', 'ts')
    s += txt(1030, 324, 'CANH / CANL', 'ts')
    s += path('M860,374 L940,300')
    s += path('M860,406 L940,320')
    s += rect(1150, 250, 120, 90, 'box')
    s += txt(1210, 282, 'СУ БПЛА', 't')
    s += txt(1210, 304, 'CAN-шина', 'ts')
    s += txt(1210, 324, 'уставка H_ср', 'ts')
    s += path('M1120,295 L1150,295')
    s += rect(940, 420, 180, 60, 'box4')
    s += txt(1030, 445, 'Зуммер (через Q1)', 't')
    s += txt(1030, 465, 'N-MOSFET + диод', 'ts')
    s += path('M860,470 L940,445')
    s += rect(940, 500, 180, 60, 'box4')
    s += txt(1030, 525, 'LED (через R)', 't')
    s += txt(1030, 545, 'R = 1 кОм', 'ts')
    s += path('M860,502 L940,525')
    s += rect(940, 580, 180, 66, 'box4')
    s += txt(1030, 606, '«LOW ALT»', 't')
    s += txt(1030, 626, 'оптопара / откр. сток', 'ts')
    s += path('M860,534 L940,606')
    s += path('M430,125 L430,560 L500,560')
    s += txt(452, 150, '+3,3 В', 'lbl', ' text-anchor="start"')
    notes = ['Примечания: 1) Макет — готовые модули XM125 + Nucleo, соединённые проводами; своя PCB — на этапе опытного образца.',
             '2) Все A121 работают на общем SPI; выбор датчика — линией CS, готовность — линией INT.',
             '3) Питание A121 — +3,3 В (на модуле XM125 есть свой стабилизатор ядра 1,8 В). Уровни SPI — 3,3 В.',
             '4) «LOW ALT» — только сигнальный выход (флаг/индикация). Никаких инициирующих цепей.',
             '5) SPI до 20…50 МГц — обеспечивает съём сырых данных за десятки микросекунд (см. временную диаграмму).']
    for i, n in enumerate(notes):
        s += txt(120, 760 + i * 24, n, 'lbl', ' text-anchor="start"')
    s += '</svg>\n'
    (OUT / 'schematic.svg').write_text(s, encoding='utf-8')


def mounting():
    W, H = 1240, 920
    s = HEAD.format(w=W, h=H) + DEFS
    s += txt(620, 34, 'Размещение датчиков: обзор 360°', 'title')
    s += txt(620, 56, 'Кольцо 4× A121 (шаг 90°, FoV ~120°, наклон 10°↓) + 1 вверх + 1 вниз = 6 каналов', 'sub')
    cx, cy, R = 300, 400, 230
    cols = ['#2980b9', '#8e44ad', '#e67e22', '#16a085']
    for i in range(4):
        s += f'  <path d="{petal(cx,cy,R,i*90,120)}" fill="{cols[i]}" opacity="0.28"/>\n'
    for i in range(4):
        s += f'  <path d="{petal(cx,cy,R,i*90,120)}" fill="none" stroke="#334" stroke-width="0.8" opacity="0.5"/>\n'
    s += f'  <circle cx="{cx}" cy="{cy}" r="42" fill="#e8f0fe" stroke="#3367d6" stroke-width="2"/>\n'
    s += txt(cx, cy - 2, 'БПЛА', 'ts', ' font-size="11"')
    s += txt(cx, cy + 14, '(центр)', 'ts', ' font-size="9"')
    for i in range(4):
        px, py = pol(cx, cy, 72, i * 90)
        s += f'  <circle cx="{px:.0f}" cy="{py:.0f}" r="8" fill="{cols[i]}" stroke="#1a1a1a" stroke-width="1.2"/>\n'
        lx, ly = pol(cx, cy, 100, i * 90)
        s += txt(lx, ly, f'S{i+1} · {i*90}°', 'ts', ' font-weight="bold" font-size="11"')
    s += txt(300, 672, '4 × 120° = 480° → перекрытие 30° на стык, «мёртвых зон» нет', 'ts')
    s += txt(300, 692, 'FoV ~120° (полусферическая антенна A121 без линзы)', 'ts')
    s += txt(930, 96, 'Вид сбоку — вертикальные каналы', 't', ' font-size="15"')
    s += '  <line x1="650" y1="640" x2="1180" y2="640" stroke="#2e7d32" stroke-width="3"/>\n'
    s += '  <rect x="650" y="640" width="530" height="34" fill="#e8f5e9"/>\n'
    s += txt(915, 662, 'земля / полоса', 'ts', ' fill="#2e7d32"')
    s += '  <line x1="650" y1="170" x2="1180" y2="170" stroke="#5d4037" stroke-width="3"/>\n'
    s += '  <rect x="650" y="136" width="530" height="34" fill="#efebe9"/>\n'
    s += txt(915, 158, 'потолок / верхнее препятствие', 'ts', ' fill="#5d4037"')
    s += '  <rect x="875" y="380" width="90" height="34" rx="8" fill="#e8f0fe" stroke="#3367d6" stroke-width="2"/>\n'
    s += txt(920, 401, 'БПЛА', 'ts', ' font-size="11"')
    for dx in (-1, 1):
        x1 = 920 + dx * 45
        x2 = 920 + dx * 250
        y2 = 400 + 250 * math.tan(math.radians(10))
        s += f'  <line x1="{x1}" y1="397" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#2980b9" stroke-width="2"/>\n'
        s += f'  <path d="M{x1},397 L{x2:.0f},{y2-38:.0f} L{x2:.0f},{y2+34:.0f} Z" fill="#2980b9" opacity="0.18"/>\n'
    s += txt(920, 470, 'кольцо: наклон 10°↓ (видит стены и землю впереди)', 'ts', ' fill="#1a3a6b"')
    s += '  <line x1="920" y1="380" x2="920" y2="180" stroke="#7fd0ff" stroke-width="2.2" stroke-dasharray="6 4"/>\n'
    s += '  <path d="M920,180 L888,250 L952,250 Z" fill="#7fd0ff" opacity="0.35"/>\n'
    s += txt(985, 210, 'U6 — A121 вверх (потолок)', 'ts', ' fill="#0b6b9c"')
    s += '  <line x1="920" y1="414" x2="920" y2="632" stroke="#37d67a" stroke-width="2.2" stroke-dasharray="6 4"/>\n'
    s += '  <path d="M920,632 L888,566 L952,566 Z" fill="#37d67a" opacity="0.35"/>\n'
    s += txt(985, 596, 'U1 — A121 вниз (высота, ≤ 1 мс)', 'ts', ' fill="#1a7a44"')
    s += '  <line x1="1180" y1="414" x2="1180" y2="632" stroke="#666" stroke-width="0.8"/>\n'
    s += txt(1150, 528, 'H = 2…10 м', 'ts', ' fill="#333"')
    s += '  <rect x="60" y="730" width="1120" height="160" rx="10" fill="#f7f9fc" stroke="#d0d7e2"/>\n'
    s += txt(80, 758, 'Почему именно так', 't', ' text-anchor="start" font-size="14"')
    notes = ['• 4 датчика в кольце: при FoV ~120° шаг 90° < 120° → сплошное покрытие с перекрытием 30°.',
             '• Наклон 10° вниз: одновременно видит и землю впереди при снижении, и стены на высоте полёта.',
             '• Ноль азимута = нос БПЛА: сектор S1 всегда смотрит вперёд, независимо от эволюций.',
             '• Выносные кронштейны: винты и корпус не затеняют обзор кольца.',
             '• Один тип датчика (A121) на все каналы: единая прошивка, единая ЭКБ, взаимозаменяемость.']
    for i, n in enumerate(notes):
        s += txt(80, 786 + i * 24, n, 'lbl', ' text-anchor="start" font-size="12"')
    s += '</svg>\n'
    (OUT / 'sensor_mounting.svg').write_text(s, encoding='utf-8')


def coverage():
    W, H = 1240, 900
    s = HEAD.format(w=W, h=H) + DEFS
    s += txt(620, 34, 'Покрытие 360°: земля, стены, потолок', 'title')
    s += txt(620, 56, '6× радар Acconeer A121 (60 ГГц PCR) — единый тип датчика на все направления', 'sub')
    s += txt(300, 96, 'Вид сверху (горизонтальный обзор)', 't', ' font-size="15"')
    cx, cy, R = 300, 380, 240
    cols = ['#27ae60', '#2980b9', '#8e44ad', '#e67e22']
    for i in range(4):
        s += f'  <path d="{petal(cx,cy,R,i*90,120)}" fill="{cols[i]}" opacity="0.35"/>\n'
    s += f'  <circle cx="{cx}" cy="{cy}" r="36" fill="#e8f0fe" stroke="#3367d6" stroke-width="2"/>\n'
    s += txt(cx, cy - 2, 'БПЛА', 'ts', ' font-size="10"')
    s += txt(cx, cy + 14, '+ 6 датчиков', 'ts', ' font-size="9"')
    for i in range(4):
        px, py = pol(cx, cy, 86, i * 90)
        s += txt(px, py, f'№{i+1}', 'ts', ' font-weight="bold" font-size="12"')
    s += f'  <circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#333" stroke-width="1" stroke-dasharray="6 4"/>\n'
    s += txt(300, 150, 'дальность до стен — до 12 м (A121)', 'ts')
    s += txt(300, 676, '4 × 120° = 480° → перекрытие 30°, «мёртвых зон» нет', 'ts')
    s += txt(300, 696, 'Масса кольца ≈ 12 г · цена ≈ 4× (при серии — чип A121)', 'ts')
    s += txt(900, 96, 'Вид сбоку (вертикальный обзор)', 't', ' font-size="15"')
    s += '  <line x1="680" y1="140" x2="1130" y2="140" stroke="#8a1c10" stroke-width="3"/>\n'
    s += txt(905, 130, 'потолок', 'ts', ' fill="#8a1c10"')
    s += '  <line x1="680" y1="140" x2="680" y2="620" stroke="#8a5000" stroke-width="3"/>\n'
    s += txt(720, 180, 'стена', 'ts', ' fill="#8a5000" text-anchor="start"')
    s += '  <line x1="680" y1="620" x2="1130" y2="620" stroke="#1a5b2b" stroke-width="3"/>\n'
    s += txt(905, 645, 'земля / пол', 'ts', ' fill="#1a5b2b"')
    s += '  <rect x="875" y="362" width="60" height="30" rx="6" fill="#e8f0fe" stroke="#3367d6" stroke-width="2"/>\n'
    s += txt(905, 382, 'БПЛА', 'ts', ' font-size="11"')
    s += '  <path d="M905,362 L858,150 L952,150 Z" fill="#c0392b" opacity="0.3"/>\n'
    s += txt(1000, 250, 'вверх (потолок)', 'ts', ' fill="#8a1c10" text-anchor="start"')
    s += txt(1000, 268, 'A121, до 12 м', 'ts', ' fill="#666" text-anchor="start"')
    s += '  <path d="M905,392 L850,610 L960,610 Z" fill="#1a5b2b" opacity="0.25"/>\n'
    s += txt(1000, 520, 'вниз (высота)', 'ts', ' fill="#1a5b2b" text-anchor="start"')
    s += txt(1000, 538, 'A121, 2…10 м', 'ts', ' fill="#666" text-anchor="start"')
    s += txt(1000, 556, 'реакция ≤ 1 мс', 'ts', ' fill="#8a1c10" text-anchor="start"')
    s += '  <line x1="875" y1="377" x2="695" y2="377" stroke="#8a5000" stroke-width="2" marker-end="url(#arw)"/>\n'
    s += txt(780, 412, 'в стороны (стены)', 'ts', ' fill="#8a5000"')
    s += txt(780, 430, 'кольцо A121, до 12 м', 'ts', ' fill="#666"')
    s += '  <line x1="1040" y1="377" x2="1040" y2="620" stroke="#333" stroke-width="1" stroke-dasharray="4 3"/>\n'
    s += txt(1055, 500, 'H = 2…10 м', 'ts', ' fill="#333" text-anchor="start"')
    s += '  <rect x="60" y="730" width="1120" height="140" rx="10" fill="#f7f7f7" stroke="#ddd"/>\n'
    s += txt(80, 758, 'Состав датчиков:', 't', ' text-anchor="start" font-size="13"')
    leg = [('#2980b9', '4× A121 — горизонт 360° (стены/земля), FoV ~120°, до 12 м, наклон 10°↓'),
           ('#c0392b', '1× A121 — вверх (потолок), до 12 м'),
           ('#1a5b2b', '1× A121 — вниз (высота 2…10 м), реакция ≤ 1 мс, всепогодный')]
    for i, (c, t) in enumerate(leg):
        s += f'  <rect x="80" y="{770+i*24}" width="14" height="14" fill="{c}"/>\n'
        s += txt(100, 782 + i * 24, t, 'lbl', ' text-anchor="start"')
    s += txt(80, 846, '⚠️ Все каналы — на одном типе датчика A121; масса изделия 84 г, серийная себестоимость ≈ 13 700 ₽ (в пределах ТЗ).', 'lbl', ' text-anchor="start" font-size="11" fill="#8a1c10"')
    s += '</svg>\n'
    (OUT / 'coverage_360.svg').write_text(s, encoding='utf-8')


def timing():
    W, H = 1240, 720
    s = HEAD.format(w=W, h=H) + DEFS
    s += f'  <rect width="{W}" height="{H}" fill="#ffffff"/>\n'
    s += txt(620, 34, 'Временная диаграмма реакции (радар A121, SPI)', 'title')
    s += txt(620, 58, 'От пересечения порога H_ср до срабатывания сигнала — не более 1 мс', 'sub')
    s += '  <line x1="120" y1="600" x2="1160" y2="600" stroke="#333" stroke-width="2"/>\n'
    s += '  <polygon points="1160,600 1148,595 1148,605" fill="#333"/>\n'
    s += txt(1166, 605, 't', 'lbl', ' text-anchor="start"')
    marks = [(240, 't₀', 'высота < H_ср'), (520, 't₁', 'кадр готов (HSM)'),
             (700, 't₂', 'SPI-кадр принят'), (850, 't₃', 'порог сравнён'), (1000, 't₄', 'выход активен')]
    for x, lab, sub in marks:
        s += f'  <line x1="{x}" y1="96" x2="{x}" y2="600" stroke="#888" stroke-width="1" stroke-dasharray="4 4"/>\n'
        s += txt(x, 640, lab, 'lbl', ' font-size="13" font-weight="bold"')
        s += txt(x, 658, sub, 'lbl', ' font-size="10" fill="#666"')
    s += txt(70, 120, 'Высота h(t)', 'lbl', ' text-anchor="start" font-size="12" font-weight="bold"')
    s += '  <line x1="120" y1="220" x2="1160" y2="220" stroke="#e0a800" stroke-width="1.5" stroke-dasharray="6 4"/>\n'
    s += txt(1166, 224, 'H_ср', 'lbl', ' text-anchor="start" font-size="10" fill="#8a6100"')
    s += '  <path d="M120,110 C320,120 420,180 540,220 C680,262 820,300 1160,344" fill="none" stroke="#3367d6" stroke-width="2.5"/>\n'
    s += '  <circle cx="540" cy="220" r="5" fill="#c0392b"/>\n'
    s += txt(70, 300, 'Кадры A121', 'lbl', ' text-anchor="start" font-size="12" font-weight="bold"')
    s += '  <line x1="120" y1="340" x2="1160" y2="340" stroke="#ddd"/>\n'
    for i in range(10):
        x = 170 + i * 100
        s += f'  <rect x="{x}" y="322" width="18" height="18" fill="#27ae60"/>\n'
    s += txt(250, 362, 'период кадров T_обн ≈ 0,2…0,5 мс (режим HSM)', 'lbl', ' text-anchor="start" font-size="10" fill="#666"')
    s += txt(70, 420, 'Обработка MCU', 'lbl', ' text-anchor="start" font-size="12" font-weight="bold"')
    s += '  <line x1="120" y1="460" x2="1160" y2="460" stroke="#ddd"/>\n'
    s += '  <rect x="700" y="442" width="150" height="18" fill="#9b59b6" opacity="0.7"/>\n'
    s += txt(775, 455, 'разбор+фильтр+сравнение (~20 мкс)', 'lbl', ' font-size="10" fill="#fff"')
    s += txt(70, 520, 'Флаг / выход', 'lbl', ' text-anchor="start" font-size="12" font-weight="bold"')
    s += '  <line x1="120" y1="560" x2="1160" y2="560" stroke="#ddd"/>\n'
    s += '  <path d="M120,560 L1000,560 L1000,530 L1160,530" fill="none" stroke="#c0392b" stroke-width="2.5"/>\n'
    s += txt(1050, 548, 'LOW ALT = 1', 'lbl', ' text-anchor="start" font-size="11" fill="#8a1c10"')
    s += '  <circle cx="1000" cy="560" r="4" fill="#c0392b"/>\n'
    s += '  <line x1="240" y1="196" x2="1000" y2="196" stroke="#666" stroke-width="1"/>\n'
    s += '  <line x1="240" y1="191" x2="240" y2="201" stroke="#666"/>\n'
    s += '  <line x1="1000" y1="191" x2="1000" y2="201" stroke="#666"/>\n'
    s += txt(620, 188, 'T_реакции = t₄ − t₀ ≤ 1 мс', 'lbl', ' font-size="12" fill="#666"')
    s += '  <rect x="60" y="670" width="1120" height="34" rx="6" fill="#f7f7f7" stroke="#ddd"/>\n'
    s += txt(80, 692, 'Составляющие: кадр A121 (~0,2…0,5 мс, HSM) + SPI-передача (~30…100 мкс) + обработка (~20 мкс) + выдача (~5 мкс).', 'lbl', ' text-anchor="start" font-size="11"')
    s += '</svg>\n'
    (OUT / 'timing_diagram.svg').write_text(s, encoding='utf-8')


PCB_STYLE = '''  <style>
    .pcb{fill:#0e5230;stroke:#062615;stroke-width:2}
    .keep{fill:#0a3d1f;stroke:#7fd0ff;stroke-width:1.2;stroke-dasharray:5 4}
    .pad{fill:#e8c65a;stroke:#8a6508;stroke-width:0.8}
    .comp{fill:#1a2330;stroke:#cfd8e6;stroke-width:1}
    .tr{stroke:#d4af37;stroke-width:1.8;fill:none;stroke-linecap:round;stroke-linejoin:round}
    .tr2{stroke:#e06666;stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}
    .trp{stroke:#f2e2a8;stroke-width:4.5;fill:none;stroke-linecap:round;opacity:0.85}
    .via{fill:#e8c65a;stroke:#8a6508;stroke-width:0.6}
    .sil{font-size:8.5px;fill:#ffffff;text-anchor:middle;font-weight:bold}
    .sil2{font-size:7.5px;fill:#cfeeff;text-anchor:middle}
    .pt{font-size:15px;font-weight:bold;fill:#12283f;text-anchor:middle}
    .rule{font-size:11.5px;fill:#22303f;text-anchor:start}
    .ruleh{font-size:12.5px;fill:#12283f;text-anchor:start;font-weight:bold}
  </style>
'''


def pcb_layout():
    W, H = 1240, 1010
    s = HEAD.format(w=W, h=H) + DEFS + PCB_STYLE
    s += f'  <rect width="{W}" height="{H}" fill="#ffffff"/>\n'
    s += txt(620, 34, 'Печатная плата: размещение элементов и трассировка', 'title')
    s += txt(620, 56, 'Плата-носитель 64×48 мм, 4 слоя · плата датчика 26×26 мм, 2 слоя · учёт зон запрета (keepout) под антеннами 60 ГГц', 'sub')

    S = 6.4
    BW, BH = 64, 48

    def X(ox, x): return ox + x * S
    def Y(oy, y): return oy + y * S

    # ---------- Панель A: размещение ----------
    ox, oy = 60, 132
    s += txt(X(ox, BW / 2), oy - 22, 'A. Плата-носитель — размещение (вид сверху)', 'pt')
    s += f'  <rect class="pcb" x="{ox}" y="{oy}" width="{BW*S:.0f}" height="{BH*S:.0f}" rx="6"/>\n'
    for mx, my in [(4, 4), (60, 4), (4, 44), (60, 44)]:
        s += f'  <circle cx="{X(ox,mx):.0f}" cy="{Y(oy,my):.0f}" r="6" fill="#0a3d1f" stroke="#cfe0ff" stroke-width="1"/>\n'
    s += txt(X(ox, 4), Y(oy, 4) - 10, 'M2.5', 'sil2')
    # зона запрета под антенной нижнего радара (U1)
    s += f'  <rect class="keep" x="{X(ox,19.5):.0f}" y="{Y(oy,11.5):.0f}" width="{25*S:.0f}" height="{25*S:.0f}" rx="3"/>\n'
    s += txt(X(ox, 32), Y(oy, 13.5), 'keepout: без меди под антенной', 'sil2')
    comps = [
        (19.5, 11.5, 25, 25, 'comp', 'U1 · XM125 (вниз)'),
        (4.5, 33.5, 10, 10, 'comp', 'U8 STM32G474'),
        (4.5, 44.0, 6, 2.5, 'comp', 'Y1 8 МГц'),
        (46.0, 33.0, 13, 9, 'comp', 'PS1 D24V5F3'),
        (46.0, 29.5, 4, 2.5, 'comp', 'F1'),
        (52.5, 29.5, 4, 2.5, 'comp', 'D2 TVS'),
        (52.0, 8.0, 7, 6, 'comp', 'U9 TJA1051'),
        (60.5, 17.0, 3, 6, 'comp', 'J1'),
        (60.5, 27.0, 3, 5, 'comp', 'J2'),
        (17.0, 0.8, 6, 2.6, 'comp', 'J3 FFC'),
        (57.5, 1.2, 5, 2.6, 'comp', 'J4 FFC'),
        (17.0, 44.6, 6, 2.6, 'comp', 'J5 FFC'),
        (0.8, 20.0, 2.6, 6, 'comp', 'J6 FFC'),
        (30.0, 6.5, 6, 2.6, 'comp', 'J7 FFC'),
        (10.0, 40.5, 3.5, 3.5, 'comp', 'Q1'),
        (16.5, 40.0, 5, 5, 'comp', 'LS1'),
        (24.0, 41.0, 3, 3, 'comp', 'HL1'),
        (44.0, 2.0, 5, 5, 'comp', 'TP'),
    ]
    for cx, cy, w, h, cls, lab in comps:
        s += f'  <rect class="{cls}" x="{X(ox,cx):.0f}" y="{Y(oy,cy):.0f}" width="{w*S:.0f}" height="{h*S:.0f}" rx="2"/>\n'
        s += txt(X(ox, cx + w / 2), Y(oy, cy + h / 2) + 3, lab, 'sil')
    s += txt(X(ox, BW / 2), oy + BH * S + 20, 'J1/J2 — JST-GH (питание+CAN, «LOW ALT») · J3…J6 — FFC кольцевых радаров · J7 — FFC радара «вверх»', 'sil2', ' font-size="9" fill="#556"')

    # ---------- Панель B: трассировка ----------
    ox2, oy2 = 660, 132
    s += txt(X(ox2, BW / 2), oy2 - 22, 'B. Плата-носитель — трассировка (верхний слой)', 'pt')
    s += f'  <rect class="pcb" x="{ox2}" y="{oy2}" width="{BW*S:.0f}" height="{BH*S:.0f}" rx="6"/>\n'

    def p(d, cls='tr'):
        return f'  <path class="{cls}" d="{d}"/>\n'

    def px(x, y):
        return f'{X(ox2,x):.1f},{Y(oy2,y):.1f}'

    # корпус модуля U1 и зона запрета (keepout) под антенной
    s += f'  <rect class="comp" x="{X(ox2,19.5):.0f}" y="{Y(oy2,11.5):.0f}" width="{25*S:.0f}" height="{25*S:.0f}" rx="2"/>\n'
    s += f'  <rect class="keep" x="{X(ox2,20.5):.0f}" y="{Y(oy2,12.5):.0f}" width="{23*S:.0f}" height="{23*S:.0f}" rx="2"/>\n'
    s += txt(X(ox2, 32), Y(oy2, 24), 'U1 XM125', 'sil')
    s += txt(X(ox2, 32), Y(oy2, 26.5), 'keepout под антенной', 'sil2')
    # контактные площадки по нижнему краю модуля (подход только снизу)
    pads = [22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42]
    for k, mx in enumerate(pads):
        s += f'  <rect class="pad" x="{X(ox2,mx)-3:.0f}" y="{Y(oy2,36.5)-3:.0f}" width="6" height="6" rx="1"/>\n'
    # выводы MCU (правая сторона)
    for k in range(3):
        s += f'  <rect class="pad" x="{X(ox2,14.5)-2:.0f}" y="{Y(oy2,33+k)-2:.0f}" width="5" height="5" rx="1"/>\n'

    # SPI: SCK/MOSI/MISO — от MCU вниз, затем вправо к площадкам (обход keepout снизу)
    for k, (dy, mx) in enumerate([(0, 22), (1, 24), (2, 26)]):
        s += p(f'M{px(14.5,33+dy)} L{px(18,33+dy)} L{px(18,38+dy)} L{px(mx,38+dy)} L{px(mx,36.5)}')
    # питание +3,3 В (широкая линия): PS1 -> площадки U1 и MCU
    s += p(f'M{px(46,36)} L{px(30,40)} L{px(30,36.5)}', 'trp')
    s += p(f'M{px(30,40)} L{px(14.5,40)}', 'trp')
    # CAN-дифференциальная пара U9 -> J1
    s += p(f'M{px(55.5,10)} L{px(60.5,14)}', 'tr2')
    s += p(f'M{px(55.5,12)} L{px(60.5,19)}', 'tr2')
    # линия зуммера: MCU -> Q1 -> LS1
    s += p(f'M{px(14.5,42)} L{px(11.75,42)}')
    s += p(f'M{px(13.5,42)} L{px(16.5,42)}')
    # переходные отверстия на слой земли
    for vx, vy in [(18, 38), (18, 39), (30, 40), (14.5, 40)]:
        s += f'  <circle class="via" cx="{X(ox2,vx):.0f}" cy="{Y(oy2,vy):.0f}" r="2.4"/>\n'
    s += txt(X(ox2, BW / 2), oy2 + BH * S + 20, 'жёлтый — сигнальные линии · бежевый (широкий) — питание +3,3 В · красный — диффпара CAN · площадки — краевые выводы модуля', 'sil2', ' font-size="9" fill="#556"')

    # ---------- Панель C: плата датчика ----------
    ox3, oy3 = 60, 600
    s += txt(X(ox3, 13), oy3 - 22, 'C. Плата датчика 26×26 мм (2 слоя)', 'pt')
    s += f'  <rect class="pcb" x="{ox3}" y="{oy3}" width="{26*S:.0f}" height="{26*S:.0f}" rx="5"/>\n'
    s += f'  <rect class="keep" x="{X(ox3,3):.0f}" y="{Y(oy3,3):.0f}" width="{20*S:.0f}" height="{20*S:.0f}" rx="3"/>\n'
    s += txt(X(ox3, 13), Y(oy3, 6.5), 'keepout 20×20 (без меди)', 'sil2')
    s += f'  <rect class="comp" x="{X(ox3,4):.0f}" y="{Y(oy3,4):.0f}" width="{18*S:.0f}" height="{18*S:.0f}" rx="2"/>\n'
    s += txt(X(ox3, 13), Y(oy3, 13), 'XM125 (A121)', 'sil')
    s += txt(X(ox3, 13), Y(oy3, 15.5), 'антенна 60 ГГц', 'sil2')
    s += f'  <rect class="comp" x="{X(ox3,9):.0f}" y="{Y(oy3,22.5):.0f}" width="{8*S:.0f}" height="{3*S:.0f}" rx="2"/>\n'
    s += txt(X(ox3, 13), Y(oy3, 24.6), 'J8 FFC 8-pin', 'sil')
    for i, dy in enumerate((0.0, 1.2, 2.4)):
        s += p(f'M{X(ox3,10+i*2):.1f},{Y(oy3,18):.1f} L{X(ox3,10+i*2):.1f},{Y(oy3,22.5):.1f}')
    for mx, my in [(2, 2), (24, 2), (2, 24), (24, 24)]:
        s += f'  <circle cx="{X(ox3,mx):.0f}" cy="{Y(oy3,my):.0f}" r="4" fill="#0a3d1f" stroke="#cfe0ff" stroke-width="0.8"/>\n'

    # ---------- Таблица правил ----------
    tx, ty = 300, 600
    rules = [
        'Стек: 4 слоя — L1 сигналы, L2 сплошная земля (GND), L3 питание (+3,3 В / +5 В), L4 сигналы/земля. FR-4, 1,6 мм, εr ≈ 4,3.',
        'Ширина проводников: сигнал 0,2 мм · питание 0,5…1,0 мм (по току) · CAN — 0,25 мм с зазором 0,25 мм.',
        'CAN (ISO 11898): диффпара 120 Ом, длина шлейфа < 10 мм, терминатор 120 Ом у разъёма J1.',
        'SPI (до 20…50 МГц): длина линий ≤ 50 мм, согласование длин SCK/MOSI/MISO ±5 мм, без разрывов опорного слоя.',
        'Зоны запрета: под антеннами 60 ГГц (U1 и все XM125) — без меди и без металла; зазор ≥ 5 мм по краю.',
        'Переходные отверстия: Ø 0,3/0,6 мм; для питания и земли — по 2…3 шт. рядом с выводами (снижение индуктивности).',
        'Питание: TVS SMBJ5.0A и предохранитель F1 — у входа J1; керамика 100 нФ + 10 мкФ у каждого модуля XM125 и MCU.',
        'ЭМС: экран (заливка GND) между цифровыми и радиочастотными цепями; линию зуммера — в стороне от антенн.',
        'Механика: 4 отверстия M2.5, крепёж с фиксацией резьбы; заливка компаундом для стойкости к 10g / 3g.',
        'Габарит: плата-носитель 64×48 мм (4 слоя) + 6× плата датчика 26×26 мм (2 слоя) на кронштейнах.',
    ]
    s += f'  <rect x="{tx-14}" y="{ty-30}" width="900" height="{len(rules)*26+62}" rx="10" fill="#f7f9fc" stroke="#d0d7e2"/>\n'
    s += txt(tx, ty - 6, 'Правила проектирования и трассировки', 'ruleh')
    for i, r in enumerate(rules):
        s += txt(tx, ty + 22 + i * 26, '• ' + r, 'rule')
    s += txt(tx, ty + 22 + len(rules) * 26 + 4, 'Итог: трассировка обеспечивает SPI-опрос 6 датчиков и CAN-связь с СУ БПЛА; зоны под антеннами свободны от меди.', 'rule')
    s += '</svg>\n'
    (OUT / 'pcb_layout.svg').write_text(s, encoding='utf-8')


if __name__ == '__main__':
    for f in (block_diagram, schematic, mounting, coverage, timing, pcb_layout):
        f()
        print('ok:', f.__name__)
