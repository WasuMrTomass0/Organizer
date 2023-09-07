# SQL Notes

Column labels:

- `[O]` - optional


## Stored items "stored_items"

| id          | containerid    | name        | description [O]    | quantity | image [O]      | created    | edited     |
|:-----------:|:--------------:|:-----------:|:------------------:|:--------:|:--------------:|:----------:|:----------:|
| `x2135a2`   | `x0132af`      | "Jacket"    | "Producer, Size"   |     1    | "binary_image" | timestamp  | timestamp  |


```sql
CREATE TABLE stored_items (
    id INT AUTO_INCREMENT NOT NULL,
    containerid INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    quantity INT NOT NULL,
    image MEDIUMBLOB,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id),
    KEY (containerid),
    FOREIGN KEY (containerid) REFERENCES containers(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```


### Items in use "items_in_use"

Note: copy table of "stored_items"

**Note:**
Used for items temporarily taken out from container - in use.
Thanks to this entry is not lost when it is taken out from container for some time.


## Containers "containers"

| id          | location       | description        |
|:-----------:|:--------------:|:------------------:|
| `x0132af`   | "Attic"        | "Shelf 1, Green"   |
<!-- | `x000001`   | "in-use"    | "in-use"       | "Out of the box"   | -->

```sql
CREATE TABLE containers (
    id INT AUTO_INCREMENT NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT,

    PRIMARY KEY (id),
    FOREIGN KEY (location) REFERENCES locations(name)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```


### Locations "locations"

| name        |
|:-----------:|
| "Garage"    |
| "Attic"     |

```sql
CREATE TABLE locations (
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (name)
) CHARACTER SET utf8mb4 COLLATE UTF8MB4_UNICODE_CI;
```
