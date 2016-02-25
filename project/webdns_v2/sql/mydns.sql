ANY VIEW:

INSERT INTO `bind_letv_any`(zone, host, type, data, ttl, mx_priority, refresh, retry, expire, minimum, serial, resp_person) VALUES ('letv.com','@','soa','ns1.letv.com.',86400,NULL,3600,60,120,60,20130724,'webmaster.letv.com.');
INSERT INTO `bind_letv_any`(zone, host, type, data, ttl, mx_priority, refresh, retry, expire, minimum, serial, resp_person) VALUES ('letv.com','@','ns','ns1.letv.com.',172800,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `bind_letv_any`(zone, host, type, data, ttl, mx_priority, refresh, retry, expire, minimum, serial, resp_person) VALUES (1424,'letv.com','@','ns','ns2.letv.com.',172800,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `bind_letv_any`(zone, host, type, data, ttl, mx_priority, refresh, retry, expire, minimum, serial, resp_person) VALUES ('letv.com','ns1','a','115.182.94.238',86400,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `bind_letv_any`(zone, host, type, data, ttl, mx_priority, refresh, retry, expire, minimum, serial, resp_person) VALUES ('letv.com','ns2','a','115.182.94.238',86400,NULL,NULL,NULL,NULL,NULL,NULL,NULL);


CT VIEW:
INSERT INTO `bind_letv_ct`(zone, host, type, data, ttl, mx_priority, refresh, retry, expire, minimum, serial, resp_person) VALUES ('letv.com','@','soa','ns1.letv.com.',86400,NULL,3600,60,120,60,20130724,'webmaster.letv.com.');
INSERT INTO `bind_letv_ct`(zone, host, type, data, ttl, mx_priority, refresh, retry, expire, minimum, serial, resp_person) VALUES ('letv.com','@','ns','ns1.letv.com.',172800,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `bind_letv_ct`(zone, host, type, data, ttl, mx_priority, refresh, retry, expire, minimum, serial, resp_person) VALUES ('letv.com','@','ns','ns2.letv.com.',172800,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `bind_letv_ct`(zone, host, type, data, ttl, mx_priority, refresh, retry, expire, minimum, serial, resp_person) VALUES ('letv.com','ns1','a','115.182.94.238',86400,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
INSERT INTO `bind_letv_ct`(zone, host, type, data, ttl, mx_priority, refresh, retry, expire, minimum, serial, resp_person) VALUES ('letv.com','ns2','a','115.182.94.238',86400,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
