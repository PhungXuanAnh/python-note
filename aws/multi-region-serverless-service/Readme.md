# Step by step to deploy this sample code to multiple region

## Deploy on singapo and sydney

```shell
.venv3
make create-singapo
make create-sydney
```

## Check result

```shell
make get-apiurl-singapo
make get-apiurl-sydney
```

Copy OutputValue and replace **SingapoDomain** and **SydneyDomain** in Makefile to test below command:

```shell
make request-singapo
make request-sydney 
```

## Deploy dns


```shell
make create-dns
```

## Test

```shell
make request-dns

{"message": "Hello from ap-southeast-1"}% 
```

Get function name:

```shell
make get-lambda-singapo
make get-lambda-sydney
```

Copy OutputValue and replace in **SingapoFunctionName** and **SydneyFunctionName** in Makefile

Then change status of Singapo lambda to **fail**

```shell
make update-lambda-singapo
```

Run request dns again to see failover


