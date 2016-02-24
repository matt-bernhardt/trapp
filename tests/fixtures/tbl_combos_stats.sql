/*
SQLyog Community v12.2.0 (64 bit)
MySQL - 10.1.11-MariaDB : Database - scouting
*********************************************************************
*/
USE trapp;

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

/*Table structure for table `tbl_combos_stats` */

DROP TABLE IF EXISTS `tbl_combos_stats`;

CREATE TABLE `tbl_combos_stats` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ComboID` int(10) unsigned NOT NULL,
  `Year` int(4) unsigned NOT NULL,
  `CompetitionID` int(10) unsigned NOT NULL,
  `TeamID` int(10) unsigned NOT NULL DEFAULT '11',
  `GP` int(10) unsigned NOT NULL,
  `Min` int(10) unsigned NOT NULL,
  `Plus` tinyint(3) unsigned NOT NULL,
  `Minus` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=25873 DEFAULT CHARSET=latin1;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
