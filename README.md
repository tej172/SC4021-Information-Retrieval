# SC4021-Information-Retrieval

# Solr Setup Guide

## Prerequisites

- **Java Installation:** Ensure Java is installed by running:
```sh
java -version
```
- **Set JAVA_HOME:**
  1. Check if `JAVA_HOME` is set:
  ```sh
echo %JAVA_HOME%
  ```
  2. If not set, locate the Java installation path:
  ```sh
where java
  ```
  Example output:
  ```sh
C:\Program Files\Eclipse Adoptium\jdk-11.0.18.10-hotspot\bin\java.exe
  ```
  3. Set `JAVA_HOME` in Command Prompt (`cmd`):
  ```cmd
setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-11.0.18.10-hotspot" /M
  ```

## Solr Installation

1. **Download Solr Binary Release:** [Apache Solr](https://solr.apache.org/downloads.html)
2. **Extract the Solr archive:**
```sh
tar -xvzf ./solr-8.5.0.tgz -C {your_chosen_directory}
```
Replace `{your_chosen_directory}` with the target directory.

## Running Solr

1. **Navigate to Solr Directory:**
```sh
cd solr-9.8.0
```

2. **Start Solr Server:**
```sh
bin/solr.cmd start -p 8983
```

3. **Access Solr Admin UI:**
```
http://localhost:8983/solr/
```

## Creating and Managing Solr Cores

- **Create a Core:**
```sh
bin/solr create -c mycore
```
- **Navigate Back to Code Folder:**
```sh
cd ..
```
- **Stop Solr Server:**
```sh
bin/solr stop -p 8983
```

## Example: Multiple Solr Cores

- `products_core`: For product information (name, category, price, description)
- `customers_core`: For customer details (name, email, address)
- `orders_core`: For order history (customer ID, order date, total amount)

## Solr vs. Relational Databases

| Feature               | Solr (Search Engine)                  | Relational Database (SQL-based)    |
|-----------------------|---------------------------------------|----------------------------------|
| Data Structure       | Schema-based (JSON/XML documents)    | Tables with rows & columns         |
| Primary Purpose      | Full-text search & fast lookups       | Data storage & transactions        |
| Query Language       | Solr Query Syntax / Lucene Queries    | SQL (SELECT, JOIN, etc.)           |
| Joins & Relations    | Limited join capabilities             | Strong support for joins & normalization |
| Performance          | Optimized for large text datasets     | Optimized for structured data transactions |

## Additional Notes for Git Bash Users

- Use `export` instead of `setx` for setting environment variables:
```sh
export JAVA_HOME="/c/Program Files/Eclipse Adoptium/jdk-21.0.6.7-hotspot"
```
- Verify with:
```sh
echo $JAVA_HOME
```

