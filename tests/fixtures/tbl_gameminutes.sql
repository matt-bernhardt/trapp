/*
SQLyog Community v10.3 
MySQL - 5.5.28-log : Database - trapp
*********************************************************************
*/
USE trapp;

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*Table structure for table `tbl_gameminutes` */

DROP TABLE IF EXISTS `tbl_gameminutes`;

CREATE TABLE `tbl_gameminutes` (
  `ID` double NOT NULL AUTO_INCREMENT,
  `GameID` int(11) DEFAULT NULL,
  `TeamID` double DEFAULT NULL,
  `PlayerID` double DEFAULT NULL,
  `TimeOn` tinyint(3) unsigned DEFAULT '0',
  `TimeOff` tinyint(3) unsigned DEFAULT '0',
  `Ejected` int(11) DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`ID`),
  KEY `ID_2` (`ID`),
  KEY `GameID` (`GameID`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
