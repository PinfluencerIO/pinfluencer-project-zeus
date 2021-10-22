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

##Public endpoints

**20 most recent products, limited to 3 products per brand**

`GET /feed`

**Get all Brands**

`GET /brands`

**Get Brand by Id**

`GET /brand/{brand_id}`

**Get all Products for Brand**

`GET /brands/{brand_id}/products`

**Get all Products**

`GET /products`

**Get Product by Id**

`GET /products/{product_id}`

##Authenticated endpoints

**Get authenticated Brand**

`GET /brands/me`

**Create authenticated Brand**

`POST /brands/me`

<span style="color:red; font-size:1rem">Only callable once at onboard</span>.

**Update authenticated Brand**

`PUT /brands/me`

**Get Products for authenticated Brand**

`GET /products/me`

**Create Product for authenticated Brand**

`POST /products/me`

**Get Product by Id for authenticated Brand**

`GET /products/me/{product_id}`

**Update Product by Id for authenticated Brand**

`PUT /products/me/{product_id}`

**Delete Product by Id for authenticated Brand**

`DELETE /products/me/{product_id}`