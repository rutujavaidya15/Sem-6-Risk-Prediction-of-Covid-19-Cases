-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 01, 2021 at 09:54 AM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `covid-user-input`
--

-- --------------------------------------------------------

--
-- Table structure for table `details`
--

CREATE TABLE `details` (
  `test_id` bigint(15) NOT NULL,
  `mail_id` varchar(50) NOT NULL,
  `test_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `gender` enum('0','1') NOT NULL,
  `age_60_and_above` enum('0','1') NOT NULL,
  `cough` enum('0','1') NOT NULL,
  `fever` enum('0','1') NOT NULL,
  `sore_throat` enum('0','1') NOT NULL,
  `shortness_of_breathe` enum('0','1') NOT NULL,
  `headache` enum('0','1') NOT NULL,
  `abroad` enum('0','1') NOT NULL,
  `contact_with_covid_object` enum('0','1') NOT NULL,
  `contact_with_covid_patient` enum('0','1') NOT NULL,
  `corona_result` enum('0','1') DEFAULT NULL,
  `risk_prob` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `details`
--

INSERT INTO `details` (`test_id`, `mail_id`, `test_date`, `gender`, `age_60_and_above`, `cough`, `fever`, `sore_throat`, `shortness_of_breathe`, `headache`, `abroad`, `contact_with_covid_object`, `contact_with_covid_patient`, `corona_result`, `risk_prob`) VALUES
(1, 'mykysid10@gmail.com', '2021-06-30 18:30:00', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `details`
--
ALTER TABLE `details`
  ADD PRIMARY KEY (`test_id`),
  ADD UNIQUE KEY `test_id` (`test_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
