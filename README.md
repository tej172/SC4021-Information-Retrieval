# SC4021 Info Ret.

# Apache Solr Setup & Usage

This guide walks you through downloading, installing, and running Apache Solr. It also covers setting up your Java environment (JAVA_HOME) and provides a quick comparison between Solr and a traditional relational database.

---

## 1. Prerequisites

### 1.1 Check Java Installation

#### On Windows (Command Prompt)
1. **Open Command Prompt:** Press `Windows + R`, type `cmd`, and press Enter.
2. **Check Java Version:**
```cmd
java -version
```
- If Java is installed, you'll see a version output like `java version "11.0.18"`.
- If not installed, download Java from [Adoptium](https://adoptium.net/download/) or [Oracle](https://www.oracle.com/java/technologies/downloads/).

#### On Git Bash or Unix-like Terminal
```bash
java -version
```
- You should see version information if Java is installed.

### 1.2 Set JAVA_HOME (Windows)

#### Find Java Path
```cmd
where java
```
- Choose the correct Java path, for example:
```cmd
C:\Users\YourName\AppData\Local\Programs\Eclipse Adoptium\jdk-21.0.6.7-hotspot\bin\java.exe
```
- Copy everything before `\bin\java.exe`, e.g.:
```cmd
C:\Users\YourName\AppData\Local\Programs\Eclipse Adoptium\jdk-21.0.6.7-hotspot
```

#### Set JAVA_HOME Temporarily
```cmd
set JAVA_HOME=C:\Users\YourName\AppData\Local\Programs\Eclipse Adoptium\jdk-21.0.6.7-hotspot
```

#### Set JAVA_HOME Permanently
```cmd
setx JAVA_HOME "C:\Users\YourName\AppData\Local\Programs\Eclipse Adoptium\jdk-21.0.6.7-hotspot" /M
```
- Close and reopen the Command Prompt.
- Verify:
```cmd
echo %JAVA_HOME%
```

### 1.3 Set JAVA_HOME in Git Bash

#### Temporary Session
```bash
export JAVA_HOME="/c/Users/YourName/AppData/Local/Programs/Eclipse Adoptium/jdk-21.0.6.7-hotspot"
```

#### Permanently in ~/.bashrc
```bash
nano ~/.bashrc
```
Add:
```bash
export JAVA_HOME="/c/Users/YourName/AppData/Local/Programs/Eclipse Adoptium/jdk-21.0.6.7-hotspot"
```
```bash
source ~/.bashrc
```

---

## 2. Download and Unpack Solr

1. **Download Solr:** [Apache Solr Downloads](https://solr.apache.org/downloads.html).

2. **Unpack Solr**
```bash
tar -xvzf ./solr-8.5.0.tgz -C {your_chosen_directory}
```
- Replace `{your_chosen_directory}` with the path where you want Solr extracted.

---

## 3. Start Solr

```cmd
cd solr-8.5.0
bin\solr.cmd start -p 8983
```
- Check in browser:
```
http://localhost:8983/solr/
```

---

## 4. Create a Solr Core
```cmd
bin\solr create -c mycore
```
- Verify in Solr Admin UI.

---

## 5. Navigation

#### Go Back to Code Folder
```cmd
cd ..
```

#### Stop Solr
```cmd
bin\solr stop -p 8983
```

---

## 6. Example of Multiple Cores

- **products_core**: Product details (name, category, price, description)
- **customers_core**: Customer details (name, email, address)
- **orders_core**: Order history (customer ID, order date, total amount)

---

## 7. Solr vs. Relational Database

| Feature             | Solr (Search Engine)                  | Relational Database (SQL-based)         |
|---------------------|---------------------------------------|---------------------------------------|
| Data Structure     | Schema-based (JSON/XML documents)    | Tables with rows & columns             |
| Primary Purpose    | Full-text search & fast lookups       | Data storage & transactions            |
| Query Language     | Solr Query Syntax / Lucene Queries    | SQL (SELECT, JOIN, etc.)               |
| Joins & Relations  | Limited join capabilities             | Strong support for joins & normalization|
| Performance        | Optimized for large text datasets     | Optimized for structured transactions  |

---

## 8. Next Steps

- **Index Your Data**: Use the Solr Admin UI or REST API.
- **Explore Querying**: Learn Solr query syntax for advanced search features.
- **Customize Schemas**: Use `schema.xml` or the Schema API for tailored data structures.

---

## Happy Searching!

