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

