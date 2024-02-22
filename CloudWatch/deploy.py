import boto3
import os

from dotenv import load_dotenv

load_dotenv()

def main():
    """
    This function serves as the entry point for the CloudFormation stack management 
    script. It orchestrates the creation a CloudFormation stack based on 
    the provided environment variables. The script reads the AWS access credentials and 
    region configuration from environment variables and utilizes the boto3 library to 
    interact with the AWS services. In this case, stack is used to create a Billing
    Alarm and it is activated if costs exceds 1 dollar.

    Parameters:
    -----------
        - None

    Returns:
    --------
        - Response of opperation
    """
    try:
        session = boto3.Session(
            aws_access_key_id = os.getenv('ACCESS_KEY_ID'),
            aws_secret_access_key = os.getenv('SECRET_ACCESS_KEY'),
            region_name = os.getenv('REGION')
        )
        cloudformation_client = session.client('cloudformation')
        stack_name = 'billing-alarm-stack'
        template_file = './yaml_templates/billing_alarm.yaml'
        with open(template_file, 'r') as file:
            template_body = file.read()
        response = cloudformation_client.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Capabilities=['CAPABILITY_NAMED_IAM']
        )
        print("Stack created:", response)
        return response
    except Exception as ex:
        print("Failed action:", ex)
        return ex

if __name__ == "__main__":
    main()