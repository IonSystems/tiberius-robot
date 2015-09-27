-- phpMyAdmin SQL Dump
-- version 4.5.0.2
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Sep 27, 2015 at 10:19 PM
-- Server version: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tiberius`
--

-- --------------------------------------------------------

--
-- Table structure for table `cell_status`
--

CREATE TABLE `cell_status` (
  `id` int(11) NOT NULL,
  `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `capacity_total` int(11) NOT NULL,
  `voltage` int(11) NOT NULL,
  `capacity_used` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `compass`
--

CREATE TABLE `compass` (
  `id` int(11) NOT NULL,
  `heading` double NOT NULL,
  `tilt` double NOT NULL,
  `pitch` double NOT NULL,
  `roll` double NOT NULL,
  `temperature` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Stores data from compass.';

-- --------------------------------------------------------

--
-- Table structure for table `gps`
--

CREATE TABLE `gps` (
  `id` int(11) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `altitude` double NOT NULL,
  `temperature` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Stores data from GPS sensor.';

-- --------------------------------------------------------

--
-- Table structure for table `mission`
--

CREATE TABLE `mission` (
  `id` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `task`
--

CREATE TABLE `task` (
  `id` int(11) NOT NULL,
  `name` int(11) NOT NULL,
  `description` int(11) NOT NULL,
  `task_type` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `task_type`
--

CREATE TABLE `task_type` (
  `id` int(11) NOT NULL,
  `task_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ultrasonic`
--

CREATE TABLE `ultrasonic` (
  `id` int(11) NOT NULL,
  `range` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Stores data from ultrasonic rangefinder.';

-- --------------------------------------------------------

--
-- Table structure for table `ultrasonic_reading`
--

CREATE TABLE `ultrasonic_reading` (
  `id` int(11) NOT NULL,
  `created` int(11) NOT NULL,
  `front_left` int(11) NOT NULL,
  `front_centre` int(11) NOT NULL,
  `front_right` int(11) NOT NULL,
  `rear_left` int(11) NOT NULL,
  `rear_centre` int(11) NOT NULL,
  `rear_right` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Stores all six ultrasonic readings';

-- --------------------------------------------------------

--
-- Table structure for table `waypoint`
--

CREATE TABLE `waypoint` (
  `id` int(11) NOT NULL,
  `gps_id` int(11) NOT NULL,
  `mission_id` int(11) NOT NULL,
  `heading` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `compass`
--
ALTER TABLE `compass`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `gps`
--
ALTER TABLE `gps`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mission`
--
ALTER TABLE `mission`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`id`),
  ADD KEY `task_type` (`task_type`);

--
-- Indexes for table `task_type`
--
ALTER TABLE `task_type`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ultrasonic`
--
ALTER TABLE `ultrasonic`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `ultrasonic_reading`
--
ALTER TABLE `ultrasonic_reading`
  ADD PRIMARY KEY (`id`),
  ADD KEY `front_left` (`front_left`,`front_centre`,`front_right`,`rear_left`,`rear_centre`,`rear_right`),
  ADD KEY `front_centre` (`front_centre`),
  ADD KEY `front_right` (`front_right`),
  ADD KEY `front_right_2` (`front_right`),
  ADD KEY `rear_left` (`rear_left`),
  ADD KEY `rear_centre` (`rear_centre`),
  ADD KEY `rear_right` (`rear_right`);

--
-- Indexes for table `waypoint`
--
ALTER TABLE `waypoint`
  ADD PRIMARY KEY (`id`),
  ADD KEY `gps_id` (`gps_id`,`mission_id`),
  ADD KEY `mission_id` (`mission_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `compass`
--
ALTER TABLE `compass`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `gps`
--
ALTER TABLE `gps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `mission`
--
ALTER TABLE `mission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `ultrasonic`
--
ALTER TABLE `ultrasonic`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `ultrasonic_reading`
--
ALTER TABLE `ultrasonic_reading`
  ADD CONSTRAINT `front_centre_constraint` FOREIGN KEY (`front_centre`) REFERENCES `ultrasonic` (`id`),
  ADD CONSTRAINT `front_left_constraint` FOREIGN KEY (`front_left`) REFERENCES `ultrasonic` (`id`),
  ADD CONSTRAINT `front_right_constraint` FOREIGN KEY (`front_right`) REFERENCES `ultrasonic` (`id`),
  ADD CONSTRAINT `rear_centre_constraint` FOREIGN KEY (`rear_centre`) REFERENCES `ultrasonic` (`id`),
  ADD CONSTRAINT `rear_left_constraint` FOREIGN KEY (`rear_left`) REFERENCES `ultrasonic` (`id`),
  ADD CONSTRAINT `rear_right_costraint` FOREIGN KEY (`rear_right`) REFERENCES `ultrasonic` (`id`);

--
-- Constraints for table `waypoint`
--
ALTER TABLE `waypoint`
  ADD CONSTRAINT `waypoint_gps_constraint` FOREIGN KEY (`gps_id`) REFERENCES `gps` (`id`),
  ADD CONSTRAINT `waypoint_mission_constraint` FOREIGN KEY (`mission_id`) REFERENCES `mission` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
