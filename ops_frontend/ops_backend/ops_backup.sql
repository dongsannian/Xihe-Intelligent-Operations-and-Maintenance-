PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
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
INSERT INTO user VALUES(1,'u1','$2b$12$5UeYBYN6/hIMl6.9wEvgY.pGmUMsukGGw2f597nFIkhvbsGy6.nnC','13800000000','user','2025-08-14 03:45:39');
INSERT INTO user VALUES(2,'王五','$2b$12$fBmxDNW.iZ1fAFMy0A1V7OPd19L/IA53BdlCU7lVjp0qt4/uMs0lS','12345678955','user','2025-08-14 08:39:44');
INSERT INTO user VALUES(3,'admin','$2b$12$7WZVzI1.USMZOPUs.BTvGegC48DValKg1HexMm8lsJbDzsCUqnn3a','','user','2025-08-14 10:56:30');
INSERT INTO user VALUES(4,'lmh','$2b$12$Q.X4TGLG8jdZgMZnyOirCuNqTFZubdpjBnI/lCjjf3up57VRNbu6e','','user','2025-08-14 11:18:43');
INSERT INTO user VALUES(5,'1111','$2b$12$GB8/Khd2G.gYtvvG737rBOFyqoy5O5cNnCWRoUFNEfwx9Wxsnhr.G','','user','2025-08-14 13:31:32');
INSERT INTO user VALUES(6,'123','$2b$12$sy871fAk3d7cCURzxtSaw.P9yz1sLUqe0GPASnBqARuWQrHjxqnG.','','user','2025-08-14 22:46:01');
INSERT INTO user VALUES(7,'liminghui','$2b$12$JKSKHKM3bVarCpvngiqpoOVm/frDTyeAqd59lKCsdaRHkZYkx8yo.','','user','2025-08-15 04:25:41');
INSERT INTO user VALUES(8,'xiaoming','$2b$12$7HWSQ9Je/6RylY8nKSxN6.U9UKhcVol3CRbre0H3aBzQ6q73Iy.Uu','','user','2025-08-15 06:04:53');
INSERT INTO user VALUES(9,'liming','$2b$12$w7F.1o9ZEXbIkEYMWrJv7..mI6.5l014uDQOpaNcIC6DsHQUxxvRO','','user','2025-08-15 09:33:34');
INSERT INTO user VALUES(10,'xiaoli','$2b$12$wR0WQkwcmR8u/b1fjRJ4N.edv2MT2igK1vMn5NO9VT1mAYOqUN1uq','','user','2025-08-15 10:54:50');
INSERT INTO user VALUES(11,'xihe','$2b$12$B4/9.bDxcsjLZXDE94/XXOV7nN9dhnc3OIshjzsVqJoGpp0zIdSr.','','user','2025-08-15 13:46:08');
INSERT INTO user VALUES(12,'xihezhiwei','$2b$12$f9gQsGEJ/G2UNvdqFufPpuavvyPtnb7Y2ZRTHNuLpdGyi.Y7GXz0y','','user','2025-08-15 13:50:36');
INSERT INTO user VALUES(13,'yunweiguanjia','$2b$12$.0MzzyV9a2F7aclWhIEDLeYt7dgQ.e.efsL.JQgIa5LB/1e0SUS1.','','user','2025-08-15 14:53:31');
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
COMMIT;
