"""Central integration module for all bot operations and analytics."""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
from contextlib import contextmanager

from src.supabase_client import get_supabase_manager
from src.analytics import get_analytics
from src.account_manager import AccountManager
from src.dashboard_api import get_dashboard_api
from src.research_reports import get_report_generator

logger = logging.getLogger(__name__)


class BotIntegration:
    """Central integration point for all bot operations."""

    def __init__(self):
        """Initialize bot integration."""
        self.db = get_supabase_manager()
        self.analytics = get_analytics()
        self.account_manager = AccountManager()
        self.dashboard = get_dashboard_api()
        self.reports = get_report_generator()

        self.current_account_id: Optional[str] = None
        self.current_session_id: Optional[str] = None
        self.current_run_id: Optional[str] = None

    @contextmanager
    def track_bot_session(self, account_id: str, platform: str, browser_fingerprint: Optional[Dict] = None, proxy: Optional[str] = None):
        """Context manager for tracking a complete bot session."""
        try:
            self.current_account_id = account_id
            session_id = self.analytics.start_session(account_id, platform, browser_fingerprint, proxy)
            self.current_session_id = session_id

            logger.info(f"Started tracking session: {session_id}")
            yield self

        except Exception as e:
            logger.error(f"Error in bot session: {e}")
            raise
        finally:
            if self.current_session_id:
                self.db.update_account_usage(account_id)
                logger.info(f"Closed session: {self.current_session_id}")
                self.current_session_id = None
                self.current_account_id = None

    @contextmanager
    def track_bot_run(self, platform: str, bot_type: str, sneaker_name: Optional[str] = None, target_size: Optional[str] = None):
        """Context manager for tracking a bot run."""
        try:
            run_id = self.analytics.start_run(platform, bot_type, sneaker_name, target_size)
            self.current_run_id = run_id

            logger.info(f"Started bot run: {run_id}")
            yield self

        except Exception as e:
            logger.error(f"Error in bot run: {e}")
            raise
        finally:
            self.current_run_id = None

    def log_bot_event(self, event_type: str, event_name: str, timestamp_ms: int, details: Optional[Dict[str, Any]] = None) -> None:
        """Log a bot performance event."""
        if self.current_run_id:
            self.analytics.record_event(event_type, event_name, timestamp_ms, details)

    def end_bot_run(
        self,
        success: bool,
        result: Optional[str] = None,
        error_message: Optional[str] = None,
        captcha_required: bool = False,
        captcha_solved: bool = False,
        queue_detected: bool = False,
        detection_triggered: bool = False,
    ) -> bool:
        """End the current bot run with results."""
        if not self.current_run_id:
            logger.warning("No active bot run to end")
            return False

        result = self.analytics.end_run(
            success=success,
            result=result,
            error_message=error_message,
            captcha_required=captcha_required,
            captcha_solved=captcha_solved,
            queue_detected=queue_detected,
            detection_triggered=detection_triggered,
        )

        if self.current_account_id:
            self.db.update_account_stats(self.current_account_id, success)

        return result

    def log_captcha_attempt(
        self,
        captcha_type: str,
        solver_service: str,
        success: bool,
        solve_time_ms: Optional[int] = None,
        cost: Optional[float] = None,
        platform: Optional[str] = None,
    ) -> bool:
        """Log CAPTCHA solving attempt."""
        return self.analytics.record_captcha_attempt(
            captcha_type=captcha_type,
            solver_service=solver_service,
            success=success,
            solve_time_ms=solve_time_ms,
            cost=cost,
            platform=platform,
        )

    def log_proxy_usage(
        self,
        proxy_address: str,
        platform: str,
        success: bool,
        response_time_ms: Optional[int] = None,
        detected: bool = False,
    ) -> bool:
        """Log proxy usage and performance."""
        return self.analytics.record_proxy_performance(
            proxy_address=proxy_address,
            platform=platform,
            success=success,
            response_time_ms=response_time_ms,
            detected=detected,
        )

    def log_purchase_attempt(
        self,
        platform: str,
        product_name: Optional[str] = None,
        product_size: Optional[str] = None,
        stage: Optional[str] = None,
        success: bool = False,
        order_id: Optional[str] = None,
    ) -> bool:
        """Log purchase attempt."""
        return self.analytics.record_purchase_attempt(
            platform=platform,
            product_name=product_name,
            product_size=product_size,
            stage=stage,
            success=success,
            order_id=order_id,
        )

    def log_notification(self, notification_type: str, channel: str, message: str, success: bool) -> bool:
        """Log notification sent."""
        return self.analytics.record_notification(
            notification_type=notification_type,
            channel=channel,
            message=message,
            success=success,
        )

    def get_account(self, platform: str, account_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get account for bot use."""
        return self.account_manager.get_account(platform, account_id)

    def get_random_account(self, platform: str) -> Optional[Dict[str, Any]]:
        """Get random active account."""
        return self.account_manager.get_random_account(platform)

    def get_all_accounts(self, platform: str):
        """Get all accounts for platform."""
        return self.account_manager.get_all_accounts(platform)

    def create_account(
        self,
        platform: str,
        email: str,
        password: str,
        username: Optional[str] = None,
        account_name: Optional[str] = None,
    ) -> Optional[str]:
        """Create new account."""
        return self.account_manager.create_account(platform, email, password, username, account_name)

    def get_platform_metrics(self, platform: str, days: int = 7) -> Dict[str, Any]:
        """Get platform metrics."""
        return self.analytics.get_platform_summary(platform, days)

    def get_bot_type_metrics(self, platform: str, bot_type: str, days: int = 7) -> Dict[str, Any]:
        """Get bot type metrics."""
        return self.analytics.get_bot_type_summary(platform, bot_type, days)

    def get_dashboard_overview(self) -> Dict[str, Any]:
        """Get dashboard overview."""
        return self.dashboard.get_overview()

    def get_platform_stats(self, platform: str, days: int = 7) -> Dict[str, Any]:
        """Get platform statistics."""
        return self.dashboard.get_platform_stats(platform, days)

    def get_captcha_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get CAPTCHA analytics."""
        return self.dashboard.get_captcha_analytics(days)

    def get_proxy_stats(self) -> Dict[str, Any]:
        """Get proxy statistics."""
        return self.dashboard.get_proxy_stats()

    def get_detection_analysis(self, days: int = 7) -> Dict[str, Any]:
        """Get detection analysis."""
        return self.dashboard.get_detection_analysis(days)

    def generate_platform_report(self, platform: str, days: int = 7) -> Dict[str, Any]:
        """Generate comprehensive platform report."""
        return self.reports.generate_platform_report(platform, days)

    def generate_bot_type_report(self, platform: str, bot_type: str, days: int = 7) -> Dict[str, Any]:
        """Generate bot type report."""
        return self.reports.generate_bot_type_report(platform, bot_type, days)

    def generate_attack_vector_analysis(self) -> Dict[str, Any]:
        """Generate attack vector analysis."""
        return self.reports.generate_attack_vector_analysis()

    def save_report(self, report: Dict[str, Any], report_type: str) -> bool:
        """Save report to file."""
        return self.reports.save_report(report, report_type)

    def save_report_html(self, report: Dict[str, Any], report_type: str) -> bool:
        """Save report as HTML."""
        return self.reports.save_report_html(report, report_type)

    def is_supabase_connected(self) -> bool:
        """Check if Supabase is connected."""
        return self.db.is_connected()

    def get_connection_status(self) -> Dict[str, Any]:
        """Get connection status of all services."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "supabase": self.db.is_connected(),
            "analytics": True,
            "dashboard": True,
            "reports": True,
        }


def get_bot_integration() -> BotIntegration:
    """Get or create bot integration singleton."""
    if not hasattr(get_bot_integration, "_instance"):
        get_bot_integration._instance = BotIntegration()
    return get_bot_integration._instance
