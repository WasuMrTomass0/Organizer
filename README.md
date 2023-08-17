# Organizer

- mariadb https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
- docker - python https://medium.com/oracledevs/create-a-simple-docker-container-with-a-python-web-server-26534205061a
- docker - python http https://www.youtube.com/watch?v=3hyIOUUBSlc

## SQL Tables

Column labels:

- `[O]` - optional

### Containers "containers"

| id          | name        | location [O]   | description [O]    |
|-------------|-------------|----------------|--------------------|
| `x0132af`   | "BOX001"    | "Attic"        | "Shelf 1, Green"   |
<!-- | `x000001`   | "in-use"    | "in-use"       | "Out of the box"   | -->

```sql
CREATE TABLE containers (
    id INT AUTO_INCREMENT NOT NULL,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    description TEXT,

    PRIMARY KEY (id)
);
```

### Elements "elements"

<!-- The goal: -->
<!-- | id          | containerid    | name        | description [O]    | category [O]   | image [O]      | created    | last edited|
|-------------|----------------|-------------|--------------------|----------------|----------------|------------|------------|
| `x2135a2`   | `x0132af`      | "Jacket"    | "Producer, Size"   | "Clothes"      | "binary_image" | timestamp  | timestamp  | -->

<!-- Basic -->
| id          | containerid    | name        | description [O]    | image [O]      | created    | edited     |
|-------------|----------------|-------------|--------------------|----------------|------------|------------|
| `x2135a2`   | `x0132af`      | "Jacket"    | "Producer, Size"   | "binary_image" | timestamp  | timestamp  |

```sql
CREATE TABLE elements (
    id INT AUTO_INCREMENT NOT NULL,
    containerid INT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    image MEDIUMBLOB,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    CONSTRAINT FK_containerid FOREIGN KEY (containerid) REFERENCES containers(id)
);
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