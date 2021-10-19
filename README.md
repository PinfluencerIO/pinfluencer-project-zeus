```
CREATE TABLE `brand` 
    (`id` varchar(36) NOT NULL,
     `name` varchar(80) NOT NULL,
     `bio` varchar(500) NOT NULL,
     `website` varchar(120) NOT NULL,
     `email` varchar(120) NOT NULL,
     `auth_user_id` varchar(64) DEFAULT NULL,
     `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`), 
     `version` int NOT NULL,
KEY `brand_id_index` (`id`) USING BTREE) 
ENGINE=InnoDB DEFAULT
CHARSET=latin1
```