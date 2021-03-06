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

/*Table structure for table `lnk_players_combos` */

DROP TABLE IF EXISTS `lnk_players_combos`;

CREATE TABLE `lnk_players_combos` (
  `ID` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ComboID` int(10) unsigned NOT NULL,
  `PlayerID` int(10) unsigned NOT NULL,
  `Exclude` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ID`),
  KEY `ComboID` (`ComboID`),
  KEY `PlayerID` (`PlayerID`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
