/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2018/5/24 16:18:59                           */
/*==============================================================*/

drop database if exists mycinema ;
create database if not exists MyCinema;
use MyCinema;

SET NAMES utf8;

/*alter table Belong 
   drop foreign key FK_BELONG_BELONG_MOVIE;

alter table Belong 
   drop foreign key FK_BELONG_BELONG2_CATEGORY;

alter table Direct 
   drop foreign key FK_DIRECT_DIRECT_MOVIE;

alter table Direct 
   drop foreign key FK_DIRECT_DIRECT2_DIRECTOR;

alter table Play 
   drop foreign key FK_PLAY_PLAY_MOVIE;

alter table Play 
   drop foreign key FK_PLAY_PLAY2_ACTOR;

alter table Review 
   drop foreign key FK_REVIEW_REVIEW_MOVIE;

alter table Review 
   drop foreign key FK_REVIEW_REVIEW2_USER;

drop table if exists Actor;


alter table Belong 
   drop foreign key FK_BELONG_BELONG_MOVIE;

alter table Belong 
   drop foreign key FK_BELONG_BELONG2_CATEGORY;*/

/*drop table if exists Belong;

drop table if exists Category;*/


/*alter table Direct 
   drop foreign key FK_DIRECT_DIRECT_MOVIE;

alter table Direct 
   drop foreign key FK_DIRECT_DIRECT2_DIRECTOR;*/

/*drop table if exists Direct;

drop table if exists Director;

drop table if exists Movie;*/


/*alter table Play 
   drop foreign key FK_PLAY_PLAY_MOVIE;

alter table Play 
   drop foreign key FK_PLAY_PLAY2_ACTOR;*/

/*drop table if exists Play;*/


/*alter table Review 
   drop foreign key FK_REVIEW_REVIEW_MOVIE;

alter table Review
   drop foreign key FK_REVIEW_REVIEW2_USER;*/

/*drop table if exists Review;

drop table if exists User;*/

/*==============================================================*/
/* Table: Actor                                                 */
/*==============================================================*/
DROP TABLE IF EXISTS actor;
create table Actor
(
   A_Name               char(255) not null  comment '',
   A_Birth              date  comment '',
   A_Gender             bool  comment '',
   A_Intro              longtext  comment '',
   A_ID                 int(11) not null  comment '',
   primary key (A_ID)
)DEFAULT CHARSET = utf8;

/*==============================================================*/
/* Table: Belong                                                */
/*==============================================================*/
DROP TABLE IF EXISTS belong;
create table Belong
(
   M_id               int(11) not null  comment '',
   C_Name               char(255) not null  comment '',
   primary key (M_id, C_Name)
)DEFAULT CHARSET = utf8;

/*==============================================================*/
/* Table: Category                                              */
/*==============================================================*/
DROP TABLE IF EXISTS category;
create table Category
(
   C_Name               char(255) not null  comment '',
   C_Intro              longtext  comment '',
   primary key (C_Name)
)DEFAULT CHARSET = utf8;

/*==============================================================*/
/* Table: Direct                                                */
/*==============================================================*/
DROP TABLE IF EXISTS direct;
create table Direct
(
   M_id              int(11) not null  comment '',
   D_ID                 int(11)  not null  comment '',
   primary key (M_id, D_ID)
)DEFAULT CHARSET = utf8;

/*==============================================================*/
/* Table: Director                                              */
/*==============================================================*/
DROP TABLE IF EXISTS director;
create table Director
(
   D_ID                 int(11)  not null  comment '',
   D_Name               char(255) not null  comment '',
   D_Birth              date  comment '',
   D_Intro              longtext  comment '',
   D_Gender             bool  comment '',
   primary key (D_ID)
)DEFAULT CHARSET = utf8;

/*==============================================================*/
/* Table: Movie                                                 */
/*==============================================================*/
DROP TABLE IF EXISTS movie;
create table Movie
(
   M_ID                 int(11) not null  comment '',
   M_Name               char(255) not null  comment '',
   M_OriginalName       char(255) default NULL comment '',
   M_ReleaseDate        varchar(10) not null  comment '',
   M_Intro              longtext  comment '',
   M_Star               float not null  comment '',
   M_Alt                char(255) comment '',
   M_image              char(255) comment '',
   M_viewnumber         int(11) default 1 comment '',
   primary key (M_id)
)
DEFAULT CHARSET = utf8;

/*==============================================================*/
/* Table: Play                                                  */
/*==============================================================*/
DROP TABLE IF EXISTS play;
create table Play
(
   M_Id               int(11) not null  comment '',
   A_ID                 int(11) not null  comment '',
   primary key (M_id, A_ID)
)DEFAULT CHARSET = utf8;

/*==============================================================*/
/* Table: Review                                                */
/*==============================================================*/
DROP TABLE IF EXISTS Review;
CREATE TABLE IF NOT EXISTS Review 
(
  R_id int(11) NOT NULL AUTO_INCREMENT,
  M_id   int(11) NOT NULL,
  R_score      int(1),
  R_time       TIMESTAMP,
  R_author     varchar(50)      DEFAULT NULL,
  R_content    longtext   DEFAULT NULL,
  PRIMARY KEY(R_id)
)
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8;

/*==============================================================*/
/* Table: User                                                  */
/*==============================================================*/
/*DROP TABLE IF EXISTS user;
create table User
(
   U_ID                 char(255) not null  comment '',
   U_NickName           char(255) not null  comment '',
   U_Email              char(255) not null  comment '',
   U_Password           char(255) not null  comment '',
   U_Intro              longtext  comment '',
   primary key (U_ID)
)DEFAULT CHARSET = utf8;*/


alter table Belong add constraint FK_BELONG_BELONG_MOVIE foreign key (M_id)
      references Movie (M_id);

alter table Belong add constraint FK_BELONG_BELONG2_CATEGORY foreign key (C_Name)
      references Category (C_Name);

alter table Direct add constraint FK_DIRECT_DIRECT_MOVIE foreign key (M_id)
      references Movie (M_id);

alter table Direct add constraint FK_DIRECT_DIRECT2_DIRECTOR foreign key (D_ID)
      references Director (D_ID);

alter table Play add constraint FK_PLAY_PLAY_MOVIE foreign key (M_id)
      references Movie (M_id);

alter table Play add constraint FK_PLAY_PLAY2_ACTOR foreign key (A_ID)
      references Actor (A_ID);

alter table Review add constraint FK_REVIEW_REVIEW_MOVIE foreign key (M_id)
      references Movie (M_id);


