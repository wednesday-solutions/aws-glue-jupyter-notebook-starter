# AWS Glue Jupyter Notebook Starter

## Philosophy
This project is a AWS glue starter project. It simulates the glue environment so that you can test your scripts out locally. 
It also comes with out of the box IaC (Infrastructure as Code) so that you can create the entire AWS Glue stack with a single command. 
This comes with
- A S3 Bucket
- 2 glue jobs
- A source crawler
- A target crawler
- Integration with Athena
- Required IAM Roles and Policies 

## Folder Structure
```
├── Dockerfile                                      |-> Custom Dockerfile to run Glue locally with support for .env
├── Makefile                                        |-> Makefile that contains all automation
├── README.md                                       |
│
├── config                                          |-> Contains configurable properties
│   ├── properties.yml                              |-> make infra will auto-populates the bucket_name which is then read in the CD script
├── assets                                          |-> This folder will contain all IaC related assets
│   ├── glue-template.yaml.j2                       |-> Jinja2 templating that creates various assets needed for Glue and prefixes the stack name
│   └── output.yaml                                 |-> Output cloudformation yaml after replacing variables
│
├── data                                            |-> Contains all data assets required for local exection
│   └── raw                                         |-> Contains all of the raw data files
│       └── sample.csv                              |-> Raw sample csv file
│
├── landing                                         |-> Contains all data post transformation
│   ├── job1                                        |-> Contains landing data related to job1
│   │   └── output                                  |-> Contains all of the parts associated to output
│   └── job2                                        |-> Contains landing data related to job2
│   │   └── output                                  |-> Contains all of the parts associated to output
│
├── scripts                                         |-> Contain all of the executables for this project
│   ├── convert-notebooks-to-scripts.sh             |-> Recursively iterates job folders and convert notebooks to scripts
│   ├── create-glue-job.sh                          |-> Creates resources on AWS, copy appropriate files to the s3 buckets and trigger crawlers
│   ├── env-to-args.sh                              |-> Recursively iterates job folders and convert env files to job parameters
│   └── run.sh                                      |-> Runs the notebook locally
│   └── tear-down-glue.sh                           |-> Brings down all created AWS resources 
│   └── update-glue-job.sh                          |-> Updates the glue job along with other resources via the cd pipeline
│
├── src                                             |-> Contains all glue job files and folders
    └── jobs                                        |-> Contains all glue jobs in individual folders
        ├── job1                                    |-> Contains all data for job1 including env, notebook and the script
        │   ├── notebook.ipynb                      |-> Notebook for job1
        │   └── script.py                           |-> Script generated from the notebook
        └── ...
            ├── ...
            └── ...

```
## Getting started

The Makefile contains the following commands
- infra: IaC for setting things up on aws. Try it out using
    ```
    make infra name=aws-glue-jupyter-notebook-starter region=ap-south-1
    ```

- local: fire up the docker container and get your glue environment running on http://localhost:8888/lab
    ```
    make local
    ```

- env-to-args: automation to convert environment variables into DefaultArguments for respective jobs
    ```
    make env-to-args
    ```

- notebooks-to-scripts: automation to convert your notebooks to scripts recursively across jobs
    ```
    make notebooks-to-scripts
    ```

- update-infra: automation to update infra and scripts in the cd pipeline
    ```
    run: make update-infra name=aws-glue-jupyter-notebook-starter region=ap-south-1
    ```
- teardown-infra: automation to delete contents of s3 and tearn dow n created infr
    ```
    make teardown-infra   
    ```        