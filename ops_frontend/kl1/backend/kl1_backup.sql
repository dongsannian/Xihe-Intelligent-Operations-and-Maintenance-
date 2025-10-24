PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
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
INSERT INTO log_entries VALUES(1,'string','DEBUG','string','string',0,'2025-08-09 08:58:17','string',NULL);
INSERT INTO log_entries VALUES(2,'PrometheusAlert','WARNING','[FIRING] 测试告警 - CPU 使用率过高','TestAlert',NULL,'2025-10-06 19:30:00.000000',NULL,NULL);
INSERT INTO log_entries VALUES(3,'PrometheusAlert','WARNING','[FIRING] 自动测试告警 - CPU超过85%','TestAuto',NULL,'2025-10-07 02:50:00.000000',NULL,NULL);
INSERT INTO log_entries VALUES(4,'PrometheusAlert','WARNING','[FIRING] 内存测试告警 - 内存使用率超过80%','HighMemoryUsage',NULL,'2025-10-07 13:59:00.000000',NULL,NULL);
INSERT INTO log_entries VALUES(5,'PrometheusAlert','WARNING','[FIRING] 内存使用率过高 - 实例 localhost:9100 的内存使用率超过 80%，当前值 82.56766453547904%','HighMemoryUsage',NULL,'2025-10-12 15:59:33.531000',NULL,NULL);
INSERT INTO log_entries VALUES(6,'PrometheusAlert','WARNING','[FIRING] 内存使用率过高 - 实例 localhost:9100 的内存使用率超过 80%，当前值 82.28789576799349%','HighMemoryUsage',NULL,'2025-10-13 02:34:48.531000',NULL,NULL);
INSERT INTO log_entries VALUES(7,'PrometheusAlert','INFO','[RESOLVED] 内存使用率过高 - 实例 localhost:9100 的内存使用率超过 80%，当前值 84.10024510001533%','HighMemoryUsage',NULL,'2025-10-13 02:34:48.531000',NULL,NULL);
INSERT INTO log_entries VALUES(8,'PrometheusAlert','WARNING','[FIRING] 内存使用率过高 - 实例 localhost:9100 的内存使用率超过 80%，当前值 89.28342511146407%','HighMemoryUsage',NULL,'2025-10-13 03:09:48.531000',NULL,NULL);
INSERT INTO log_entries VALUES(9,'PrometheusAlert','WARNING','[FIRING] 内存使用率过高 - 实例 localhost:9100 的内存使用率超过 80%，当前值 88.01801565737598%','HighMemoryUsage',NULL,'2025-10-13 15:10:18.531000',NULL,NULL);
INSERT INTO log_entries VALUES(10,'PrometheusAlert','WARNING','[FIRING] 内存使用率过高 - 实例 localhost:9100 的内存使用率超过 80%，当前值 95.12551297659456%','HighMemoryUsage',NULL,'2025-10-13 15:10:18.531000',NULL,NULL);
INSERT INTO log_entries VALUES(11,'PrometheusAlert','INFO','[RESOLVED] 内存使用率过高 - 实例 localhost:9100 的内存使用率超过 80%，当前值 95.58215284888455%','HighMemoryUsage',NULL,'2025-10-13 15:10:18.531000',NULL,NULL);
INSERT INTO log_entries VALUES(12,'PrometheusAlert','WARNING','[FIRING] 内存使用率过高 - 实例 localhost:9100 的内存使用率超过 80%，当前值 81.06148866009303%','HighMemoryUsage',NULL,'2025-10-16 08:19:18.531000',NULL,NULL);
INSERT INTO log_entries VALUES(13,'PrometheusAlert','INFO','[RESOLVED] 内存使用率过高 - 实例 localhost:9100 的内存使用率超过 80%，当前值 80.07141359821335%','HighMemoryUsage',NULL,'2025-10-16 08:19:18.531000',NULL,NULL);
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
CREATE INDEX ix_log_entries_id ON log_entries (id);
CREATE INDEX ix_log_entries_source ON log_entries (source);
CREATE INDEX ix_log_entries_level ON log_entries (level);
CREATE INDEX ix_log_entries_timestamp ON log_entries (timestamp);
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE INDEX ix_users_id ON users (id);
CREATE UNIQUE INDEX ix_users_username ON users (username);
COMMIT;
