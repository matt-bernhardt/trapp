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
/*Table structure for table `tbl_teams` */

DROP TABLE IF EXISTS `tbl_teams`;

CREATE TABLE `tbl_teams` (
  `ID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `teamname` varchar(100) DEFAULT '',
  `team3ltr` varchar(6) DEFAULT '',
  `TeamGfx32` varchar(100) DEFAULT '',
  `League` varchar(10) DEFAULT '',
  `TeamNickname` varchar(30) DEFAULT '',
  `HomeVenue` varchar(80) DEFAULT '',
  `ClubID` int(11) unsigned NOT NULL DEFAULT '0',
  `VenueID` int(11) DEFAULT '0',
  `YearFounded` int(4) unsigned zerofill DEFAULT '0000',
  `YearFolded` int(4) unsigned zerofill DEFAULT NULL,
  `HomeLocation` varchar(50) DEFAULT NULL,
  `TeamRadioEnglish` varchar(255) DEFAULT NULL,
  `TeamRadioEnglishURL` varchar(255) DEFAULT NULL,
  `TeamRadioESP` varchar(255) DEFAULT NULL,
  `TeamRadioESPURL` varchar(255) DEFAULT NULL,
  `TeamRadioOther` varchar(255) DEFAULT NULL,
  `TeamRadioOtherURL` varchar(255) DEFAULT NULL,
  `TeamRadioOtherDesc` varchar(50) DEFAULT NULL,
  `HomeLocationZip` varchar(7) DEFAULT NULL,
  `TeamURL` varchar(255) DEFAULT NULL,
  `TeamFanURL` varchar(255) DEFAULT NULL,
  `TeamFanURLName` varchar(255) DEFAULT NULL,
  `TeamWebcastURL` varchar(255) DEFAULT NULL,
  `TeamWebcastName` varchar(100) DEFAULT NULL,
  `TeamSB` varchar(50) DEFAULT NULL,
  `Conference` varchar(10) DEFAULT NULL,
  `ConferencePlace` tinyint(3) unsigned DEFAULT NULL,
  `Division` varchar(10) DEFAULT NULL,
  `DivisionPlace` tinyint(3) unsigned DEFAULT NULL,
  `Ranking` tinyint(3) unsigned DEFAULT NULL,
  `TeamRadioInfo` text,
  `GamesPlayed` tinyint(3) unsigned DEFAULT NULL,
  `GamesWon` tinyint(3) unsigned DEFAULT NULL,
  `GamesLost` tinyint(3) unsigned DEFAULT NULL,
  `GamesTied` tinyint(3) unsigned DEFAULT NULL,
  `GamesOTL` tinyint(3) unsigned DEFAULT NULL,
  `WinPct` double(15,3) DEFAULT NULL,
  `GoalsFor` double(12,0) DEFAULT NULL,
  `GoalsAgainst` double(12,0) DEFAULT NULL,
  `TotalPoints` decimal(3,1) DEFAULT NULL,
  `LastYearFinish` tinyint(3) unsigned DEFAULT NULL,
  `TeamRosterURL` varchar(255) DEFAULT NULL,
  `TicketsURL` varchar(255) DEFAULT NULL,
  `StadiumURL` varchar(255) DEFAULT NULL,
  `GoalDiff` double(12,0) DEFAULT NULL,
  `GamesWonHome` tinyint(3) DEFAULT NULL,
  `GamesWonAway` tinyint(3) DEFAULT NULL,
  `GamesLostHome` tinyint(3) DEFAULT NULL,
  `GamesLostAway` tinyint(3) DEFAULT NULL,
  `GamesTiedHome` tinyint(3) DEFAULT NULL,
  `GamesTiedAway` tinyint(3) DEFAULT NULL,
  `PowerPoints` double DEFAULT NULL,
  `PowerPPG` double DEFAULT NULL,
  `AdjPowerPoints` double(12,5) DEFAULT NULL,
  `ResultsList` varchar(255) DEFAULT NULL,
  `LastRanking` tinyint(3) unsigned DEFAULT NULL,
  `CurrentRanking` tinyint(3) unsigned DEFAULT NULL,
  `TeamRadioEnglishHome` char(1) DEFAULT NULL,
  `TeamRadioEnglishAway` char(1) DEFAULT NULL,
  `TeamRadioEnglishLimited` char(1) DEFAULT NULL,
  `TeamRadioESPHome` char(1) DEFAULT NULL,
  `TeamRadioESPAway` char(1) DEFAULT NULL,
  `TeamRadioESPLimited` char(1) DEFAULT NULL,
  `HeatIndex` double(12,5) DEFAULT NULL,
  `TeamGfx60` varchar(100) DEFAULT NULL,
  `LastFiveWon` tinyint(3) unsigned DEFAULT NULL,
  `LastFiveLost` tinyint(3) unsigned DEFAULT NULL,
  `LastFiveTied` tinyint(3) unsigned DEFAULT NULL,
  `LastFiveGF` tinyint(3) unsigned DEFAULT NULL,
  `LastFiveGA` tinyint(3) unsigned DEFAULT NULL,
  `PointsPerGame` double(7,5) DEFAULT NULL,
  `LastFivePPG` double(7,5) DEFAULT NULL,
  `ProjectedPoints` double(7,5) DEFAULT NULL,
  `TimeZone` char(2) DEFAULT NULL,
  `Eliminated` smallint(1) DEFAULT NULL,
  `Tiebreaker` tinyint(1) DEFAULT NULL,
  `TeamGfx40` varchar(100) DEFAULT NULL,
  `TeamGfx80` varchar(100) DEFAULT NULL,
  `TeamGfx160` varchar(100) DEFAULT NULL,
  `teamcountry` varchar(30) DEFAULT NULL,
  `MNNWebsite` varchar(255) DEFAULT NULL,
  `MNNWebsiteURL` varchar(255) DEFAULT NULL,
  `TeamStats` text,
  `Newspage` varchar(255) DEFAULT NULL,
  `NewspageURL` varchar(255) DEFAULT NULL,
  `NewspageCriteria` varchar(255) DEFAULT NULL,
  `TeamWebcastHome` char(1) DEFAULT NULL,
  `TeamWebcastAway` char(1) DEFAULT NULL,
  `TeamWebcastLimited` char(1) DEFAULT NULL,
  `OCQ` char(1) DEFAULT NULL,
  `MNNArticlesTable` varchar(100) DEFAULT NULL,
  `MNNArticlesDS` varchar(100) DEFAULT NULL,
  `MNNArticlesPage` varchar(255) DEFAULT NULL,
  `GoogleNews` varchar(255) DEFAULT NULL,
  `OpenCupTeam` tinyint(1) DEFAULT NULL,
  `ChampionsCupTeam` tinyint(1) DEFAULT NULL,
  `TeamHardware` text,
  `RSSNewsSource` varchar(255) DEFAULT NULL,
  `TeamNameCustom` varchar(255) DEFAULT NULL,
  `MaxPowerPoints` double(15,3) DEFAULT NULL,
  `AdjHeatIndex` double(15,3) DEFAULT NULL,
  `BlogID` int(11) DEFAULT NULL,
  `StubHubURL` varchar(250) DEFAULT NULL,
  `WCGroup` char(2) DEFAULT NULL,
  `WCPreviewID` int(11) NOT NULL DEFAULT '0',
  `NCAATeamSB` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`ID`),
  KEY `ID_2` (`ID`),
  KEY `TotalPoints` (`TotalPoints`,`teamname`),
  KEY `HeatIndex` (`League`,`HeatIndex`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
