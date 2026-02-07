# Supabase Integration Guide - SneakerBot Ultimate

## Overview

SneakerBot Ultimate has been expanded with full Supabase integration for cloud-based data persistence, analytics, and comprehensive research reporting. This guide covers setup, usage, and features.

## Features Added

### 1. Cloud Database (Supabase PostgreSQL)
- **Account Management**: Store and manage bot accounts across platforms
- **Bot Sessions**: Track individual browser sessions and fingerprints
- **Bot Runs**: Detailed logging of each bot execution
- **Analytics**: Comprehensive metrics collection and analysis
- **Research Sessions**: Group related bot runs for organized research

### 2. Real-Time Analytics
- Success rate tracking by platform and bot type
- CAPTCHA solving effectiveness analysis
- Proxy performance monitoring
- Detection rate analysis
- Performance event logging

### 3. Research Reports
- Platform-specific security analysis reports
- Attack vector effectiveness ratings
- Comparative cross-platform analysis
- Defense effectiveness evaluation
- HTML and JSON export formats

### 4. Dashboard API
- Real-time metrics and statistics
- Platform performance summaries
- Account usage analytics
- CAPTCHA and proxy performance tracking
- Detection pattern analysis

## Setup Instructions

### Prerequisites
- Python 3.8+
- Supabase account (free tier available at supabase.com)

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up and create a new project
3. Wait for project initialization
4. Get your credentials from **Project Settings > API**:
   - `SUPABASE_URL`: Project URL
   - `SUPABASE_ANON_KEY`: Anon public key

### Step 2: Configure Environment

Create or update `.env` file:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
```

### Step 3: Install Dependencies

```bash
pip install supabase postgrest-py
```

Or use the complete requirements:
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database

The database schema is automatically created on first connection. Tables include:
- accounts
- bot_sessions
- bot_runs
- purchase_attempts
- analytics_metrics
- captcha_attempts
- proxy_performance
- notifications
- research_sessions
- performance_logs

## Usage Examples

### Basic Bot Integration

```python
from src.bot_integration import get_bot_integration

# Get integration instance
bot_integration = get_bot_integration()

# Track a complete bot session
with bot_integration.track_bot_session(
    account_id="account-123",
    platform="Nike",
    browser_fingerprint={"screen": "1920x1080"},
    proxy="http://proxy:8080"
):
    # Track individual bot run
    with bot_integration.track_bot_run(
        platform="Nike",
        bot_type="nike_purchase",
        sneaker_name="Air Jordan 1",
        target_size="10.5"
    ):
        # Log events
        bot_integration.log_bot_event(
            event_type="navigation",
            event_name="product_page_loaded",
            timestamp_ms=1500,
            details={"load_time_ms": 1200}
        )

        # Log CAPTCHA attempt
        bot_integration.log_captcha_attempt(
            captcha_type="reCAPTCHA v2",
            solver_service="2Captcha",
            success=True,
            solve_time_ms=3200,
            cost=0.50,
            platform="Nike"
        )

        # Log proxy usage
        bot_integration.log_proxy_usage(
            proxy_address="http://proxy:8080",
            platform="Nike",
            success=True,
            response_time_ms=450,
            detected=False
        )

        # Log purchase attempt
        bot_integration.log_purchase_attempt(
            platform="Nike",
            product_name="Air Jordan 1",
            product_size="10.5",
            stage="checkout",
            success=True,
            order_id="ORDER-123456"
        )

        # End the run
        bot_integration.end_bot_run(
            success=True,
            result="purchase_successful",
            captcha_required=True,
            captcha_solved=True,
            queue_detected=False,
            detection_triggered=False
        )
```

### Account Management

```python
# Get random account for platform
account = bot_integration.get_random_account("Nike")

# Get all accounts
accounts = bot_integration.get_all_accounts("Adidas")

# Create new account
account_id = bot_integration.create_account(
    platform="Nike",
    email="user@example.com",
    password="SecurePassword123!",
    username="nike_user",
    account_name="Main Nike Account"
)

# Get specific account
account = bot_integration.get_account("Nike", account_id)
```

### Analytics & Metrics

```python
# Get platform metrics (last 7 days)
metrics = bot_integration.get_platform_metrics("Nike", days=7)
# Returns: {
#     "platform": "Nike",
#     "total_attempts": 150,
#     "successful_attempts": 95,
#     "failed_attempts": 55,
#     "success_rate": "63.33%",
#     ...
# }

# Get bot type metrics
stats = bot_integration.get_bot_type_metrics("Nike", "nike_purchase", days=7)

# Get dashboard overview
overview = bot_integration.get_dashboard_overview()

# Get CAPTCHA analytics
captcha_stats = bot_integration.get_captcha_analytics(days=30)

# Get proxy statistics
proxy_stats = bot_integration.get_proxy_stats()

