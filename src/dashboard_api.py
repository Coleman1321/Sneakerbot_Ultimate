"""Dashboard API backend for SneakerBot Ultimate."""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from src.supabase_client import get_supabase_manager
from src.analytics import get_analytics

logger = logging.getLogger(__name__)


class DashboardAPI:
    """Provides API endpoints for the dashboard."""

    def __init__(self):
        """Initialize dashboard API."""
        self.db = get_supabase_manager()
        self.analytics = get_analytics()

    def get_overview(self) -> Dict[str, Any]:
        """Get dashboard overview."""
        try:
            platforms = ["Nike", "Adidas", "Shopify", "Supreme", "Footsites"]

            overview = {
                "timestamp": datetime.utcnow().isoformat(),
                "platforms": {},
                "total_metrics": {
                    "total_runs_today": 0,
                    "success_rate_today": 0,
                    "total_accounts": 0,
                },
            }

            for platform in platforms:
                metrics = self.db.get_platform_metrics(platform, days=1)
                overview["platforms"][platform] = {
                    "total_attempts": metrics.get("total_attempts", 0),
                    "successful": metrics.get("successful_attempts", 0),
                    "success_rate": f"{metrics.get('success_rate', 0):.2f}%",
                    "captcha_solve_rate": f"{self.db.get_captcha_success_rate(platform, days=1):.2f}%",
                }
                overview["total_metrics"]["total_runs_today"] += metrics.get("total_attempts", 0)

            return overview
        except Exception as e:
            logger.error(f"Error getting overview: {e}")
            return {}

    def get_platform_stats(self, platform: str, days: int = 7) -> Dict[str, Any]:
        """Get detailed stats for a platform."""
        try:
            metrics = self.db.get_platform_metrics(platform, days)
            captcha_rate = self.db.get_captcha_success_rate(platform, days)

            return {
                "platform": platform,
                "period_days": days,
                "total_attempts": metrics.get("total_attempts", 0),
                "successful_attempts": metrics.get("successful_attempts", 0),
                "failed_attempts": metrics.get("failed_attempts", 0),
                "success_rate": f"{metrics.get('success_rate', 0):.2f}%",
                "average_duration_ms": metrics.get("average_duration_ms", 0),
                "captcha_success_rate": f"{captcha_rate:.2f}%",
                "detection_rate": f"{metrics.get('detection_rate', 0):.2f}%",
            }
        except Exception as e:
            logger.error(f"Error getting platform stats: {e}")
            return {}

    def get_bot_type_stats(self, platform: str, bot_type: str, days: int = 7) -> Dict[str, Any]:
        """Get stats for specific bot type."""
        try:
            stats = self.db.get_bot_run_stats(platform, bot_type, days)
            return {
                **stats,
                "success_rate": f"{stats.get('success_rate', 0):.2f}%",
                "average_duration_seconds": f"{stats.get('average_duration_ms', 0) / 1000:.2f}",
            }
        except Exception as e:
            logger.error(f"Error getting bot type stats: {e}")
            return {}

    def get_account_stats(self, platform: Optional[str] = None) -> Dict[str, Any]:
        """Get account statistics."""
        try:
            stats = {
                "timestamp": datetime.utcnow().isoformat(),
                "platform_breakdown": {},
            }

            platforms = [platform] if platform else ["Nike", "Adidas", "Shopify", "Supreme", "Footsites"]

            for p in platforms:
                accounts = self.db.client.table("accounts").select("*").eq("platform", p).execute().data or []
                active_accounts = [a for a in accounts if a.get("status") == "active"]

                if active_accounts:
                    avg_success = sum(a.get("success_count", 0) for a in active_accounts) / len(active_accounts)
                    avg_failure = sum(a.get("failure_count", 0) for a in active_accounts) / len(active_accounts)

                    stats["platform_breakdown"][p] = {
                        "total_accounts": len(accounts),
                        "active_accounts": len(active_accounts),
                        "average_success_per_account": f"{avg_success:.2f}",
                        "average_failures_per_account": f"{avg_failure:.2f}",
                    }

            return stats
        except Exception as e:
            logger.error(f"Error getting account stats: {e}")
            return {}

    def get_captcha_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get CAPTCHA analytics."""
        try:
            platforms = ["Nike", "Adidas", "Shopify", "Supreme", "Footsites"]

            analytics = {
                "timestamp": datetime.utcnow().isoformat(),
                "period_days": days,
                "platform_breakdown": {},
            }

            for platform in platforms:
                rate = self.db.get_captcha_success_rate(platform, days)
                analytics["platform_breakdown"][platform] = {
                    "solve_success_rate": f"{rate:.2f}%",
                    "estimated_cost": f"${(100 - rate) * 0.01:.2f} per 100 attempts" if rate < 100 else "No failures",
                }

            return analytics
        except Exception as e:
            logger.error(f"Error getting CAPTCHA analytics: {e}")
            return {}

    def get_proxy_stats(self) -> Dict[str, Any]:
        """Get proxy performance statistics."""
        try:
            proxies_data = self.db.client.table("proxy_performance").select("*").execute().data or []

            if not proxies_data:
                return {
                    "timestamp": datetime.utcnow().isoformat(),
                    "total_proxies": 0,
                    "working_proxies": 0,
                    "success_rate": 0,
                }

            working = sum(1 for p in proxies_data if p.get("success_count", 0) > p.get("failure_count", 0))
            total_success = sum(p.get("success_count", 0) for p in proxies_data)
            total_attempts = total_success + sum(p.get("failure_count", 0) for p in proxies_data)

            return {
                "timestamp": datetime.utcnow().isoformat(),
                "total_proxies": len(proxies_data),
                "working_proxies": working,
                "success_rate": f"{(total_success / total_attempts * 100) if total_attempts > 0 else 0:.2f}%",
                "detection_rate": f"{(sum(p.get('detection_count', 0) for p in proxies_data) / len(proxies_data) if proxies_data else 0):.2f}%",
                "top_performing": sorted(
                    proxies_data,
                    key=lambda x: x.get("success_count", 0) / max(x.get("success_count", 1) + x.get("failure_count", 1), 1),
                    reverse=True
                )[:5],
            }
        except Exception as e:
            logger.error(f"Error getting proxy stats: {e}")
            return {}

    def get_daily_trend(self, platform: str, days: int = 30) -> Dict[str, Any]:
        """Get daily trend data."""
        try:
            date_from = (datetime.utcnow() - timedelta(days=days)).date().isoformat()

            metrics_data = (
                self.db.client.table("analytics_metrics")
                .select("metric_date, total_attempts, successful_attempts")
                .eq("platform", platform)
                .gte("metric_date", date_from)
                .order("metric_date", desc=False)
                .execute()
                .data or []
            )

            trend = {
                "platform": platform,
                "period_days": days,
                "daily_data": [
                    {
                        "date": m.get("metric_date"),
                        "attempts": m.get("total_attempts", 0),
                        "successful": m.get("successful_attempts", 0),
                    }
                    for m in metrics_data
                ],
            }

            return trend
        except Exception as e:
            logger.error(f"Error getting daily trend: {e}")
            return {}

    def get_detection_analysis(self, days: int = 7) -> Dict[str, Any]:
        """Get detection analysis."""
        try:
            bot_runs = self.db.client.table("bot_runs").select("*").gte("created_at", (datetime.utcnow() - timedelta(days=days)).isoformat()).execute().data or []

            if not bot_runs:
                return {
                    "total_runs": 0,
                    "detected_runs": 0,
                    "detection_rate": 0,
                }

            detected = sum(1 for r in bot_runs if r.get("detection_triggered"))

            analysis = {
                "timestamp": datetime.utcnow().isoformat(),
                "period_days": days,
                "total_runs": len(bot_runs),
                "detected_runs": detected,
                "detection_rate": f"{(detected / len(bot_runs) * 100) if bot_runs else 0:.2f}%",
                "by_platform": {},
            }

            platforms = list(set(r.get("platform") for r in bot_runs if r.get("platform")))
            for platform in platforms:
                platform_runs = [r for r in bot_runs if r.get("platform") == platform]
                platform_detected = sum(1 for r in platform_runs if r.get("detection_triggered"))

                analysis["by_platform"][platform] = {
                    "total_runs": len(platform_runs),
                    "detected": platform_detected,
                    "detection_rate": f"{(platform_detected / len(platform_runs) * 100) if platform_runs else 0:.2f}%",
                }

            return analysis
        except Exception as e:
            logger.error(f"Error getting detection analysis: {e}")
            return {}

    def get_research_session_summary(self) -> Dict[str, Any]:
        """Get research session summary."""
        try:
            sessions = self.db.client.table("research_sessions").select("*").eq("status", "active").execute().data or []

            summary = {
                "timestamp": datetime.utcnow().isoformat(),
                "active_sessions": len(sessions),
                "sessions": [],
            }

            for session in sessions:
                summary["sessions"].append({
                    "id": session.get("id"),
                    "name": session.get("name"),
                    "platform": session.get("platform"),
                    "started_at": session.get("started_at"),
                    "total_runs": session.get("total_runs", 0),
                    "successful_runs": session.get("successful_runs", 0),
                })

            return summary
        except Exception as e:
            logger.error(f"Error getting research session summary: {e}")
            return {}

    def export_data_as_json(self, data_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """Export data as JSON."""
        try:
            if data_type == "platform_stats":
                platform = filters.get("platform", "Nike") if filters else "Nike"
                data = self.get_platform_stats(platform)
            elif data_type == "overview":
                data = self.get_overview()
            elif data_type == "captcha":
                data = self.get_captcha_analytics()
            elif data_type == "proxy":
                data = self.get_proxy_stats()
            else:
                data = {}

            return json.dumps(data, indent=2)
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return "{}"


def get_dashboard_api() -> DashboardAPI:
    """Get or create dashboard API singleton."""
    if not hasattr(get_dashboard_api, "_instance"):
        get_dashboard_api._instance = DashboardAPI()
    return get_dashboard_api._instance
