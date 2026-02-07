"""Supabase client and database utilities for SneakerBot Ultimate."""

import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from uuid import uuid4
import logging
from functools import lru_cache

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

logger = logging.getLogger(__name__)


class SupabaseManager:
    """Manages all Supabase database operations."""

    def __init__(self):
        """Initialize Supabase client."""
        self.client: Optional[Client] = None
        self.initialized = False
        self._init_client()

    def _init_client(self) -> None:
        """Initialize Supabase connection."""
        if not SUPABASE_AVAILABLE:
            logger.warning("Supabase library not available. Install with: pip install supabase")
            return

        try:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_ANON_KEY")

            if not url or not key:
                logger.warning("SUPABASE_URL or SUPABASE_ANON_KEY not set in environment")
                return

            self.client = create_client(url, key)
            self.initialized = True
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase: {e}")

    def is_connected(self) -> bool:
        """Check if Supabase is connected."""
        return self.initialized and self.client is not None

    # Account Management
    def create_account(
        self,
        platform: str,
        email: str,
        password_encrypted: str,
        username: Optional[str] = None,
        account_name: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Optional[str]:
        """Create a new account record."""
        if not self.is_connected():
            return None

        try:
            data = {
                "platform": platform,
                "email": email,
                "password_encrypted": password_encrypted,
                "username": username,
                "account_name": account_name,
                "notes": notes,
                "status": "active",
                "created_at": datetime.utcnow().isoformat(),
            }

            response = self.client.table("accounts").insert(data).execute()
            if response.data:
                return response.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating account: {e}")
            return None

    def get_account(self, account_id: str) -> Optional[Dict[str, Any]]:
        """Get account by ID."""
        if not self.is_connected():
            return None

        try:
            response = self.client.table("accounts").select("*").eq("id", account_id).maybeSingle().execute()
            return response.data
        except Exception as e:
            logger.error(f"Error getting account: {e}")
            return None

    def get_accounts_by_platform(self, platform: str) -> List[Dict[str, Any]]:
        """Get all accounts for a platform."""
        if not self.is_connected():
            return []

        try:
            response = (
                self.client.table("accounts").select("*").eq("platform", platform).eq("status", "active").execute()
            )
            return response.data or []
        except Exception as e:
            logger.error(f"Error getting accounts: {e}")
            return []

    def update_account_usage(self, account_id: str) -> bool:
        """Update last_used timestamp."""
        if not self.is_connected():
            return False

        try:
            self.client.table("accounts").update({"last_used": datetime.utcnow().isoformat()}).eq("id", account_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating account: {e}")
            return False

    def update_account_stats(self, account_id: str, success: bool) -> bool:
        """Update account success/failure counts."""
        if not self.is_connected():
            return False

        try:
            account = self.get_account(account_id)
            if not account:
                return False

            if success:
                new_success = (account.get("success_count") or 0) + 1
                self.client.table("accounts").update({"success_count": new_success}).eq("id", account_id).execute()
            else:
                new_failure = (account.get("failure_count") or 0) + 1
                self.client.table("accounts").update({"failure_count": new_failure}).eq("id", account_id).execute()

            return True
        except Exception as e:
            logger.error(f"Error updating account stats: {e}")
            return False

    # Bot Session Management
    def create_session(
        self,
        account_id: str,
        platform: str,
        browser_fingerprint: Optional[Dict] = None,
        proxy: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Optional[str]:
        """Create a new bot session."""
        if not self.is_connected():
            return None

        try:
            session_token = str(uuid4())
            data = {
                "account_id": account_id,
                "platform": platform,
                "session_token": session_token,
                "browser_fingerprint": browser_fingerprint or {},
                "proxy_used": proxy,
                "user_agent": user_agent,
                "status": "active",
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
            }

            response = self.client.table("bot_sessions").insert(data).execute()
            if response.data:
                return response.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            return None

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID."""
        if not self.is_connected():
            return None

        try:
            response = (
                self.client.table("bot_sessions").select("*").eq("id", session_id).eq("status", "active").maybeSingle().execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error getting session: {e}")
            return None

    # Bot Run Tracking
    def create_bot_run(
        self,
        session_id: str,
        account_id: str,
        platform: str,
        bot_type: str,
        sneaker_name: Optional[str] = None,
        target_size: Optional[str] = None,
    ) -> Optional[str]:
        """Create a new bot run record."""
        if not self.is_connected():
            return None

        try:
            data = {
                "session_id": session_id,
                "account_id": account_id,
                "platform": platform,
                "bot_type": bot_type,
                "sneaker_name": sneaker_name,
                "target_size": target_size,
                "status": "pending",
                "started_at": datetime.utcnow().isoformat(),
            }

            response = self.client.table("bot_runs").insert(data).execute()
            if response.data:
                return response.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating bot run: {e}")
            return None

    def update_bot_run(self, run_id: str, **kwargs) -> bool:
        """Update bot run record."""
        if not self.is_connected():
            return False

        try:
            update_data = {}
            for key, value in kwargs.items():
                if key == "completed_at" and value is True:
                    update_data["completed_at"] = datetime.utcnow().isoformat()
                else:
                    update_data[key] = value

            self.client.table("bot_runs").update(update_data).eq("id", run_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating bot run: {e}")
            return False

    def get_bot_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get bot run by ID."""
        if not self.is_connected():
            return None

        try:
            response = self.client.table("bot_runs").select("*").eq("id", run_id).maybeSingle().execute()
            return response.data
        except Exception as e:
            logger.error(f"Error getting bot run: {e}")
            return None

    # Purchase Attempt Tracking
    def create_purchase_attempt(
        self,
        bot_run_id: str,
        account_id: str,
        platform: str,
        product_name: Optional[str] = None,
        product_size: Optional[str] = None,
        stage: Optional[str] = None,
    ) -> Optional[str]:
        """Create purchase attempt record."""
        if not self.is_connected():
            return None

        try:
            data = {
                "bot_run_id": bot_run_id,
                "account_id": account_id,
                "platform": platform,
                "product_name": product_name,
                "product_size": product_size,
                "stage": stage,
                "completed_at": datetime.utcnow().isoformat(),
            }

            response = self.client.table("purchase_attempts").insert(data).execute()
            if response.data:
                return response.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating purchase attempt: {e}")
            return None

    def update_purchase_attempt(self, attempt_id: str, success: bool, order_id: Optional[str] = None) -> bool:
        """Update purchase attempt with result."""
        if not self.is_connected():
            return False

        try:
            update_data = {"success": success}
            if order_id:
                update_data["order_id"] = order_id

            self.client.table("purchase_attempts").update(update_data).eq("id", attempt_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating purchase attempt: {e}")
            return False

    # Analytics Tracking
    def record_captcha_attempt(
        self,
        bot_run_id: str,
        platform: str,
        captcha_type: str,
        solver_service: str,
        success: bool,
        solve_time_ms: Optional[int] = None,
        cost: Optional[float] = None,
    ) -> bool:
        """Record CAPTCHA solving attempt."""
        if not self.is_connected():
            return False

        try:
            data = {
                "bot_run_id": bot_run_id,
                "platform": platform,
                "captcha_type": captcha_type,
                "solver_service": solver_service,
                "success": success,
                "solve_time_ms": solve_time_ms,
                "cost": cost,
                "created_at": datetime.utcnow().isoformat(),
            }

            self.client.table("captcha_attempts").insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Error recording CAPTCHA attempt: {e}")
            return False

    def record_proxy_performance(
        self,
        proxy_address: str,
        platform: str,
        success: bool,
        response_time_ms: Optional[int] = None,
        detected: bool = False,
    ) -> bool:
        """Record proxy performance metrics."""
        if not self.is_connected():
            return False

        try:
            response = (
                self.client.table("proxy_performance")
                .select("*")
                .eq("proxy_address", proxy_address)
                .eq("platform", platform)
                .maybeSingle()
                .execute()
            )

            if response.data:
                # Update existing record
                perf = response.data
                new_success_count = perf.get("success_count", 0) + (1 if success else 0)
                new_failure_count = perf.get("failure_count", 0) + (0 if success else 1)
                new_detection_count = perf.get("detection_count", 0) + (1 if detected else 0)

                self.client.table("proxy_performance").update(
                    {
                        "success_count": new_success_count,
                        "failure_count": new_failure_count,
                        "detection_count": new_detection_count,
                        "last_tested": datetime.utcnow().isoformat(),
                        "last_success": datetime.utcnow().isoformat() if success else perf.get("last_success"),
                    }
                ).eq("proxy_address", proxy_address).eq("platform", platform).execute()
            else:
                # Create new record
                data = {
                    "proxy_address": proxy_address,
                    "platform": platform,
                    "success_count": 1 if success else 0,
                    "failure_count": 0 if success else 1,
                    "detection_count": 1 if detected else 0,
                    "last_tested": datetime.utcnow().isoformat(),
                    "last_success": datetime.utcnow().isoformat() if success else None,
                    "created_at": datetime.utcnow().isoformat(),
                }
                self.client.table("proxy_performance").insert(data).execute()

            return True
        except Exception as e:
            logger.error(f"Error recording proxy performance: {e}")
            return False

    def record_notification(
        self,
        bot_run_id: str,
        notification_type: str,
        channel: str,
        message: str,
        success: bool,
    ) -> bool:
        """Record sent notification."""
        if not self.is_connected():
            return False

        try:
            data = {
                "bot_run_id": bot_run_id,
                "notification_type": notification_type,
                "channel": channel,
                "message": message,
                "success": success,
                "sent_at": datetime.utcnow().isoformat(),
            }

            self.client.table("notifications").insert(data).execute()
            return True
        except Exception as e:
            logger.error(f"Error recording notification: {e}")
            return False

    # Research Session Management
    def create_research_session(
        self,
        name: str,
        platform: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[str]:
        """Create a new research session."""
        if not self.is_connected():
            return None

        try:
            data = {
                "name": name,
                "platform": platform,
                "description": description,
                "status": "active",
                "started_at": datetime.utcnow().isoformat(),
            }

            response = self.client.table("research_sessions").insert(data).execute()
            if response.data:
                return response.data[0]["id"]
            return None
        except Exception as e:
            logger.error(f"Error creating research session: {e}")
            return None

    def update_research_session(self, session_id: str, **kwargs) -> bool:
        """Update research session."""
        if not self.is_connected():
            return False

        try:
            update_data = {}
            for key, value in kwargs.items():
                if key == "completed_at" and value is True:
                    update_data["completed_at"] = datetime.utcnow().isoformat()
                else:
                    update_data[key] = value

            self.client.table("research_sessions").update(update_data).eq("id", session_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating research session: {e}")
            return False

    # Analytics Retrieval
    def get_platform_metrics(self, platform: str, days: int = 7) -> Dict[str, Any]:
        """Get platform metrics for last N days."""
        if not self.is_connected():
            return {}

        try:
            date_from = (datetime.utcnow() - timedelta(days=days)).date().isoformat()

            response = (
                self.client.table("analytics_metrics")
                .select("*")
                .eq("platform", platform)
                .gte("metric_date", date_from)
                .execute()
            )

            metrics = response.data or []

            if not metrics:
                return {
                    "platform": platform,
                    "total_attempts": 0,
                    "successful_attempts": 0,
                    "failed_attempts": 0,
                    "success_rate": 0,
                }

            total_attempts = sum(m.get("total_attempts", 0) for m in metrics)
            successful = sum(m.get("successful_attempts", 0) for m in metrics)
            failed = sum(m.get("failed_attempts", 0) for m in metrics)

            return {
                "platform": platform,
                "total_attempts": total_attempts,
                "successful_attempts": successful,
                "failed_attempts": failed,
                "success_rate": (successful / total_attempts * 100) if total_attempts > 0 else 0,
                "days": days,
            }
        except Exception as e:
            logger.error(f"Error getting metrics: {e}")
            return {}

    def get_captcha_success_rate(self, platform: str, days: int = 7) -> float:
        """Get CAPTCHA solving success rate."""
        if not self.is_connected():
            return 0

        try:
            date_from = (datetime.utcnow() - timedelta(days=days)).date().isoformat()

            response = (
                self.client.table("captcha_attempts")
                .select("success")
                .eq("platform", platform)
                .gte("created_at", date_from)
                .execute()
            )

            attempts = response.data or []
            if not attempts:
                return 0

            successful = sum(1 for a in attempts if a.get("success"))
            return (successful / len(attempts) * 100) if attempts else 0
        except Exception as e:
            logger.error(f"Error getting CAPTCHA success rate: {e}")
            return 0

    def get_bot_run_stats(self, platform: str, bot_type: str, days: int = 7) -> Dict[str, Any]:
        """Get bot run statistics."""
        if not self.is_connected():
            return {}

        try:
            date_from = (datetime.utcnow() - timedelta(days=days)).date().isoformat()

            response = (
                self.client.table("bot_runs")
                .select("*")
                .eq("platform", platform)
                .eq("bot_type", bot_type)
                .gte("created_at", date_from)
                .execute()
            )

            runs = response.data or []
            if not runs:
                return {"platform": platform, "bot_type": bot_type, "total_runs": 0, "success_count": 0, "success_rate": 0}

            successful = sum(1 for r in runs if r.get("success"))
            durations = [r.get("duration_ms", 0) for r in runs if r.get("duration_ms")]

            return {
                "platform": platform,
                "bot_type": bot_type,
                "total_runs": len(runs),
                "success_count": successful,
                "success_rate": (successful / len(runs) * 100) if runs else 0,
                "average_duration_ms": sum(durations) / len(durations) if durations else 0,
                "captcha_required_count": sum(1 for r in runs if r.get("captcha_required")),
                "detection_triggered_count": sum(1 for r in runs if r.get("detection_triggered")),
            }
        except Exception as e:
            logger.error(f"Error getting bot run stats: {e}")
            return {}


@lru_cache(maxsize=1)
def get_supabase_manager() -> SupabaseManager:
    """Get or create Supabase manager singleton."""
    return SupabaseManager()
