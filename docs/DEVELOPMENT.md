# SneakerBot Ultimate - Development Guide

## Project Architecture

### Core Components

#### 1. **Supabase Client** (`src/supabase_client.py`)
Central database abstraction layer managing all Supabase operations.

**Key Classes:**
- `SupabaseManager` - Manages database connections and operations
  - Account management (create, retrieve, update)
  - Bot session tracking
  - Bot run recording
  - Purchase attempt logging
  - Analytics metrics aggregation
  - Proxy performance tracking

**Features:**
- Fallback to local SQLite if Supabase unavailable
- Connection pooling and caching
- Error logging and recovery
- Type hints for IDE support

#### 2. **Analytics Engine** (`src/analytics.py`)
Comprehensive metrics collection and tracking system.

**Key Classes:**
- `Analytics` - Tracks bot performance metrics
  - Session management
  - Performance event logging
  - CAPTCHA attempt recording
  - Purchase tracking
  - Notification logging

**Data Classes:**
- `BotRunMetrics` - Encapsulates bot run metrics
- `PerformanceEvent` - Individual performance events

#### 3. **Dashboard API** (`src/dashboard_api.py`)
REST-like API for dashboard and reporting needs.

**Key Classes:**
- `DashboardAPI` - Provides analytics endpoints
  - Platform overview and statistics
  - Account analytics
  - CAPTCHA and proxy analytics
  - Daily trending
  - Detection analysis
  - Data export (JSON)

#### 4. **Research Reports** (`src/research_reports.py`)
Automated research report generation from collected data.

**Key Classes:**
- `ResearchReportGenerator` - Generates comprehensive reports
  - Platform analysis reports
  - Bot type analysis
  - Cross-platform comparisons
  - Attack vector effectiveness
  - Defense effectiveness evaluation
  - HTML and JSON export

#### 5. **Bot Integration** (`src/bot_integration.py`)
Central hub connecting all components together.

**Key Features:**
- Context managers for session and run tracking
- Unified API for all bot operations
- Account management interface
- Analytics aggregation
- Report generation interface
- Connection status monitoring

#### 6. **Enhanced Account Manager** (`src/account_manager.py`)
Account management supporting both SQLite and Supabase.

**Key Features:**
- Dual-backend support (SQLite/Supabase auto-selection)
- Account CRUD operations
- Usage statistics tracking
- Multi-platform account support

## Database Schema

### Tables

**accounts**
```sql
- id: uuid (primary key)
- platform: text
- email: text (unique)
- password_encrypted: text
- username: text
- account_name: text
- status: text (active/inactive)
- created_at: timestamp
- last_used: timestamp
- success_count: integer
- failure_count: integer
- metadata: jsonb
```

**bot_sessions**
```sql
- id: uuid (primary key)
- account_id: uuid (foreign key)
- platform: text
- session_token: text (unique)
- browser_fingerprint: jsonb
- proxy_used: text
- user_agent: text
- status: text (active/expired)
- created_at: timestamp
- expires_at: timestamp
```

**bot_runs**
```sql
- id: uuid (primary key)
- session_id: uuid (foreign key)
- account_id: uuid (foreign key)
- platform: text
- bot_type: text
- sneaker_name: text
- target_size: text
- status: text (pending/completed/failed)
- result: text
- started_at: timestamp
- completed_at: timestamp
- duration_ms: integer
- error_message: text
- captcha_required: boolean
- captcha_solved: boolean
- queue_detected: boolean
- detection_triggered: boolean
- success: boolean
- metadata: jsonb
```

**analytics_metrics**
```sql
- id: uuid
- platform: text
- bot_type: text
- metric_date: date
- total_attempts: integer
- successful_attempts: integer
- failed_attempts: integer
- average_duration_ms: integer
- captcha_success_rate: numeric
- detection_rate: numeric
- success_rate: numeric
```

**captcha_attempts**
```sql
- id: uuid
- bot_run_id: uuid (foreign key)
- platform: text
- captcha_type: text
- solver_service: text
- success: boolean
- solve_time_ms: integer
- cost: numeric
- created_at: timestamp
```

**proxy_performance**
```sql
- id: uuid
- proxy_address: text
- platform: text
- success_count: integer
- failure_count: integer
- average_response_time_ms: integer
- detection_count: integer
- last_tested: timestamp
- last_success: timestamp
```

**research_sessions**
```sql
- id: uuid
- name: text
- platform: text
- description: text
- started_at: timestamp
- completed_at: timestamp
- status: text (active/completed)
- total_runs: integer
- successful_runs: integer
- failed_runs: integer
- research_findings: text
- metadata: jsonb
```

## Code Patterns

### Session Tracking Pattern

```python
from src.bot_integration import get_bot_integration

integration = get_bot_integration()

# Session context manager automatically:
# - Creates session record
# - Tracks all bot runs
# - Updates account last_used
# - Handles cleanup on exit
with integration.track_bot_session(account_id, platform, fingerprint, proxy):
    with integration.track_bot_run(platform, bot_type, product, size):
        # All operations automatically tracked
        integration.log_bot_event(...)
        integration.log_captcha_attempt(...)
        integration.end_bot_run(success=True)
```

