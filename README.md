# DevOps ⚙️
## Manually Triggered 🤓
* Manual deploy of head of main branch
## GitHub Event Triggered 🤖
* On push to main branch runs ci tests and deploys
# Run Locally 💻
## Steps 🕹️
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
  * Enter command **'python local_api.py'**
# Run Tests 🧪
## Steps 🕹️
  * Enter command **'python test_runner.py'**