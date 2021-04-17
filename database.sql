CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) DEFAULT NULL,
  `last_name` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `username` varchar(45) DEFAULT NULL,
  `gender` varchar(45) DEFAULT NULL,
  `dob` varchar(45) DEFAULT NULL,
  `country` varchar(45) DEFAULT NULL,
  `phone_no` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ;



CREATE TABLE `tracks` (
  `track_id` int NOT NULL AUTO_INCREMENT,
  `track_name` varchar(45) DEFAULT NULL,
  `artist` varchar(45) DEFAULT NULL,
  `genre` varchar(45) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL,
  `track_link` varchar(45) DEFAULT NULL,
  `album_link` varchar(45) DEFAULT NULL,
  `track_user_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`track_id`)
) ;