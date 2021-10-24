
#Pinfluencer Backend


##API Documentation in Postman

https://go.postman.co/workspace/Pinfluencer~46fb64d6-e904-40ee-ba52-e706aaf77031/collection/13079574-85ccb13b-1609-4717-b6ec-1d3820ccf73a


##Tables
```sql
CREATE TABLE `brand` 
(`id` varchar(36) NOT NULL,
 `name` varchar(120) NOT NULL,
 `description` varchar(500) NOT NULL,
 `website` varchar(120) NOT NULL,
 `email` varchar(120) NOT NULL,
 `image` varchar(120) NOT NULL,
 `auth_user_id` varchar(64) DEFAULT NULL,
 `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, 
 PRIMARY KEY (`id`), 
 KEY `brand_id_index` (`id`) USING BTREE)
```

```sql
CREATE TABLE `product` 
( `id` varchar(36) NOT NULL, 
`name` varchar(120) NOT NULL, 
`description` varchar(500) NOT NULL, 
`requirements` varchar(500) DEFAULT NULL, 
`image` varchar(120) DEFAULT NULL, 
`brand_id` varchar(36) NOT NULL, 
`brand_name` varchar(500) DEFAULT NULL, 
`created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP, 
PRIMARY KEY (`id`), 
KEY `fk_brand_id` (`brand_id`), 
KEY `product_id_index` (`id`) 
USING BTREE, CONSTRAINT `fk_brand_id` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`id`) ) 
```
