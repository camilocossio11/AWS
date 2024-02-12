import boto3
import os

from dotenv import load_dotenv

load_dotenv()

def update_cloudformation_stack(cloudformation_client, stack_name, template_body):
    """
    This function updates an existing CloudFormation stack with the provided template 
    body. It utilizes the AWS CloudFormation client to perform the stack update 
    operation. The function assumes that the stack exists and is accessible by the 
    provided `stack_name`.

    Parameters:
    -----------
        - cloudformation_client (boto3.client('cloudformation') object): The AWS 
        CloudFormation client object used to interact with the CloudFormation service. 
        It should have the necessary permissions to perform stack update operations.
        - stack_name (str): The name of the CloudFormation stack to update.
        - template_body (YAML formatted template): The structure containing the updated 
        CloudFormation template body.
    
    Returns:
        - response (dict): The response from the CloudFormation service after 
        attempting to update the stack.

    """
    response = cloudformation_client.update_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_NAMED_IAM']
    )
    return response

def create_cloudformation_stack(cloudformation_client, stack_name, template_body):
    """
    This function creates a CloudFormation stack with the provided template 
    body. It utilizes the AWS CloudFormation client to perform the stack create 
    operation. The function assumes that the stack exists and is accessible by the 
    provided `stack_name`.

    Parameters:
    -----------
        - cloudformation_client (boto3.client('cloudformation') object): The AWS 
        CloudFormation client object used to interact with the CloudFormation service. 
        It should have the necessary permissions to perform stack create operations.
        - stack_name (str): The name of the CloudFormation stack to create.
        - template_body (YAML formatted template): The structure containing the created 
        CloudFormation template body.
    
    Returns:
        - response (dict): The response from the CloudFormation service after 
        attempting to create the stack.

    """
    response = cloudformation_client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_NAMED_IAM']
    )
    return response

def main():
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
        - None

    Returns:
    --------
        - None
    """
    session = boto3.Session(
        aws_access_key_id = os.getenv('ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('SECRET_ACCESS_KEY'),
        region_name = os.getenv('REGION')
    )
    cloudformation_client = session.client('cloudformation')
    stack_name = 'my-stack-admin-user'
    template_file = './yaml_templates/admin_user.yaml'
    with open(template_file, 'r') as file:
        template_body = file.read()
    if os.getenv('ACTION').upper() == 'CREATE':
        response = create_cloudformation_stack(cloudformation_client, stack_name, template_body)
    elif os.getenv('ACTION').upper() == 'UPDATE':
        response = update_cloudformation_stack(cloudformation_client, stack_name, template_body)
    print("Stack creado:", response)

if __name__ == "__main__":
    main()
