/*
  # SneakerBot Ultimate Core Schema

  Core tables for bot research and analytics
*/

CREATE TABLE IF NOT EXISTS accounts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  platform text NOT NULL,
  email text NOT NULL,
  password_encrypted text NOT NULL,
  username text,
  account_name text,
  status text DEFAULT 'active',
  created_at timestamptz DEFAULT now(),
  last_used timestamptz,
  success_count integer DEFAULT 0,
  failure_count integer DEFAULT 0,
  notes text,
  metadata jsonb
);

CREATE TABLE IF NOT EXISTS bot_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id uuid REFERENCES accounts(id),
  platform text NOT NULL,
  session_token text UNIQUE,
  browser_fingerprint jsonb,
  proxy_used text,
  user_agent text,
  status text DEFAULT 'active',
  created_at timestamptz DEFAULT now(),
  expires_at timestamptz,
  metadata jsonb
);

CREATE TABLE IF NOT EXISTS bot_runs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id uuid REFERENCES bot_sessions(id),
  account_id uuid REFERENCES accounts(id),
  platform text NOT NULL,
  bot_type text NOT NULL,
  sneaker_name text,
  target_size text,
  status text DEFAULT 'pending',
  result text,
  started_at timestamptz DEFAULT now(),
  completed_at timestamptz,
  duration_ms integer,
  error_message text,
  captcha_required boolean DEFAULT false,
  captcha_solved boolean DEFAULT false,
  queue_detected boolean DEFAULT false,
  detection_triggered boolean DEFAULT false,
  success boolean DEFAULT false,
  metadata jsonb
);

CREATE TABLE IF NOT EXISTS purchase_attempts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  bot_run_id uuid REFERENCES bot_runs(id),
  account_id uuid REFERENCES accounts(id),
  platform text NOT NULL,
  product_name text,
  product_size text,
  quantity integer DEFAULT 1,
  stage text,
  success boolean,
  completed_at timestamptz DEFAULT now(),
  order_id text,
  error_details jsonb
);

CREATE TABLE IF NOT EXISTS analytics_metrics (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  platform text NOT NULL,
  bot_type text,
  metric_date date DEFAULT CURRENT_DATE,
  total_attempts integer DEFAULT 0,
  successful_attempts integer DEFAULT 0,
  failed_attempts integer DEFAULT 0,
  average_duration_ms integer DEFAULT 0,
  captcha_success_rate numeric(5,2) DEFAULT 0,
  detection_rate numeric(5,2) DEFAULT 0,
  success_rate numeric(5,2) DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS captcha_attempts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  bot_run_id uuid REFERENCES bot_runs(id),
  platform text NOT NULL,
  captcha_type text,
  solver_service text,
  success boolean,
  solve_time_ms integer,
  cost numeric(8,4),
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS proxy_performance (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  proxy_address text NOT NULL,
  platform text,
  success_count integer DEFAULT 0,
  failure_count integer DEFAULT 0,
  average_response_time_ms integer DEFAULT 0,
  detection_count integer DEFAULT 0,
  last_tested timestamptz,
  last_success timestamptz,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS notifications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  bot_run_id uuid REFERENCES bot_runs(id),
  notification_type text,
  channel text,
  message text,
  success boolean,
  sent_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS research_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  platform text,
  description text,
  started_at timestamptz DEFAULT now(),
  completed_at timestamptz,
  status text DEFAULT 'active',
  total_runs integer DEFAULT 0,
  successful_runs integer DEFAULT 0,
  failed_runs integer DEFAULT 0,
  research_findings text,
  metadata jsonb
);

CREATE TABLE IF NOT EXISTS performance_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  bot_run_id uuid REFERENCES bot_runs(id),
  event_type text,
  event_name text,
  timestamp_ms integer,
  details jsonb,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE bot_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE bot_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE purchase_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE captcha_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE proxy_performance ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE research_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE performance_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "research_all" ON accounts FOR ALL USING (true);
CREATE POLICY "research_all" ON bot_sessions FOR ALL USING (true);
CREATE POLICY "research_all" ON bot_runs FOR ALL USING (true);
CREATE POLICY "research_all" ON purchase_attempts FOR ALL USING (true);
CREATE POLICY "research_all" ON analytics_metrics FOR ALL USING (true);
CREATE POLICY "research_all" ON captcha_attempts FOR ALL USING (true);
CREATE POLICY "research_all" ON proxy_performance FOR ALL USING (true);
CREATE POLICY "research_all" ON notifications FOR ALL USING (true);
CREATE POLICY "research_all" ON research_sessions FOR ALL USING (true);
CREATE POLICY "research_all" ON performance_logs FOR ALL USING (true);
