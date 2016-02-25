apnic_ip_database | CREATE TABLE `apnic_ip_database` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `subnet` int(4) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `city_id` bigint(10) DEFAULT NULL,
  `ip` varchar(20) DEFAULT NULL,
  `region` varchar(50) DEFAULT NULL,
  `region_id` bigint(20) DEFAULT NULL,
  `isp_id` bigint(20) DEFAULT NULL,
  `isp` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=7626 DEFAULT CHARSET=utf8 
