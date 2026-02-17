from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .models import JobApplication


@dataclass(slots=True)
class FunnelMetrics:
    """Aggregate KPIs used by the stats command."""
    total: int
    interviews: int
    offers: int
    rejected: int
    response_rate: float
    offer_rate: float
    avg_days_to_update: float


def _days_between(start: str, end: str) -> int:
    # Guard against bad ordering so metrics never go negative.
    s = datetime.strptime(start, "%Y-%m-%d")
    e = datetime.strptime(end, "%Y-%m-%d")
    return max((e - s).days, 0)


def build_funnel_metrics(applications: Iterable[JobApplication]) -> FunnelMetrics:
    """Compute top-of-funnel and conversion metrics from application records."""
    apps = list(applications)
    total = len(apps)
    # Any app that reached phone screen/interview/offer is treated as an interview-stage response.
    interviews = sum(1 for a in apps if a.status in {"phone_screen", "interview", "offer"})
    offers = sum(1 for a in apps if a.status == "offer")
    rejected = sum(1 for a in apps if a.status == "rejected")

    touched = [a for a in apps if a.last_updated and a.applied_date]
    avg_days = 0.0
    if touched:
        # Average time from application date to most recent status update.
        avg_days = sum(_days_between(a.applied_date, a.last_updated) for a in touched) / len(touched)

    response_rate = (interviews + rejected + offers) / total if total else 0.0
    offer_rate = offers / total if total else 0.0

    return FunnelMetrics(
        total=total,
        interviews=interviews,
        offers=offers,
        rejected=rejected,
        response_rate=round(response_rate, 3),
        offer_rate=round(offer_rate, 3),
        avg_days_to_update=round(avg_days, 2),
    )
