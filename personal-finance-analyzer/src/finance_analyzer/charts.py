from __future__ import annotations

from pathlib import Path


def _svg_header(width: int, height: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
    )


def write_spending_trend_svg(path: str | Path, monthly_expenses: list[tuple[str, float]]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)

    width, height = 900, 360
    pad_left, pad_right, pad_top, pad_bottom = 60, 20, 20, 60
    chart_w = width - pad_left - pad_right
    chart_h = height - pad_top - pad_bottom

    if not monthly_expenses:
        content = _svg_header(width, height) + "<text x='20' y='40'>No data</text></svg>"
        out.write_text(content, encoding="utf-8")
        return

    values = [value for _, value in monthly_expenses]
    max_v = max(values) or 1.0

    points: list[tuple[float, float]] = []
    for i, (_, value) in enumerate(monthly_expenses):
        x = pad_left + (i / max(len(monthly_expenses) - 1, 1)) * chart_w
        y = pad_top + chart_h - (value / max_v) * chart_h
        points.append((x, y))

    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)

    labels = []
    for i, (month, _) in enumerate(monthly_expenses):
        x = pad_left + (i / max(len(monthly_expenses) - 1, 1)) * chart_w
        labels.append(f"<text x='{x:.1f}' y='{height - 20}' font-size='11' text-anchor='middle'>{month}</text>")

    circles = "".join(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='4' fill='#0b7285'/>" for x, y in points)

    svg = [
        _svg_header(width, height),
        "<rect x='0' y='0' width='100%' height='100%' fill='#f8f9fa'/>",
        f"<line x1='{pad_left}' y1='{pad_top + chart_h}' x2='{pad_left + chart_w}' y2='{pad_top + chart_h}' stroke='#adb5bd'/>",
        f"<line x1='{pad_left}' y1='{pad_top}' x2='{pad_left}' y2='{pad_top + chart_h}' stroke='#adb5bd'/>",
        f"<polyline points='{polyline}' fill='none' stroke='#0b7285' stroke-width='3'/>",
        circles,
        "".join(labels),
        "<text x='20' y='20' font-size='14' font-weight='bold'>Monthly Spending Trend</text>",
        "</svg>",
    ]
    out.write_text("".join(svg), encoding="utf-8")


def write_category_bar_svg(path: str | Path, category_spending: dict[str, float], title: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)

    width, height = 900, 420
    pad_left, pad_right, pad_top, pad_bottom = 60, 20, 30, 80
    chart_w = width - pad_left - pad_right
    chart_h = height - pad_top - pad_bottom

    items = sorted(category_spending.items(), key=lambda kv: kv[1], reverse=True)

    if not items:
        content = _svg_header(width, height) + "<text x='20' y='40'>No data</text></svg>"
        out.write_text(content, encoding="utf-8")
        return

    max_v = max(value for _, value in items) or 1.0
    bar_w = chart_w / max(len(items), 1)

    bars: list[str] = []
    labels: list[str] = []

    for i, (category, spend) in enumerate(items):
        x = pad_left + i * bar_w + 8
        bar_height = (spend / max_v) * chart_h
        y = pad_top + chart_h - bar_height
        bars.append(
            f"<rect x='{x:.1f}' y='{y:.1f}' width='{max(bar_w - 16, 10):.1f}' height='{bar_height:.1f}' fill='#1971c2'/>"
        )
        labels.append(
            f"<text x='{(x + bar_w / 2):.1f}' y='{height - 40}' font-size='11' text-anchor='middle'>{category}</text>"
        )

    svg = [
        _svg_header(width, height),
        "<rect x='0' y='0' width='100%' height='100%' fill='#f8f9fa'/>",
        f"<line x1='{pad_left}' y1='{pad_top + chart_h}' x2='{pad_left + chart_w}' y2='{pad_top + chart_h}' stroke='#adb5bd'/>",
        "".join(bars),
        "".join(labels),
        f"<text x='20' y='20' font-size='14' font-weight='bold'>{title}</text>",
        "</svg>",
    ]

    out.write_text("".join(svg), encoding="utf-8")
