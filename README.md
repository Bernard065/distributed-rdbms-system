# Distributed RDBMS System

**Version:** 0.1.0
**Author:** Benard Omboga
**Architecture:** Client-Server over TCP

## 1. Overview

This project is a custom-built, lightweight Relational Database Management System (RDBMS). It implements a layered architecture separating the **Network Interface**, **Query Execution**, and **Storage Engine**.

It demonstrates core database engineering concepts including:

* **TCP/Socket Networking:** Custom protocol for client-server communication.
* **SQL Parsing:** Lexical analysis and command dispatching.
* **Persistence:** Write-Ahead Logging (WAL) for crash recovery.
* **Separation of Concerns:** Decoupled Client, Server, and Storage logic.

## 2. Architecture

The system operates on a synchronous Client-Server model.

```mermaid
[Web Client / REPL]  <--TCP Socket-->  [Networking Layer]
                                            |
                                      [SQL Parser]
                                            |
                                      [Executor Engine]
                                       /           \
                                  [In-Memory     [WAL Logger
                                   Index]         (Disk)]

```

* **Client:** Sends raw SQL strings encoded in UTF-8.
* **Networking:** A multi-threaded TCP server listening on port `9999`.
* **Storage:** Currently utilizes in-memory Hash Maps (Python Dictionaries) for O(1) Primary Key lookups, backed by an append-only log file for durability.

## 3. Project Structure

```text
/distributed-rdbms-system
├── /data                    # Physical Storage (WAL logs)
├── /rdbms_engine            # The Database Server Source Code
│   ├── main.py              # Entry point (bootstraps server)
│   ├── networking.py        # TCP Socket & Threading logic
│   ├── sql_parser.py        # Regex-based SQL Lexer
│   ├── executor.py          # Query Plan Orchestrator
│   └── storage/             # Storage Subsystem
│       ├── btree.py         # In-memory data structures
│       └── wal.py           # Persistence logic
├── /web_client              # Client Application
│   ├── app.py               # Flask Web Server
│   └── db_driver.py         # Custom TCP Client SDK
├── /tests                   # Unit & Integration Tests
└── requirements.txt         # Dependencies

```

## 4. Getting Started

### Prerequisites

* Python 3.8+
* Linux/MacOS/Windows environment

### Installation

1. **Clone/Navigate to the repository:**
```bash
cd ~/Development/distributed-rdbms-system

```


2. **Initialize Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


*(Note: `requirements.txt` should contain `flask`)*

### Running the System

You will need two separate terminal windows.

**Terminal 1: The Database Server**

```bash
# Starts the TCP Server on port 9999
python -m rdbms_engine.main

```

**Terminal 2: The Web Client**

```bash
# Starts the Flask App on port 5000
python web_client/app.py

```

## 5. Usage & API

### SQL Support (MVP)

The engine currently supports a subset of SQL:

* `CREATE TABLE table_name (col1, col2)`
* `INSERT INTO table_name VALUES (val1, val2)`
* `SELECT * FROM table_name`
* `SELECT * FROM t1 JOIN t2 ON t1.id = t2.id`

### HTTP API (via Web Client)

* **POST** `/users`: Create a user
* Body: `{"id": 1, "name": "John"}`


* **GET** `/users`: Retrieve all users

## 6. Engineering Decisions & Trade-offs

1. **Concurrency:** We rely on Python's `threading` module. Due to the Global Interpreter Lock (GIL), this provides concurrency (I/O bound) but not true parallelism (CPU bound).
2. **Durability:** We use **Write-Ahead Logging (WAL)**. Every write is flushed to disk (`data/wal.log`) before the in-memory state is updated. This ensures data survives a crash, mimicking Redis AOF persistence.
3. **Indexing:** Currently `O(1)` for Primary Key lookups (Hash Map). Future versions will implement B-Trees for `O(log n)` range queries.

## 7. Roadmap

* [ ] Implement `DELETE` and `UPDATE` operations.
* [ ] Replace Regex parser with a proper Tokenizer.
* [ ] Implement a Buffer Pool for caching pages.
* [ ] Add basic authentication to the TCP protocol.
