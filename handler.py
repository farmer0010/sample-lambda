import json
import os
import boto3
import socket

def handler(event, context):
    ssm_prefix = os.environ.get('SSM_PREFIX')
    ssm = boto3.client('ssm')
    
    results = {}
    
    try:
        endpoint_res = ssm.get_parameter(Name=f"{ssm_prefix}/RDS_ENDPOINT")
        rds_host = endpoint_res['Parameter']['Value'].split(':')[0]
        results['ssm_endpoint'] = "ok"
        
        ssm.get_parameter(Name=f"{ssm_prefix}/DB_PASSWORD", WithDecryption=True)
        results['ssm_password'] = "ok"
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((rds_host, 3306))
        s.close()
        results['rds'] = "ok"
        
    except Exception as e:
        results['error'] = str(e)

    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }