Viewport Lambda
=====================
Project for AWS Lambda

Moving Parts
-------

* Python lambda function
* API Gateway setup
* Javascript client

Lambda Setup Guide
--------
Create a Python Virtual Environment:
```bash
mkdir my_lambda_function
cd my_lambda_function
python3 -m venv venv
source venv/bin/activate
```
Create a Deployment Package:
```bash
deactivate
mkdir package
source venv/bin/activate
pip install Your-Modules -t ./package
deactivate
```

Copy your lambda function into the package directory:
```bash
cp lambda_function.py package/
```

Zip your deployment package:
```bash
pushd package
zip -r ../my_lambda_function.zip .
popd
```

Create the Lambda function in AWS:
```bash
aws lambda create-function --function-name mySpreadsheetLambda \\
   --zip-file fileb://my_lambda_function.zip --handler lambda_function.lambda_handler \\
   --runtime python3.8 --role arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_LAMBDA_EXECUTION_ROLE
```

Support and Documentation
-------------------------
For AWS CLI support Follow the instructions in the [AWS CLI User Guide](https://docs.aws.amazon.com/cli/latest/userguide/).
