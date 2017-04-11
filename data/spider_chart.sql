# ************************************************************
# Sequel Pro SQL dump
# Version 4529
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Database: spider_chart
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table cms_pull_day_logs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cms_pull_day_logs`;

CREATE TABLE `cms_pull_day_logs` (
  `group_name` varchar(50) NOT NULL DEFAULT '' COMMENT '频道英文名',
  `time_day` int(12) NOT NULL COMMENT '只存年月日的时间戳',
  `auto_check_count` int(11) DEFAULT NULL COMMENT '自动发布总数',
  `no_check_count` int(11) DEFAULT NULL COMMENT '不自动发布总数',
  KEY `idx_cms_pull_day_group_name` (`group_name`),
  KEY `idx_cms_pull_day_time` (`time_day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table cms_pull_logs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `cms_pull_logs`;

CREATE TABLE `cms_pull_logs` (
  `group_name` varchar(50) NOT NULL DEFAULT '' COMMENT '频道英文名',
  `time_hour` int(12) NOT NULL COMMENT '只存年月日时的时间戳',
  `auto_check_count` int(11) DEFAULT NULL COMMENT '自动发布总数',
  `no_check_count` int(11) DEFAULT NULL COMMENT '不自动发布总数',
  UNIQUE KEY `idx_pull_log_group_time` (`group_name`,`time_hour`),
  KEY `idx_pull_log_time` (`time_hour`),
  KEY `idx_pull_log_group` (`group_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table detect_mobile
# ------------------------------------------------------------

DROP TABLE IF EXISTS `detect_mobile`;

CREATE TABLE `detect_mobile` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `mobile_type` varchar(100) NOT NULL DEFAULT '' COMMENT '手机型号：ios、android、windows_phone',
  `dt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '扫码时间',
  PRIMARY KEY (`id`),
  KEY `idx_mobile_type` (`mobile_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table groups
# ------------------------------------------------------------

DROP TABLE IF EXISTS `groups`;

CREATE TABLE `groups` (
  `group_name` varchar(50) NOT NULL DEFAULT '' COMMENT '频道英文名'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table nodejs_thumb_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `nodejs_thumb_log`;

CREATE TABLE `nodejs_thumb_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `pic_url` varchar(500) NOT NULL DEFAULT '' COMMENT '原图URL',
  `thumb_url` varchar(500) NOT NULL DEFAULT '' COMMENT '缩图URL',
  `pic_size` int(10) NOT NULL COMMENT '原图大小',
  `thumb_size` int(10) NOT NULL COMMENT '缩图大小',
  `percentage` varchar(50) NOT NULL DEFAULT '0' COMMENT '百分比',
  `dt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '缩图时间',
  `pic_width` varchar(20) DEFAULT '' COMMENT '原图宽',
  `pic_height` varchar(20) DEFAULT '' COMMENT '原图高',
  `thumb_width` varchar(20) DEFAULT '' COMMENT '缩图请求的宽',
  `thumb_height` varchar(20) DEFAULT NULL COMMENT '缩图请求的高',
  PRIMARY KEY (`id`),
  KEY `idx_node_thumb_thumb_url` (`thumb_url`(255)),
  KEY `idx_node_thumb_percentage` (`percentage`),
  KEY `idx_node_thumb_dt` (`dt`),
  KEY `idx_node_thumb_pic_size` (`pic_size`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table spider_grab_day_logs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `spider_grab_day_logs`;

CREATE TABLE `spider_grab_day_logs` (
  `group_name` varchar(50) NOT NULL DEFAULT '' COMMENT '频道英文名',
  `time_day` int(12) NOT NULL COMMENT '只存年月日的时间戳',
  `grab_count` int(11) DEFAULT NULL COMMENT '抓取总数',
  KEY `idx_spider_grab_day_group_name` (`group_name`),
  KEY `idx_spider_grab_day_time` (`time_day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table spider_grab_logs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `spider_grab_logs`;

CREATE TABLE `spider_grab_logs` (
  `group_name` varchar(50) NOT NULL DEFAULT '' COMMENT '频道英文名',
  `time_hour` int(12) NOT NULL COMMENT '只存年月日时的时间戳',
  `grab_count` int(11) DEFAULT NULL COMMENT '抓取总数',
  UNIQUE KEY `idx_grab_log_time_group` (`group_name`,`time_hour`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table spider_push_day_logs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `spider_push_day_logs`;

CREATE TABLE `spider_push_day_logs` (
  `group_name` varchar(50) NOT NULL DEFAULT '' COMMENT 'CMS频道英文名',
  `time_day` int(12) NOT NULL COMMENT '只存年月日的时间戳',
  `push_count` int(11) DEFAULT NULL COMMENT '推送总数',
  `category_id` int(11) DEFAULT NULL COMMENT 'CMS分类ID',
  KEY `idx_spider_push_day_group_name` (`group_name`),
  KEY `idx_spider_push_day_time` (`time_day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table spider_push_logs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `spider_push_logs`;

CREATE TABLE `spider_push_logs` (
  `group_name` varchar(50) NOT NULL DEFAULT '' COMMENT 'CMS频道英文名',
  `time_hour` int(12) NOT NULL COMMENT '只存年月日时的时间戳',
  `push_count` int(11) DEFAULT NULL COMMENT '推送总数',
  `category_id` int(11) DEFAULT NULL COMMENT 'CMS分类ID',
  UNIQUE KEY `idx_push_log_time_cid` (`time_hour`,`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
