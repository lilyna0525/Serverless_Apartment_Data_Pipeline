# Serverless Apartment Data Pipeline

A serverless data ingestion pipeline that collects apartment sales information from the Zigbang API, transforms the API response into structured records, and stores the data in MariaDB hosted on Amazon RDS.

The project started as a Python-based data collection script on Amazon EC2 and was later migrated to AWS Lambda to create a lightweight serverless data ingestion workflow.

---

## 1. Project Overview

The goal of this project was to collect apartment sales information from a selected area through the Zigbang REST API and store the structured data in a relational database.

### Data Flow

```text
Zigbang API
     │
     │ HTTPS GET
     ▼
AWS Lambda
     │
     │ JSON Parsing & Transformation
     ▼
Amazon RDS
MariaDB
     │
     ▼
apart_sales_info
     │
     ▼
DataGrip
```

The final pipeline demonstrates an end-to-end workflow from external API ingestion to database storage and validation.

---

## 2. Architecture

```text
                     ┌─────────────────────┐
                     │     Zigbang API     │
                     │      REST API       │
                     └──────────┬──────────┘
                                │
                                │ HTTPS GET
                                ▼
                     ┌─────────────────────┐
                     │    AWS Lambda       │
                     │                     │
                     │ Python 3.13         │
                     │ JSON Parsing        │
                     │ Data Transformation │
                     └──────────┬──────────┘
                                │
                                │ SQL INSERT
                                ▼
                     ┌─────────────────────┐
                     │     Amazon RDS      │
                     │      MariaDB        │
                     │                     │
                     │   pipelinedb        │
                     │ apart_sales_info    │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │      DataGrip       │
                     │ Data Validation     │
                     └─────────────────────┘
```

### Deployment Flow

```text
Python Dependencies
        │
        ▼
   ZIP Package
        │
        ▼
    Amazon S3
        │
        ▼
    AWS Lambda
```

---

## 3. Technology Stack

| Category         | Technology                       |
| ---------------- | -------------------------------- |
| Programming      | Python 3.13                      |
| API              | Zigbang REST API                 |
| Cloud            | AWS                              |
| Compute          | AWS Lambda                       |
| Storage          | Amazon S3                        |
| Database         | Amazon RDS / MariaDB             |
| Database Client  | DataGrip                         |
| Development      | Amazon EC2 / Amazon Linux 2023   |
| Python Libraries | requests, mysql-connector-python |
| SQL              | MariaDB SQL                      |
| Version Control  | Git / GitHub                     |

---

## 4. Data Pipeline

The pipeline processes apartment information through the following stages.

### 1. Data Ingestion

Apartment information is retrieved from the Zigbang REST API using Python's `requests` library.

```python
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()

apartments = data.get('filtered', [])
```

### 2. Data Transformation

The nested JSON response is transformed into structured records matching the MariaDB schema.

```python
sales_data = json_data.get('price', {}).get('sales', {})

insert_data = {
    'id': json_data['id'],
    'name': json_data['name'],
    'lat': json_data['lat'],
    'lng': json_data['lng'],
    'total_units': json_data.get('총세대수'),
    'approval_date': json_data.get('사용승인일'),
    'service_type': json_data.get('서비스구분'),
    'real_type': json_data.get('real_type'),
    'sido': json_data.get('sido'),
    'gugun': json_data.get('gugun'),
    'dong': json_data.get('dong'),
    'image_url': json_data.get('image'),
    'is_after_prefunding': json_data.get('is후분양'),
    'min_sales_price': sales_data.get('min'),
    'max_sales_price': sales_data.get('max'),
    'avg_sales_price': sales_data.get('avg'),
    'price_per_area': sales_data.get('perArea')
}
```

### 3. Data Storage

The transformed records are inserted into the `apart_sales_info` table in MariaDB.

```text
pipelinedb
└── apart_sales_info
```

Parameterized SQL was used to separate SQL syntax from data values.

---

## 5. AWS Lambda Migration

The initial pipeline was developed and tested as a Python script running on Amazon EC2.

After validating API ingestion and database insertion, the application logic was migrated to AWS Lambda.

### Lambda Workflow

```text
API Request
     ↓
JSON Response
     ↓
Data Extraction
     ↓
Data Transformation
     ↓
MariaDB Connection
     ↓
SQL INSERT
     ↓
Database
```

The final Lambda function uses:

```text
lambda_function.py
└── lambda_handler(event, context)
```

### Python Runtime Migration

The original course environment used Python 3.9.
For the final implementation, the project environment was migrated to Python 3.13.

```bash
python3.13 -m venv scr_env
source ./scr_env/bin/activate
```

The Lambda deployment package was then rebuilt using the Python 3.13 environment.

---

## 6. Deployment & Configuration

AWS Lambda does not automa
