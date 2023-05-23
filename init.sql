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

CREATE TABLE coupons (
  coupon_id UUID,
  selections JSONB,
  stake NUMERIC,
  timestamp TIMESTAMPTZ,
  user_id INTEGER CHECK (user_id >= 1),
  PRIMARY KEY (coupon_id)
);