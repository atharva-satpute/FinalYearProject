# Duplicate Bug Report Detection

## INTRODUCTION

Using bug tracking tools, organizations can manage test reports more efficiently and deliver high quality products with reduced development costs and higher customer satisfaction. It is common for all testers to encounter the same bug, resulting in duplicate bugs being reported in the system. These duplicate bugs can be solved if common code files are handled properly.In light of this, duplicate bug report detection is a critical process that can significantly improve development quality and
efficiency. It also helps organizations provide their customers with better services.

## PROBLEM STATEMENT

Developers rely on bug reports to fix bugs. Typically, bug reports are stored and managed via bug tracking software. There is a high possibility that many testers
may encounter same bug as a result of which bug tracking systems may contains many duplicate bug reports. Thus implement a tool for effective detection of duplicate bug reports so as to reduce time and cost of operation and human resources.

## Getting Started

### Prerequisites

* [Node js](https://nodejs.org/en/)
* [Python](https://www.python.org/downloads/)
* [MongoDB](https://www.mongodb.com/try/download/community)

## Installation

1. Clone the repository

   ```sh
   git clone https://github.com/Veritasosrb/veridical.git
   ```

   And checkout to `PICT-2022-DBRD` branch.

2. Install Python Libraries

   ```sh
   pip install -r requirement.txt
   ```

   **Note:** Microsoft Visual C++ 14.0 or greater is required for [gensim](https://radimrehurek.com/gensim/) library to work.

3. Install NPM packages

   ```sh
   cd client
   npm install
   ```

4. Download the Eclipse Dataset

   ```http
   http://alazar.people.ysu.edu/msr14data/datasets/eclipse.tar.gz
   ```

   After downloading, execute the following commands in the terminal.

   ```sh
   tar zxvf eclipse.tar.gz
   mongorestore
   ```

   After restoring the database, we will be using the `initial` collection from the `eclipse` database for the project.

5. Execute `mongoDBPreprocess.py` file to create a processed collection that will contain the processed reports.

   ```sh
   python ./server/mongoDBPreprocess.py
   ```

   After executing the file, `initial_processed` collection will be created that will have the processed documents. For execution purpose, 400 documents will be processed and new documents will be added automatically as the software is used based on the searches.

6. Execute `sqlitePreprocess.py` file to create the processed table that will contain the processed reports.

   ```sh
   python ./server/sqlitePreprocess.py
   ```

   After executing the file, `reports.db` file will be generated in `./server/databases` directory that will contain the unprocessed reports, and the processed reports. For execution purpose, 2000 documents will be processed and new documents will be added automatically as the software is used based on the searches.  

7. Download the trained skip-gram model

   ```http
   https://drive.google.com/drive/folders/1yBtjVgJnmVe-_UZoqapXiJ8kSsfQcypI?usp=sharing
   ```

   After downloading the model, save it under `./dbrd/trained_model` directory.

## Repository Structure

* The `client` directory contains the source code and UI components for the website.

* The `dbrd` directory contains the skip-gram model and other pre-processing files.

* The `server` directory contains the Flask App and database files.

## Development

* Change the directory to `/client` and run the following command in the terminal

   ```cmd
   npm start
   ```

* Change the directory to `/server` and run the `app.py` file in a new terminal with the following arguements to start the Flask server
  * Using MongoDB database

    ```shell
    python ./server/app.py -db_url {Database URL} -db_name {Database Name} -col_name {Collection name}
    ```

    **Example:**

    ```shell
    python ./server/app.py -db_url mongodb://127.0.0.1:27017/ -db_name eclipse -col_name initial
    ```

  * Using sqlite3 database

    ```shell
    python ./server/app.py -db_url {Database URL} -db_type 2 -db_name {Database Name} -col_name {Table Name}
    ```

    **Example:**

    ```shell
    python ./server/app.py -db_url ./server/databases -db_type 2 -db_name reports -col_name initial
    ```

    **Note:** db_type = 1 (For MongoDB,default), 2 (sqlite3)

## ENTITY RELATIONSHIP DIAGRAM

<p align="center">
<img src="https://github.com/DuplicateBugReportDetection/FinalCode/blob/main/Images/ER%20Diagram.png" height="450" width="800">
</p>

## ARCHITECTURE DIAGRAM

<p align="center">
<img src="https://github.com/DuplicateBugReportDetection/FinalCode/blob/main/Images/Architecture%20Diagram.jpeg" height="950" width="900">
</p>

## SCREENSHOT

<p align="center">
<img src="https://github.com/DuplicateBugReportDetection/FinalCode/blob/main/Images/UI.png" height="500" width="900">
</p>

## MADE BY TEAM

Omkar Amilkanthwar  &nbsp; -  [lnx2000](https://github.com/lnx2000)\
Aniruddha Deshmukh   - [Aniruddha004](https://github.com/Aniruddha004) \
Atharva Satpute     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - [atharva-satpute](https://github.com/atharva-satpute) \
Pranav Deshmukh      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [pranav918](https://github.com/pranav918)
