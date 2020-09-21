-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 21, 2020 at 06:41 AM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jmzv13_twitter`
--

-- --------------------------------------------------------

--
-- Table structure for table `favorites`
--

CREATE TABLE `favorites` (
  `user_id` bigint(30) NOT NULL,
  `tweet_id` bigint(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `followers`
--

CREATE TABLE `followers` (
  `id` bigint(30) NOT NULL,
  `follower_id` bigint(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `followers_names`
--

CREATE TABLE `followers_names` (
  `user` text NOT NULL,
  `time_update` int(11) NOT NULL,
  `follower` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `following`
--

CREATE TABLE `following` (
  `id` bigint(30) NOT NULL,
  `following_id` bigint(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `following_names`
--

CREATE TABLE `following_names` (
  `user` text NOT NULL,
  `time_update` int(11) NOT NULL,
  `follows` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `post`
--

CREATE TABLE `post` (
  `id` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `title` varchar(1024) NOT NULL,
  `description` varchar(4096) NOT NULL,
  `image_url` varchar(1024) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `post`
--

INSERT INTO `post` (`id`, `userid`, `title`, `description`, `image_url`, `created_at`, `modified_at`) VALUES
(1, 2, 'Headrest Chair', 'This is a good headrest chair', 'upload/images/chair.jpg', '2020-06-22 00:00:00', '2020-06-22 07:04:42'),
(2, 2, 'Dash Core Components | Dash for Python Documentation | Plotly', 'Dash ships with supercharged components for interactive user interfaces. A core set of components, written and maintained by the Dash team, is available in the dash-core-components library.. The source is on GitHub at plotly/dash-core-components.. These docs are using version 1.10.1.', 'upload/images/dash.png', '2020-06-22 00:00:00', '2020-06-22 07:05:40'),
(3, 2, 'What is Python?', 'Python is a best programming language.', 'upload/images/python.png', '2020-06-22 00:00:00', '2020-06-22 07:05:40');

-- --------------------------------------------------------

--
-- Table structure for table `replies`
--

CREATE TABLE `replies` (
  `tweet_id` bigint(30) NOT NULL,
  `user_id` bigint(30) NOT NULL,
  `username` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `retweets`
--

CREATE TABLE `retweets` (
  `user_id` bigint(30) NOT NULL,
  `username` text NOT NULL,
  `tweet_id` bigint(30) NOT NULL,
  `retweet_id` bigint(30) NOT NULL,
  `retweet_date` bigint(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `site_user`
--

CREATE TABLE `site_user` (
  `id` int(11) NOT NULL,
  `userid` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `created_at` datetime NOT NULL,
  `modified_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `site_user`
--

