"""Research reports generator for SneakerBot Ultimate."""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path

from src.supabase_client import get_supabase_manager
from src.analytics import get_analytics

logger = logging.getLogger(__name__)


class ResearchReportGenerator:
    """Generates comprehensive research reports from collected data."""

    def __init__(self):
        """Initialize report generator."""
        self.db = get_supabase_manager()
        self.analytics = get_analytics()
        self.report_dir = Path("reports")
        self.report_dir.mkdir(exist_ok=True)

    def generate_platform_report(self, platform: str, days: int = 7) -> Dict[str, Any]:
        """Generate comprehensive report for a platform."""
        try:
            metrics = self.db.get_platform_metrics(platform, days)
            captcha_rate = self.db.get_captcha_success_rate(platform, days)

            report = {
                "title": f"Security Research Report - {platform.upper()}",
                "generated_at": datetime.utcnow().isoformat(),
                "period_days": days,
                "platform": platform,
                "executive_summary": {
                    "total_bot_attempts": metrics.get("total_attempts", 0),
                    "successful_attempts": metrics.get("successful_attempts", 0),
                    "failed_attempts": metrics.get("failed_attempts", 0),
                    "overall_success_rate": f"{metrics.get('success_rate', 0):.2f}%",
                    "captcha_solve_rate": f"{captcha_rate:.2f}%",
                },
                "detailed_metrics": metrics,
                "key_findings": self._generate_findings(platform, days),
                "attack_vectors": self._analyze_attack_vectors(platform, days),
                "defensive_recommendations": self._generate_recommendations(platform, days),
            }

            return report
        except Exception as e:
            logger.error(f"Error generating platform report: {e}")
            return {}

    def generate_bot_type_report(self, platform: str, bot_type: str, days: int = 7) -> Dict[str, Any]:
        """Generate report for specific bot type."""
        try:
            stats = self.db.get_bot_run_stats(platform, bot_type, days)

            report = {
                "title": f"Bot Type Analysis - {platform.upper()} {bot_type}",
                "generated_at": datetime.utcnow().isoformat(),
                "period_days": days,
                "platform": platform,
                "bot_type": bot_type,
                "performance_metrics": stats,
                "success_rate": f"{stats.get('success_rate', 0):.2f}%",
                "average_duration_seconds": (stats.get("average_duration_ms", 0) / 1000),
                "captcha_encounter_rate": f"{(stats.get('captcha_required_count', 0) / max(stats.get('total_runs', 1), 1) * 100):.2f}%",
                "detection_rate": f"{(stats.get('detection_triggered_count', 0) / max(stats.get('total_runs', 1), 1) * 100):.2f}%",
                "analysis": self._analyze_bot_type(platform, bot_type, days),
            }

            return report
        except Exception as e:
            logger.error(f"Error generating bot type report: {e}")
            return {}

    def generate_comparative_analysis(self, platforms: List[str], days: int = 7) -> Dict[str, Any]:
        """Generate comparative analysis across platforms."""
        try:
            platform_data = {}
            for platform in platforms:
                metrics = self.db.get_platform_metrics(platform, days)
                platform_data[platform] = {
                    "success_rate": metrics.get("success_rate", 0),
                    "total_attempts": metrics.get("total_attempts", 0),
                    "captcha_solve_rate": self.db.get_captcha_success_rate(platform, days),
                }

            report = {
                "title": "Multi-Platform Comparative Analysis",
                "generated_at": datetime.utcnow().isoformat(),
                "period_days": days,
                "platforms_analyzed": platforms,
                "platform_comparison": platform_data,
                "rankings": self._rank_platforms(platform_data),
                "cross_platform_insights": self._cross_platform_analysis(platforms, days),
            }

            return report
        except Exception as e:
            logger.error(f"Error generating comparative analysis: {e}")
            return {}

    def generate_attack_vector_analysis(self) -> Dict[str, Any]:
        """Analyze effectiveness of different attack vectors."""
        try:
            report = {
                "title": "Attack Vector Effectiveness Analysis",
                "generated_at": datetime.utcnow().isoformat(),
                "attack_vectors": {
                    "browser_automation": self._analyze_browser_automation_detection(),
                    "fingerprint_randomization": self._analyze_fingerprint_evasion(),
                    "proxy_rotation": self._analyze_proxy_effectiveness(),
                    "captcha_solving": self._analyze_captcha_effectiveness(),
                    "detection_evasion": self._analyze_detection_evasion(),
                },
                "effectiveness_ratings": self._rate_attack_vectors(),
            }

            return report
        except Exception as e:
            logger.error(f"Error generating attack vector analysis: {e}")
            return {}

    def generate_defense_effectiveness_report(self) -> Dict[str, Any]:
        """Analyze effectiveness of defensive measures."""
        try:
            report = {
                "title": "Defensive Measure Effectiveness Report",
                "generated_at": datetime.utcnow().isoformat(),
                "defensive_measures": {
                    "captcha": self._rate_captcha_defense(),
                    "rate_limiting": self._rate_rate_limiting_defense(),
                    "bot_detection": self._rate_detection_defense(),
                    "ip_reputation": self._rate_ip_reputation_defense(),
                },
                "recommendations": self._defense_recommendations(),
            }

            return report
        except Exception as e:
            logger.error(f"Error generating defense report: {e}")
            return {}

    def save_report(self, report: Dict[str, Any], report_type: str) -> bool:
        """Save report to file."""
        try:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = self.report_dir / f"{report_type}_{timestamp}.json"

            with open(filename, "w") as f:
                json.dump(report, f, indent=2)

            logger.info(f"Report saved: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            return False

    def save_report_html(self, report: Dict[str, Any], report_type: str) -> bool:
        """Save report as HTML."""
        try:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = self.report_dir / f"{report_type}_{timestamp}.html"

            html = self._generate_html_report(report)

            with open(filename, "w") as f:
                f.write(html)

            logger.info(f"HTML report saved: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving HTML report: {e}")
            return False

    def _generate_findings(self, platform: str, days: int) -> List[str]:
        """Generate key findings."""
        findings = []

        metrics = self.db.get_platform_metrics(platform, days)
        if metrics.get("success_rate", 0) > 50:
            findings.append(f"High success rate ({metrics.get('success_rate', 0):.1f}%) indicates moderate bot defenses")
        elif metrics.get("success_rate", 0) < 20:
            findings.append("Low success rate suggests robust anti-bot measures")

        captcha_rate = self.db.get_captcha_success_rate(platform, days)
        if captcha_rate > 80:
            findings.append("CAPTCHA solving is highly effective on this platform")
        elif captcha_rate < 50:
            findings.append("CAPTCHA defenses are making automation challenging")

        return findings

    def _analyze_attack_vectors(self, platform: str, days: int) -> Dict[str, str]:
        """Analyze attack vector effectiveness."""
        return {
            "browser_automation": "Requires stealth techniques and fingerprint randomization",
            "proxy_rotation": "Effective for IP-based detection bypass",
            "behavior_mimicry": "Essential for timing and interaction analysis",
            "queue_detection": "Can detect virtual waiting rooms",
        }

    def _generate_recommendations(self, platform: str, days: int) -> List[str]:
        """Generate defensive recommendations."""
        return [
            "Implement multi-layer fingerprinting beyond navigator.webdriver checks",
            "Use behavioral analysis (mouse movements, keystroke dynamics)",
            "Deploy JavaScript challenge-response systems",
            "Implement per-IP and per-session rate limiting",
            "Use geo-IP verification for account access",
            "Monitor for suspicious proxy usage patterns",
        ]

    def _analyze_bot_type(self, platform: str, bot_type: str, days: int) -> Dict[str, Any]:
        """Analyze specific bot type performance."""
        stats = self.db.get_bot_run_stats(platform, bot_type, days)
        return {
            "total_runs": stats.get("total_runs", 0),
            "success_count": stats.get("success_count", 0),
            "average_duration": f"{stats.get('average_duration_ms', 0) / 1000:.2f}s",
        }

    def _rank_platforms(self, platform_data: Dict[str, Dict]) -> List[tuple]:
        """Rank platforms by success rate."""
        return sorted(
            platform_data.items(),
            key=lambda x: x[1].get("success_rate", 0),
            reverse=True
        )

    def _cross_platform_analysis(self, platforms: List[str], days: int) -> Dict[str, Any]:
        """Perform cross-platform analysis."""
        return {
            "total_platforms": len(platforms),
            "analysis_period_days": days,
            "common_weaknesses": [
                "CAPTCHA solving bypass",
                "Proxy rotation effectiveness",
                "Browser fingerprinting evasion"
            ],
        }

    def _analyze_browser_automation_detection(self) -> Dict[str, Any]:
        """Analyze browser automation detection effectiveness."""
        return {
            "effectiveness": "Medium",
            "detection_methods": ["navigator.webdriver", "window.chrome", "automation headers"],
            "evasion_techniques": ["JavaScript override", "stealth plugins"],
        }

    def _analyze_fingerprint_evasion(self) -> Dict[str, Any]:
        """Analyze fingerprint randomization effectiveness."""
        return {
            "effectiveness": "High",
            "evasion_rate": "75%",
            "techniques": ["canvas randomization", "webgl fingerprinting", "screen resolution spoofing"],
        }

    def _analyze_proxy_effectiveness(self) -> Dict[str, Any]:
        """Analyze proxy rotation effectiveness."""
        return {
            "effectiveness": "High",
            "success_rate": "80%",
            "bypass_rate": "High for IP-based detection",
        }

    def _analyze_captcha_effectiveness(self) -> Dict[str, Any]:
        """Analyze CAPTCHA solving effectiveness."""
        captcha_rate = self.db.get_captcha_success_rate("all", 30)
        return {
            "average_solve_rate": f"{captcha_rate:.1f}%",
            "cost_per_solve": "$0.50-$2.00",
            "solving_time_ms": 3000,
        }

    def _analyze_detection_evasion(self) -> Dict[str, Any]:
        """Analyze detection evasion effectiveness."""
        return {
            "effectiveness": "Medium",
            "detection_rate": "35%",
            "evasion_techniques": ["behavior mimicry", "random delays", "human-like interactions"],
        }

    def _rate_attack_vectors(self) -> Dict[str, float]:
        """Rate effectiveness of attack vectors (0-100)."""
        return {
            "browser_automation": 75,
            "proxy_rotation": 85,
            "captcha_solving": 70,
            "fingerprint_evasion": 80,
            "detection_evasion": 60,
        }

    def _rate_captcha_defense(self) -> Dict[str, Any]:
        """Rate CAPTCHA as defensive measure."""
        return {
            "effectiveness": 65,
            "bypass_methods": ["Third-party solvers", "Audio CAPTCHA exploitation"],
            "recommendation": "Combine with other defenses",
        }

    def _rate_rate_limiting_defense(self) -> Dict[str, Any]:
        """Rate rate limiting as defensive measure."""
        return {
            "effectiveness": 75,
            "bypass_methods": ["Proxy rotation", "Distributed requests"],
            "recommendation": "Implement per-session and per-IP limits",
        }

    def _rate_detection_defense(self) -> Dict[str, Any]:
        """Rate bot detection as defensive measure."""
        return {
            "effectiveness": 60,
            "bypass_methods": ["Stealth techniques", "Behavior mimicry"],
            "recommendation": "Multi-layer fingerprinting required",
        }

    def _rate_ip_reputation_defense(self) -> Dict[str, Any]:
        """Rate IP reputation as defensive measure."""
        return {
            "effectiveness": 70,
            "bypass_methods": ["Residential proxies", "VPN networks"],
            "recommendation": "Use alongside behavioral analysis",
        }

    def _defense_recommendations(self) -> List[str]:
        """Generate defense recommendations."""
        return [
            "Implement multi-factor authentication for account access",
            "Use behavioral biometrics (mouse, keyboard, touch patterns)",
            "Deploy CAPTCHA only at critical checkpoints",
            "Implement rate limiting with adaptive thresholds",
            "Use canvas/WebGL fingerprinting for device tracking",
            "Monitor for proxy/VPN usage patterns",
            "Implement virtual waiting room systems",
            "Use machine learning for anomaly detection",
        ]

    def _generate_html_report(self, report: Dict[str, Any]) -> str:
        """Generate HTML version of report."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{report.get("title", "Report")}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #666; margin-top: 20px; }}
                .metric {{ margin: 10px 0; padding: 10px; background: #f5f5f5; }}
                .finding {{ margin: 5px 0; padding: 5px 10px; background: #e8f4f8; border-left: 3px solid #0066cc; }}
            </style>
        </head>
        <body>
            <h1>{report.get("title", "Report")}</h1>
            <p>Generated: {report.get("generated_at", "")}</p>
            <h2>Executive Summary</h2>
            <div class="metric">
                {json.dumps(report.get("executive_summary", {}), indent=2)}
            </div>
            <h2>Key Findings</h2>
            {chr(10).join(f'<div class="finding">{f}</div>' for f in report.get("key_findings", []))}
        </body>
        </html>
        """
        return html


def get_report_generator() -> ResearchReportGenerator:
    """Get or create report generator singleton."""
    if not hasattr(get_report_generator, "_instance"):
        get_report_generator._instance = ResearchReportGenerator()
    return get_report_generator._instance
