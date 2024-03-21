# de-totes-project

Northcoders Data Engineer Nov 2023 cohort project

Team Name: TotesOps

Project specification can be found here: https://github.com/northcoders/de-project-specification

## Set-up
##### Setting up variable environment for the project
Before running the project, you will need to run the following command to set up your variable environment and install any required dependencies:

`make requirements`

##### Creating bucket to store Terraform tf state file
Run the following command to create an s3 bucket to store the terraform state file (you will be prompted to name the bucket):

`make run-make-bucket`

##### Setting up AWS SNS topic
You should then run the following command from the root of the project to create an AWS SNS topic using your email address. This is where alerts and alarms will be sent:

`./deployment/email_subscriber.sh myemail@email.com`

##### Storing database credentials in AWS Secrets Manager
In order to create a secret containing login credentials on AWS SecretsManager, you will need a db_credentials.json file in the following format:

```
{ 
    "database" : "databasename",
    "user" : "username",
    "password" : "password",
    "host" : "awshostname",
    "port" : "0000"
}
```

The contents of this JSON file is created through the command line AWS Secrets Manager and accessed in Lambda handlers to access the totesys database.

You will then need to repeat this process to store the credentials for the data warehouse in a separate secret.

## Deployment
All required AWS infrastructure is deployed via Terraform (except for the aforementioned tf state bucket, SNS topic and secrets).

The deployment is automated via a CI/CD pipeline carried out with GitHub Actions.


## Lambda 1 (extract_handler1)

### Description
This lambda handler operates on a 2 minute schedule and checks all tables in the totesys database for new data at each invocation.
If new data is found, it writes this data to a csv file and saves it to a designated S3 bucket (ingestion bucket - organised in sub-folders for each table).


### Util functions
This lambda handler utilises the following util functions:
- get_table_names
- get_bucket_name
- is_bucket_empty
- L1_extract_data
- get_most_recent_file
- get_timestamp
- format_data
- write_csv

## Lambda 2 (transform_handler2)

### Description
This lambda handler is triggered by an update to the ingestion bucket. The lambda handler reads the most recent file in the ingestion bucket and converts the file from csv to a dataframe. The lambda handler then transforms the data to the desired format and writes the transformed dataframe to a parquet file and saves it to a designated S3 bucket (processed bucket - organised in sub-folders for each table).

### Util functions
This lambda handler utilises the following util functions:

- get_file_and_ingestion_bucket_name
- get_bucket_name_2
- get_most_recent_file_2
- make_dim_counterparty
- make_dim_currency
- make_dim_date
- make_dim_design
- make_dim_location
- make_dim_staff
- make_fact_sales_order
- read_csv_to_df
- write_to_parquet

## Lambda 3 (load_handler3)

### Description
This lambda handler is triggered by an update to the processed bucket. The lambda handler reads the most recent parquet file in the processed bucket, converts the data into a dataframe and inserts it into the correct table in the data warehouse.

### Util functions
This lamba handler utilises the following util functions:

- get_file_and_bucket
- get_table_name
- read_parquet
- upload_data


