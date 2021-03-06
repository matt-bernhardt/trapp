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

/*Data for the table `lkp_matchtypes` */

insert into `lkp_matchtypes`(`ID`,`MatchType`,`CompetitionType`,`Official`) values (1,'MLS League','League',1);
insert into `lkp_matchtypes`(`ID`,`MatchType`,`CompetitionType`,`Official`) values (2,'MLS Playoffs','Playoffs',1);
insert into `lkp_matchtypes`(`ID`,`MatchType`,`CompetitionType`,`Official`) values (3,'MLS Cup','Playoffs',1);
insert into `lkp_matchtypes`(`ID`,`MatchType`,`CompetitionType`,`Official`) values (4,'MLS Preseason','Preseason',0);

/*Data for the table `lnk_players_combos` */

insert  into `lnk_players_combos`(`ID`,`ComboID`,`PlayerID`,`Exclude`) values (1,1,1,0);
insert  into `lnk_players_combos`(`ID`,`ComboID`,`PlayerID`,`Exclude`) values (2,1,2,0);
insert  into `lnk_players_combos`(`ID`,`ComboID`,`PlayerID`,`Exclude`) values (3,2,1,0);
insert  into `lnk_players_combos`(`ID`,`ComboID`,`PlayerID`,`Exclude`) values (4,2,2,1);
insert  into `lnk_players_combos`(`ID`,`ComboID`,`PlayerID`,`Exclude`) values (5,3,1,1);
insert  into `lnk_players_combos`(`ID`,`ComboID`,`PlayerID`,`Exclude`) values (6,3,2,0);
insert  into `lnk_players_combos`(`ID`,`ComboID`,`PlayerID`,`Exclude`) values (7,4,1,1);
insert  into `lnk_players_combos`(`ID`,`ComboID`,`PlayerID`,`Exclude`) values (8,4,2,1);

/*Data for the table `tbl_combos` */

insert  into `tbl_combos`(`ID`,`Description`) values (1,'1_0,2_0');
insert  into `tbl_combos`(`ID`,`Description`) values (2,'1_0,2_1');
insert  into `tbl_combos`(`ID`,`Description`) values (3,'1_1,2_0');
insert  into `tbl_combos`(`ID`,`Description`) values (4,'1_1,2_1');

/*Data for the table `tbl_games` */

insert  into `tbl_games`(`ID`,`MatchTime`,`MatchTypeID`,`HTeamID`,`HScore`,`ATeamID`,`AScore`,`VenueID`,`Duration`,`Attendance`,`Notes`) values (1,'1980-01-01 19:30:00',1,1,3,2,0,1,90,0,'Sample');
insert  into `tbl_games`(`ID`,`MatchTime`,`MatchTypeID`,`HTeamID`,`HScore`,`ATeamID`,`AScore`,`VenueID`,`Duration`,`Attendance`,`Notes`) values (2,'1980-01-08 19:30:00',1,2,0,1,0,2,90,0,'Sample');

/*Data for the table `tbl_gameevents` */

insert  into `tbl_gameevents`(`ID`,`GameID`,`TeamID`,`PlayerID`,`MinuteID`,`Event`,`Notes`) values (1,1,2,3,4,1,'');
insert  into `tbl_gameevents`(`ID`,`GameID`,`TeamID`,`PlayerID`,`MinuteID`,`Event`,`Notes`) values (2,0,0,0,0,0,'EditMe');

/*Data for the table `tbl_gameminutes` */

insert  into `tbl_gameminutes`(`ID`,`GameID`,`TeamID`,`PlayerID`,`TimeOn`,`TimeOff`,`Ejected`) values (1,1,2,3,0,90,0);
insert  into `tbl_gameminutes`(`ID`,`GameID`,`TeamID`,`PlayerID`,`TimeOn`,`TimeOff`,`Ejected`) values (2,0,0,0,0,0,0);

/*Data for the table `tbl_gamestats` */

insert  into `tbl_gamestats`(`ID`,`GameID`,`TeamID`,`PlayerID`,`Goals`,`Ast`,`Shots`,`SOG`,`FC`,`FS`,`Off`,`CK`,`Blk`,`YC`,`RC`,`ShotsFaced`,`Saves`,`GA`,`CP`,`Plus`,`Minus`) values (1,1,2,3,0,0,0,0,0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0);

/*Data for the table `tbl_players` */

insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (1,'the Rabbit','Harvey','Goalkeeper',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (2,'Rains','Claude','Defender',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (3,'Man','Invisible','Defender',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (4,'Phantom','','Midfielder',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (5,'Bogeyman','','Defender',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (6,'Gyfre','','Defender',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (7,'Potter','Harry','Midfielder',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Surrey, England',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (8,'Storm','Sue','Midfielder',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (9,'Griffin','','Defender',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (10,'Vehl','Mahr','Midfielder',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (11,'Faustus','Doctor','Midfielder',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (12,'Mephistopheles','','Midfielder',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (13,'Caine','Sebastian','Forward',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (14,'Hart','Amos','Forward',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Bedford Falls, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (15,'Player','Sample','Midfielder',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Oneonta, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (16,'Substitution','','Midfielder',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Oneonta, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (17,'Substitution','First','Midfielder',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Oneonta, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (18,'Substitution','Second','Midfielder',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Oneonta, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);
insert  into `tbl_players`(`ID`,`LastName`,`FirstName`,`Position`,`RosterNumber`,`Picture`,`Class`,`Eligible`,`College`,`Current_Club`,`ContractStatus`,`LastClub`,`YouthClub`,`Height_Feet`,`Height_Inches`,`Birthplace`,`HomeTown`,`Citizenship`,`Bio`,`Visible`,`Award_Pts`,`Intl_Pts`,`Weight`,`DOB`,`Expansion2014`) values (19,'Substitution','Third','Midfielder',NULL,'coming_soon.gif',0,'0','','',NULL,NULL,NULL,NULL,NULL,NULL,'Oneonta, NY',NULL,NULL,0,NULL,NULL,NULL,'1980-01-01',0);

/*Data for the table `tbl_teams` */

insert  into `tbl_teams`(`ID`,`teamname`) values (1,'Columbus Crew');
insert  into `tbl_teams`(`ID`,`teamname`) values (2,'D.C. United');
insert  into `tbl_teams`(`ID`,`teamname`) values (3,'Duplicate Sample Team');
insert  into `tbl_teams`(`ID`,`teamname`) values (4,'Duplicate Sample Team');

/*Data for the table `tbl_vnues` */

insert  into `tbl_venues`(`ID`,`VenueName`,`VenueCity`,`VenueState`,`VenueCountry`,`VenueZip`,`VenueURL`,`AltWXURL`,`TenantID`,`VenueCampus`,`FieldSurface`,`FansGuideURL`) values (1,'MAPFRE Stadium','Columbus','OH','USA','43211',NULL,NULL,NULL,NULL,NULL,NULL);
insert  into `tbl_venues`(`ID`,`VenueName`,`VenueCity`,`VenueState`,`VenueCountry`,`VenueZip`,`VenueURL`,`AltWXURL`,`TenantID`,`VenueCampus`,`FieldSurface`,`FansGuideURL`) values (2,'RFK Stadium','Washington','DC','USA','20003',NULL,NULL,NULL,NULL,NULL,NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
