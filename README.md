# Organizer

mariadb https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
docker - python https://medium.com/oracledevs/create-a-simple-docker-container-with-a-python-web-server-26534205061a
docker - python http https://www.youtube.com/watch?v=3hyIOUUBSlc

## SQL Tables

- `[O]` - optional

### Containers "containers"

| id          | name        | location [O]   | description [O]    | image [O]      |
|-------------|-------------|----------------|--------------------|----------------|
| `x0132af`   | "BOX001"    | "Attic"        | "Shelf 1, Green"   | "base64_image" |

querry:

```sql
CREATE TABLE containers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    description TEXT,
    image LONGBLOB
)
```

**Note:**
How to connect location with entries in table? 
Is it needed?

### Elements "elements"

| id          | container      | name        | description [O]    | category [O]   | image [O]      | created    | last edited|
|-------------|----------------|-------------|--------------------|----------------|----------------|------------|------------|
| `x2135a2`   | `x0132af`      | "Jacket"    | "Producer, Size"   | "Clothes"      | "base64_image" | timestamp  | timestamp  |

### Elements in use "elements-in-use"

| id          | container (previous) | name        | description [O]    | category [O]   | image [O]      | created    | last edited|
|-------------|----------------------|-------------|--------------------|----------------|----------------|------------|------------|
| `x2135a2`   | `x0132af`            | "Jacket"    | "Producer, Size"   | "Clothes"      | "base64_image" | timestamp  | timestamp  |

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
| `x13`       | "Attic"     |