

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `adminDB` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
CREATE USER 'admin'@'localhost' IDENTIFIED BY '1z^4A6U9N0pf7#doVkNzNEf&PKED^GCa';
GRANT SELECT ON adminDB.* TO 'admin'@'localhost';

USE `adminDB`;
DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `username` varchar(25) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;


LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Administrator','s00p3rs3cr3tpa$$w0rd!'),(2,'ali','s9N!26BMO5Zq@n70D9'),(3,'yasho','Na987J*0d0ruoXB'),(4,'amirabbas','F70i8!btKMmLQCV#2'),(5,'mohammad','8A66%beEuZQRBJjCFd'),(6,'sadra','37Jw6!d0K5vf4gOXA'),(7,'mari','r7PW88*bb7^');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