# Get detection analysis
detection = bot_integration.get_detection_analysis(days=7)
```

### Generate Research Reports

```python
# Generate platform report
report = bot_integration.generate_platform_report("Nike", days=30)

# Generate bot type report
bot_report = bot_integration.generate_bot_type_report("Nike", "nike_purchase", days=7)

# Generate attack vector analysis
attack_vectors = bot_integration.generate_attack_vector_analysis()

# Save reports
bot_integration.save_report(report, "nike_platform_analysis")
bot_integration.save_report_html(report, "nike_platform_analysis")
```

## Database Schema

### accounts
Stores bot account credentials and metadata.

```sql
- id (uuid) - Primary key
- platform (text) - Platform name (Nike, Adidas, etc.)
- email (text) - Account email
- password_encrypted (text) - Encrypted password
- username (text) - Optional username
- account_name (text) - Friendly account name
- status (text) - active/inactive
- created_at (timestamp)
- last_used (timestamp)
- success_count (integer) - Successful runs
- failure_count (integer) - Failed runs
- notes (text) - Optional notes
- metadata (jsonb) - Custom data
```

### bot_runs
Detailed tracking of each bot execution.

```sql
- id (uuid) - Primary key
- session_id (uuid) - Reference to session
- account_id (uuid) - Reference to account
- platform (text) - Platform name
- bot_type (text) - Type of bot
- sneaker_name (text) - Product targeted
- target_size (text) - Target size
- status (text) - pending/completed/failed
- result (text) - Outcome
- started_at (timestamp)
- completed_at (timestamp)
- duration_ms (integer) - Execution time
- error_message (text) - Error details
- captcha_required (boolean)
- captcha_solved (boolean)
- queue_detected (boolean)
- detection_triggered (boolean)
- success (boolean) - Was it successful
- metadata (jsonb) - Custom data
```

### analytics_metrics
Aggregated metrics for analysis.

```sql
- id (uuid)
- platform (text)
- bot_type (text)
- metric_date (date)
- total_attempts (integer)
- successful_attempts (integer)
- failed_attempts (integer)
- average_duration_ms (integer)
- captcha_success_rate (numeric)
- detection_rate (numeric)
- success_rate (numeric)
```

## Security Considerations

### Row Level Security (RLS)
All tables have RLS enabled with permissive policies for the research environment. In production, implement restrictive policies based on user authentication.

### Password Encryption
Account passwords should be encrypted before storage. Use the encryption module:

```python
from cryptography.fernet import Fernet

# Generate a key (store securely)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt password
encrypted = cipher.encrypt(password.encode()).decode()
```

### API Key Management
- Store Supabase keys in environment variables
- Never commit .env to version control
- Use anon key for client-side operations
- Use service_role key for server-side admin operations

## Performance Optimization

### Indexes
Automatically created on:
- accounts (platform, status)
- bot_runs (platform, account_id, status, created_at)
- analytics_metrics (platform, metric_date)

### Query Best Practices
```python
# Use filters to reduce data transfer
from src.dashboard_api import get_dashboard_api

api = get_dashboard_api()

# Get only recent data
recent_metrics = api.get_platform_stats("Nike", days=7)

# Aggregate at database level
stats = bot_integration.get_bot_type_metrics("Nike", "nike_purchase")
```

## Monitoring & Alerts

### Connection Status
```python
status = bot_integration.get_connection_status()
# Returns: {
#     "supabase": true,
#     "analytics": true,
#     "dashboard": true,
#     "reports": true
# }

if not status["supabase"]:
    # Fallback to local SQLite
    pass
```

### Error Handling
```python
try:
    with bot_integration.track_bot_session(...):
        # Bot operations
        pass
except Exception as e:
    logger.error(f"Bot session failed: {e}")
    # Metrics still recorded in local cache
    # Will sync to Supabase when connection restored
```

## Troubleshooting

### Connection Issues
```bash
# Test connection
python3 -c "from src.supabase_client import get_supabase_manager; db = get_supabase_manager(); print('Connected!' if db.is_connected() else 'Failed')"
```

### Missing Tables
The schema is created automatically on first connection. If tables are missing:

1. Check `.env` has correct Supabase credentials
2. Verify Supabase project is active
3. Check API key has correct permissions
4. Tables will be created by the migration system

### Data Not Syncing
```python
# Check integration status
integration = get_bot_integration()
status = integration.get_connection_status()
print(f"Supabase: {status['supabase']}")

# Falls back to local SQLite if Supabase unavailable
```

## Next Steps

1. Set up Supabase project
2. Add environment variables
3. Start using bot_integration in your bots
4. Monitor metrics in dashboard
5. Generate research reports regularly

## Support & Documentation

- [Supabase Docs](https://supabase.com/docs)
- [Supabase Python SDK](https://github.com/supabase/supabase-py)
- [SneakerBot Ultimate Docs](./README.md)
- [Security Analysis](./SECURITY_ANALYSIS.md)

## Examples Repository

See `/examples` directory for complete integration examples.
