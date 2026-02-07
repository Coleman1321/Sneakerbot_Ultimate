"""Analytics and metrics tracking for SneakerBot Ultimate."""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import json

from src.supabase_client import get_supabase_manager

logger = logging.getLogger(__name__)


@dataclass
class BotRunMetrics:
    """Metrics for a single bot run."""

    platform: str
    bot_type: str
    success: bool
    duration_ms: int
    captcha_required: bool
    captcha_solved: bool
    detection_triggered: bool
    queue_detected: bool
    error: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class PerformanceEvent:
    """Single performance event during bot execution."""

    event_type: str
    event_name: str
    timestamp_ms: int
    details: Dict[str, Any]


class Analytics:
    """Handles all analytics and metrics collection."""

    def __init__(self):
        """Initialize analytics."""
        self.db = get_supabase_manager()
        self.current_run_id: Optional[str] = None
        self.current_session_id: Optional[str] = None
        self.run_start_time: Optional[datetime] = None
        self.performance_events: List[PerformanceEvent] = []

    def start_session(self, account_id: str, platform: str, browser_fingerprint: Optional[Dict] = None, proxy: Optional[str] = None) -> Optional[str]:
        """Start a new tracking session."""
        try:
            session_id = self.db.create_session(
                account_id=account_id,
                platform=platform,
                browser_fingerprint=browser_fingerprint,
                proxy=proxy,
            )
            self.current_session_id = session_id
            return session_id
        except Exception as e:
            logger.error(f"Error starting session: {e}")
            return None

    def start_run(
        self,
        platform: str,
        bot_type: str,
        sneaker_name: Optional[str] = None,
        target_size: Optional[str] = None,
    ) -> Optional[str]:
        """Start tracking a new bot run."""
        try:
            if not self.current_session_id:
                logger.warning("No active session for bot run")
                return None

            run_id = self.db.create_bot_run(
                session_id=self.current_session_id,
                account_id="",  # Will be set later
                platform=platform,
                bot_type=bot_type,
                sneaker_name=sneaker_name,
                target_size=target_size,
            )

            self.current_run_id = run_id
            self.run_start_time = datetime.utcnow()
            self.performance_events = []

            logger.info(f"Started bot run: {run_id}")
            return run_id
        except Exception as e:
            logger.error(f"Error starting bot run: {e}")
            return None

    def record_event(
        self,
        event_type: str,
        event_name: str,
        timestamp_ms: int,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record a performance event."""
        try:
            event = PerformanceEvent(
                event_type=event_type,
                event_name=event_name,
                timestamp_ms=timestamp_ms,
                details=details or {},
            )
            self.performance_events.append(event)
        except Exception as e:
            logger.error(f"Error recording event: {e}")

    def end_run(
        self,
        success: bool,
        result: Optional[str] = None,
        error_message: Optional[str] = None,
        captcha_required: bool = False,
        captcha_solved: bool = False,
        queue_detected: bool = False,
        detection_triggered: bool = False,
    ) -> bool:
        """End bot run and record metrics."""
        try:
            if not self.current_run_id or not self.run_start_time:
                logger.warning("No active run to end")
                return False

            duration_ms = int((datetime.utcnow() - self.run_start_time).total_seconds() * 1000)

            # Update bot run
            update_data = {
                "success": success,
                "status": "completed",
                "result": result,
                "error_message": error_message,
                "completed_at": datetime.utcnow().isoformat(),
                "duration_ms": duration_ms,
                "captcha_required": captcha_required,
                "captcha_solved": captcha_solved,
                "queue_detected": queue_detected,
                "detection_triggered": detection_triggered,
            }

            self.db.update_bot_run(self.current_run_id, **update_data)

            logger.info(f"Ended bot run: {self.current_run_id} - Success: {success}")
            return True
        except Exception as e:
            logger.error(f"Error ending bot run: {e}")
            return False

    def record_captcha_attempt(
        self,
        captcha_type: str,
        solver_service: str,
        success: bool,
        solve_time_ms: Optional[int] = None,
        cost: Optional[float] = None,
        platform: Optional[str] = None,
    ) -> bool:
        """Record CAPTCHA solving attempt."""
        try:
            if not self.current_run_id:
                logger.warning("No active run for CAPTCHA attempt")
                return False

            self.db.record_captcha_attempt(
                bot_run_id=self.current_run_id,
                platform=platform or "unknown",
                captcha_type=captcha_type,
                solver_service=solver_service,
                success=success,
                solve_time_ms=solve_time_ms,
                cost=cost,
            )

            logger.info(f"Recorded CAPTCHA attempt - Success: {success}")
            return True
        except Exception as e:
            logger.error(f"Error recording CAPTCHA: {e}")
            return False

    def record_proxy_performance(
        self,
        proxy_address: str,
        platform: str,
        success: bool,
        response_time_ms: Optional[int] = None,
        detected: bool = False,
    ) -> bool:
        """Record proxy performance."""
        try:
            self.db.record_proxy_performance(
                proxy_address=proxy_address,
                platform=platform,
                success=success,
                response_time_ms=response_time_ms,
                detected=detected,
            )

            logger.info(f"Recorded proxy performance - Proxy: {proxy_address[:20]}... - Success: {success}")
            return True
        except Exception as e:
            logger.error(f"Error recording proxy performance: {e}")
            return False

    def record_purchase_attempt(
        self,
        platform: str,
        product_name: Optional[str] = None,
        product_size: Optional[str] = None,
        stage: Optional[str] = None,
        success: bool = False,
        order_id: Optional[str] = None,
    ) -> bool:
        """Record purchase attempt."""
        try:
            if not self.current_run_id:
                logger.warning("No active run for purchase attempt")
                return False

            attempt_id = self.db.create_purchase_attempt(
                bot_run_id=self.current_run_id,
                account_id="",
                platform=platform,
                product_name=product_name,
                product_size=product_size,
                stage=stage,
            )

            if attempt_id:
                self.db.update_purchase_attempt(attempt_id, success, order_id)
                logger.info(f"Recorded purchase attempt - Success: {success}")
                return True

            return False
        except Exception as e:
            logger.error(f"Error recording purchase attempt: {e}")
            return False

    def record_notification(
        self,
        notification_type: str,
        channel: str,
        message: str,
        success: bool,
    ) -> bool:
        """Record notification sent."""
        try:
            if not self.current_run_id:
                logger.warning("No active run for notification")
                return False

            self.db.record_notification(
                bot_run_id=self.current_run_id,
                notification_type=notification_type,
                channel=channel,
                message=message,
                success=success,
            )

            logger.info(f"Recorded notification - Channel: {channel} - Success: {success}")
            return True
        except Exception as e:
            logger.error(f"Error recording notification: {e}")
            return False

    def get_platform_summary(self, platform: str, days: int = 7) -> Dict[str, Any]:
        """Get summary metrics for a platform."""
        try:
            metrics = self.db.get_platform_metrics(platform, days)
            captcha_rate = self.db.get_captcha_success_rate(platform, days)

            return {
                **metrics,
                "captcha_success_rate": captcha_rate,
                "days_analyzed": days,
            }
        except Exception as e:
            logger.error(f"Error getting platform summary: {e}")
            return {}

    def get_bot_type_summary(self, platform: str, bot_type: str, days: int = 7) -> Dict[str, Any]:
        """Get summary for specific bot type."""
        try:
            return self.db.get_bot_run_stats(platform, bot_type, days)
        except Exception as e:
            logger.error(f"Error getting bot type summary: {e}")
            return {}

    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate performance report from events."""
        try:
            if not self.performance_events:
                return {"total_events": 0, "events": []}

            return {
                "total_events": len(self.performance_events),
                "events": [asdict(e) for e in self.performance_events],
                "event_types": list(set(e.event_type for e in self.performance_events)),
            }
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return {}


def get_analytics() -> Analytics:
    """Get or create Analytics singleton."""
    if not hasattr(get_analytics, "_instance"):
        get_analytics._instance = Analytics()
    return get_analytics._instance
