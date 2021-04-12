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
