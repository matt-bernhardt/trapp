/*
SQLyog Community v10.3 
MySQL - 5.5.28-log : Database - trapp
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
USE `trapp`;

/*Table structure for table `tbl_gamestats` */

DROP TABLE IF EXISTS `tbl_gamestats`;

CREATE TABLE `tbl_gamestats` (
  `ID` double NOT NULL AUTO_INCREMENT,
  `GameID` double NOT NULL DEFAULT '0',
  `TeamID` double NOT NULL DEFAULT '0',
  `PlayerID` double NOT NULL DEFAULT '0',
  `Goals` tinyint(2) unsigned DEFAULT '0',
  `Ast` tinyint(2) unsigned DEFAULT '0',
  `Shots` tinyint(2) unsigned DEFAULT '0',
  `SOG` tinyint(2) unsigned DEFAULT '0',
  `FC` tinyint(2) unsigned DEFAULT '0',
  `FS` tinyint(2) unsigned DEFAULT '0',
  `Off` tinyint(2) unsigned DEFAULT '0',
  `CK` tinyint(2) unsigned DEFAULT NULL,
  `Blk` tinyint(2) unsigned DEFAULT NULL,
  `YC` tinyint(2) unsigned DEFAULT NULL,
  `RC` tinyint(2) unsigned DEFAULT NULL,
  `ShotsFaced` tinyint(2) unsigned DEFAULT NULL,
  `Saves` tinyint(2) unsigned DEFAULT NULL,
  `GA` tinyint(2) unsigned DEFAULT NULL,
  `CP` tinyint(2) unsigned DEFAULT NULL,
  `Plus` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `Minus` tinyint(2) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`ID`),
  KEY `ID_2` (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
