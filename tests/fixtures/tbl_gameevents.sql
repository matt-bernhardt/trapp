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
/*Table structure for table `tbl_gameevents` */

DROP TABLE IF EXISTS `tbl_gameevents`;

CREATE TABLE `tbl_gameevents` (
  `ID` double NOT NULL AUTO_INCREMENT,
  `GameID` double DEFAULT NULL,
  `TeamID` double DEFAULT NULL,
  `MinuteID` tinyint(4) unsigned DEFAULT NULL,
  `Event` tinyint(2) unsigned DEFAULT NULL,
  `PlayerID` double DEFAULT NULL,
  `Notes` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`ID`),
  KEY `ID_2` (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
