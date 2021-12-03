
# Pinfluencer Backend

```sql
CREATE TABLE brand
( id varchar(36) PRIMARY KEY NOT NULL, 
  name varchar(120) NOT NULL, 
  description varchar(500) NOT NULL, 
  website varchar(120) NOT NULL, 
  email varchar(120) NOT NULL, 
  instahandle varchar(30) DEFAULT NULL, 
  auth_user_id varchar(64) DEFAULT NULL, 
  created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
) 

CREATE TABLE product
( id varchar(36) PRIMARY KEY NOT NULL, 
  name varchar(120) NOT NULL,
  description varchar(500) NOT NULL, 
  requirements varchar(500) DEFAULT NULL, 
  brand_id varchar(36) NOT NULL, 
  created TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, 
  CONSTRAINT fk_brand
    FOREIGN KEY(brand_id) 
	REFERENCES brand(id)
)
 
```

## API Documentation in Postman

https://go.postman.co/workspace/Pinfluencer~46fb64d6-e904-40ee-ba52-e706aaf77031/collection/13079574-0eddc995-40a9-4891-9319-b1d0edabcc1e
