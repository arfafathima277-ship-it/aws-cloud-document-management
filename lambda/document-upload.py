import json
import boto3
import base64
import uuid
import os
from datetime import datetime, timezone

# Connect to AWS services
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# Get values from Lambda environment variables
BUCKET_NAME = os.environ["S3_BUCKET"]
TABLE_NAME = os.environ["DDB_TABLE"]

table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):

    try:
        # Get HTTP method
        method = event.get("requestContext", {}).get(
            "http", {}
        ).get("method", "")

        # ==============================
        # UPLOAD DOCUMENT
        # ==============================

        if method == "POST":

            body = event.get("body")

            if not body:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message": "Request body is required"
                    })
                }

            # Decode request body if API Gateway sends Base64
            if event.get("isBase64Encoded"):
                body = base64.b64decode(body).decode("utf-8")

            data = json.loads(body)

            file_name = data.get("fileName")
            file_content = data.get("fileContent")
            content_type = data.get(
                "contentType",
                "application/octet-stream"
            )

            if not file_name or not file_content:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message":
                        "fileName and fileContent are required"
                    })
                }

            # Generate unique document ID
            document_id = str(uuid.uuid4())

            # S3 location
            s3_key = f"documents/{document_id}/{file_name}"

            # Convert Base64 to actual file bytes
            file_bytes = base64.b64decode(file_content)

            # Upload document to S3
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=s3_key,
                Body=file_bytes,
                ContentType=content_type,
                ServerSideEncryption="AES256"
            )

            # Upload timestamp
            upload_time = datetime.now(
                timezone.utc
            ).isoformat()

            # Save metadata in DynamoDB
            table.put_item(
                Item={
                    "documentId": document_id,
                    "fileName": file_name,
                    "s3Key": s3_key,
                    "contentType": content_type,
                    "uploadedAt": upload_time
                }
            )

            return {
                "statusCode": 201,
                "body": json.dumps({
                    "message":
                    "Document uploaded successfully",
                    "documentId": document_id,
                    "fileName": file_name,
                    "s3Key": s3_key
                })
            }

        # ==============================
        # GET DOCUMENT
        # ==============================

        elif method == "GET":

            document_id = (
                event.get("pathParameters") or {}
            ).get("documentId")

            if not document_id:
                return {
                    "statusCode": 400,
                    "body": json.dumps({
                        "message":
                        "documentId is required"
                    })
                }

            # Get metadata from DynamoDB
            result = table.get_item(
                Key={
                    "documentId": document_id
                }
            )

            item = result.get("Item")

            if not item:
                return {
                    "statusCode": 404,
                    "body": json.dumps({
                        "message": "Document not found"
                    })
                }

            # Generate temporary secure S3 URL
            download_url = s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": BUCKET_NAME,
                    "Key": item["s3Key"]
                },
                ExpiresIn=900
            )

            item["downloadUrl"] = download_url

            return {
                "statusCode": 200,
                "body": json.dumps(item)
            }

        else:

            return {
                "statusCode": 405,
                "body": json.dumps({
                    "message": "Method not allowed"
                })
            }

    except Exception as e:

        print(f"ERROR: {str(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Internal server error",
                "error": str(e)
            })
        }
