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
