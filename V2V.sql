-- MySQL dump 10.13  Distrib 9.3.0, for macos13.7 (x86_64)
--
-- Host: localhost    Database: V2V
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bengaluru_hospitals`
--

DROP TABLE IF EXISTS `bengaluru_hospitals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bengaluru_hospitals` (
  `name` varchar(255) DEFAULT NULL,
  `latitude` decimal(9,6) DEFAULT NULL,
  `longitude` decimal(9,6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bengaluru_hospitals`
--

LOCK TABLES `bengaluru_hospitals` WRITE;
/*!40000 ALTER TABLE `bengaluru_hospitals` DISABLE KEYS */;
INSERT INTO `bengaluru_hospitals` VALUES ('Manipal Hospital',12.960600,77.641200),('Apollo Hospitals',12.896600,77.595000),('Fortis Hospital',12.896600,77.595000),('Narayana Health (Narayana Hrudayalaya)',12.834200,77.684600),('Aster CMI Hospital',13.019600,77.641200),('Columbia Asia Hospital',13.009600,77.556000),('St. John\'s Medical College Hospital',12.935200,77.622600),('MS Ramaiah Memorial Hospital',13.032900,77.556000),('Vikram Hospital',12.991600,77.591300),('BGS Gleneagles Global Hospital',12.912000,77.501000),('Bowring & Lady Curzon Hospitals',12.984200,77.605000),('Indira Gandhi Institute of Child Health',12.935000,77.596000),('SDS Tuberculosis Sanatorium',12.934000,77.594000),('Sri Jayadeva Institute of Cardiovascular Sciences and Research',12.918000,77.604000),('Victoria Hospital',12.961000,77.573000),('Maharaja Agrasen Hospital',12.924000,77.573000),('Sagar Hospital, KumaraSwamy Layout',12.907950,77.565063),('Bangalore Hospital',13.006752,77.561737),('Zion Hospitals and Research Centre',13.021000,77.641000),('P D Hinduja Sindhi Hospital',12.966000,77.591000),('Cloudnine Hospital – Old Airport Road',12.960000,77.641000),('Cloudnine Hospital – Whitefield',12.969000,77.749000),('Kaade Hospital',12.984000,77.548000),('Rangadore Memorial Hospital',12.944000,77.573000),('Sevakshetra Hospital',12.938000,77.573000),('Greenview Medical Center',12.927000,77.627000),('Specialist Hospital',13.019000,77.641000),('HCG – The Specialist in Cancer Care',12.961000,77.591000),('Femiint Health Family Clinics',13.010000,77.750000),('Sri Ram Hospital',13.009000,77.680000),('Cloud Nine Maternity Hospital (Jayanagar)',12.925000,77.593000),('Manipal Hospital Malleshwaram',13.006000,77.561000),('Sai Thunga Hospital',12.915000,77.638000),('Cloudnine Hospital – Bellandur',12.930000,77.680000),('H K Hospital',12.912000,77.501000),('S K Hospital',12.972000,77.541000),('Chaitanya Hospital',13.010000,77.591000),('Jeevika Hospital',12.960000,77.641000),('Kavya Hospital',12.888000,77.610000),('Apollo Spectra Hospitals',12.935000,77.614000),('Brindhavvan Areion Hospital',12.961000,77.573000),('Gangothri Hospital',12.915000,77.610000),('Nano Hospitals',12.900000,77.610000),('Panacea Hospital',12.972000,77.541000),('The Bangalore Hospital',12.944000,77.573000),('Spurthy Hospital',12.915000,77.610000),('Sri Krishna Seva Shrama Hospital',12.935000,77.614000),('Srujana Hospital',12.910000,77.630000),('Suguna Hospital',12.984000,77.548000),('Wellbeeing',13.050000,77.590000),('Abhaya Hospital',12.961000,77.591000),('A V Hospital',12.944000,77.573000),('Aster Women & Children Hospital',13.010000,77.750000),('Banaswadi Medical Centre',13.019000,77.641000),('Bhagwan Mahaveer Jain Hospital',12.938000,77.573000),('Dr Rudrappa\'s Hospital',12.961000,77.591000);
/*!40000 ALTER TABLE `bengaluru_hospitals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Clients`
--

DROP TABLE IF EXISTS `Clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Clients` (
  `vehicle_id` int NOT NULL,
  `client_id` varchar(45) NOT NULL,
  PRIMARY KEY (`vehicle_id`),
  UNIQUE KEY `vehicle_id` (`vehicle_id`),
  UNIQUE KEY `client_id` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Clients`
--

LOCK TABLES `Clients` WRITE;
/*!40000 ALTER TABLE `Clients` DISABLE KEYS */;
INSERT INTO `Clients` VALUES (14,'151b8d81-b3b0-4fcc-86b4-10997cf87992'),(13,'208c255e-3b92-496b-b300-adaee943db54'),(1,'872988c4-d6e4-4d32-b80e-1cfc0432ff9c'),(15,'8b24f32b-ebb8-4c4e-8f78-5176be98db5c');
/*!40000 ALTER TABLE `Clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `VehicleLocations`
--

DROP TABLE IF EXISTS `VehicleLocations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `VehicleLocations` (
  `location_id` int NOT NULL AUTO_INCREMENT,
  `vehicle_id` int DEFAULT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`location_id`),
  KEY `vehicle_id` (`vehicle_id`),
  CONSTRAINT `vehiclelocations_ibfk_1` FOREIGN KEY (`vehicle_id`) REFERENCES `Vehicles` (`vehicle_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `VehicleLocations`
--

LOCK TABLES `VehicleLocations` WRITE;
/*!40000 ALTER TABLE `VehicleLocations` DISABLE KEYS */;
INSERT INTO `VehicleLocations` VALUES (11,1,13.032029,77.653661,'2025-02-28 10:09:05'),(12,1,13.032029,77.653661,'2025-02-28 10:10:03'),(13,1,13.037379,77.648175,'2025-02-28 10:10:52');
/*!40000 ALTER TABLE `VehicleLocations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Vehicles`
--

DROP TABLE IF EXISTS `Vehicles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Vehicles` (
  `vehicle_id` int NOT NULL AUTO_INCREMENT,
  `owner_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `VehicleNo` varchar(10) DEFAULT NULL,
  `vehicle_type` enum('OV','EV','AD') DEFAULT NULL,
  PRIMARY KEY (`vehicle_id`),
  UNIQUE KEY `VehicleNo` (`VehicleNo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Vehicles`
--

LOCK TABLES `Vehicles` WRITE;
/*!40000 ALTER TABLE `Vehicles` DISABLE KEYS */;
INSERT INTO `Vehicles` VALUES (1,'test3','test3@gmail.com','test1234','KA03LA8309','OV');
/*!40000 ALTER TABLE `Vehicles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-16 11:43:47