INSERT INTO `site_user` (`id`, `userid`, `username`, `created_at`, `modified_at`) VALUES
(2, 'admin', 'Victor Lorenzo', '2020-06-22 04:00:00', '2020-06-22 07:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `tweets`
--

CREATE TABLE `tweets` (
  `id` bigint(30) NOT NULL,
  `id_str` text NOT NULL,
  `tweet` text DEFAULT NULL,
  `conversation_id` text NOT NULL,
  `created_at` bigint(30) NOT NULL,
  `date` text NOT NULL,
  `time` text NOT NULL,
  `timezone` text NOT NULL,
  `place` text DEFAULT NULL,
  `replies_count` int(11) DEFAULT NULL,
  `likes_count` int(11) DEFAULT NULL,
  `retweets_count` int(11) DEFAULT NULL,
  `user_id` bigint(30) NOT NULL,
  `user_id_str` text NOT NULL,
  `screen_name` text NOT NULL,
  `name` text DEFAULT NULL,
  `link` text DEFAULT NULL,
  `mentions` text DEFAULT NULL,
  `hashtags` text DEFAULT NULL,
  `cashtags` text DEFAULT NULL,
  `urls` text DEFAULT NULL,
  `photos` text DEFAULT NULL,
  `quote_url` text DEFAULT NULL,
  `video` int(11) DEFAULT NULL,
  `geo` text DEFAULT NULL,
  `near` text DEFAULT NULL,
  `source` text DEFAULT NULL,
  `time_update` bigint(30) NOT NULL,
  `translate` text DEFAULT NULL,
  `trans_src` text DEFAULT NULL,
  `trans_dest` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `twitterdb`
--

CREATE TABLE `twitterdb` (
  `idtwitterdb` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `twitters`
--

CREATE TABLE `twitters` (
  `id_str` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `text` varchar(768) DEFAULT NULL,
  `polarity` int(11) DEFAULT NULL,
  `subjectivity` int(11) DEFAULT NULL,
  `user_created_at` varchar(255) DEFAULT NULL,
  `user_location` varchar(255) DEFAULT NULL,
  `user_description` varchar(255) DEFAULT NULL,
  `user_followers_count` int(11) DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `retweet_count` int(11) DEFAULT NULL,
  `favorite_count` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(30) NOT NULL,
  `id_str` text NOT NULL,
  `name` text DEFAULT NULL,
  `username` text NOT NULL,
  `bio` text DEFAULT NULL,
  `location` text DEFAULT NULL,
  `url` text DEFAULT NULL,
  `join_date` text NOT NULL,
  `join_time` text NOT NULL,
  `tweets` int(11) DEFAULT NULL,
  `following` int(11) DEFAULT NULL,
  `followers` int(11) DEFAULT NULL,
  `likes` int(11) DEFAULT NULL,
  `media` int(11) DEFAULT NULL,
  `private` int(11) NOT NULL,
  `verified` int(11) NOT NULL,
  `profile_image_url` text NOT NULL,
  `background_image` text DEFAULT NULL,
  `hex_dig` text NOT NULL,
  `time_update` bigint(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`user_id`,`tweet_id`),
  ADD KEY `favories_tweet_id_fk` (`tweet_id`);

--
-- Indexes for table `followers`
--
ALTER TABLE `followers`
  ADD PRIMARY KEY (`id`,`follower_id`),
  ADD KEY `followers_follower_id_fk` (`follower_id`);

--
-- Indexes for table `followers_names`
--
ALTER TABLE `followers_names`
  ADD PRIMARY KEY (`user`(150),`follower`(150));

--
-- Indexes for table `following`
--
ALTER TABLE `following`
  ADD PRIMARY KEY (`id`,`following_id`),
  ADD KEY `following_following_id_fk` (`following_id`);

--
-- Indexes for table `following_names`
--
ALTER TABLE `following_names`
  ADD PRIMARY KEY (`user`(150),`follows`(150));

--
-- Indexes for table `post`
--
ALTER TABLE `post`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `replies`
--
ALTER TABLE `replies`
  ADD PRIMARY KEY (`user_id`,`tweet_id`),
  ADD KEY `replies_tweet_id_fk` (`tweet_id`);

--
-- Indexes for table `retweets`
--
ALTER TABLE `retweets`
  ADD PRIMARY KEY (`user_id`,`tweet_id`),
  ADD KEY `retweets_tweet_id_fk` (`tweet_id`);

--
-- Indexes for table `site_user`
--
ALTER TABLE `site_user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tweets`
--
ALTER TABLE `tweets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `twitterdb`
--
ALTER TABLE `twitterdb`
  ADD PRIMARY KEY (`idtwitterdb`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`,`hex_dig`(150));

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `post`
--
ALTER TABLE `post`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `site_user`
--
ALTER TABLE `site_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `favorites`
--
ALTER TABLE `favorites`
  ADD CONSTRAINT `favories_tweet_id_fk` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`id`),
  ADD CONSTRAINT `favories_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `followers`
--
ALTER TABLE `followers`
  ADD CONSTRAINT `followers_follower_id_fk` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `followers_id_fk` FOREIGN KEY (`id`) REFERENCES `users` (`id`);

--
-- Constraints for table `following`
--
ALTER TABLE `following`
  ADD CONSTRAINT `following_following_id_fk` FOREIGN KEY (`following_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `following_id_fk` FOREIGN KEY (`id`) REFERENCES `users` (`id`);

--
-- Constraints for table `replies`
--
ALTER TABLE `replies`
  ADD CONSTRAINT `replies_tweet_id_fk` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`id`);

--
-- Constraints for table `retweets`
--
ALTER TABLE `retweets`
  ADD CONSTRAINT `retweets_tweet_id_fk` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`id`),
  ADD CONSTRAINT `retweets_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
