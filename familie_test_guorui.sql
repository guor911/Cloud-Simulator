/*
SQLyog Enterprise v12.08 (32 bit)
MySQL - 5.7.9-log : Database - familie_test_guorui
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`familie_test_guorui` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `familie_test_guorui`;

/*Table structure for table `t_binary_conf` */

DROP TABLE IF EXISTS `t_binary_conf`;

CREATE TABLE `t_binary_conf` (
  `conf_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `conf_url` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `conf_type` tinyint(4) DEFAULT NULL,
  `conf_before` text COLLATE utf8_unicode_ci,
  `conf_after` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`conf_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Table structure for table `t_xml_conf` */

DROP TABLE IF EXISTS `t_xml_conf`;

CREATE TABLE `t_xml_conf` (
  `conf_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `conf_url` varchar(128) CHARACTER SET utf8 DEFAULT NULL,
  `conf_response` text CHARACTER SET utf8,
  `conf_request` text CHARACTER SET utf8,
  PRIMARY KEY (`conf_id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
