CREATE TABLE log_entries (
	id INTEGER NOT NULL, 
	source VARCHAR(100), 
	level VARCHAR(8), 
	message TEXT, 
	module VARCHAR(100), 
	line_number INTEGER, 
	timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
	extra TEXT, user_id VARCHAR(50), 
	PRIMARY KEY (id)
);
CREATE INDEX ix_log_entries_id ON log_entries (id);
CREATE INDEX ix_log_entries_source ON log_entries (source);
CREATE INDEX ix_log_entries_level ON log_entries (level);
CREATE INDEX ix_log_entries_timestamp ON log_entries (timestamp);
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(50), 
	email VARCHAR(100), 
	hashed_password VARCHAR(255), 
	full_name VARCHAR(100), 
	role VARCHAR(6), 
	is_active BOOLEAN, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	updated_at DATETIME, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE INDEX ix_users_id ON users (id);
CREATE UNIQUE INDEX ix_users_username ON users (username);
