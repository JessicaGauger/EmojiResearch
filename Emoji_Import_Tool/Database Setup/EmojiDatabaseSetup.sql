DROP DATABASE IF EXISTS `covid_emoji_proj`;
CREATE DATABASE `covid_emoji_proj` DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;
USE `covid_emoji_proj`;

-- Note: Use if not dropping / recreating the database
DROP TABLE IF EXISTS emoji_unicode;
DROP TABLE IF EXISTS tweet_emoji;
DROP TABLE IF EXISTS emoji;
DROP TABLE IF EXISTS search_result;
DROP TABLE IF EXISTS tweet;
DROP TABLE IF EXISTS search_history;

CREATE TABLE IF NOT EXISTS `emoji` (
	`emoji_id` SMALLINT NOT NULL AUTO_INCREMENT
    , `name` VARCHAR(100) NOT NULL
    , `image_url` VARCHAR(500)
    , `emoji` VARCHAR(100) NOT NULL
    , PRIMARY KEY (`emoji_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `emoji_unicode` (
	`emoji_unicode_id` SMALLINT NOT NULL AUTO_INCREMENT
    , `unicode` VARCHAR(255) NOT NULL
    , `emoji_id` SMALLINT NOT NULL
    , PRIMARY KEY (`emoji_unicode_id`)
    , FOREIGN KEY (`emoji_id`) REFERENCES `emoji`(`emoji_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS twitter_post (
    `twitter_post_id` MEDIUMINT NOT NULL AUTO_INCREMENT
    , `message` VARCHAR(500) NOT NULL
    , `posted_date` DATETIME NOT NULL
    , `contains_emoji` BIT NOT NULL
    , `total_emoji_count` SMALLINT NOT NULL
    , `unique_emoji_count` SMALLINT NOT NULL
    , `tweet_guid` VARCHAR(100) NOT NULL
    , PRIMARY KEY (`twitter_post_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS twitter_post_emoji (
    `id` MEDIUMINT NOT NULL AUTO_INCREMENT
    , `emoji_id` SMALLINT
    , `twitter_post_id` MEDIUMINT
    , PRIMARY KEY (`id`)
    , FOREIGN KEY (`emoji_id`) REFERENCES `emoji`(`emoji_id`)
    , FOREIGN KEY (`twitter_post_id`) REFERENCES `twitter_post`(`twitter_post_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS search_history (
    `search_history_id` SMALLINT NOT NULL AUTO_INCREMENT
    , `keyword` VARCHAR(100) NOT NULL
    , `start_date` DATE NOT NULL
    , `end_date` DATE NOT NULL
    , PRIMARY KEY (`search_history_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS search_result (
    `search_result_id` MEDIUMINT NOT NULL AUTO_INCREMENT
    , `twitter_post_id` MEDIUMINT NOT NULL
    , `search_history_id` SMALLINT NOT NULL
    , PRIMARY KEY (`search_result_id`)
    , FOREIGN KEY (`search_history_id`) REFERENCES `search_history`(`search_history_id`)
    , FOREIGN KEY (`twitter_post_id`) REFERENCES `twitter_post`(`twitter_post_id`)
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;