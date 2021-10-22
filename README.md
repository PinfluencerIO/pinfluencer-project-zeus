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

#####Response
```json
[]
```
----

###Get all Brands

`GET /brands`

#####Response
```json
[
    {
        "id": "1a7eae3a-aab9-4186-9dfa-ba59cd6f6b94",
        "name": "Business name",
        "bio": "Some bio information",
        "description": "",
        "website": "https://www.business-name.x.com",
        "email": "aidanwilliamgannon@gmail.com",
        "image": {
            "filename": "filename.jpg"
        },
        "auth_user_id": "google_111301613487480417915"
    }
]
```

-----------

**Get Brand by Id**

`GET /brands/{brand_id}`
#####Request
`GET /brands/1a7eae3a-aab9-4186-9dfa-ba59cd6f6b94`
#####Response
```json
{
    "id": "1a7eae3a-aab9-4186-9dfa-ba59cd6f6b94",
    "name": "Business name",
    "bio": "Some bio information",
    "description": "",
    "website": "https://www.business-name.x.com",
    "email": "aidanwilliamgannon@gmail.com",
    "image": {
        "filename": "filename.jpg"
    },
    "auth_user_id": "google_111301613487480417915"
}
```
-----------

**Get all Products for Brand**

`GET /brands/{brand_id}/products`
#####Request
`GET /brands/1a7eae3a-aab9-4186-9dfa-ba59cd6f6b94/products`
#####Response
```json
[
    {
        "id": "4f9cf273-f37f-44db-be0c-a081fd200a54",
        "name": "Product Name",
        "description": "Some product information",
        "image": {
            "filename": "product-image.jpg"
        },
        "requirements": "",
        "brand_id": "180f6e0c-cc58-46e4-9d89-5d74b32c7bb5",
        "brand_name": "Business name"
    }
]
```
-----------


**Get all Products**

`GET /products`
#####Request
`GET /products`
#####Response
```json
[
  {
    "id": "4f9cf273-f37f-44db-be0c-a081fd200a54",
    "name": "Product Name",
    "description": "Some product information",
    "image": {
        "filename": "product-image.jpg"
    },
    "requirements": "",
    "brand_id": "180f6e0c-cc58-46e4-9d89-5d74b32c7bb5",
    "brand_name": "Business name"
  }
]
```
-----------


**Get Product by Id**

`GET /products/{product_id}`
#####Request
`GET /products/4f9cf273-f37f-44db-be0c-a081fd200a54`

#####Response
```json
{
    "id": "4f9cf273-f37f-44db-be0c-a081fd200a54",
    "name": "Product Name",
    "description": "Some product information",
    "image": {
        "filename": "product-image.jpg"
    },
    "requirements": "",
    "brand_id": "180f6e0c-cc58-46e4-9d89-5d74b32c7bb5",
    "brand_name": "Business name"
}
```
-----------


##Authenticated endpoints

**Get authenticated Brand**

`GET /brands/me`
#####Request
`GET /brands/me`
#####Response
```json
{
    "id": "1a7eae3a-aab9-4186-9dfa-ba59cd6f6b94",
    "name": "Business name",
    "bio": "Some bio information",
    "description": "",
    "website": "https://www.business-name.x.com",
    "email": "aidanwilliamgannon@gmail.com",
    "image": {
        "filename": "filename.jpg"
    },
    "auth_user_id": "google_111301613487480417915"
}
```
-----------


**Create authenticated Brand**

`POST /brands/me`

<span style="color:red; font-size:1rem">Only callable once at onboard</span>.

email is only used if cognito claim for email is blank
#####Request
`POST /brands/me`
```json
{
  "name": "Business name",
    "bio": "Some bio information",
    "description": "",
    "website": "https://www.business-name.x.com",
    "email": "aidanwilliamgannon@gmail.com",
    "image": {
        "filename": "filename.jpg",
        "bytes": "BASE64 ENCODED IMAGE BYTES"
    }
}
```
#####Response
```json
1a7eae3a-aab9-4186-9dfa-ba59cd6f6b94
```
-----------


**Update authenticated Brand**

`PUT /brands/me`

Email is ignored is cognito claim has email already
#####Request
```json
{
  "name": "NEW Business name",
    "bio": "Updated business information",
    "description": "",
    "website": "https://www.business-name.x.com",
    "email": "aidanwilliamgannon@gmail.com",
    "image": {
        "filename": "filename.jpg",
        "bytes": "BASE64 ENCODED IMAGE BYTES"
    }
}
```
-----------


**Get all Products for authenticated Brand**

`GET /products/me`
#####Response
```json
[
  {
    "id": "4f9cf273-f37f-44db-be0c-a081fd200a54",
    "name": "Product Name",
    "description": "Some product information",
    "image": {
        "filename": "product-image.jpg"
    },
    "requirements": "",
    "brand_id": "180f6e0c-cc58-46e4-9d89-5d74b32c7bb5",
    "brand_name": "Business name"
  }
]
```
-----------


**Create Product for authenticated Brand**

`POST /products/me`
#####Response
```json
4f9cf273-f37f-44db-be0c-a081fd200a54
```
-----------


**Get Product by Id for authenticated Brand**

`GET /products/me/{product_id}`
#####Response
```json
{
    "id": "4f9cf273-f37f-44db-be0c-a081fd200a54",
    "name": "Product Name",
    "description": "Some product information",
    "image": {
        "filename": "product-image.jpg"
    },
    "requirements": "",
    "brand_id": "180f6e0c-cc58-46e4-9d89-5d74b32c7bb5",
    "brand_name": "Business name"
}
```
-----------


**Update Product by Id for authenticated Brand**

`PUT /products/me/{product_id}`
#####Request
```json
{

    "name": "UPDATED Product Name",
    "description": "Some product information",
    "image": {
        "filename": "product-image.jpg"
    },
    "requirements": "",
    "brand_id": "180f6e0c-cc58-46e4-9d89-5d74b32c7bb5",
    "brand_name": "Business name"
  }
```
#####Response
```json
{
    "id": "4f9cf273-f37f-44db-be0c-a081fd200a54",
    "name": "UPDATEDProduct Name",
    "description": "Some product information",
    "image": {
        "filename": "product-image.jpg"
    },
    "requirements": "",
    "brand_id": "180f6e0c-cc58-46e4-9d89-5d74b32c7bb5",
    "brand_name": "Business name"
  }
```
-----------


**Delete Product by Id for authenticated Brand**

`DELETE /products/me/{product_id}`
#####Response
```json
{}
```
-----------
