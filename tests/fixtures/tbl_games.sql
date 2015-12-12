/*
SQLyog Community v10.3 
MySQL - 5.5.28-log : Database - scouting
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*Table structure for table `tbl_games` */

DROP TABLE IF EXISTS `tbl_games`;

CREATE TABLE `tbl_games` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `MatchTime` datetime DEFAULT NULL,
  `MatchTypeID` int(10) unsigned NOT NULL DEFAULT '0',
  `HteamID` int(11) DEFAULT NULL,
  `Hscore` int(11) DEFAULT '0',
  `AteamID` int(11) DEFAULT NULL,
  `Ascore` int(11) DEFAULT '0',
  `VenueID` int(11) DEFAULT NULL,
  `Duration` int(11) unsigned NOT NULL DEFAULT '0',
  `Attendance` int(11) DEFAULT NULL,
  `MeanTemperature` int(3) unsigned DEFAULT NULL COMMENT 'Mean Daily Temperature, from Weather Underground',
  `Precipitation` double(2,1) DEFAULT NULL,
  `WeatherEvents` varchar(255) NOT NULL DEFAULT '""',
  `Notes` text,
  PRIMARY KEY (`ID`),
  KEY `EventDate` (`MatchTime`),
  KEY `HTeamID` (`HteamID`),
  KEY `ATeamID` (`AteamID`)
) ENGINE=MyISAM AUTO_INCREMENT=17216 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
