CREATE DATABASE  IF NOT EXISTS "petswale" /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `petswale`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: mysql-petswale-manavdodani2005-1c65.f.aivencloud.com    Database: petswale
-- ------------------------------------------------------
-- Server version	8.0.35

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '17fa7ef5-6339-11f0-b3a4-862ccfb013fe:1-235,
9bb93b51-61bc-11f0-9830-862ccfb01a0e:1-27';

--
-- Table structure for table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `addresses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `address_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `company_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `street_address` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `apartment` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `city` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `state` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `country` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `pin_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_default` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `addresses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
INSERT INTO `addresses` VALUES (1,1,'home',NULL,'214','fagfagfa','Chennai','Tamil Nadu','India','123455',0);
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('47c35232812c');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart_items`
--

DROP TABLE IF EXISTS `cart_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quantity` int NOT NULL,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `cart_items_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `cart_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart_items`
--

LOCK TABLES `cart_items` WRITE;
/*!40000 ALTER TABLE `cart_items` DISABLE KEYS */;
INSERT INTO `cart_items` VALUES (3,1,9,2),(4,4,10,1);
/*!40000 ALTER TABLE `cart_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Food','food','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMmjOp16EFp4cwmMat-EDMRaOYinfu6Iu45g&s','High-quality nutritious food options for your pets, including dry food, wet food, and treats.'),(2,'Toys','toys','/static/images/categories/toys.jpg','Fun and engaging toys to keep your pets entertained and active.'),(5,'Grooming','grooming','/static/images/categories/grooming.jpg','Grooming supplies and tools to keep your pet looking and feeling their best.'),(6,'Beds & Furniture','beds-furniture','/static/images/categories/beds.jpg','Comfortable beds, furniture, and housing options for your pets.');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `price_at_purchase` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,1,1,1,54.99),(2,1,2,1,34.99),(3,1,3,1,14.99),(4,1,18,1,90),(5,2,1,1,54.99),(6,2,2,1,34.99),(7,2,3,1,14.99),(8,2,18,1,90),(9,3,2,2,34.99),(10,4,2,2,34.99),(11,3,3,1,14.99),(12,4,3,1,14.99),(13,5,2,2,34.99),(14,5,3,1,14.99),(15,6,2,2,34.99),(16,6,3,1,14.99),(17,7,18,1,90),(18,8,18,1,90),(19,7,19,1,999),(20,8,19,1,999),(21,9,1,1,54.99),(22,10,1,1,54.99),(23,11,1,1,54.99),(24,12,1,1,54.99),(25,13,1,1,54.99),(26,14,1,1,54.99),(27,15,1,1,54.99),(28,16,1,1,54.99),(29,17,18,1,90),(30,18,18,1,90),(31,19,3,1,14.99),(32,19,18,1,90),(33,20,29,1,450),(34,20,34,1,1450),(35,20,30,1,330),(36,21,29,1,450),(37,21,34,1,1450),(38,21,30,1,330),(39,22,1,1,54.99),(40,22,2,1,34.99),(41,23,26,1,769),(42,24,23,1,600);
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `total_price` float NOT NULL,
  `payment_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `order_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `payment_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,'2025-07-19 18:48:04',219.467,NULL,'order_Qv1wcJSN8qNjqy','pending'),(2,1,'2025-07-19 18:48:04',219.467,'pay_Qv1wqUn3RPrDc9','order_Qv1wclobK40eJb','failed'),(3,1,'2025-07-19 19:41:37',98.467,NULL,'order_Qv2rAyaA1BWTJb','pending'),(4,1,'2025-07-19 19:41:37',98.467,NULL,'order_Qv2rAwfvYlQifU','pending'),(5,1,'2025-07-19 19:41:46',98.467,NULL,'order_Qv2rK6nb5aUAum','pending'),(6,1,'2025-07-19 19:41:46',98.467,'pay_Qv2rTfWIfwwoG5','order_Qv2rKl3a6bHnir','failed'),(7,1,'2025-07-19 19:48:45',1202.9,'pay_Qv2yoMFWuBqWWy','order_Qv2yhqX4sI5Kqj','failed'),(8,1,'2025-07-19 19:48:45',1202.9,NULL,'order_Qv2yhrFTPMq2MG','pending'),(9,1,'2025-07-19 20:15:37',65.489,NULL,'order_Qv3R5AutLqTvmp','pending'),(10,1,'2025-07-19 20:15:37',65.489,NULL,'order_Qv3R5STv5ku4pa','pending'),(11,1,'2025-07-19 20:15:44',65.489,NULL,'order_Qv3RDEtEJTe0dr','pending'),(12,1,'2025-07-19 20:15:44',65.489,NULL,'order_Qv3RDEIbLJU7YZ','pending'),(13,1,'2025-07-19 20:15:57',65.489,NULL,'order_Qv3RRMTB66RLgu','pending'),(14,1,'2025-07-19 20:15:57',65.489,NULL,'order_Qv3RRNNUWRNT8L','pending'),(15,1,'2025-07-19 20:16:43',65.489,NULL,'order_Qv3SFC97AuHKbb','pending'),(16,1,'2025-07-19 20:16:43',65.489,'pay_Qv3SKHRU2He2QN','order_Qv3SFCPKaHU7XB','failed'),(17,1,'2025-07-19 20:20:43',104,NULL,'order_Qv3WTHPurBZbuD','pending'),(18,1,'2025-07-19 20:20:43',104,'pay_Qv3WZbarzFHvZd','order_Qv3WTH34mqV70B','failed'),(19,1,'2025-07-19 20:31:46',120.489,'pay_Qv3iIqjdVZuUVE','order_Qv3i9XdlcsNum9','completed'),(20,1,'2025-07-19 20:35:44',2458,NULL,'order_Qv3mKvTtB4gibj','pending'),(21,1,'2025-07-19 20:35:46',2458,'pay_Qv3mSHkGTzJG3Q','order_Qv3mNM5fD94bEE','completed'),(22,1,'2025-07-19 20:39:45',103.978,'pay_Qv3qj9EzPQEeZQ','order_Qv3qaUnpHMYVTO','completed'),(23,1,'2025-07-19 20:41:50',850.9,'pay_Qv3su6EXZhHvWI','order_Qv3sn4etP0gjcw','completed'),(24,1,'2025-07-19 20:46:43',665,'pay_Qv3y5AZMAJbDmj','order_Qv3xw25AMFIgSY','completed');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `page_views`
--

DROP TABLE IF EXISTS `page_views`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `page_views` (
  `id` int NOT NULL AUTO_INCREMENT,
  `page` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ip_address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `user_agent` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `page_views_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `page_views`
--

LOCK TABLES `page_views` WRITE;
/*!40000 ALTER TABLE `page_views` DISABLE KEYS */;
/*!40000 ALTER TABLE `page_views` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pet_types`
--

DROP TABLE IF EXISTS `pet_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pet_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pet_types`
--

LOCK TABLES `pet_types` WRITE;
/*!40000 ALTER TABLE `pet_types` DISABLE KEYS */;
INSERT INTO `pet_types` VALUES (1,'Dog','https://cdn.shopify.com/s/files/1/1708/4041/files/custom_resized_lab_600x600.jpg?v=1668581125'),(2,'Cat','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeYtG28d9Rk0ObhCc5ilT8Cz0TsFPztP0V9w&s'),(3,'Birds','https://www.green-feathers.co.uk/cdn/shop/articles/robin-on-branch-royalty-free-image-1567774522.jpg?v=1729597011'),(4,'Fish','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSrO8Ln2MP__1A_Gs_1oN4DBtXeKTfbby1TKg&s');
/*!40000 ALTER TABLE `pet_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_analytics`
--

DROP TABLE IF EXISTS `product_analytics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_analytics` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `date` date NOT NULL,
  `view_count` int DEFAULT NULL,
  `cart_add_count` int DEFAULT NULL,
  `purchase_count` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_product_analytics_product_id` (`product_id`),
  CONSTRAINT `fk_product_analytics_product_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_analytics`
--

LOCK TABLES `product_analytics` WRITE;
/*!40000 ALTER TABLE `product_analytics` DISABLE KEYS */;
INSERT INTO `product_analytics` VALUES (1,31,'2025-07-02',2,0,0),(2,1,'2025-07-04',19,0,0),(3,3,'2025-07-04',1,0,0),(4,30,'2025-07-04',8,0,0),(5,27,'2025-07-04',1,0,0),(6,31,'2025-07-04',1,0,0),(7,25,'2025-07-04',2,0,0),(8,2,'2025-07-04',2,0,0),(9,23,'2025-07-04',1,0,0),(10,29,'2025-07-04',1,0,0),(11,24,'2025-07-04',2,0,0),(12,21,'2025-07-04',1,0,0),(13,18,'2025-07-04',4,0,0),(14,34,'2025-07-14',1,0,0),(15,1,'2025-07-14',9,0,0),(16,18,'2025-07-14',1,0,0),(17,3,'2025-07-14',1,0,0),(18,25,'2025-07-14',1,0,0),(19,2,'2025-07-17',1,0,0),(20,1,'2025-07-19',2,0,0);
/*!40000 ALTER TABLE `product_analytics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_attributes`
--

DROP TABLE IF EXISTS `product_attributes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_attributes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `display_order` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `product_attributes_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_attributes`
--

LOCK TABLES `product_attributes` WRITE;
/*!40000 ALTER TABLE `product_attributes` DISABLE KEYS */;
INSERT INTO `product_attributes` VALUES (1,2,'Dimensions','55*35*12',1);
/*!40000 ALTER TABLE `product_attributes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_images`
--

DROP TABLE IF EXISTS `product_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `image_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_primary` tinyint(1) DEFAULT NULL,
  `display_order` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `product_images_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_images`
--

LOCK TABLES `product_images` WRITE;
/*!40000 ALTER TABLE `product_images` DISABLE KEYS */;
INSERT INTO `product_images` VALUES (1,1,'https://placehold.co/800x800/46f27a/ffffff?text=Main',1,0),(2,1,'https://placehold.co/800x800/46f27a/ffffff?text=Side',0,1),(3,1,'https://placehold.co/800x800/46f27a/ffffff?text=Back',0,2),(4,1,'https://placehold.co/800x800/46f27a/ffffff?text=Detail',0,3),(6,3,'https://m.media-amazon.com/images/I/71fwkZg9m6L._AC_UF1000,1000_QL80_.jpg',0,2),(7,3,'https://plus.unsplash.com/premium_photo-1666777247416-ee7a95235559?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZG9nfGVufDB8fDB8fHww',0,1),(9,2,'https://m.media-amazon.com/images/I/71BdAbA9D7L._AC_UL480_FMwebp_QL65_.jpg',0,1);
/*!40000 ALTER TABLE `product_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_views`
--

DROP TABLE IF EXISTS `product_views`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_views` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `ip_address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_product_view_product_id` (`product_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `fk_product_view_product_id` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
  CONSTRAINT `product_views_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_views`
--

LOCK TABLES `product_views` WRITE;
/*!40000 ALTER TABLE `product_views` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_views` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `price` float NOT NULL,
  `stock` int DEFAULT NULL,
  `image_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `weight` float DEFAULT NULL,
  `parent_id` int DEFAULT NULL,
  `pet_type_id` int NOT NULL,
  `category_id` int NOT NULL,
  `uploader_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_product_parent` (`parent_id`),
  KEY `pet_type_id` (`pet_type_id`),
  KEY `category_id` (`category_id`),
  KEY `uploader_id` (`uploader_id`),
  CONSTRAINT `fk_product_parent` FOREIGN KEY (`parent_id`) REFERENCES `products` (`id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`pet_type_id`) REFERENCES `pet_types` (`id`),
  CONSTRAINT `products_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `products_ibfk_3` FOREIGN KEY (`uploader_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Royal Canin Maxi Adult Dog Food','Premium dry dog food specially formulated for large adult dogs',54.99,70,'https://m.media-amazon.com/images/I/71fwkZg9m6L._AC_UF1000,1000_QL80_.jpg','2025-04-23 12:58:09',NULL,NULL,1,1,1),(2,'Hills Science Diet Wet Dog Food','Grain-free wet food with real chicken',34.99,134,'https://m.media-amazon.com/images/I/71BdAbA9D7L._AC_UL480_FMwebp_QL65_.jpg','2025-04-23 12:58:09',NULL,NULL,1,1,1),(3,'KONG Classic Dog Toy','Durable rubber chew toy for mental stimulation',14.99,71,'https://tse3.mm.bing.net/th/id/OIP.DwBQA_UAZaEwWgPHHS5-sQAAAA?pid=Api&P=0&h=180','2025-04-23 12:58:09',NULL,NULL,1,2,1),(18,'  Royal Canin Maxi Adult Dog Food, 5kg','anything for now',90,1,'https://images.unsplash.com/photo-1567752881298-894bb81f9379?q=80&w=600&auto=format&fit=crop','2025-05-03 01:30:32',5,1,1,1,NULL),(19,'Grain-Free Chicken Chow','Made using farm fresh chicken and nutrient-packed veggies simmered in our 24-hour Bone Broth. This NO GRAIN, high-protein, low-carb meal is packed with natural vitamins and collagen for your dog’s health, energy and happiness – and ZERO fillers or preservatives.',999,10,'https://petchef.co.in/cdn/shop/files/grain_free_chicken_chow_f7e4833f-85f0-4747-ad31-73e9517effaa.jpg?v=1740665508&width=800','2025-07-02 12:55:50',NULL,NULL,1,1,NULL),(20,'Grain-Free Mutton Nom Nom','Mutton muscle, organ meat, high-nutrition vegetables and all-natural supplements cooked in our signature 24-hour Bone Broth. This NO GRAIN, high-protein, low-carb meal is a fully balanced meal that provides your dogs with all the macro and micronutrients they need.\r\n\r\n',550,5,'https://petchef.co.in/cdn/shop/files/grain_free_motton_nom_618da3b9-9731-4e76-824d-68bef6678336.jpg?v=1740664254&width=800','2025-07-02 12:57:16',NULL,NULL,1,1,NULL),(21,'Wholesome Mutton Nom Nom','Mutton muscle, organ meat, vegetables like pumpkin and sweet potato, all-natural supplements and brown rice cooked in our signature 24-hour Bone Broth. High in protein and collagen, it’s great for your dog’s coat and gut.',700,7,'https://petchef.co.in/cdn/shop/files/mutton_nom_6f33f0c1-f011-4a46-9a46-895c3a9d7f23.jpg?v=1740664370&width=800','2025-07-02 12:58:10',NULL,NULL,1,1,NULL),(22,'Grain-Free Chicken Chow','Made using farm fresh chicken and nutrient-packed veggies simmered in our 24-hour Bone Broth. This NO GRAIN, high-protein, low-carb meal is packed with natural vitamins and collagen for your dog’s health, energy and happiness – and ZERO fillers or preservatives',400,6,'https://petchef.co.in/cdn/shop/files/grain_free_chicken_chow_f7e4833f-85f0-4747-ad31-73e9517effaa.jpg?v=1740665508&width=800','2025-07-02 12:59:05',NULL,NULL,1,1,NULL),(23,'Wobble Wag Giggle ball Interactive Dog Toy','FUN FOR ALL BIG OR SMALL: This interactive dog toy is great for dogs of all ages and sizes! The 6 clutch pockets on this interactive toy make it easy for your dog to pick up during playtime!\r\nWOBBLE WAG GIGGLE BALL: With just the nudge of a nose, off the ball, goes! Wobble Wag Giggle does not require batteries - the secret is the internal tube noisemaker inside the dog ball, and the enticing “play-with-me” sounds are sure to engage your pup as the toy rolls around!',600,10,'https://pawsindia.com/cdn/shop/products/57c91479-aef4-4a3d-a304-44835df6846b_1.448de7dbef33fe2b8477034b9fd6c6b6_1_4238e93e-7d75-4402-8e36-f9f11b63ad7b.webp?v=1666088744','2025-07-02 13:06:48',NULL,NULL,1,2,NULL),(24,'Barrel Treat Dog Toy- Blue','Natural Rubber: Natural rubber is used in the toy, keeping in mind your dog\'s safety. The natural rubber is safe to chew and suitable for your dog\'s jaw. The natural rubber has just the right amount of hardness which makes chewing on the toy desirable and stimulating for your dog.\r\nEco-friendly: Unlike plastic and other harmful materials, natural rubber is eco-friendly.',800,20,'https://pawsindia.com/cdn/shop/products/7_4.jpg?v=1617613123','2025-07-02 13:07:38',NULL,NULL,1,2,NULL),(25,'Brush Ball Teeth Cleaning Toy','The ball is made from high-quality, non-toxic rubber that is safe for your dog to play with. The soft bristles are designed to gently brush your dog’s teeth as they play, helping to remove plaque and tartar buildup and promote better oral hygiene.\r\nIt isn\'t just a toothbrush — it\'s also a fun and engaging toy! Playtime with this toy will keep your dog active & engaged which will improve their intelligence & happiness. It is great for playing fetch and interacting with your dog. The toy produces fun sounds when your dog moves it around, picks it up, or shakes it, which can keep them entertained. It does not require batteries and is an excellent way to keep your pet occupied when you are not available.\r\n',500,10,'https://pawsindia.com/cdn/shop/files/1_2870219f-3461-4399-a7b4-a743d0bd83ce.jpg?v=1683290555','2025-07-02 13:12:34',NULL,NULL,1,2,NULL),(26,'Ultimate Chew Stick Dog Toy','The Ultimate Chew Stick is the last chew toy you\'ll need for your dog. This chew toy\'s rubber body can easily handle the strongest bites. Just give it to your dog and watch them go to town with the toy. If your dog feels like losing interest in the toy, the built-in squeaker will keep it hooked.',769,20,'https://pawsindia.com/cdn/shop/products/red1.jpg?v=1661421340','2025-07-02 13:13:27',NULL,NULL,1,2,NULL),(27,'Self Cleaning Slicker Brush','Clean Pets, Clean House. emily cat & dog brush for shedding can easily remove loose hair, shedding mats, tangled hair, dander and dirt of your lovely pet, which not only keep your pet clean, but also provide you with a clean and hygienic home environment.\r\n',247,10,'https://m.media-amazon.com/images/I/61qjyzM3+BL._SL1500_.jpg','2025-07-02 13:18:19',NULL,NULL,1,5,NULL),(29,'PET Grooming Wet Wipes','Wipe provides a fast,convenient way to keep your pet clean and fresh everyday.Each extra soft pet wipe is moistened with a natural formula that helps maintain a clean and healthy pet.Gentle enough to use everyday around pet\'s eyes,ears,face and body\r\n\r\n',450,21,'https://m.media-amazon.com/images/I/81xU7fjrNcL._SL1500_.jpg','2025-07-02 13:20:04',NULL,NULL,1,5,NULL),(30,'Animal Nail Cutter ','The pet nail clippers are made out of high quality 4.0 mm thick stainless steel sharp blades, it is powerful enough to trim your dogs or cats nails with just one cut, these durable clippers won\'t bend, scratch or rust, and the blades still keep sharp even through many sessions on dog tough nails.',330,10,'https://m.media-amazon.com/images/I/61oJ7Q+BOaL._SL1500_.jpg','2025-07-02 13:27:53',NULL,NULL,1,5,NULL),(31,'Velvet Cave House Bed','Material: Made of high quality soft velvet, good quality foam and cotton filling. It offers your pet a comfortable place for sleeping and resting.\r\nMaintenance: It is easy to clean and washable in gentle mode in washing machine or hand wash. The product is vacuum sealed for safe transportation, hence recommended to pat it, shake it and leave for 48 hours before using so that it gets back to its actual fluffy shape\r\nNote: If your pet has an excessive chewing habit, please keep a toy on the bed so that the pet will not damage the bed by treating it as a chew toy',2000,5,'https://m.media-amazon.com/images/I/818848PvqNL._SL1500_.jpg','2025-07-02 13:30:04',NULL,NULL,1,6,NULL),(32,'Light Weight Mat','MULTI-USAGE - Absorbs body heat and helps relax your pets. A perfect crate and sleeping mat for your pets, can be used on the floor, sofa, bed.\r\nThis stylish dog mat measures (Size - 20X 28 Inches) for Puppies & Small Dogs\r\nDog mats are washable and easy to maintain.',1100,8,'https://m.media-amazon.com/images/I/61VRUdkZaBL._SL1440_.jpg','2025-07-02 13:31:15',NULL,NULL,1,6,NULL),(34,'Round Donut Pet Bed ','Zexsazone Pet Bed, meticulously designed to offer the utmost comfort and style for your furry friend. Measuring 50 x 50 x 12 cm, this small-sized bed is perfect for cats, puppies, and small dog breeds.\r\nEco-Friendly Materials: Made from sustainable and non-toxic materials, this bed is safe for your pet and the environment. The high-quality stuffing retains its shape, providing consistent comfort and durability.',1450,5,'https://m.media-amazon.com/images/I/41BoiTIO43L.jpg','2025-07-02 13:32:49',NULL,NULL,1,6,NULL),(35,'Igloo Dog House','PLENTY OF ROOM INSIDE – Perfectly stitched bed roomy & comfy for pets to turn around and lie straight inside, your furry babies love this cozy igloo bed!\r\nCOMFORTABLE PRIVACY SPACE – Provides a private enclosed mansion for your furry babies, they can hide in their own secluded safety room when they want some peace.',1250,13,'https://m.media-amazon.com/images/I/71z1GFCtpZL._SL1498_.jpg','2025-07-02 13:34:21',NULL,NULL,1,6,NULL);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promo_codes`
--

DROP TABLE IF EXISTS `promo_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promo_codes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `discount_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `discount_value` float NOT NULL,
  `valid_from` datetime NOT NULL,
  `valid_until` datetime NOT NULL,
  `max_uses` int DEFAULT NULL,
  `uses` int DEFAULT NULL,
  `min_order_value` float DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promo_codes`
--

LOCK TABLES `promo_codes` WRITE;
/*!40000 ALTER TABLE `promo_codes` DISABLE KEYS */;
INSERT INTO `promo_codes` VALUES (1,'pet50','fixed',50,'2025-06-02 14:54:00','2025-12-31 00:00:00',20,1,199,1);
/*!40000 ALTER TABLE `promo_codes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `user_id` int NOT NULL,
  `rating` int NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,1,1,3,'great product','2025-05-01 13:41:49','2025-06-20 13:39:22'),(2,1,2,5,'great product , love it','2025-05-01 13:42:58','2025-05-22 10:09:00'),(3,2,1,2,'great product','2025-05-01 18:02:41','2025-05-01 19:30:15'),(5,3,2,3,'nice product','2025-06-02 11:46:07','2025-06-02 11:46:07'),(6,1,6,3,'best','2025-06-10 18:39:45','2025-06-10 18:59:00'),(7,3,1,3,'great product','2025-06-20 18:32:25','2025-06-20 18:32:25'),(8,30,1,3,'great product','2025-07-04 21:22:49','2025-07-04 21:22:49');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_analytics`
--

DROP TABLE IF EXISTS `sales_analytics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_analytics` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `total_sales` float DEFAULT NULL,
  `order_count` int DEFAULT NULL,
  `avg_order_value` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_analytics`
--

LOCK TABLES `sales_analytics` WRITE;
/*!40000 ALTER TABLE `sales_analytics` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_analytics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password_hash` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `google_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `profile_picture` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `google_id` (`google_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin@petpocket.com',NULL,'scrypt:32768:8:1$ELya5Hc12NLzSVU5$c29ebd8ad1af81be176b5f38cdb6f035a9adca93eb7d702887211f9ca96c2165cbc128352b06f83f45d9ddbcaf90709c09c439a7cc82947d16c79bc30564275d',1,'2025-07-17 18:27:17',NULL,NULL),(2,'manav','manavchawla146@gmail.com',NULL,'scrypt:32768:8:1$stF67v1n4HZBLMBV$475ca506bdd81e005bce9fc1a50e479587a3078350476a88184f62fb60d30f2e35471f52f8cce6b036623e6dad5391dc5235a3acbf5e4f2b8791ee07d8b09352',0,'2025-04-24 17:22:05',NULL,NULL),(3,'manav dodani','me@mydomain.com',NULL,'scrypt:32768:8:1$wiWM7A7hF6sqyIjr$1843f022ff5cd81c98ca21240cc8adb770de6af19487fccc9c0b8e454728b29082df47e8712e4e505fe690ecd1129a60482c1735e9c00ea97a544720617ecfa5',0,'2025-04-27 15:00:49',NULL,NULL),(4,'fav','fav@gmail.com',NULL,'scrypt:32768:8:1$2bF2qEQseUXiKM1W$455865e8e603e25dbb2115de7be85064f790aca27e2686864f9d21aa78efaafd73f117fe95c7f890b38a2da817c5825f5661b40cd0a81f68f06c6fd5f1a93360',0,'2025-05-22 21:30:52',NULL,NULL),(5,'frontend','frontend@gmail.com',NULL,'scrypt:32768:8:1$w83PwGwMQ84nTlle$ccb253312739ff64681bc34c7eb6052021e49310455762a843b3f8044d0f36b38816f0c7ef91bd0adc96691340a6755a7bc3530cbc87e25b9a7f47dbd172d21a',0,'2025-05-27 04:51:31',NULL,NULL),(6,'manavdodani','manavdodani2005@gmail.com',NULL,NULL,0,'2025-06-10 17:35:10','106839467905922325780','https://lh3.googleusercontent.com/a/ACg8ocIq4rkojZaq7-IRi1Eucp3uNsTZa0G_E1mhZbAvIVnGuUNk8MEB=s96-c'),(7,'rew','rew@gmail.com',NULL,'scrypt:32768:8:1$Qb4RKCVqUfu18e0Y$2351eb665c027f93cef988fcda65a470c9552a92c9b207ce0e29aa22c4619f0dc3e9eca27e862aef4faa561c39d233b9ab4a5a76634639da6d2ccf92ed236290',0,'2025-07-02 16:06:33',NULL,NULL),(8,'varun0406','varun.k@ahduni.edu.in',NULL,'scrypt:32768:8:1$0IeMacaWIu3QvGTL$9e4de3c87a2305f388f6d3116c16867a570abb7e3e5c7d1ca1670554676bb309abe324499203b7c39662ea8d5d8a872fba1b814d60ac0b10e0e92c1daf9dc297',0,'2025-07-17 20:09:02',NULL,NULL),(9,'varun000','kotwaniv03@outlook.com',NULL,'scrypt:32768:8:1$8WUaTKldm7lvnOMs$3b5182689abc0c48de72c976bacf5186312425c7f0f37543c15efaf911eedaffa6f0d4a75149775cface12b70533972607ed5ac90a706880e9173bf690999169',0,'2025-07-17 20:09:47',NULL,NULL),(10,'Babludon','babludon@gmail.com',NULL,'scrypt:32768:8:1$7E6UGEba05FSYsLl$18fed22f40145045cef56b6f0f93bd651dd3cb5202a77a89d681c01a126aa2ad068770a8d7f38596e26248fb091f7394c63f88f1c163e8272573f4d4b2cb7ab9',0,'2025-07-18 14:38:07',NULL,NULL),(11,'petswale','petswale.in@gmail.com',NULL,NULL,0,'2025-07-19 21:01:18','112866992872802231175','https://lh3.googleusercontent.com/a/ACg8ocIXEIdyvQ8kiP_kTJUMbJANh-U9j751ZoFDgY_b6fCif5GtZA=s96-c');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlist_items`
--

DROP TABLE IF EXISTS `wishlist_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishlist_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `wishlist_items_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `wishlist_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlist_items`
--

LOCK TABLES `wishlist_items` WRITE;
/*!40000 ALTER TABLE `wishlist_items` DISABLE KEYS */;
INSERT INTO `wishlist_items` VALUES (1,1,24),(4,1,30),(5,1,19),(6,1,18),(7,9,2);
/*!40000 ALTER TABLE `wishlist_items` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-24  1:23:54
