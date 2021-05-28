CREATE DATABASE IF NOT EXISTS telegrambot;
USE telegrambot;

SET character_set_client = utf8;
SET character_set_connection = utf8;
SET character_set_results = utf8;
SET collation_connection = utf8_general_ci;

CREATE TABLE IF NOT EXISTS users (
    id integer auto_increment primary key,
    username varchar(255) not null ,
    telegram_id varchar(255) not null,
    zabbix_user varchar(255),
    is_admin boolean not null default false,
    CONSTRAINT telegram_id_UNIQUE UNIQUE (telegram_id)
);
ALTER TABLE `users` ADD COLUMN `glpi_user` varchar(255);
ALTER TABLE `users` ADD COLUMN `admin_level` INTEGER(2) default 0;

CREATE TABLE IF NOT EXISTS status_control (
    id integer auto_increment primary key,
    user_id varchar(255) not null,
    chat_id varchar(255) not null,
    proccess varchar(100) not null,
    datetime datetime not null,
    stage integer default 0,
    completed boolean default false
);
CREATE TABLE IF NOT EXISTS ticket_creation (
    id integer auto_increment primary key,
    proccess_id integer not null,
    title varchar(255),
    description varchar(100),
    CONSTRAINT procress_id_UNIQUE UNIQUE (proccess_id),
    CONSTRAINT FOREIGN KEY (proccess_id) REFERENCES status_control(id)
);

CREATE TABLE IF NOT EXISTS glpi_user_registration (
    id integer auto_increment primary key,
    proccess_id integer not null,
    user varchar(255),
    CONSTRAINT procress_id_UNIQUE UNIQUE (proccess_id),
    CONSTRAINT FOREIGN KEY (proccess_id) REFERENCES status_control(id)
);
