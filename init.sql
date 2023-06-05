CREATE TABLE users (
    user_id INTEGER CHECK (user_id >= 1),
    PRIMARY KEY (user_id),
    birth_year INTEGER CHECK (birth_year >= 1900 AND birth_year <= 2023),
    country VARCHAR(3) CHECK (country ~ '^[A-Z]{3}$'),
    currency VARCHAR(3) CHECK (currency ~ '^[A-Z]{3}$'),
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
    registration_date TIMESTAMPTZ
);

CREATE TABLE events (
  begin_timestamp TIMESTAMPTZ,
  country VARCHAR(255),
  end_timestamp TIMESTAMPTZ,
  event_id UUID,
  league VARCHAR(255),
  participants VARCHAR(255)[2] CHECK (cardinality(participants) = 2),
  sport VARCHAR(255),
  PRIMARY KEY (event_id)
);

CREATE TABLE historical_events (
  event_id UUID PRIMARY KEY,
  result VARCHAR(10) CHECK (result IN ('home win', 'away win', 'draw')),
  goals_scored_home INT,
  goals_scored_away INT,
  shots_on_target_home INT,
  shots_on_target_away INT,
  total_shots_home INT,
  total_shots_away INT,
  possession_percentage_home DECIMAL(5, 2),
  possession_percentage_away DECIMAL(5, 2),
  pass_accuracy_home DECIMAL(5, 2),
  pass_accuracy_away DECIMAL(5, 2),
  fouls_committed_home INT,
  fouls_committed_away INT,
  corners_home INT,
  corners_away INT,
  yellow_cards_home INT,
  yellow_cards_away INT,
  red_cards_home INT,
  red_cards_away INT,
  offsides_home INT,
  offsides_away INT,
  saves_home INT,
  saves_away INT,
  FOREIGN KEY (event_id) REFERENCES events (event_id)
);


CREATE TABLE coupons (
  coupon_id UUID,
  selections JSONB,
  stake NUMERIC,
  timestamp TIMESTAMPTZ,
  user_id INTEGER CHECK (user_id >= 1),
  PRIMARY KEY (coupon_id)
);