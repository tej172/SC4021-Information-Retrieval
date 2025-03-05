# SC4021 Info Ret.

Good yoiutube for solr set up:https://www.youtube.com/watch?v=tJRwI_P290A (more updated) & https://www.youtube.com/watch?v=Zw4M4NGv-Rw (best but is for older 8.X.X versions so some commands dont work like to push json to the solr core)

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

### Command Example
```cmd
curl "http://localhost:8983/solr/AI_and_JobMarket/update?commit=true" ^
     -H "Content-Type: application/json" ^
     --data-binary "@C:\Users\tegti\OneDrive\Documents\MERN\School\SC4021-InfoRet\SC4021-Information-Retrieval\data\combined_data\combined.json"
```

### Explanation
- **http://localhost:8983/solr/AI_and_JobMarket/update?commit=true**: The Solr update endpoint
  - `AI_and_JobMarket` = The Solr core name where data will be indexed
  - `?commit=true` = Forces Solr to commit changes immediately
- **-H "Content-Type: application/json"**: Specifies that the data format is JSON
- **--data-binary**: Indicates that the data is sent as a raw binary file
- **"@...\combined.json"**: Path to the JSON file being uploaded

### Expected Output
```json
{
  "responseHeader":{
    "status":0,
    "QTime":8141
  }
}
```
- **"status":0** indicates a successful update
- **"QTime"** shows the time taken for the request in milliseconds

---

## Happy Searching!

