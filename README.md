
#Pinfluencer Backend


##API Documentation in Postman

https://go.postman.co/workspace/Pinfluencer~46fb64d6-e904-40ee-ba52-e706aaf77031/collection/13079574-0eddc995-40a9-4891-9319-b1d0edabcc1e

##Tables
```sql
CREATE TABLE `brand` 
( `id` varchar(36) NOT NULL, 
`name` varchar(120) NOT NULL, 
`description` varchar(500) NOT NULL, 
`website` varchar(120) NOT NULL, 
`email` varchar(120) NOT NULL, 
`instahandle` varchar(30) DEFAULT NULL, 
`auth_user_id` varchar(64) DEFAULT NULL, 
`created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, 
PRIMARY KEY (`id`), KEY `brand_id_index` (`id`) USING BTREE ) 
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```

```sql
CREATE TABLE `product` 
( `id` varchar(36) NOT NULL, 
`name` varchar(120) NOT NULL,
`description` varchar(500) NOT NULL, 
`requirements` varchar(500) DEFAULT NULL, 
`brand_id` varchar(36) NOT NULL, 
`created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, 
PRIMARY KEY (`id`), KEY `fk_brand_id` (`brand_id`), 
KEY `product_id_index` (`id`) USING BTREE, CONSTRAINT `fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`) ) 
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
```