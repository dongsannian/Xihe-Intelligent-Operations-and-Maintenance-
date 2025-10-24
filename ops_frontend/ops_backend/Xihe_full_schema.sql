CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(64) NOT NULL, 
	password VARCHAR(128) NOT NULL, 
	phone VARCHAR(20), 
	role VARCHAR(20) NOT NULL, 
	create_time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username)
);
CREATE TABLE poll_task (
	id INTEGER NOT NULL, 
	name VARCHAR(128) NOT NULL, 
	hardware_type VARCHAR(32), 
	group_name VARCHAR(64), 
	status VARCHAR(16), 
	start_time DATETIME, 
	end_time DATETIME, 
	create_time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE status_snapshot (
	id INTEGER NOT NULL, 
	gpu_usage VARCHAR(16), 
	cpu_usage VARCHAR(16), 
	memory_usage VARCHAR(16), 
	disk_usage VARCHAR(16), 
	network_status VARCHAR(32), 
	temperature VARCHAR(16), 
	create_time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE overview (
	id INTEGER NOT NULL, 
	title VARCHAR(64), 
	description VARCHAR(128), 
	menu_key VARCHAR(32), 
	PRIMARY KEY (id)
);
CREATE TABLE alarm (
	id INTEGER NOT NULL, 
	type VARCHAR(32), 
	content VARCHAR(256), 
	status VARCHAR(16), 
	create_time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE poll_record (
	id INTEGER NOT NULL, 
	task_id INTEGER NOT NULL, 
	device_param VARCHAR(128), 
	status VARCHAR(16), 
	record_time DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(task_id) REFERENCES poll_task (id)
);
CREATE TABLE gpu_details (
	id INTEGER NOT NULL, 
	snapshot_id INTEGER NOT NULL, 
	utilization VARCHAR(16), 
	memory_usage VARCHAR(16), 
	memory_used VARCHAR(32), 
	memory_free VARCHAR(32), 
	encode_utilization VARCHAR(16), 
	decode_utilization VARCHAR(16), 
	PRIMARY KEY (id), 
	FOREIGN KEY(snapshot_id) REFERENCES status_snapshot (id)
);
CREATE TABLE cpu_details (
	id INTEGER NOT NULL, 
	snapshot_id INTEGER NOT NULL, 
	total_usage VARCHAR(16), 
	core_usage VARCHAR(64), 
	user_usage VARCHAR(16), 
	kernel_usage VARCHAR(16), 
	io_wait VARCHAR(16), 
	PRIMARY KEY (id), 
	FOREIGN KEY(snapshot_id) REFERENCES status_snapshot (id)
);
CREATE TABLE memory_details (
	id INTEGER NOT NULL, 
	snapshot_id INTEGER NOT NULL, 
	total VARCHAR(16), 
	used VARCHAR(16), 
	free VARCHAR(16), 
	buffers_cache VARCHAR(16), 
	swap_usage VARCHAR(32), 
	PRIMARY KEY (id), 
	FOREIGN KEY(snapshot_id) REFERENCES status_snapshot (id)
);
CREATE TABLE disk_details (
	id INTEGER NOT NULL, 
	snapshot_id INTEGER NOT NULL, 
	read_rate VARCHAR(16), 
	write_rate VARCHAR(16), 
	io_wait VARCHAR(16), 
	usage VARCHAR(16), 
	free_space VARCHAR(32), 
	PRIMARY KEY (id), 
	FOREIGN KEY(snapshot_id) REFERENCES status_snapshot (id)
);
CREATE TABLE network_details (
	id INTEGER NOT NULL, 
	snapshot_id INTEGER NOT NULL, 
	upload VARCHAR(16), 
	download VARCHAR(16), 
	packet_loss VARCHAR(16), 
	latency VARCHAR(16), 
	PRIMARY KEY (id), 
	FOREIGN KEY(snapshot_id) REFERENCES status_snapshot (id)
);
CREATE TABLE sys_log (
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	action VARCHAR(128), 
	log_time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
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
