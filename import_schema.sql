-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: sagigaming
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cart_products`
--

DROP TABLE IF EXISTS `cart_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart_products` (
  `ProductId` int NOT NULL,
  `CartId` int NOT NULL,
  `Quantity` int unsigned NOT NULL DEFAULT '0',
  `UnitPrice` float unsigned NOT NULL DEFAULT '0',
  KEY `ProductId_idx` (`ProductId`),
  KEY `CartId_idx` (`CartId`),
  CONSTRAINT `CartId` FOREIGN KEY (`CartId`) REFERENCES `carts` (`Id`),
  CONSTRAINT `ProductId` FOREIGN KEY (`ProductId`) REFERENCES `products` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_products`
--

LOCK TABLES `cart_products` WRITE;
/*!40000 ALTER TABLE `cart_products` DISABLE KEYS */;
INSERT INTO `cart_products` VALUES (1,5,1,0),(6,5,1,2619),(7,5,2,979),(1,4,1,1809),(1,6,1,1809);
/*!40000 ALTER TABLE `cart_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carts`
--

DROP TABLE IF EXISTS `carts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carts` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `IsGuestCart` tinyint NOT NULL DEFAULT '1',
  `CreatedAt` date NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carts`
--

LOCK TABLES `carts` WRITE;
/*!40000 ALTER TABLE `carts` DISABLE KEYS */;
INSERT INTO `carts` VALUES (1,0,'2025-02-11'),(2,1,'2025-02-11'),(3,1,'2025-02-11'),(4,0,'2025-02-11'),(5,0,'2025-02-11'),(6,0,'2025-02-18');
/*!40000 ALTER TABLE `carts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Image` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Monitor',NULL),(2,'Headphones',NULL),(3,'Console',NULL),(4,'Keyboard',NULL),(5,'Monitor',NULL),(6,'Headphones',NULL),(7,'Console',NULL),(8,'Keyboard',NULL);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `manufacturers`
--

DROP TABLE IF EXISTS `manufacturers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `manufacturers` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `Logo` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `manufacturers`
--

LOCK TABLES `manufacturers` WRITE;
/*!40000 ALTER TABLE `manufacturers` DISABLE KEYS */;
INSERT INTO `manufacturers` VALUES (1,'Asus',NULL),(2,'Sony',NULL),(3,'Xbox',NULL),(4,'Logitech',NULL),(5,'JBL',NULL),(6,'Apple',NULL),(7,'HyperX',NULL),(8,'Asus',NULL),(9,'Sony',NULL),(10,'Xbox',NULL),(11,'Logitech',NULL),(12,'JBL',NULL),(13,'Apple',NULL),(14,'HyperX',NULL);
/*!40000 ALTER TABLE `manufacturers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `models`
--

DROP TABLE IF EXISTS `models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `models` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `models`
--

LOCK TABLES `models` WRITE;
/*!40000 ALTER TABLE `models` DISABLE KEYS */;
INSERT INTO `models` VALUES (1,'Playstation 5'),(2,'Xbox One Series X'),(3,'Cloud'),(4,'ROG Strix'),(5,'PRO X 60'),(6,'Playstation 5'),(7,'Xbox One Series X'),(8,'Cloud'),(9,'ROG Strix'),(10,'PRO X 60');
/*!40000 ALTER TABLE `models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `CartId` int NOT NULL,
  `CustomerId` int NOT NULL,
  `OrderDate` date NOT NULL,
  `DeliveryDate` date DEFAULT NULL,
  `City` varchar(45) DEFAULT NULL,
  `Street` varchar(45) DEFAULT NULL,
  `HouseNum` int unsigned DEFAULT NULL,
  `Status` enum('pending','delivered','canceled') NOT NULL DEFAULT 'pending',
  PRIMARY KEY (`Id`),
  KEY `CustomerId_idx` (`CustomerId`),
  KEY `OrderCartId_idx` (`CartId`),
  CONSTRAINT `CustomerId` FOREIGN KEY (`CustomerId`) REFERENCES `users` (`id`),
  CONSTRAINT `OrderCartId` FOREIGN KEY (`CartId`) REFERENCES `carts` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,4,1,'2025-02-19',NULL,'Shoham','Mitzpe',26,'pending'),(3,6,5,'2025-02-20',NULL,'Or Yehuda','Moshe Dayan',1,'pending');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Description` varchar(45) DEFAULT NULL,
  `CategoryId` int NOT NULL,
  `ManufacturerId` int NOT NULL,
  `ModelId` int NOT NULL,
  `UnitPrice` float unsigned NOT NULL DEFAULT '0',
  `UnitsInStock` int unsigned NOT NULL DEFAULT '0',
  `Image` varchar(45) DEFAULT NULL,
  `TechnicalDetails` varchar(45) DEFAULT NULL,
  `OtherDetails` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `CategoryId_idx` (`CategoryId`),
  KEY `ManufacturerId_idx` (`ManufacturerId`),
  KEY `ModelId_idx` (`ModelId`),
  CONSTRAINT `CategoryId` FOREIGN KEY (`CategoryId`) REFERENCES `categories` (`Id`),
  CONSTRAINT `ManufacturerId` FOREIGN KEY (`ManufacturerId`) REFERENCES `manufacturers` (`Id`),
  CONSTRAINT `ModelId` FOREIGN KEY (`ModelId`) REFERENCES `models` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Playstation 5 Slim 1TB Digital',NULL,3,2,1,1809,0,NULL,NULL,NULL),(6,'XBOX Series X',NULL,3,3,2,2619,2,NULL,NULL,NULL),(7,'Logitech PRO X 60 Wireless Gaming Keyboard',NULL,4,4,5,979,3,NULL,NULL,NULL),(8,'ASUS ROG Strix XG27AQMR Gaming Monitor',NULL,1,1,2,3639,2,NULL,NULL,NULL),(9,'HyperX Cloud II Core Wireless Gaming Headset',NULL,2,6,3,399,1,NULL,NULL,NULL),(10,'Playstation 5 Slim 1TB Digital',NULL,3,2,1,1809,1,NULL,NULL,NULL),(11,'XBOX Series X',NULL,3,3,2,2619,2,NULL,NULL,NULL),(12,'Logitech PRO X 60 Wireless Gaming Keyboard',NULL,4,4,5,979,3,NULL,NULL,NULL),(13,'ASUS ROG Strix XG27AQMR Gaming Monitor',NULL,1,1,2,3639,2,NULL,NULL,NULL),(14,'HyperX Cloud II Core Wireless Gaming Headset',NULL,2,6,3,399,1,NULL,NULL,NULL);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ratings`
--

DROP TABLE IF EXISTS `ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ratings` (
  `ProductId` int NOT NULL,
  `UserId` int NOT NULL,
  `rating` int NOT NULL,
  KEY `UserId_idx` (`UserId`),
  KEY `ProductId_idx` (`ProductId`),
  CONSTRAINT `RatedProductId` FOREIGN KEY (`ProductId`) REFERENCES `products` (`Id`),
  CONSTRAINT `UserId` FOREIGN KEY (`UserId`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratings`
--

LOCK TABLES `ratings` WRITE;
/*!40000 ALTER TABLE `ratings` DISABLE KEYS */;
INSERT INTO `ratings` VALUES (1,5,4),(1,1,5);
/*!40000 ALTER TABLE `ratings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `Email` varchar(45) NOT NULL,
  `Phone` varchar(10) DEFAULT NULL,
  `Password` varchar(45) NOT NULL,
  `ActiveCartId` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ActiveCartId_idx` (`ActiveCartId`),
  CONSTRAINT `ActiveCartId` FOREIGN KEY (`ActiveCartId`) REFERENCES `carts` (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Sagi','Haklay','sahaklay@gmail.com','0544989884','admin',NULL),(2,'Israel','Israeli','israelisraeli@gmail.com','0501234567','1234567890',NULL),(5,'C','D','cd@gmail.com','05444477','password2',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-26 16:13:00
