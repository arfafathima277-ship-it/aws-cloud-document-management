# AWS Cloud Document Management System

## 📌 Project Overview

This project is a serverless cloud-based document management system built using AWS.

The system provides APIs to upload and retrieve documents. Documents are securely stored in Amazon S3, while document metadata is stored in Amazon DynamoDB.

AWS Lambda handles the application logic, and Amazon API Gateway exposes the application through HTTP APIs.

---

## 🏗️ Architecture

```text
                    Client
                       |
                       v
               Amazon API Gateway
                       |
                       v
                AWS Lambda
                 /       \
                /         \
               v           v
        Amazon S3      DynamoDB
       (Documents)    (Metadata)


       ## 🔄 How the System Works

### 1. Document Upload

The client sends a POST request to the API Gateway endpoint:

POST /documents

The request contains:

- File name
- Content type
- Base64-encoded file content

API Gateway forwards the request to the CloudDocumentManager Lambda function.

Lambda validates the request and decodes the Base64 file content into binary data.

A unique UUID is generated for every document.

The document is then uploaded to Amazon S3 using the following structure:

documents/<documentId>/<fileName>

After the S3 upload is successful, Lambda stores the document metadata in the DocumentMetadata DynamoDB table.

The API returns the document ID and S3 key to the client.

### 2. Document Retrieval

The client sends:

GET /documents/{documentId}

Lambda receives the document ID and searches the DocumentMetadata DynamoDB table.

If the document exists, Lambda generates a temporary pre-signed S3 URL.

The API returns the document metadata along with the temporary download URL.

### 3. Data Flow

Client
→ API Gateway
→ Lambda
→ S3

Lambda
→ DynamoDB

For retrieval:

Client
→ API Gateway
→ Lambda
→ DynamoDB
→ Pre-signed S3 URL


## 💡 Why These AWS Services?

### API Gateway
Used to expose the document management functionality through HTTP APIs.

### Lambda
Provides serverless application logic without managing servers.

### S3
Provides scalable and durable storage for uploaded documents.

### DynamoDB
Stores document metadata and allows fast lookup using the document ID.

### IAM
Controls what AWS resources the Lambda function can access.

### CloudWatch
Provides logs for monitoring and troubleshooting Lambda executions.
