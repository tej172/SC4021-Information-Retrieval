```markdown
# Apache Solr Setup & Usage

This guide walks you through downloading, installing, and running Apache Solr. It also covers setting up your Java environment (JAVA_HOME) and provides a quick comparison between Solr and a traditional relational database.

---

## 1. Prerequisites

### 1.1 Check Java Installation

1. **Open Command Prompt (Windows)**  
   Press `Windows + R`, type `cmd`, and press Enter. Then run:
   ```cmd
   java -version
   ```
   - If Java is installed, you'll see a version output like `java version "11.0.18"`.
   - If not installed, proceed to [Download Java](https://adoptium.net/download/) or [Oracle Java](https://www.oracle.com/java/technologies/downloads/).

2. **Open Git Bash (Alternatively on Windows)**  
   In Git Bash, check Java by typing:
   ```bash
   java -version
   ```
   - If installed, you'll see version information. If not, install Java as mentioned above.

### 1.2 Set `JAVA_HOME` (Windows)

- **Find Java Path**  
  In **Command Prompt**, run:
  ```cmd
  where java
  ```
  You might see multiple paths; choose the path for the Java version you want to use:
  ```
  C:\Users\YourName\AppData\Local\Programs\Eclipse Adoptium\jdk-21.0.6.7-hotspot\bin\java.exe
  ```
  Copy everything **before** `\bin\java.exe`. For example:
  ```
  C:\Users\YourName\AppData\Local\Programs\Eclipse Adoptium\jdk-21.0.6.7-hotspot
  ```

- **Set `JAVA_HOME` Temporarily (Within Current CMD Session)**
  ```cmd
  set JAVA_HOME=C:\Users\YourName\AppData\Local\Programs\Eclipse Adoptium\jdk-21.0.6.7-hotspot
  ```
- **Set `JAVA_HOME` Permanently (System-Wide)**
  ```cmd
  setx JAVA_HOME "C:\Users\YourName\AppData\Local\Programs\Eclipse Adoptium\jdk-21.0.6.7-hotspot" /M
  ```
  - Close and reopen the Command Prompt for changes to take effect.
  - Verify by typing:
    ```cmd
    echo %JAVA_HOME%
    ```
    You should see:
    ```
    C:\Users\YourName\AppData\Local\Programs\Eclipse Adoptium\jdk-21.0.6.7-hotspot
    ```

### 1.3 Set `JAVA_HOME` in Git Bash (Optional)

- **Temporary Session Only**
  ```bash
  export JAVA_HOME="/c/Users/YourName/AppData/Local/Programs/Eclipse Adoptium/jdk-21.0.6.7-hotspot"
  ```
- **Permanently in `~/.bashrc` or `~/.bash_profile`**
  1. Open the file in Nano:
     ```bash
     nano ~/.bashrc
     ```
  2. Add the following line at the end of the file:
     ```bash
     export JAVA_HOME="/c/Users/YourName/AppData/Local/Programs/Eclipse Adoptium/jdk-21.0.6.7-hotspot"
     ```
  3. Save and exit (`Ctrl + O`, then `Enter`, then `Ctrl + X`).
  4. Apply changes:
     ```bash
     source ~/.bashrc
     ```
  5. Verify:
     ```bash
     echo $JAVA_HOME
     ```

---

## 2. Download and Unpack Solr

1. **Download Solr**  
   Go to [Apache Solr Downloads](https://solr.apache.org/downloads.html) and download the **Binary release** (e.g., `solr-8.5.0.tgz`).

2. **Unpack the Archive**  
   - **Using Command Prompt (if you have a program like 7-Zip):** Right-click the `.tgz` file and extract it to your preferred directory.
   - **Using Git Bash or a Unix-like Terminal:**
     ```bash
     tar -xvzf ./solr-8.5.0.tgz -C {your_chosen_directory}
     ```
     Replace `{your_chosen_directory}` with the path where you want Solr extracted.  
   - After unzipping, you should have a folder named something like `solr-8.5.0`.

---

## 3. Starting Solr (Windows Command Prompt)

1. **Change Directory to Solr Folder**  
   ```cmd
   cd solr-8.5.0
   ```
2. **Start Solr**  
   ```cmd
   bin\solr.cmd start -p 8983
   ```
   You should see an output similar to:
   ```
   Waiting up to 180 seconds to see Solr running on port 8983
   Started Solr server on port 8983 (pid=12345). Happy searching!
   ```
3. **Verify Solr is Running**  
   Open your browser and go to:
   ```
   http://localhost:8983/solr/
   ```
   You should see the Solr Admin interface.

---

## 4. Creating a Solr Core

1. **In the Solr Directory**, run:
   ```cmd
   bin\solr create -c mycore
   ```
   This creates a new core named `mycore`.

2. **Check Your Cores**  
   Open `http://localhost:8983/solr/` and look for `mycore` in the Admin UI.

---

## 5. Returning to Your Code Folder

From the Solr directory, go back one level:
```cmd
cd ..
```
(Adjust the path as needed.)

---

## 6. Stopping Solr

While in the Solr directory:
```cmd
bin\solr stop -p 8983
```
This stops Solr running on port `8983`.

---

## 7. Example of Multiple Cores

You might need separate cores for different data types, for example:

- **products_core** → Product details (name, category, price, description)  
- **customers_core** → Customer details (name, email, address)  
- **orders_core** → Order history (customer ID, order date, total amount)

---

## 8. Comparison: Solr vs. Relational Database

| **Feature**         | **Solr (Search Engine)**                       | **Relational Database (SQL-based)**       |
|---------------------|------------------------------------------------|-------------------------------------------|
| **Data Structure**  | Schema-based (JSON/XML documents)             | Tables with rows & columns                |
| **Primary Purpose** | Full-text search & fast lookups               | Data storage & transactions               |
| **Query Language**  | Solr Query Syntax / Lucene Queries            | SQL (SELECT, JOIN, etc.)                 |
| **Joins & Relations** | Limited join capabilities                   | Strong support for joins & normalization  |
| **Performance**     | Optimized for searching large text datasets   | Optimized for structured data transactions|

---

## 9. Next Steps

- **Index Your Data**: Use the Solr Admin UI or various clients (cURL, Python, etc.) to index data.
- **Explore Querying**: Learn Solr query syntax to utilize features like faceting, highlighting, etc.
- **Customize Schemas**: Update `schema.xml` or use the Schema API to define custom fields and analyzers.

---

**Happy Searching!**
```
