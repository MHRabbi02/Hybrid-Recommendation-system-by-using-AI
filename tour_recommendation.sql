-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 20, 2025 at 08:23 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tour_recommendation`
--

-- --------------------------------------------------------

--
-- Table structure for table `ratings`
--

CREATE TABLE `ratings` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `destination` varchar(255) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ratings`
--

INSERT INTO `ratings` (`id`, `user_id`, `destination`, `rating`) VALUES
(31, 8, 'Cox\'s Bazar Sea Beach', 5),
(32, 8, 'Sajek Valley', 4),
(33, 1, 'Cox\'s Bazar Sea Beach', 5),
(34, 2, 'Sundarbans Mangrove Forest', 5),
(35, 2, 'Saint Martin\'s Island', 4),
(38, 4, 'Cox\'s Bazar Sea Beach', 4),
(39, 4, 'Kuakata Sea Beach', 4),
(40, 5, 'Lalakhal River', 3),
(41, 5, 'Jaflong', 4),
(42, 6, 'Patenga Sea Beach', 2),
(43, 6, 'Ratargul Swamp Forest', 4),
(44, 7, 'Tanguar Haor', 5),
(45, 7, 'Tanguar Haor', 4),
(46, 9, 'Bisanakandi', 4),
(47, 9, 'Cox\'s Bazar Sea Beach', 5),
(48, 11, 'Sajek Valley', 4),
(54, 3, 'Sylhet Tea Gardens', 3),
(55, 3, 'Saint Martin\'s Island', 3),
(56, 3, 'Sitakunda Eco Park', 4),
(57, 12, 'Cox\'s Bazar Sea Beach', 5),
(58, 12, 'Saint Martin\'s Island', 3);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'mahmud', 'scrypt:32768:8:1$pFDgOhgjY9kt8Zwd$c14d8fdc7a6052e1d60fa0ce5f7e3f15c64c902a39e477b9c5838bcf9366fa9ea75e381a536353da626e604d4acd0865c58e693aaa20f82679f472f10ae72176'),
(2, 'hassan', 'scrypt:32768:8:1$qSCKpBVaZbO4QIlf$101f011136b160a4e07deb5bad5856a2c7523a05127e9c9ae6024fad6c01313a1fd1f934c80f133948119e28e40b7a8df4b05a4da6065f7d6761568bcc4775ff'),
(3, 'rabbi', 'scrypt:32768:8:1$6nTUHMzIv7cTixxq$641ddca882cb75bd8094abbe2ec6896c50d0f3c19c29593db6e212ad0da663db9a0c24cd4e3f9c4deb6794ce720409628a8eca4671d74de7347b815f425739bd'),
(4, 'mashura', 'scrypt:32768:8:1$Ss3pVZDE9utYfb92$982284a1e5569a20720909f5b45cc7230f3064b7ce7a5df5d3f77d7a6da42d83612b0d38e911fdd4c5729520e591c34b960b3665c15b1fa9228a91955aee62a0'),
(5, 'tabassum', 'scrypt:32768:8:1$BhGNcVRuaxDFXr4E$d0303e8bb6f7d1cddbdf5cda4389d080fe7853f11ffeca6cc3bfc603600e8c558ad17caa2e6fca8e73043712fefaa2f2f9724a7d8f09afd5cc0c423292bfcb11'),
(6, 'roza', 'scrypt:32768:8:1$IU99vIcFiEt6Wj1T$db769b36b0dfe1724f7792e39d2c4f00ad2191015c23948099fac37f982316923e1fa4b6947bada237ff44d4298de19621418861eb62cbedb9fa02481b09eb3e'),
(7, 'mahzabin', 'scrypt:32768:8:1$9bzxIuHZKKF4pLjz$8d73dd9fdb1a1ec16d07ea7f8458b2c3e38edd504246c6f7d24eb5e1150a133c2faf22e117a10e67636cffed75cb0e8ebc766eee98829362524a32eb6a1b068f'),
(8, 'MH Rabbi', 'scrypt:32768:8:1$ceSPohzddsgeDOlg$ba03a06e9db6926d30db9d38ef105362360807f8d2dcba0123e85e9bec18db414a51fd297d9253b777e46c385f79a65504e97d8d4a6dadfa1ddedce66315218a'),
(9, 'dider', 'scrypt:32768:8:1$j7qQLrnIlQVIZ6MK$6f8d4cd007f6549cf53b66713234dd477696894ce0a10ceab3c511171b9c47f766a63eb078f41602aaa05e7390ab79027695eba5c7e234dd73c0338a8c022b81'),
(10, 'rifat', 'scrypt:32768:8:1$OoV9l3LUXLkuoHC1$93ea27173253bdbb2e757222c799b09f4257222e84290384f3b6cf505d28e860bf5a3327c89636ab03ee7e12bebccfa115bfcb85e9ea9b27fb88a7873431128f'),
(11, 'sifat', 'scrypt:32768:8:1$Ht2QaJMz2JYeIDK6$e91b78fa03a1fa89dfa7665f288e4097a7cc27aedd843aea31409c9325c185e4712b1f5d8c4080a8c5ac6c795c3ceb57cc62f7c6a24ef27d56518ef1d8626493'),
(12, 'jaheen', 'scrypt:32768:8:1$zpt9y8630yVM5EaE$d91cb1a6f2b146a9af4f4728978c478665ea79f1a3be0b18c84721046cf6e162b702831d97cb980244d5acc3cd277d02eb749e9f17457ff13ae91478d33bfbd7'),
(13, 'mahi', 'scrypt:32768:8:1$UlrFpixUHwYRwXq7$12716310435a7a36cd3a138e24be99ef698ed59856caea42eae69044a224718996742b98c8f90bdb8ef689cb10634353dfe40c8a1ee5ca36926389858a4b723d');

-- --------------------------------------------------------

--
-- Table structure for table `user_history`
--

CREATE TABLE `user_history` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `destination` varchar(255) DEFAULT NULL,
  `score` float DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ratings`
--
ALTER TABLE `ratings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `user_history`
--
ALTER TABLE `user_history`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ratings`
--
ALTER TABLE `ratings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `user_history`
--
ALTER TABLE `user_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ratings`
--
ALTER TABLE `ratings`
  ADD CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
