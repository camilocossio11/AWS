import boto3
import os

from dotenv import load_dotenv

load_dotenv()

def main(bucket_name, tags):
    """
    This function serves as the entry point for the CloudFormation stack management 
    script. It orchestrates the creation or update of a CloudFormation stack based on 
    the provided environment variables. The script reads the AWS access credentials and 
    region configuration from environment variables and utilizes the boto3 library to 
    interact with the AWS services. Depending on the value of the 'ACTION' environment 
    variable, it either creates a new stack or updates an existing one with the 
    specified template file. In this case, stack is used to create a new user and 
    assign AdministratorAccess policy.

    Parameters:
    -----------
        - bucket_name (str): S3 Bucket name to be assigned
        - tags (str): String in dict format to assign tags for easy management.

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
        template_file = './yaml_templates/bucket_creation.yaml'
        with open(template_file, 'r') as file:
            template_body = file.read()
        response = cloudformation_client.create_stack(
            StackName = f'{bucket_name}-stack',
            TemplateBody = template_body,
            Parameters = [
                {
                    'ParameterKey': 'BucketName',
                    'ParameterValue': bucket_name
                },
                {
                    'ParameterKey': 'Tags',
                    'ParameterValue': tags
                }
            ],
            Capabilities = ['CAPABILITY_NAMED_IAM']
        )
        print("Stack created:", response)
        return response
    except Exception as ex:
        print("Failed action:", ex)
        return ex

if __name__ == "__main__":
    bucket_name = 'DataStorage-1'
    tags = '{"ResourceType":"Developments"}'
    main(bucket_name, tags)
