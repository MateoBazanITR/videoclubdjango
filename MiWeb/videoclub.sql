-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 06, 2026 at 06:36 PM
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
-- Database: `videoclub`
--

-- --------------------------------------------------------

--
-- Table structure for table `actor`
--

CREATE TABLE `actor` (
  `id_actor` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `nacionalidad` varchar(50) DEFAULT NULL,
  `sexo` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `actor`
--

INSERT INTO `actor` (`id_actor`, `nombre`, `nacionalidad`, `sexo`) VALUES
(1, 'Matoe', 'peru', 'M'),
(2, 'mateo', 'argentino', 'M'),
(3, 'alien', 'extraterrestre', 'M');

-- --------------------------------------------------------

--
-- Table structure for table `alquiler`
--

CREATE TABLE `alquiler` (
  `id_alquiler` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_devolucion` date DEFAULT NULL,
  `dni_socio` varchar(15) DEFAULT NULL,
  `id_ejemplar` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alquiler`
--

INSERT INTO `alquiler` (`id_alquiler`, `fecha_inicio`, `fecha_devolucion`, `dni_socio`, `id_ejemplar`) VALUES
(1, '2026-06-28', NULL, '49496793', 4),
(2, '2026-06-28', '2026-06-28', '49496793', 5),
(3, '2026-06-28', '2026-06-28', '49496793', 7),
(4, '2026-06-28', '2026-06-28', '49496793', 6),
(5, '2026-06-28', NULL, '49496793', 8),
(6, '2026-06-28', NULL, '49496793', 5),
(7, '2026-06-28', NULL, '49496793', 7),
(8, '2026-06-28', NULL, '49496794', 9);

-- --------------------------------------------------------

--
-- Table structure for table `director`
--

CREATE TABLE `director` (
  `id_director` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `nacionalidad` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `director`
--

INSERT INTO `director` (`id_director`, `nombre`, `nacionalidad`) VALUES
(1, 'mateo', 'peru'),
(2, 'thomas', 'eeuu'),
(3, 'jonathan', 'peru');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(18, 'sessions', '0001_initial', '2026-08-06 15:37:29.175801');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('dmvhbbjexrf9quo0ecrei62d1sfp5e6l', '.eJxVjMsOgjAQAP9lz6bZgn1x9M43kG13a1FTEgon478bEg56nZnMGybatzLtTdZpZhhAw-WXRUpPqYfgB9X7otJSt3WO6kjUaZsaF5bX7Wz_BoVagQGMzd657H0vyKTz1ZML1oauwxQ1oo4oxkQjlJwIMWEvZDFxDtzH4OHzBd5hOGI:1ws0AK:JCXdODr7MoxPHlymhXnE1Fu4-WJ6_nyYuPWNNYfeAbE', '2026-08-20 15:37:52.343838'),
('fhsw7ua04621gidxnl3dlko58nfwu3qa', '.eJxVjMsOgjAQAP9lz6bZgn1x9M43kG13a1FTEgon478bEg56nZnMGybatzLtTdZpZhhAw-WXRUpPqYfgB9X7otJSt3WO6kjUaZsaF5bX7Wz_BoVagQGMzd657H0vyKTz1ZML1oauwxQ1oo4oxkQjlJwIMWEvZDFxDtzH4OHzBd5hOGI:1ws0CK:YUYia_ob3kxhzDCsKzVOadC-zM1679cWfpF4pME2F48', '2026-08-20 15:39:56.158845'),
('iilzzud6wnrkqyguif3him64u2jerkjy', '.eJxVjMsOgjAQAP9lz6bZgn1x9M43kG13a1FTEgon478bEg56nZnMGybatzLtTdZpZhhAw-WXRUpPqYfgB9X7otJSt3WO6kjUaZsaF5bX7Wz_BoVagQGMzd657H0vyKTz1ZML1oauwxQ1oo4oxkQjlJwIMWEvZDFxDtzH4OHzBd5hOGI:1ws0Ap:h7EJAsnx_2XffrGArQmBArLSMSjoecbT8wif7vK1MOE', '2026-08-20 15:38:23.504611'),
('j3pfml4vx9wbnorzzzd0vpmzktrw9gsz', '.eJxVjMsOgjAQAP9lz6bZgn1x9M43kG13a1FTEgon478bEg56nZnMGybatzLtTdZpZhhAw-WXRUpPqYfgB9X7otJSt3WO6kjUaZsaF5bX7Wz_BoVagQGMzd657H0vyKTz1ZML1oauwxQ1oo4oxkQjlJwIMWEvZDFxDtzH4OHzBd5hOGI:1ws0AZ:V1yvxi_uJuIpAjfxFmx9C1q-_mI5_wevajJADG9Mw1k', '2026-08-20 15:38:07.469786'),
('l4psxp7189murm0aroifmjzb1m1dyeii', '.eJxVjMsOgjAQAP9lz6bZgn1x9M43kG13a1FTEgon478bEg56nZnMGybatzLtTdZpZhhAw-WXRUpPqYfgB9X7otJSt3WO6kjUaZsaF5bX7Wz_BoVagQGMzd657H0vyKTz1ZML1oauwxQ1oo4oxkQjlJwIMWEvZDFxDtzH4OHzBd5hOGI:1ws0C2:PSOY4IqiYF1yggw1ggN-Z3jGLUtMlsd-WZ12geqfZOA', '2026-08-20 15:39:38.523292');

-- --------------------------------------------------------

--
-- Table structure for table `ejemplar`
--

CREATE TABLE `ejemplar` (
  `id_ejemplar` int(11) NOT NULL,
  `numero_ejemplar` int(11) NOT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `id_pelicula` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ejemplar`
--

INSERT INTO `ejemplar` (`id_ejemplar`, `numero_ejemplar`, `estado`, `id_pelicula`) VALUES
(4, 1, 'Alquilado', 2),
(5, 2, 'Alquilado', 2),
(6, 3, 'Disponible', 2),
(7, 4, 'Alquilado', 2),
(8, 5, 'Alquilado', 2),
(9, 1, 'Alquilado', 3),
(10, 2, 'Disponible', 3);

-- --------------------------------------------------------

--
-- Table structure for table `pelicula`
--

CREATE TABLE `pelicula` (
  `id_pelicula` int(11) NOT NULL,
  `titulo` varchar(150) NOT NULL,
  `nacionalidad` varchar(50) DEFAULT NULL,
  `productora` varchar(100) DEFAULT NULL,
  `anio` int(11) DEFAULT NULL,
  `id_director` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pelicula`
--

INSERT INTO `pelicula` (`id_pelicula`, `titulo`, `nacionalidad`, `productora`, `anio`, `id_director`) VALUES
(2, 'Toy story', 'EEUU', 'pixar', 2015, 2),
(3, 'Paul', 'EEUU', 'Universal Pictures', 2011, 3);

-- --------------------------------------------------------

--
-- Table structure for table `pelicula_actor`
--

CREATE TABLE `pelicula_actor` (
  `id_pelicula` int(11) NOT NULL,
  `id_actor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pelicula_actor`
--

INSERT INTO `pelicula_actor` (`id_pelicula`, `id_actor`) VALUES
(2, 2),
(3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `socio`
--

CREATE TABLE `socio` (
  `dni` varchar(15) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `telefono` varchar(30) DEFAULT NULL,
  `avalador_dni` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `socio`
--

INSERT INTO `socio` (`dni`, `nombre`, `direccion`, `telefono`, `avalador_dni`) VALUES
('49496793', 'mateo', NULL, NULL, NULL),
('49496794', 'mateo 2', NULL, NULL, '49496793');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `actor`
--
ALTER TABLE `actor`
  ADD PRIMARY KEY (`id_actor`);

--
-- Indexes for table `alquiler`
--
ALTER TABLE `alquiler`
  ADD PRIMARY KEY (`id_alquiler`),
  ADD KEY `dni_socio` (`dni_socio`),
  ADD KEY `id_ejemplar` (`id_ejemplar`);

--
-- Indexes for table `director`
--
ALTER TABLE `director`
  ADD PRIMARY KEY (`id_director`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `ejemplar`
--
ALTER TABLE `ejemplar`
  ADD PRIMARY KEY (`id_ejemplar`),
  ADD KEY `id_pelicula` (`id_pelicula`);

--
-- Indexes for table `pelicula`
--
ALTER TABLE `pelicula`
  ADD PRIMARY KEY (`id_pelicula`),
  ADD KEY `id_director` (`id_director`);

--
-- Indexes for table `pelicula_actor`
--
ALTER TABLE `pelicula_actor`
  ADD PRIMARY KEY (`id_pelicula`,`id_actor`),
  ADD KEY `id_actor` (`id_actor`);

--
-- Indexes for table `socio`
--
ALTER TABLE `socio`
  ADD PRIMARY KEY (`dni`),
  ADD KEY `avalador_dni` (`avalador_dni`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `actor`
--
ALTER TABLE `actor`
  MODIFY `id_actor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `alquiler`
--
ALTER TABLE `alquiler`
  MODIFY `id_alquiler` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `director`
--
ALTER TABLE `director`
  MODIFY `id_director` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `ejemplar`
--
ALTER TABLE `ejemplar`
  MODIFY `id_ejemplar` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `pelicula`
--
ALTER TABLE `pelicula`
  MODIFY `id_pelicula` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `alquiler`
--
ALTER TABLE `alquiler`
  ADD CONSTRAINT `alquiler_ibfk_1` FOREIGN KEY (`dni_socio`) REFERENCES `socio` (`dni`),
  ADD CONSTRAINT `alquiler_ibfk_2` FOREIGN KEY (`id_ejemplar`) REFERENCES `ejemplar` (`id_ejemplar`);

--
-- Constraints for table `ejemplar`
--
ALTER TABLE `ejemplar`
  ADD CONSTRAINT `ejemplar_ibfk_1` FOREIGN KEY (`id_pelicula`) REFERENCES `pelicula` (`id_pelicula`);

--
-- Constraints for table `pelicula`
--
ALTER TABLE `pelicula`
  ADD CONSTRAINT `pelicula_ibfk_1` FOREIGN KEY (`id_director`) REFERENCES `director` (`id_director`);

--
-- Constraints for table `pelicula_actor`
--
ALTER TABLE `pelicula_actor`
  ADD CONSTRAINT `pelicula_actor_ibfk_1` FOREIGN KEY (`id_pelicula`) REFERENCES `pelicula` (`id_pelicula`),
  ADD CONSTRAINT `pelicula_actor_ibfk_2` FOREIGN KEY (`id_actor`) REFERENCES `actor` (`id_actor`);

--
-- Constraints for table `socio`
--
ALTER TABLE `socio`
  ADD CONSTRAINT `socio_ibfk_1` FOREIGN KEY (`avalador_dni`) REFERENCES `socio` (`dni`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
