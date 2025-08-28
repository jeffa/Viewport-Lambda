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
mkdir my_lambda_project
cd my_lambda_project
python3 -m venv venv
```
Create a Deployment Package:
```bash
mkdir package
source venv/bin/activate
pip install window-viewport -t ./package
deactivate
```
Copy your lambda function into the package directory:
```bash
cp /path/to/lambda_function.py package/
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

API Gateway Setup Guide
--------
Create a resource with a name such as `tform` or `transform` and create a POST method for it.
Despite Cors being handled within the lambda you will still need to configure it for the Gateway.

Javascript Client
--------
The incoming JSON should have the following structure:
```json
{
    "coordinates": [[x1, y1], [x2, y2], ..., [xn, yn]],
    "world_bounds": [xmin, xmax, ymin, ymax],   // Optional
    "view_bounds": [xmin, xmax, ymin, ymax]     // Optional
}
```

Support and Documentation
-------------------------
[curl examples](curl-examples.md)

For AWS CLI support Follow the instructions in the [AWS CLI User Guide](https://docs.aws.amazon.com/cli/latest/userguide/).
