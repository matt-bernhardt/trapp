/*
SQLyog Community v10.3 
MySQL - 5.5.28-log : Database - scouting
*********************************************************************
*/
USE TRAPP;

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*Table structure for table `tbl_players` */

DROP TABLE IF EXISTS `tbl_players`;

CREATE TABLE `tbl_players` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `LastName` varchar(255) DEFAULT NULL,
  `FirstName` varchar(255) DEFAULT NULL,
  `Position` varchar(255) DEFAULT '',
  `RosterNumber` int(3) unsigned DEFAULT NULL,
  `Picture` varchar(50) DEFAULT 'coming_soon.gif',
  `Class` int(4) DEFAULT '0',
  `Eligible` char(1) NOT NULL DEFAULT '0',
  `College` varchar(255) DEFAULT '',
  `Current_Club` varchar(50) DEFAULT '',
  `ContractStatus` tinyint(3) unsigned DEFAULT NULL,
  `LastClub` varchar(50) DEFAULT NULL,
  `YouthClub` varchar(50) DEFAULT NULL,
  `Height_Feet` tinyint(4) DEFAULT NULL,
  `Height_Inches` tinyint(4) DEFAULT NULL,
  `Birthplace` varchar(255) DEFAULT NULL,
  `HomeTown` varchar(255) DEFAULT NULL,
  `Citizenship` varchar(255) DEFAULT NULL,
  `Bio` text,
  `Visible` int(1) NOT NULL DEFAULT '0',
  `Award_Pts` double DEFAULT NULL,
  `Intl_Pts` double DEFAULT NULL,
  `Weight` double DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `Expansion2014` int(1) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `RosterID` (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=5203 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
