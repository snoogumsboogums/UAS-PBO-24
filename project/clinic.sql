-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 31, 2024 at 02:53 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `clinic`
--

-- --------------------------------------------------------

--
-- Table structure for table `Admins`
--

CREATE TABLE `Admins` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `Admins`
--

INSERT INTO `Admins` (`id`, `username`, `password`) VALUES
(1, 'admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `Appointments`
--

CREATE TABLE `Appointments` (
  `id` int(11) NOT NULL,
  `treatment_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `schedule_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `BeautyProducts`
--

CREATE TABLE `BeautyProducts` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `BeautyProducts`
--

INSERT INTO `BeautyProducts` (`id`, `name`, `price`) VALUES
(1, 'poosham', 15.00),
(2, 'mouse', 14.00),
(3, 'testupdate', 14.00);

-- --------------------------------------------------------

--
-- Table structure for table `CartItems`
--

CREATE TABLE `CartItems` (
  `id` int(11) NOT NULL,
  `cart_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Carts`
--

CREATE TABLE `Carts` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `Carts`
--

INSERT INTO `Carts` (`id`, `user_id`) VALUES
(1, 5);

-- --------------------------------------------------------

--
-- Table structure for table `Doctors`
--

CREATE TABLE `Doctors` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `specialties` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Haircare`
--

CREATE TABLE `Haircare` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `hair_type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `Haircare`
--

INSERT INTO `Haircare` (`id`, `product_id`, `hair_type`) VALUES
(1, 1, 'popo hair type'),
(2, 3, 'pepe hair');

-- --------------------------------------------------------

--
-- Table structure for table `Schedules`
--

CREATE TABLE `Schedules` (
  `id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `duration` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Skincare`
--

CREATE TABLE `Skincare` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `skin_type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `Skincare`
--

INSERT INTO `Skincare` (`id`, `product_id`, `skin_type`) VALUES
(1, 2, 'rough');

-- --------------------------------------------------------

--
-- Table structure for table `Treatments`
--

CREATE TABLE `Treatments` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `duration` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `cart_id` int(11) DEFAULT NULL,
  `appointment_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`id`, `username`, `password`, `cart_id`, `appointment_id`) VALUES
(5, 'user', 'user', 1, NULL),
(6, 'test', 'test', NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Admins`
--
ALTER TABLE `Admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `Appointments`
--
ALTER TABLE `Appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `treatment_id` (`treatment_id`),
  ADD KEY `doctor_id` (`doctor_id`),
  ADD KEY `schedule_id` (`schedule_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `BeautyProducts`
--
ALTER TABLE `BeautyProducts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `CartItems`
--
ALTER TABLE `CartItems`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cart_id` (`cart_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `Carts`
--
ALTER TABLE `Carts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `Doctors`
--
ALTER TABLE `Doctors`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Haircare`
--
ALTER TABLE `Haircare`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `Schedules`
--
ALTER TABLE `Schedules`
  ADD PRIMARY KEY (`id`),
  ADD KEY `doctor_id` (`doctor_id`);

--
-- Indexes for table `Skincare`
--
ALTER TABLE `Skincare`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `Treatments`
--
ALTER TABLE `Treatments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `cart_id` (`cart_id`),
  ADD KEY `appointment_id` (`appointment_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Admins`
--
ALTER TABLE `Admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `Appointments`
--
ALTER TABLE `Appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `BeautyProducts`
--
ALTER TABLE `BeautyProducts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `CartItems`
--
ALTER TABLE `CartItems`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `Carts`
--
ALTER TABLE `Carts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `Doctors`
--
ALTER TABLE `Doctors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Haircare`
--
ALTER TABLE `Haircare`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `Schedules`
--
ALTER TABLE `Schedules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Skincare`
--
ALTER TABLE `Skincare`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `Treatments`
--
ALTER TABLE `Treatments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Users`
--
ALTER TABLE `Users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Appointments`
--
ALTER TABLE `Appointments`
  ADD CONSTRAINT `Appointments_ibfk_1` FOREIGN KEY (`treatment_id`) REFERENCES `Treatments` (`id`),
  ADD CONSTRAINT `Appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `Doctors` (`id`),
  ADD CONSTRAINT `Appointments_ibfk_3` FOREIGN KEY (`schedule_id`) REFERENCES `Schedules` (`id`),
  ADD CONSTRAINT `Appointments_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`);

--
-- Constraints for table `CartItems`
--
ALTER TABLE `CartItems`
  ADD CONSTRAINT `CartItems_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `Carts` (`id`),
  ADD CONSTRAINT `CartItems_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `BeautyProducts` (`id`);

--
-- Constraints for table `Carts`
--
ALTER TABLE `Carts`
  ADD CONSTRAINT `Carts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`);

--
-- Constraints for table `Haircare`
--
ALTER TABLE `Haircare`
  ADD CONSTRAINT `Haircare_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `BeautyProducts` (`id`);

--
-- Constraints for table `Schedules`
--
ALTER TABLE `Schedules`
  ADD CONSTRAINT `Schedules_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `Doctors` (`id`);

--
-- Constraints for table `Skincare`
--
ALTER TABLE `Skincare`
  ADD CONSTRAINT `Skincare_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `BeautyProducts` (`id`);

--
-- Constraints for table `Users`
--
ALTER TABLE `Users`
  ADD CONSTRAINT `Users_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `Carts` (`id`),
  ADD CONSTRAINT `Users_ibfk_2` FOREIGN KEY (`appointment_id`) REFERENCES `Appointments` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
