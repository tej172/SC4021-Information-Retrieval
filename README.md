# SC4021 Info Ret.

## Apache Solr Setup & Usage

This guide walks you through downloading, installing, and running Apache Solr. It also covers setting up your Java environment (`JAVA_HOME`) and provides a quick comparison between Solr and a traditional relational database.

---

## 1. Prerequisites

### 1.1 Check Java Installation

#### On Windows (Command Prompt)

1. **Open Command Prompt:**  
   Press `Windows + R`, type `cmd`, and press Enter.

2. **Check Java Version**  
   ```cmd
   java -version
   ```
   **Example Output:**
   ```
   java version "17.0.2" 2022-01-18 LTS
   Java(TM) SE Runtime Environment (build 17.0.2+8-LTS-86)
   Java HotSpot(TM) 64-Bit Server VM (build 17.0.2+8-LTS-86, mixed mode, sharing)
   ```
   - If not installed, download Java from [Adoptium](https://adoptium.net/download/) or [Oracle](https://www.oracle.com/java/technologies/downloads/).

#### On Git Bash or Unix-like Terminal
```bash
java -version
```

**Example Output:**
```bash
openjdk version "17.0.2" 2022-01-18
OpenJDK Runtime Environment (build 17.0.2+8)
OpenJDK 64-Bit Server VM (build 17.0.2+8, mixed mode)
```

---

### 1.2 Set `JAVA_HOME` (Windows)

#### Find Java Path
```cmd
where java
```

**Example Output:**
```cmd
C:\Program Files\Eclipse Adoptium\jdk-21.0.6.7-hotspot\bin\java.exe
```

- Copy everything before `\bin\java.exe`, for example:
```cmd
C:\Program Files\Eclipse Adoptium\jdk-21.0.6.7-hotspot
```

#### Set `JAVA_HOME` Temporarily
```cmd
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.6.7-hotspot
```

#### Set `JAVA_HOME` Permanently
```cmd
setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-21.0.6.7-hotspot" /M
```

**Verify:**
```cmd
echo %JAVA_HOME%
```

**Example Output:**
```cmd
C:\Program Files\Eclipse Adoptium\jdk-21.0.6.7-hotspot
```

---

### 1.3 Set `JAVA_HOME` in Git Bash

#### Temporary Session
```bash
export JAVA_HOME="/c/Program Files/Eclipse Adoptium/jdk-21.0.6.7-hotspot"
```

#### Permanently in `~/.bashrc`
```bash
nano ~/.bashrc
```
Add this line:
```bash
export JAVA_HOME="/c/Program Files/Eclipse Adoptium/jdk-21.0.6.7-hotspot"
```
Load new settings:
```bash
source ~/.bashrc
```

---

## 2. Download and Unpack Solr

1. **Download Solr:**  
   Visit [Apache Solr Downloads](https://solr.apache.org/downloads.html).

2. **Unpack Solr**
```bash
tar -xvzf ./solr-9.8.0.tgz -C /home/user/solr
```

---

## 3. Start Solr

```cmd
cd solr-9.8.0
bin\solr.cmd start -p 8983
```

Open in browser:
```
http://localhost:8983/solr/
```

---

## 4. Create a Solr Core
```cmd
bin\solr.cmd create -c mycore
```

---

## 5. Navigation

```cmd
cd ..
```

---

## 6. Stop Solr
```cmd
bin\solr.cmd stop -p 8983
```

---

## 7. Example of Multiple Cores

```cmd
bin\solr.cmd create -c products_core
bin\solr.cmd create -c customers_core
bin\solr.cmd create -c orders_core
```

---

## 8. Solr vs. Relational Database

| Feature | Solr (Search Engine) | Relational Database (SQL-based) |
|---------|-----------------------|---------------------------------|
| Data Structure | JSON/XML documents | Tables with rows & columns |
| Primary Purpose | Full-text search | Data storage & transactions |
| Query Language | Solr Query Syntax | SQL |
| Joins & Relations | Limited | Strong support for joins |
| Performance | Optimized for search | Optimized for transactions |

---

## 9. Index Data Using `curl`

```cmd
curl "http://localhost:8983/solr/mycore/update?commit=true" ^
     -H "Content-Type: application/json" ^
     --data-binary "@C:\data\books.json"
```

---

## 10. Querying Solr

In the Solr Admin UI, use the query:
```
q=*:*
```

---

## 11. Customize Schemas via API

```bash
curl -X POST -H 'Content-type:application/json' \
--data-binary '{
  "add-field": {
    "name":"new_field",
    "type":"string",
    "stored":true
  }
}' \
http://localhost:8983/solr/mycore/schema
```

---

## Happy Searching!