### Error Handling Pattern

```python
try:
    with integration.track_bot_session(...):
        # Operations
        pass
except Exception as e:
    # Errors are logged automatically
    # Supabase connection failures fall back to local SQLite
    # Data syncs when connection restored
    logger.error(f"Session failed: {e}")
```

### Analytics Pattern

```python
# Metrics are aggregated at database level
metrics = integration.get_platform_metrics("Nike", days=7)

# Results include:
# - Total attempts
# - Success rates
# - CAPTCHA effectiveness
# - Detection rates
# - Average durations

# Export for reporting
report = integration.generate_platform_report("Nike", days=30)
integration.save_report(report, "nike_analysis")
```

## Integration Points

### With Nike Bot
```python
from src.nike_bot import NikeBot
from src.bot_integration import get_bot_integration

integration = get_bot_integration()
account = integration.get_random_account("Nike")

with integration.track_bot_session(account["id"], "Nike"):
    with integration.track_bot_run("Nike", "nike_purchase", "Jordan 1", "10.5"):
        bot = NikeBot(account["email"], account["password"])
        # Bot operations are automatically tracked
```

### With Other Bots
All bot implementations can be integrated the same way by wrapping with context managers.

## Testing

### Unit Tests
```python
# Test account manager
from src.account_manager import AccountManager

am = AccountManager(use_supabase=False)  # Use local SQLite for tests
account_id = am.create_account("Nike", "test@example.com", "password")
assert account_id is not None
```

### Integration Tests
```python
# Test full bot session
from src.bot_integration import get_bot_integration

integration = get_bot_integration()
with integration.track_bot_session(...):
    with integration.track_bot_run(...):
        # Verify data is stored
        metrics = integration.get_platform_metrics(...)
        assert metrics["total_attempts"] > 0
```

## Performance Considerations

### Database Indexes
Automatically created on:
- accounts (platform, status)
- bot_runs (platform, account_id, status, created_at)
- analytics_metrics (platform, metric_date)

### Query Optimization
```python
# Efficient: Filters applied at database level
metrics = integration.get_platform_metrics("Nike", days=7)

# Inefficient: Would pull all data
all_data = integration.db.client.table("bot_runs").select("*").execute()
```

### Caching
- Supabase manager is singleton (cached in memory)
- Analytics instance is singleton
- Connection pooling handled by Supabase SDK

## Monitoring

### Connection Health
```python
status = integration.get_connection_status()
if not status["supabase"]:
    # Fallback to local SQLite
    logger.warning("Supabase unavailable, using local storage")
```

### Error Tracking
All errors are logged to console and file. Check `bot.log` for issues.

## Deployment

### Production Setup
1. Set Supabase environment variables
2. Run database migrations (automatic on first connection)
3. Implement stricter RLS policies
4. Enable backups in Supabase settings
5. Monitor performance with Supabase analytics

### Local Development
1. Use .env.example as template
2. SQLite fallback works out of the box
3. No Supabase required for development
4. All analytics available locally when Supabase unavailable

## Future Enhancements

### Planned Features
1. Real-time analytics dashboard (WebSockets)
2. Advanced ML-based detection evasion analysis
3. Multi-tenant support for bot operators
4. Advanced query builder for custom reports
5. Bot optimization recommendations
6. Geographic distribution analysis
7. Behavioral pattern matching
8. Predictive success rate modeling

### Extension Points
- Add custom metrics to `Analytics` class
- Create new report types in `ResearchReportGenerator`
- Extend dashboard with new endpoints in `DashboardAPI`
- Add new table structures in Supabase migrations

## Contributing

### Code Standards
- Type hints for all functions
- Docstrings for classes and public methods
- Error handling with logging
- Follows PEP 8 style guide
- No hardcoded values (use config/env)

### Pull Request Process
1. Create feature branch
2. Add/update tests
3. Update documentation
4. Verify all tests pass
5. Submit PR with description

### Documentation
- Update docs/ for user-facing changes
- Update docstrings for code changes
- Include examples for new features
- Document database schema changes

## Troubleshooting

### Supabase Connection Fails
- Verify SUPABASE_URL and SUPABASE_ANON_KEY in .env
- Check Supabase project is active
- Verify network connectivity
- Falls back to local SQLite automatically

### Data Not Syncing
- Check connection status: `integration.get_connection_status()`
- Review logs in `bot.log`
- Verify table permissions in Supabase

### Import Errors
```bash
# Install missing dependencies
pip install -r requirements.txt

# Verify installations
python3 -c "import supabase; print('OK')"
```

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Python SDK](https://github.com/supabase/supabase-py)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Security Analysis Guide](./SECURITY_ANALYSIS.md)
- [API Documentation](./API.md)
