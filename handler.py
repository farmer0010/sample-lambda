import json
import socket

def handler(event, context):
    host = "juyo-serverless-dev-db.cvcmqeyyopul.ap-northeast-2.rds.amazonaws.com"
    
    try:
        socket.create_connection((host, 3306), timeout=2)
        
        return {
            'statusCode': 200,
            'body': json.dumps({"result": "SUCCESS!"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"result": "FAIL", "error": str(e)})
        }