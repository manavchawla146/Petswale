START TRANSACTION;

CREATE TABLE IF NOT EXISTS `users` (
	`id`	INT NOT NULL,
	`username`	VARCHAR(64) NOT NULL,
	`email`	VARCHAR(120) NOT NULL,
	`phone`	VARCHAR(15),
	`password_hash`	VARCHAR(128),
	`is_admin`	TINYINT(1),
	`created_at`	DATETIME,
	`google_id`	VARCHAR(100),
	`profile_picture`	VARCHAR(200),
	UNIQUE(`email`),
	CONSTRAINT `uq_users_google_id` UNIQUE(`google_id`),
	UNIQUE(`username`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `categories` (
	`id`	INT NOT NULL,
	`name`	VARCHAR(50) NOT NULL,
	`slug`	VARCHAR(50) NOT NULL,
	`image_url`	VARCHAR(200),
	`description`	TEXT,
	UNIQUE(`name`),
	UNIQUE(`slug`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `pet_types` (
	`id`	INT NOT NULL,
	`name`	VARCHAR(50) NOT NULL,
	`image_url`	VARCHAR(200),
	UNIQUE(`name`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `products` (
	`id`	INT NOT NULL,
	`name`	VARCHAR(100) NOT NULL,
	`description`	TEXT,
	`price`	FLOAT NOT NULL,
	`stock`	INT,
	`image_url`	VARCHAR(200),
	`created_at`	DATETIME,
	`pet_type_id`	INT NOT NULL,
	`category_id`	INT NOT NULL,
	`uploader_id`	INT,
	`weight`	FLOAT,
	`parent_id`	INT,
	FOREIGN KEY(`uploader_id`) REFERENCES `users`(`id`),
	CONSTRAINT `fk_product_parent` FOREIGN KEY(`parent_id`) REFERENCES `products`(`id`),
	FOREIGN KEY(`category_id`) REFERENCES `categories`(`id`),
	FOREIGN KEY(`pet_type_id`) REFERENCES `pet_types`(`id`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `orders` (
	`id`	INT NOT NULL,
	`user_id`	INT NOT NULL,
	`timestamp`	DATETIME,
	`total_price`	FLOAT NOT NULL,
	`payment_id`	VARCHAR(100),
	`order_id`	VARCHAR(100),
	`payment_status`	VARCHAR(20),
	FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `cart_items` (
	`id`	INT NOT NULL,
	`quantity`	INT NOT NULL,
	`user_id`	INT NOT NULL,
	`product_id`	INT NOT NULL,
	FOREIGN KEY(`product_id`) REFERENCES `products`(`id`),
	FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `order_items` (
	`id`	INT NOT NULL,
	`order_id`	INT NOT NULL,
	`product_id`	INT NOT NULL,
	`quantity`	INT NOT NULL,
	`price_at_purchase`	FLOAT NOT NULL,
	FOREIGN KEY(`order_id`) REFERENCES `orders`(`id`),
	FOREIGN KEY(`product_id`) REFERENCES `products`(`id`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `wishlist_items` (
	`id`	INT NOT NULL,
	`user_id`	INT NOT NULL,
	`product_id`	INT NOT NULL,
	FOREIGN KEY(`product_id`) REFERENCES `products`(`id`),
	FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `sales_analytics` (
	`id`	INT NOT NULL,
	`date`	DATE NOT NULL,
	`total_sales`	FLOAT,
	`order_count`	INT,
	`avg_order_value`	FLOAT,
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `page_views` (
	`id`	INT NOT NULL,
	`page`	VARCHAR(128) NOT NULL,
	`ip_address`	VARCHAR(45),
	`user_id`	INT,
	`user_agent`	VARCHAR(256),
	`timestamp`	DATETIME,
	FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `product_analytics` (
	`id`	INT NOT NULL,
	`product_id`	INT NOT NULL,
	`date`	DATE NOT NULL,
	`view_count`	INT,
	`cart_add_count`	INT,
	`purchase_count`	INT,
	FOREIGN KEY(`product_id`) REFERENCES `products`(`id`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `product_views` (
	`id`	INT NOT NULL,
	`product_id`	INT NOT NULL,
	`user_id`	INT,
	`ip_address`	VARCHAR(45),
	`timestamp`	DATETIME,
	FOREIGN KEY(`product_id`) REFERENCES `products`(`id`),
	FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `product_images` (
	`id`	INT NOT NULL,
	`product_id`	INT NOT NULL,
	`image_url`	VARCHAR(200) NOT NULL,
	`is_primary`	TINYINT(1),
	`display_order`	INT,
	FOREIGN KEY(`product_id`) REFERENCES `products`(`id`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `reviews` (
	`id`	INT NOT NULL,
	`product_id`	INT NOT NULL,
	`user_id`	INT NOT NULL,
	`rating`	INT NOT NULL,
	`content`	TEXT NOT NULL,
	`created_at`	DATETIME,
	`updated_at`	DATETIME,
	FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
	FOREIGN KEY(`product_id`) REFERENCES `products`(`id`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `product_attributes` (
	`id`	INT NOT NULL,
	`product_id`	INT NOT NULL,
	`key`	VARCHAR(100) NOT NULL,
	`value`	VARCHAR(200) NOT NULL,
	`display_order`	INT,
	FOREIGN KEY(`product_id`) REFERENCES `products`(`id`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `addresses` (
	`id`	INT NOT NULL,
	`user_id`	INT NOT NULL,
	`address_type`	VARCHAR(20) NOT NULL,
	`company_name`	VARCHAR(128),
	`street_address`	VARCHAR(256) NOT NULL,
	`apartment`	VARCHAR(128),
	`city`	VARCHAR(64) NOT NULL,
	`state`	VARCHAR(64) NOT NULL,
	`country`	VARCHAR(64) NOT NULL,
	`pin_code`	VARCHAR(10) NOT NULL,
	`is_default`	TINYINT(1),
	FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `promo_codes` (
	`id`	INT NOT NULL,
	`code`	VARCHAR(20) NOT NULL,
	`discount_type`	VARCHAR(20) NOT NULL,
	`discount_value`	FLOAT NOT NULL,
	`valid_from`	DATETIME NOT NULL,
	`valid_until`	DATETIME NOT NULL,
	`max_uses`	INT,
	`uses`	INT,
	`min_order_value`	FLOAT,
	`active`	TINYINT(1),
	UNIQUE(`code`),
	PRIMARY KEY(`id`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `alembic_version` (
	`version_num`	VARCHAR(32) NOT NULL,
	CONSTRAINT `alembic_version_pkc` PRIMARY KEY(`version_num`)
) ENGINE=InnoDB;

START TRANSACTION;

COMMIT;

INSERT INTO `alembic_version` (`version_num`) VALUES ('47c35232812c');

INSERT INTO `categories` (`id`,`name`,`slug`,`image_url`,`description`) VALUES (1,'Food','food','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMmjOp16EFp4cwmMat-EDMRaOYinfu6Iu45g&s','High-quality nutritious food options for your pets, including dry food, wet food, and treats.'),
 (2,'Toys','toys','/static/images/categories/toys.jpg','Fun and engaging toys to keep your pets entertained and active.'),
 (5,'Grooming','grooming','/static/images/categories/grooming.jpg','Grooming supplies and tools to keep your pet looking and feeling their best.'),
 (6,'Beds & Furniture','beds-furniture','/static/images/categories/beds.jpg','Comfortable beds, furniture, and housing options for your pets.');

INSERT INTO `pet_types` (`id`,`name`,`image_url`) VALUES (1,'Dog','https://cdn.shopify.com/s/files/1/1708/4041/files/custom_resized_lab_600x600.jpg?v=1668581125'),
 (2,'Cat','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeYtG28d9Rk0ObhCc5ilT8Cz0TsFPztP0V9w&s'),
 (3,'Birds','https://www.green-feathers.co.uk/cdn/shop/articles/robin-on-branch-royalty-free-image-1567774522.jpg?v=1729597011'),
 (4,'Fish','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSrO8Ln2MP__1A_Gs_1oN4DBtXeKTfbby1TKg&s');

INSERT INTO `addresses` (`id`,`user_id`,`address_type`,`company_name`,`street_address`,`apartment`,`city`,`state`,`country`,`pin_code`,`is_default`) VALUES (1,1,'home','','street address line number one','street address line number two','city name','Tamil Nadu','India','ZIP CODE OR POSTAL CODE',1),
 (2,2,'home','','street address line number one','street address line number two','jadjafd','Telangana','India','120123',0),
 (3,3,'home','','street address line number one','street address line number two','city name','Maharashtra','India','123456',0);

INSERT INTO `cart_items` (`id`,`quantity`,`user_id`,`product_id`) VALUES (1,1,1,1),
 (2,1,1,2);

INSERT INTO `wishlist_items` (`id`,`user_id`,`product_id`) VALUES (1,1,24),
 (4,1,30),
 (5,1,19),
 (6,1,18);

INSERT INTO `product_analytics` (`id`,`product_id`,`date`,`view_count`,`cart_add_count`,`purchase_count`) VALUES (1,31,'2025-07-02',2,0,0),
 (2,1,'2025-07-04',19,0,0),
 (3,3,'2025-07-04',1,0,0),
 (4,30,'2025-07-04',8,0,0),
 (5,27,'2025-07-04',1,0,0),
 (6,31,'2025-07-04',1,0,0),
 (7,25,'2025-07-04',2,0,0),
 (8,2,'2025-07-04',2,0,0),
 (9,23,'2025-07-04',1,0,0),
 (10,29,'2025-07-04',1,0,0),
 (11,24,'2025-07-04',2,0,0),
 (12,21,'2025-07-04',1,0,0),
 (13,18,'2025-07-04',4,0,0),
 (14,34,'2025-07-14',1,0,0),
 (15,1,'2025-07-14',9,0,0),
 (16,18,'2025-07-14',1,0,0),
 (17,3,'2025-07-14',1,0,0),
 (18,25,'2025-07-14',1,0,0);

INSERT INTO `product_images` (`id`,`product_id`,`image_url`,`is_primary`,`display_order`) VALUES (1,1,'https://placehold.co/800x800/46f27a/ffffff?text=Main',1,0),
 (2,1,'https://placehold.co/800x800/46f27a/ffffff?text=Side',0,1),
 (3,1,'https://placehold.co/800x800/46f27a/ffffff?text=Back',0,2),
 (4,1,'https://placehold.co/800x800/46f27a/ffffff?text=Detail',0,3),
 (6,3,'https://m.media-amazon.com/images/I/71fwkZg9m6L._AC_UF1000,1000_QL80_.jpg',0,2),
 (7,3,'https://plus.unsplash.com/premium_photo-1666777247416-ee7a95235559?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZG9nfGVufDB8fDB8fHww',0,1),
 (9,2,'https://m.media-amazon.com/images/I/71BdAbA9D7L._AC_UL480_FMwebp_QL65_.jpg',0,1);

INSERT INTO `reviews` (`id`,`product_id`,`user_id`,`rating`,`content`,`created_at`,`updated_at`) VALUES (1,1,1,3,'great product','2025-05-01 13:41:49.325894','2025-06-20 13:39:21.531043'),
 (2,1,2,5,'great product , love it','2025-05-01 13:42:57.856186','2025-05-22 10:08:59.696986'),
 (3,2,1,2,'great product','2025-05-01 18:02:41.418195','2025-05-01 19:30:14.899292'),
 (5,3,2,3,'nice product','2025-06-02 11:46:07.122333','2025-06-02 11:46:07.122333'),
 (6,1,6,3,'best','2025-06-10 18:39:45.357265','2025-06-10 18:59:00.069759'),
 (7,3,1,3,'great product','2025-06-20 18:32:25.131633','2025-06-20 18:32:25.131633'),
 (8,30,1,3,'great product','2025-07-04 21:22:48.791191','2025-07-04 21:22:48.791191');

INSERT INTO `products` (`id`,`name`,`description`,`price`,`stock`,`image_url`,`created_at`,`pet_type_id`,`category_id`,`uploader_id`,`weight`,`parent_id`) VALUES (1,'Royal Canin Maxi Adult Dog Food','Premium dry dog food specially formulated for large adult dogs',54.99,70,'https://m.media-amazon.com/images/I/71fwkZg9m6L._AC_UF1000,1000_QL80_.jpg','2025-04-23 12:58:08.998450',1,1,1,NULL,NULL),
 (2,'Hills Science Diet Wet Dog Food','Grain-free wet food with real chicken',34.99,134,'https://m.media-amazon.com/images/I/71BdAbA9D7L._AC_UL480_FMwebp_QL65_.jpg','2025-04-23 12:58:08.998450',1,1,1,NULL,NULL),
 (3,'KONG Classic Dog Toy','Durable rubber chew toy for mental stimulation',14.99,71,'https://tse3.mm.bing.net/th/id/OIP.DwBQA_UAZaEwWgPHHS5-sQAAAA?pid=Api&P=0&h=180','2025-04-23 12:58:08.998450',1,2,1,NULL,NULL),
 (18,'  Royal Canin Maxi Adult Dog Food, 5kg','anything for now',90.0,1,'https://images.unsplash.com/photo-1567752881298-894bb81f9379?q=80&w=600&auto=format&fit=crop','2025-05-03 01:30:32.235501',1,1,NULL,5.0,1),
 (19,'Grain-Free Chicken Chow','Made using farm fresh chicken and nutrient-packed veggies simmered in our 24-hour Bone Broth. This NO GRAIN, high-protein, low-carb meal is packed with natural vitamins and collagen for your dog’s health, energy and happiness – and ZERO fillers or preservatives.',999.0,10,'https://petchef.co.in/cdn/shop/files/grain_free_chicken_chow_f7e4833f-85f0-4747-ad31-73e9517effaa.jpg?v=1740665508&width=800','2025-07-02 12:55:49.732833',1,1,NULL,NULL,NULL),
 (20,'Grain-Free Mutton Nom Nom','Mutton muscle, organ meat, high-nutrition vegetables and all-natural supplements cooked in our signature 24-hour Bone Broth. This NO GRAIN, high-protein, low-carb meal is a fully balanced meal that provides your dogs with all the macro and micronutrients they need.



',550.0,5,'https://petchef.co.in/cdn/shop/files/grain_free_motton_nom_618da3b9-9731-4e76-824d-68bef6678336.jpg?v=1740664254&width=800','2025-07-02 12:57:15.816983',1,1,NULL,NULL,NULL),
 (21,'Wholesome Mutton Nom Nom','Mutton muscle, organ meat, vegetables like pumpkin and sweet potato, all-natural supplements and brown rice cooked in our signature 24-hour Bone Broth. High in protein and collagen, it’s great for your dog’s coat and gut.',700.0,7,'https://petchef.co.in/cdn/shop/files/mutton_nom_6f33f0c1-f011-4a46-9a46-895c3a9d7f23.jpg?v=1740664370&width=800','2025-07-02 12:58:10.225846',1,1,NULL,NULL,NULL),
 (22,'Grain-Free Chicken Chow','Made using farm fresh chicken and nutrient-packed veggies simmered in our 24-hour Bone Broth. This NO GRAIN, high-protein, low-carb meal is packed with natural vitamins and collagen for your dog’s health, energy and happiness – and ZERO fillers or preservatives',400.0,6,'https://petchef.co.in/cdn/shop/files/grain_free_chicken_chow_f7e4833f-85f0-4747-ad31-73e9517effaa.jpg?v=1740665508&width=800','2025-07-02 12:59:04.963254',1,1,NULL,NULL,NULL),
 (23,'Wobble Wag Giggle ball Interactive Dog Toy','FUN FOR ALL BIG OR SMALL: This interactive dog toy is great for dogs of all ages and sizes! The 6 clutch pockets on this interactive toy make it easy for your dog to pick up during playtime!

WOBBLE WAG GIGGLE BALL: With just the nudge of a nose, off the ball, goes! Wobble Wag Giggle does not require batteries - the secret is the internal tube noisemaker inside the dog ball, and the enticing “play-with-me” sounds are sure to engage your pup as the toy rolls around!',600.0,10,'https://pawsindia.com/cdn/shop/products/57c91479-aef4-4a3d-a304-44835df6846b_1.448de7dbef33fe2b8477034b9fd6c6b6_1_4238e93e-7d75-4402-8e36-f9f11b63ad7b.webp?v=1666088744','2025-07-02 13:06:48.028521',1,2,NULL,NULL,NULL),
 (24,'Barrel Treat Dog Toy- Blue','Natural Rubber: Natural rubber is used in the toy, keeping in mind your dog''s safety. The natural rubber is safe to chew and suitable for your dog''s jaw. The natural rubber has just the right amount of hardness which makes chewing on the toy desirable and stimulating for your dog.

Eco-friendly: Unlike plastic and other harmful materials, natural rubber is eco-friendly.',800.0,20,'https://pawsindia.com/cdn/shop/products/7_4.jpg?v=1617613123','2025-07-02 13:07:38.149872',1,2,NULL,NULL,NULL),
 (25,'Brush Ball Teeth Cleaning Toy','The ball is made from high-quality, non-toxic rubber that is safe for your dog to play with. The soft bristles are designed to gently brush your dog’s teeth as they play, helping to remove plaque and tartar buildup and promote better oral hygiene.

It isn''t just a toothbrush — it''s also a fun and engaging toy! Playtime with this toy will keep your dog active & engaged which will improve their intelligence & happiness. It is great for playing fetch and interacting with your dog. The toy produces fun sounds when your dog moves it around, picks it up, or shakes it, which can keep them entertained. It does not require batteries and is an excellent way to keep your pet occupied when you are not available.

',500.0,10,'https://pawsindia.com/cdn/shop/files/1_2870219f-3461-4399-a7b4-a743d0bd83ce.jpg?v=1683290555','2025-07-02 13:12:34.234609',1,2,NULL,NULL,NULL),
 (26,'Ultimate Chew Stick Dog Toy','The Ultimate Chew Stick is the last chew toy you''ll need for your dog. This chew toy''s rubber body can easily handle the strongest bites. Just give it to your dog and watch them go to town with the toy. If your dog feels like losing interest in the toy, the built-in squeaker will keep it hooked.',769.0,20,'https://pawsindia.com/cdn/shop/products/red1.jpg?v=1661421340','2025-07-02 13:13:27.142425',1,2,NULL,NULL,NULL),
 (27,'Self Cleaning Slicker Brush','Clean Pets, Clean House. emily cat & dog brush for shedding can easily remove loose hair, shedding mats, tangled hair, dander and dirt of your lovely pet, which not only keep your pet clean, but also provide you with a clean and hygienic home environment.

',247.0,10,'https://m.media-amazon.com/images/I/61qjyzM3+BL._SL1500_.jpg','2025-07-02 13:18:18.775017',1,5,NULL,NULL,NULL),
 (29,'PET Grooming Wet Wipes','Wipe provides a fast,convenient way to keep your pet clean and fresh everyday.Each extra soft pet wipe is moistened with a natural formula that helps maintain a clean and healthy pet.Gentle enough to use everyday around pet''s eyes,ears,face and body



',450.0,21,'https://m.media-amazon.com/images/I/81xU7fjrNcL._SL1500_.jpg','2025-07-02 13:20:03.904485',1,5,NULL,NULL,NULL),
 (30,'Animal Nail Cutter ','The pet nail clippers are made out of high quality 4.0 mm thick stainless steel sharp blades, it is powerful enough to trim your dogs or cats nails with just one cut, these durable clippers won''t bend, scratch or rust, and the blades still keep sharp even through many sessions on dog tough nails.',330.0,10,'https://m.media-amazon.com/images/I/61oJ7Q+BOaL._SL1500_.jpg','2025-07-02 13:27:53.239185',1,5,NULL,NULL,NULL),
 (31,'Velvet Cave House Bed','Material: Made of high quality soft velvet, good quality foam and cotton filling. It offers your pet a comfortable place for sleeping and resting.

Maintenance: It is easy to clean and washable in gentle mode in washing machine or hand wash. The product is vacuum sealed for safe transportation, hence recommended to pat it, shake it and leave for 48 hours before using so that it gets back to its actual fluffy shape

Note: If your pet has an excessive chewing habit, please keep a toy on the bed so that the pet will not damage the bed by treating it as a chew toy',2000.0,5,'https://m.media-amazon.com/images/I/818848PvqNL._SL1500_.jpg','2025-07-02 13:30:04.012786',1,6,NULL,NULL,NULL),
 (32,'Light Weight Mat','MULTI-USAGE - Absorbs body heat and helps relax your pets. A perfect crate and sleeping mat for your pets, can be used on the floor, sofa, bed.

This stylish dog mat measures (Size - 20X 28 Inches) for Puppies & Small Dogs

Dog mats are washable and easy to maintain.',1100.0,8,'https://m.media-amazon.com/images/I/61VRUdkZaBL._SL1440_.jpg','2025-07-02 13:31:15.467165',1,6,NULL,NULL,NULL),
 (34,'Round Donut Pet Bed ','Zexsazone Pet Bed, meticulously designed to offer the utmost comfort and style for your furry friend. Measuring 50 x 50 x 12 cm, this small-sized bed is perfect for cats, puppies, and small dog breeds.

Eco-Friendly Materials: Made from sustainable and non-toxic materials, this bed is safe for your pet and the environment. The high-quality stuffing retains its shape, providing consistent comfort and durability.',1450.0,5,'https://m.media-amazon.com/images/I/41BoiTIO43L.jpg','2025-07-02 13:32:49.423426',1,6,NULL,NULL,NULL),
 (35,'Igloo Dog House','PLENTY OF ROOM INSIDE – Perfectly stitched bed roomy & comfy for pets to turn around and lie straight inside, your furry babies love this cozy igloo bed!

COMFORTABLE PRIVACY SPACE – Provides a private enclosed mansion for your furry babies, they can hide in their own secluded safety room when they want some peace.',1250.0,13,'https://m.media-amazon.com/images/I/71z1GFCtpZL._SL1498_.jpg','2025-07-02 13:34:21.408022',1,6,NULL,NULL,NULL);

INSERT INTO `product_attributes` (`id`,`product_id`,`key`,`value`,`display_order`) VALUES (1,2,'Dimensions','55*35*12',1);

INSERT INTO `users` (`id`,`username`,`email`,`phone`,`password_hash`,`is_admin`,`created_at`,`google_id`,`profile_picture`) VALUES (1,'admin','admin@petpocket.com',NULL,'scrypt:32768:8:1$ELya5Hc12NLzSVU5$c29ebd8ad1af81be176b5f38cdb6f035a9adca93eb7d702887211f9ca96c2165cbc128352b06f83f45d9ddbcaf90709c09c439a7cc82947d16c79bc30564275d',1,NULL,NULL,NULL),
 (2,'manav','manavchawla146@gmail.com',NULL,'scrypt:32768:8:1$stF67v1n4HZBLMBV$475ca506bdd81e005bce9fc1a50e479587a3078350476a88184f62fb60d30f2e35471f52f8cce6b036623e6dad5391dc5235a3acbf5e4f2b8791ee07d8b09352',0,'2025-04-24 17:22:04.653215',NULL,NULL),
 (3,'manav dodani','me@mydomain.com',NULL,'scrypt:32768:8:1$wiWM7A7hF6sqyIjr$1843f022ff5cd81c98ca21240cc8adb770de6af19487fccc9c0b8e454728b29082df47e8712e4e505fe690ecd1129a60482c1735e9c00ea97a544720617ecfa5',0,'2025-04-27 15:00:48.949265',NULL,NULL),
 (4,'fav','fav@gmail.com',NULL,'scrypt:32768:8:1$2bF2qEQseUXiKM1W$455865e8e603e25dbb2115de7be85064f790aca27e2686864f9d21aa78efaafd73f117fe95c7f890b38a2da817c5825f5661b40cd0a81f68f06c6fd5f1a93360',0,'2025-05-22 21:30:51.904536',NULL,NULL),
 (5,'frontend','frontend@gmail.com',NULL,'scrypt:32768:8:1$w83PwGwMQ84nTlle$ccb253312739ff64681bc34c7eb6052021e49310455762a843b3f8044d0f36b38816f0c7ef91bd0adc96691340a6755a7bc3530cbc87e25b9a7f47dbd172d21a',0,'2025-05-27 04:51:30.826015',NULL,NULL),
 (6,'manavdodani','manavdodani2005@gmail.com',NULL,NULL,0,'2025-06-10 17:35:10.364218','106839467905922325780','https://lh3.googleusercontent.com/a/ACg8ocIq4rkojZaq7-IRi1Eucp3uNsTZa0G_E1mhZbAvIVnGuUNk8MEB=s96-c'),
 (7,'rew','rew@gmail.com',NULL,'scrypt:32768:8:1$Qb4RKCVqUfu18e0Y$2351eb665c027f93cef988fcda65a470c9552a92c9b207ce0e29aa22c4619f0dc3e9eca27e862aef4faa561c39d233b9ab4a5a76634639da6d2ccf92ed236290',0,'2025-07-02 16:06:33.272102',NULL,NULL);

INSERT INTO `promo_codes` (`id`,`code`,`discount_type`,`discount_value`,`valid_from`,`valid_until`,`max_uses`,`uses`,`min_order_value`,`active`) VALUES (1,'pet50','fixed',50.0,'2025-06-02 14:54:00.000000','2025-12-31 00:00:00.000000',20,1,199.0,1);

COMMIT;