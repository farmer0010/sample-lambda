import json
import os
import boto3
import socket

def handler(event, context):
    ssm_prefix = os.environ.get('SSM_PREFIX')
    ssm = boto3.client('ssm')
    
    results = {}
    
    try:
        endpoint_res = ssm.get_parameter(Name=f"{ssm_prefix}/DB_ENDPOINT")
        rds_host = endpoint_res['Parameter']['Value'].split(':')[0]
        
        ssm.get_parameter(Name=f"{ssm_prefix}/db_password", WithDecryption=True)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((rds_host, 3306))
        s.close()
        
        results['status'] = "success"
        results['connected_to'] = rds_host
        
    except Exception as e:
        results['status'] = "fail"
        results['error'] = str(e)

    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }