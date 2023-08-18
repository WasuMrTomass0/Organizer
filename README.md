# Organizer

- mariadb https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
- docker - python https://medium.com/oracledevs/create-a-simple-docker-container-with-a-python-web-server-26534205061a
- docker - python http https://www.youtube.com/watch?v=3hyIOUUBSlc

## SQL Tables

Column labels:

- `[O]` - optional


## Containers "containers"

| id          | location [O]   | description [O]    |
|-------------|----------------|--------------------|
| `x0132af`   | "Attic"        | "Shelf 1, Green"   |
<!-- | `x000001`   | "in-use"    | "in-use"       | "Out of the box"   | -->

```sql
CREATE TABLE containers (
    id INT AUTO_INCREMENT NOT NULL,
    location VARCHAR(255),
    description TEXT,

    PRIMARY KEY (id),
    UNIQUE (name)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Add container

all values

```sql
INSERT INTO containers
VALUES ("Attic", "Big black container");
```

not all values

```sql
INSERT INTO containers (description)
VALUES ("Big black container");
```

### Edit container

all values

```sql
UPDATE containers
SET location = "Garage",
    description = "Shelf 1, Green"
WHERE id = 1;
```

not all values

```sql
UPDATE containers
SET description = "Shelf 1, Green"
WHERE id = 1;
```

### Remove container
```sql
DELETE FROM containers
WHERE id = 1;
```

## Stored items "stored_items"

<!-- The goal: -->
<!-- | id          | containerid    | name        | description [O]    | category [O]   | image [O]      | created    | last edited|
|-------------|----------------|-------------|--------------------|----------------|----------------|------------|------------|
| `x2135a2`   | `x0132af`      | "Jacket"    | "Producer, Size"   | "Clothes"      | "binary_image" | timestamp  | timestamp  | -->

<!-- Basic -->
| id          | containerid    | name        | description [O]    | image [O]      | created    | edited     |
|-------------|----------------|-------------|--------------------|----------------|------------|------------|
| `x2135a2`   | `x0132af`      | "Jacket"    | "Producer, Size"   | "binary_image" | timestamp  | timestamp  |

```sql
CREATE TABLE stored_items (
    id INT AUTO_INCREMENT NOT NULL,
    containerid INT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    image MEDIUMBLOB,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    FOREIGN KEY (containerid) REFERENCES containers(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

<!-- ## TODO


### Elements in use "elements-in-use"

Note: copy table of "elements" or simple container called "in use"

**Note:**
Used for elements temporarily taken out from container - in use.
Thanks to this entry is not lost (name, image, description).

### Users ?????

| id    | username | password |
|-------|----------|----------|
| `x69` | `wasu`   | "qwerty" |

### Categories "categories" ?????

| id          | name        |
|-------------|-------------|
| `x12`       | "Clothes"   |
| `x16`       | "Shoes"     |
### Locations "locations" ?????

| id          | name        |
|-------------|-------------|
| `x12`       | "Garage"    |
| `x13`       | "Attic"     | -->