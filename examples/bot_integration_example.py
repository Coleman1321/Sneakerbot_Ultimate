"""
Complete example of using SneakerBot Ultimate with Supabase integration.
Demonstrates analytics, reporting, and account management.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bot_integration import get_bot_integration
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_account_management():
    """Example: Account management with Supabase."""
    print("\n=== ACCOUNT MANAGEMENT EXAMPLE ===\n")

    integration = get_bot_integration()

    # Create a new account
    account_id = integration.create_account(
        platform="Nike",
        email="research@example.com",
        password="SecurePassword123!",
        username="research_account",
        account_name="Nike Research Account"
    )
    print(f"Created account: {account_id}")

    # Get random account for platform
    account = integration.get_random_account("Nike")
    if account:
        print(f"Retrieved account: {account}")

    # Get all accounts for platform
    accounts = integration.get_all_accounts("Nike")
    print(f"Total Nike accounts: {len(accounts)}")


def example_bot_tracking():
    """Example: Track bot session and run with analytics."""
    print("\n=== BOT TRACKING EXAMPLE ===\n")

    integration = get_bot_integration()

    # Get an account to use
    account = integration.get_random_account("Nike")
    if not account:
        print("No Nike accounts found. Create one first.")
        return

    account_id = account.get("id") if isinstance(account, dict) else str(account)

    # Track complete session
    try:
        with integration.track_bot_session(
            account_id=account_id,
            platform="Nike",
            browser_fingerprint={
                "screen_resolution": "1920x1080",
                "color_depth": 24,
                "timezone": -240,
                "canvas_fingerprint": "abcdef123456"
            },
            proxy="http://proxy.example.com:8080"
        ):
            print("Session started")

            # Track individual bot run
            with integration.track_bot_run(
                platform="Nike",
                bot_type="nike_purchase",
                sneaker_name="Air Jordan 1 Low",
                target_size="10.5"
            ):
                print("Bot run started")

                # Log navigation event
                integration.log_bot_event(
                    event_type="navigation",
                    event_name="login_page",
                    timestamp_ms=100,
                    details={"url": "nike.com/login"}
                )
                print("Logged navigation event")

                # Log login event
                integration.log_bot_event(
                    event_type="authentication",
                    event_name="login_successful",
                    timestamp_ms=2500,
                    details={"auth_method": "email_password"}
                )

                # Simulate CAPTCHA encounter
                integration.log_captcha_attempt(
                    captcha_type="reCAPTCHA v2",
                    solver_service="2Captcha",
                    success=True,
                    solve_time_ms=3200,
                    cost=0.50,
                    platform="Nike"
                )
                print("Logged CAPTCHA solving")

                # Log proxy usage
                integration.log_proxy_usage(
                    proxy_address="http://proxy.example.com:8080",
                    platform="Nike",
                    success=True,
                    response_time_ms=450,
                    detected=False
                )
                print("Logged proxy usage")

                # Log purchase attempt
                integration.log_purchase_attempt(
                    platform="Nike",
                    product_name="Air Jordan 1 Low",
                    product_size="10.5",
                    stage="checkout",
                    success=True,
                    order_id="ORDER-123456"
                )
                print("Logged purchase attempt")

                # Log notification
                integration.log_notification(
                    notification_type="success",
                    channel="discord",
                    message="Nike purchase successful!",
                    success=True
                )
                print("Logged notification")

                # End run with success
                integration.end_bot_run(
                    success=True,
                    result="purchase_successful",
                    captcha_required=True,
                    captcha_solved=True,
                    queue_detected=False,
                    detection_triggered=False
                )
                print("Bot run completed successfully")

    except Exception as e:
        logger.error(f"Error in bot tracking: {e}")


def example_analytics():
    """Example: Retrieve and display analytics."""
    print("\n=== ANALYTICS EXAMPLE ===\n")

    integration = get_bot_integration()

    # Get platform metrics
    print("Getting platform metrics...")
    metrics = integration.get_platform_metrics("Nike", days=7)
    print(f"Nike (last 7 days):")
    print(f"  Total attempts: {metrics.get('total_attempts', 0)}")
    print(f"  Successful: {metrics.get('successful_attempts', 0)}")
    print(f"  Success rate: {metrics.get('success_rate', 0):.2f}%")

    # Get bot type metrics
    print("\nGetting bot type metrics...")
    bot_stats = integration.get_bot_type_metrics("Nike", "nike_purchase", days=7)
    print(f"Nike Purchase Bot (last 7 days):")
    print(f"  Total runs: {bot_stats.get('total_runs', 0)}")
    print(f"  Successful: {bot_stats.get('success_count', 0)}")
    print(f"  Success rate: {bot_stats.get('success_rate', 0):.2f}%")
    print(f"  Average duration: {bot_stats.get('average_duration_ms', 0) / 1000:.2f}s")

    # Get dashboard data
    print("\nGetting dashboard overview...")
    overview = integration.get_dashboard_overview()
    print(f"Dashboard Overview:")
    print(f"  Platforms: {list(overview.get('platforms', {}).keys())}")
    print(f"  Total runs today: {overview.get('total_metrics', {}).get('total_runs_today', 0)}")

    # Get CAPTCHA analytics
    print("\nGetting CAPTCHA analytics...")
    captcha_stats = integration.get_captcha_analytics(days=30)
    print(f"CAPTCHA Analytics (last 30 days):")
    for platform, data in captcha_stats.get('platform_breakdown', {}).items():
        print(f"  {platform}: {data.get('solve_success_rate')}")

    # Get proxy statistics
    print("\nGetting proxy statistics...")
    proxy_stats = integration.get_proxy_stats()
    print(f"Proxy Statistics:")
    print(f"  Total proxies: {proxy_stats.get('total_proxies', 0)}")
    print(f"  Working proxies: {proxy_stats.get('working_proxies', 0)}")
    print(f"  Success rate: {proxy_stats.get('success_rate')}")

    # Get detection analysis
    print("\nGetting detection analysis...")
    detection = integration.get_detection_analysis(days=7)
    print(f"Detection Analysis (last 7 days):")
    print(f"  Total runs: {detection.get('total_runs', 0)}")
    print(f"  Detected runs: {detection.get('detected_runs', 0)}")
    print(f"  Detection rate: {detection.get('detection_rate')}")


def example_reports():
    """Example: Generate research reports."""
    print("\n=== RESEARCH REPORTS EXAMPLE ===\n")

    integration = get_bot_integration()

    # Generate platform report
    print("Generating platform report...")
    platform_report = integration.generate_platform_report("Nike", days=30)
    print(f"Report title: {platform_report.get('title')}")
    print(f"Key findings: {platform_report.get('key_findings', [])[:2]}...")

    # Save report
    if platform_report:
        success = integration.save_report(platform_report, "nike_analysis")
        print(f"Report saved: {success}")

        success_html = integration.save_report_html(platform_report, "nike_analysis")
        print(f"HTML report saved: {success_html}")

    # Generate bot type report
    print("\nGenerating bot type report...")
    bot_report = integration.generate_bot_type_report("Nike", "nike_purchase", days=7)
    if bot_report:
        print(f"Bot type: {bot_report.get('bot_type')}")
        print(f"Total runs: {bot_report.get('performance_metrics', {}).get('total_runs', 0)}")
        print(f"Success rate: {bot_report.get('success_rate')}")

    # Generate attack vector analysis
    print("\nGenerating attack vector analysis...")
    attack_analysis = integration.generate_attack_vector_analysis()
    print(f"Report title: {attack_analysis.get('title')}")
    effectiveness = attack_analysis.get('effectiveness_ratings', {})
    for vector, rating in list(effectiveness.items())[:3]:
        print(f"  {vector}: {rating}/100")


def example_connection_status():
    """Example: Check connection status."""
    print("\n=== CONNECTION STATUS EXAMPLE ===\n")

    integration = get_bot_integration()

    status = integration.get_connection_status()
    print("Service Status:")
    for service, connected in status.items():
        if service != "timestamp":
            print(f"  {service}: {'Connected' if connected else 'Disconnected'}")

    print(f"\nSupabase available: {integration.is_supabase_connected()}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("SneakerBot Ultimate - Supabase Integration Examples")
    print("=" * 60)

    try:
        example_account_management()
        example_bot_tracking()
        example_analytics()
        example_reports()
        example_connection_status()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)

    except Exception as e:
        logger.error(f"Error running examples: {e}", exc_info=True)


if __name__ == "__main__":
    main()
