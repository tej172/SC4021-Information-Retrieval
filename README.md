# SC4021 Info Ret.

Youtube guide for solr set up: [Link](https://www.youtube.com/watch?v=tJRwI_P290A) (Updated) 

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

### 1.2 Set `JAVA_HOME` (Windows) (if using windows cmd)

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

### 1.3 Set `JAVA_HOME` in Git Bash (if using git)

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

#### Windows
##### **Option A: Temporary (Current Session Only)**
```cmd
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-11.0.18.10-hotspot
```

##### **Option B: Permanent (Requires Admin for System-Wide)**
- **For current user (no admin needed):**
  ```cmd
  setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-11.0.18.10-hotspot"
  ```
- **For all users (admin required):**
  ```cmd
  setx JAVA_HOME "C:\Program Files\Eclipse Adoptium\jdk-11.0.18.10-hotspot" /M
  ```
  *(Remove quotes if they cause issues.)*
---

## 2. Download and Unpack Solr

2. **Download Apache Solr**  
   - Get the latest binary from:  
     **[https://solr.apache.org/downloads.html](https://solr.apache.org/downloads.html)**  (e.g., `solr-9.8.1.zip`).

3. **Extract Solr into the Repo Folder**  
   - Move the downloaded `solr-9.8.1.zip` into your repo folder (e.g., `Information_Retrieval/`).  
   - Extract it there, resulting in:  
     ```
     Information_Retrieval/
     ├── solr-9.8.1/  
     ├── other_repo_files/  
     └── ...
     ```
---

---

## **3: Application Start Up**
1. Run the `start.py` file in the Repo:
2. cmd print out:
   ```cmd
   JAVA_HOME is set to: ...\Programs\Eclipse Adoptium\jdk-21.0.6.7-hotspot
   Starting Solr in the background...
   Solr started with PID: 21132
   To access Solr: http://localhost:8983/solr/
   ```
3. Open `http://localhost:8983/solr/` in a browser to confirm it’s running.

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

