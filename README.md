## Pithy Text Lambda
Exposes a public API over a dynamo table of couplets that I find funny or profound. Serves alexprinsen.com splash page.
The method for pulling a random record out of a dynamo table is from [this stack overflow answer](https://stackoverflow.com/questions/10666364/aws-dynamodb-pick-a-record-item-randomly)


#### Why Dynamo and Lambda?
I have worked with aws serverless solutions (in particular chalice microservices),
but wanted to deploy one end to end as an exercise.
