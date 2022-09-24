# DevOps ⚙️
## Manually Triggered 🤓
* Manual deploy of head of main branch
## GitHub Event Triggered 🤖
* On push to main branch runs ci tests and deploys
# Run API Locally 💻
## Steps 🕹️
  * Set up dependencies with:
    * pip install -r /requirements.txt
    * pip install -r /requirements-test.txt
  * Set env vars:
    * AWS_DEFAULT_REGION
    * AWS_SAM_STACK_NAME
    * USER_POOL_ID
    * DB_URL
    * DB_NAME
    * DB_SECRET_ARN
    * DB_CLUSTER_ARN
    * DB_PASSWORD
    * DB_USER
  * Run **'local_api.py'** with **'Flask'**
# Run Tests Locally 🧪
## Steps 🕹️
  * Set up dependencies with:
    * pip install -r /requirements.txt
    * pip install -r /requirements-test.txt
  * Enter command **'python test_runner.py'**
# View CloudWatch Logs 🔎
## Steps 🕹️
  * Install aws CLI
  * Run command **'aws logs tail /aws/lambda/pinfluencer-api-staging-PinfluencerFunction-AMRq3Jv7jD4M --follow --filter-pattern <pattern>'**
    * Filter pattern can be anything that the log contains such as:
      * The log type: **'ERROR'**, **'EXCEPTION'**, **'TRACE'**, **'DEBUG'**, **'INFO'**
      * The module name: **'src.web.middleware.MiddlewarePipeline.execute_middleware'**