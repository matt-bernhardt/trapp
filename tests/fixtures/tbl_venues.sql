/*
SQLyog Community v11.31 (64 bit)
MySQL - 5.5.36-MariaDB : Database - trapp
*********************************************************************
*/
USE trapp;

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*Table structure for table `tbl_venues` */

DROP TABLE IF EXISTS `tbl_venues`;

CREATE TABLE `tbl_venues` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `VenueName` varchar(100) DEFAULT NULL,
  `VenueCity` varchar(100) DEFAULT '',
  `VenueState` varchar(20) DEFAULT NULL,
  `VenueCountry` varchar(30) DEFAULT 'USA',
  `VenueZip` varchar(7) DEFAULT NULL,
  `VenueURL` varchar(255) DEFAULT NULL,
  `AltWXURL` varchar(255) DEFAULT NULL,
  `TenantID` varchar(255) DEFAULT NULL,
  `VenueCampus` varchar(255) DEFAULT NULL,
  `FieldSurface` varchar(100) DEFAULT NULL,
  `FansGuideURL` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
