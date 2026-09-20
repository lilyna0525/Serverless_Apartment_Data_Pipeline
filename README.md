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

AWS Lambda does not automatically include third-party libraries such as `requests` and `mysql-connector-python`.

The required dependencies were therefore packaged together with the Lambda function.

```text
lambda_function.py
requests/
mysql/
urllib3/
certifi/
charset_normalizer/
idna/
...
```

The deployment package was created as a ZIP file and uploaded to Amazon S3.

```bash
zip -r ~/apart_cost_scraping.zip .
zip -g apart_cost_scraping.zip lambda_function.py

aws s3 cp apart_cost_scraping.zip s3://fc-storydata/
```

### Lambda Configuration

```text
Runtime:
Python 3.13

Handler:
lambda_function.lambda_handler
```

The deployment package included Python 3.13-compatible dependencies, including the compiled MySQL Connector module.

---

## 7. Challenges & Solutions

### Python Runtime Compatibility

**Challenge:**
The original project used Python 3.9 while the final Lambda environment used Python 3.13.

**Solution:**
A new Python 3.13 virtual environment was created, dependencies were reinstalled, and the Lambda deployment package was rebuilt.

### Lambda Dependency Packaging

**Challenge:**
Third-party libraries were not included in the default Lambda runtime.

**Solution:**
Required dependencies were installed into the Python environment and packaged with the Lambda function.

### Compiled Dependency Compatibility

**Challenge:**
`mysql-connector-python` contains compiled components that must be compatible with the Lambda runtime.

**Solution:**
The deployment package was rebuilt inside the Amazon Linux 2023 EC2 environment using Python 3.13.

### Lambda Syntax Errors

**Challenge:**
Manual editing of the Lambda function caused string and indentation errors.

**Solution:**
The function was reformatted with consistent Python indentation and the API URL was corrected.

### Database Connectivity

**Challenge:**
The Lambda function needed to connect to MariaDB hosted on Amazon RDS.

**Solution:**
The RDS connection configuration was validated and the final database insertion was verified using DataGrip.

---

## 8. Data Validation

After successfully executing the Lambda function, the inserted records were checked in MariaDB using DataGrip.

The validation confirmed the complete pipeline:

```text
Zigbang API
     ↓
AWS Lambda
     ↓
JSON Transformation
     ↓
Amazon RDS / MariaDB
     ↓
apart_sales_info
     ↓
DataGrip
```

The database contained the transformed apartment records retrieved from the API.

### Key Data Fields

| Field                 | Description            |
| --------------------- | ---------------------- |
| `id`                  | Apartment identifier   |
| `name`                | Apartment name         |
| `lat / lng`           | Location coordinates   |
| `total_units`         | Number of households   |
| `approval_date`       | Building approval date |
| `sido / gugun / dong` | Location information   |
| `min_sales_price`     | Minimum sales price    |
| `max_sales_price`     | Maximum sales price    |
| `avg_sales_price`     | Average sales price    |
| `price_per_area`      | Price per area         |

---

## 9. Project Structure & Screenshots

### Repository Structure

```text
serverless-apartment-data-pipeline/
│
├── README.md
│
├── lambda/
│   └── lambda_function.py
│
├── screenshots/
│   ├── 01-lambda-function.png
│   ├── 02-lambda-test-success.png
│   ├── 03-database-schema.png
│   ├── 04-database-result.png
│   └── 05-s3-deployment-package.png
│
└── .gitignore
```

### Screenshots

#### AWS Lambda Function

The Lambda function retrieves apartment data from the Zigbang API, transforms the JSON response, and inserts the data into Amazon RDS.

![AWS Lambda Function](screenshots/01-lambda-function.png)

#### Lambda Test Result

The deployed Lambda function successfully executed the data ingestion process.

![Lambda Test Success](screenshots/02-lambda-test-success.png)

#### Database Schema

The `apart_sales_info` table stores structured apartment and sales information.

![Database Schema](screenshots/03-database-schema.png)

#### Database Result

The collected apartment data was successfully stored in Amazon RDS and verified using DataGrip.

![Database Result](screenshots/04-database-result.png)

#### S3 Deployment Package

The Lambda deployment package containing the Python function and required dependencies was uploaded to Amazon S3.

![S3 Deployment Package](screenshots/05-s3-deployment-package.png)

---

## 10. Project Outcome & Future Improvements

### Project Outcome

The final implementation successfully demonstrates an end-to-end serverless data ingestion workflow:

```text
External REST API
       ↓
AWS Lambda
       ↓
JSON Transformation
       ↓
SQL INSERT
       ↓
Amazon RDS / MariaDB
       ↓
Data Validation
```

Through this project, I gained hands-on experience with:

* REST API data ingestion
* JSON parsing and transformation
* Relational database storage
* SQL and MariaDB
* AWS Lambda
* Amazon RDS
* Amazon S3
* Python dependency management
* Lambda deployment packages
* Cloud-based data pipeline architecture
* Troubleshooting cloud deployments

### Future Improvements

Potential improvements for a production-oriented version include:

* **Scheduled Data Collection** — Use Amazon EventBridge to trigger Lambda automatically.
* **Secure Credential Management** — Use AWS Secrets Manager or Parameter Store instead of hard-coded credentials.
* **Duplicate Handling** — Implement `UPSERT` or duplicate detection.
* **Monitoring** — Add CloudWatch Logs, Metrics, and Alarms.
* **Data Quality Validation** — Validate missing IDs, invalid coordinates, prices, dates, and duplicate records.
* **Analytics Dashboard** — Connect the database to Power BI for apartment price and geographic analysis.

---

## Conclusion

This project demonstrates the migration of a traditional Python-based data collection script into a cloud-based serverless data pipeline.

It provided practical experience in building an end-to-end ingestion workflow using **Python, REST APIs, SQL, AWS Lambda, Amazon RDS, Amazon S3, and Linux-based deployment workflows**.
