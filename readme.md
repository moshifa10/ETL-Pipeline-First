# Sales ETL Pipeline

A Python-based **ETL (Extract, Transform, Load)** pipeline that processes supermarket sales data from a CSV file, validates and transforms the data, loads it into a SQLite database, and generates business reports.

This project was built as part of my Data Engineering learning roadmap to practice designing real-world data pipelines and applying core ETL concepts.

---

# Objectives

The purpose of this project is to simulate how a Data Engineer processes raw business data by:

* Extracting data from a CSV source
* Validating data quality
* Transforming raw data into business-ready information
* Loading clean data into a database
* Generating analytical reports
* Logging every stage of the pipeline

---

# Technologies Used

* Python
* Pandas
* SQLite
* SQLAlchemy ORM
* CSV
* Logging
* Object-Oriented Programming (OOP)

---

# ETL Pipeline Architecture

```text
                 sales.csv
                      │
                      ▼
              ┌────────────────┐
              │    Extract     │
              │ Read CSV File  │
              └───────┬────────┘
                      │
                      ▼
              ┌────────────────┐
              │    Validate    │
              │ Data Quality   │
              └───────┬────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
         ▼                         ▼
  Valid Records             Invalid Records
         │                         │
         │                  invalid_transactions.csv
         ▼
 ┌──────────────────┐
 │    Transform     │
 │ Calculate Revenue│
 │ Add load_date    │
 └────────┬─────────┘
          │
          ▼
 ┌──────────────────┐
 │      Load        │
 │ SQLite Database  │
 └────────┬─────────┘
          │
          ▼
 ┌──────────────────┐
 │    Analytics     │
 │ Business Reports │
 └──────────────────┘
```

---

# Data Flow

```text
sales.csv
      │
      ▼
Extract raw records
      │
      ▼
Validate records
      │
      ├── Invalid → invalid_transactions.csv
      │
      ▼
Transform valid records
      │
      ▼
Load into SQLite
      │
      ▼
Generate Reports
```

---

# Project Structure

```text
sales_etl_pipeline/
│
├── data/
│   └── sales.csv
│
├── database/
│   └── sales.db
│
├── logs/
│   └── pipeline.log
│
├── reports/
│   ├── valid_transactions.csv
│   ├── invalid_transactions.csv
│   ├── revenue_by_product.csv
│   └── revenue_by_category.csv
│
├── src/
│   ├── extract.py
│   ├── validate.py
│   ├── transform.py
│   ├── load.py
│   ├── analytics.py
│   ├── models.py
│   └── logger.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Validation Rules

The pipeline validates incoming data before loading it into the database.

Checks performed include:

* Duplicate transaction IDs
* Missing product names
* Missing categories
* Negative quantities
* Negative prices
* Zero quantities
* Zero prices
* Invalid data types
* Suspicious/outlier quantities

Invalid records are separated from valid records and exported for further investigation.

---

# Transformations

After validation, the pipeline performs business transformations.

Examples include:

* Calculating total sale

```
total_sale = quantity × price
```

* Adding a load date
* Preparing clean data for database storage

---

# Database

The project loads validated data into a SQLite database.

## sales

Stores clean business transactions.

Example columns:

* id
* transaction_id
* product
* category
* quantity
* price
* total_sale
* load_date

---

## invalid_transactions

Stores rejected records together with the reason they failed validation.

Example:

| transaction_id | reason                   |
| -------------- | ------------------------ |
| 8              | Negative Quantity        |
| 11             | Duplicate Transaction ID |

Keeping invalid data allows issues to be investigated instead of silently discarding records.

---

# Reports Generated

The pipeline automatically generates:

## Valid Transactions

Contains all cleaned records.

```
valid_transactions.csv
```

---

## Invalid Transactions

Contains rejected records and the validation reason.

```
invalid_transactions.csv
```

---

## Revenue by Product

Example:

| Product | Revenue |
| ------- | ------- |
| Coke    | R150    |
| Bread   | R80     |

---

## Revenue by Category

Example:

| Category | Revenue |
| -------- | ------- |
| Drinks   | R150    |
| Dairy    | R142    |

---

# Logging

Every execution of the pipeline is logged.

Example log output:

```text
Pipeline Started
25 records extracted
18 valid records
7 invalid records
Revenue reports generated
18 records inserted into database
Pipeline Completed Successfully
```

Logging provides visibility into the ETL process and helps diagnose failures.

---

# Running the Project

1. Clone the repository.

```bash
git clone <repository-url>
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Place the sales dataset inside the `data` directory.

4. Run the pipeline.

```bash
python main.py
```

---

# Expected Output

Running the pipeline will automatically:

* Read the sales CSV
* Validate every record
* Separate valid and invalid data
* Calculate business metrics
* Create analytical reports
* Load clean records into SQLite
* Store invalid records
* Generate execution logs

---

# Skills Demonstrated

This project demonstrates practical Data Engineering concepts including:

* ETL Pipeline Design
* Data Validation
* Data Quality Management
* Data Transformation
* Database Loading
* SQLAlchemy ORM
* SQLite
* Business Analytics
* Logging
* Project Architecture
* Modular Python Development

---

# Future Improvements

Planned enhancements include:

* PostgreSQL support
* PySpark implementation
* Apache Airflow orchestration
* Databricks integration
* Docker containerization
* Automated unit testing
* CI/CD pipeline
* Cloud deployment (Azure or AWS)

---

# Learning Outcome

This project was developed as part of my journey toward becoming a Data Engineer. Rather than focusing only on Python programming, the goal was to understand how data flows through a complete ETL pipeline—from raw source data to validated, transformed, and business-ready information.
