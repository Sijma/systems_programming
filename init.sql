CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    birth_year INTEGER NOT NULL,
    country CHAR(3) NOT NULL,
    currency CHAR(3) NOT NULL,
    gender VARCHAR(6) NOT NULL,
    registration_date TIMESTAMP NOT NULL
);

CREATE TABLE events (
    event_id UUID PRIMARY KEY,
    begin_timestamp TIMESTAMP NOT NULL,
    end_timestamp TIMESTAMP NOT NULL,
    country CHAR(3) NOT NULL,
    league VARCHAR(255) NOT NULL,
    participants VARCHAR(255)[],
    sport VARCHAR(255) NOT NULL
);

CREATE TABLE coupons (
    coupon_id UUID PRIMARY KEY,
    stake NUMERIC(10,2) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(user_id)
);

CREATE TABLE selections (
    event_id UUID NOT NULL REFERENCES events(event_id),
    coupon_id UUID NOT NULL REFERENCES coupons(coupon_id),
    odds NUMERIC(4,2) NOT NULL,
    PRIMARY KEY (event_id, coupon_id)
);
