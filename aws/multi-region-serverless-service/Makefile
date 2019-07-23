
StackName=dev-SHM-TestMultiRegion
Sydney=ap-southeast-2
Singapo=ap-southeast-1
Region1TargetDomainName=d-j6ein3i4kd.execute-api.ap-southeast-1.amazonaws.com
Region2TargetDomainName=d-m7ull8gzaj.execute-api.ap-southeast-2.amazonaws.com
HostedZoneId=Z3NEZJXMZLM0JX
MultiregionDomainName=devapi.inslifeguard.com
BasePath=test-multi-region

package-sydney:
	sam package \
		--template-file helloworld-sam.yaml \
		--output-template-file packaged.yaml \
		--s3-bucket test-xuananh-multi-region-sedney \
		--s3-prefix ${StackName} \
		--region ${Sydney}

package-singapo:
	sam package \
		--template-file helloworld-sam.yaml \
		--output-template-file packaged.yaml \
		--s3-bucket test-xuananh-multi-region-singapo \
		--s3-prefix ${StackName} \
		--region ${Singapo}

deploy-sydney:
	sam deploy \
		--template-file packaged.yaml \
		--stack-name ${StackName} \
		--capabilities CAPABILITY_IAM \
		--region ${Sydney}

deploy-singapo:
	sam deploy \
		--template-file packaged.yaml \
		--stack-name ${StackName} \
		--capabilities CAPABILITY_IAM \
		--region ${Singapo}

create-sydney: package-sydney deploy-sydney
	REGION=${Sydney} \
	BasePath=${BasePath} \
	MultiregionDomainName=${MultiregionDomainName} \
		python base_path_mapping.py create

undeploy-sydney:
	REGION=${Sydney} \
	BasePath=${BasePath} \
	MultiregionDomainName=${MultiregionDomainName} \
		python base_path_mapping.py delete
	aws cloudformation delete-stack --stack-name ${StackName} --region ${Sydney}

create-singapo: package-singapo deploy-singapo
	REGION=${Singapo} \
	BasePath=${BasePath} \
	MultiregionDomainName=${MultiregionDomainName} \
		python base_path_mapping.py create

undeploy-singapo:
	REGION=${Singapo} \
	BasePath=${BasePath} \
	MultiregionDomainName=${MultiregionDomainName} \
		python base_path_mapping.py delete
	aws cloudformation delete-stack --stack-name ${StackName} --region ${Singapo}

package-dns:
	sam package \
		--template-file helloworld-dns.yaml \
		--output-template-file packaged.yaml \
		--s3-bucket test-xuananh \
		--s3-prefix ${StackName}-dns \

deploy-dns:
	sam deploy \
		--template-file packaged.yaml \
		--stack-name ${StackName}-dns \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides "Region1TargetDomainName=${Region1TargetDomainName}" \
							  "Region2TargetDomainName=${Region2TargetDomainName}" \
							  "HostedZoneId=${HostedZoneId}" \
							  "MultiregionDomainName=${MultiregionDomainName}"

create-dns: package-dns deploy-dns
undeploy-dns:
	aws cloudformation delete-stack --stack-name ${StackName}-dns


request-dns:
	curl https://devapi.inslifeguard.com/${BasePath}/helloworld/

validate:
	sam validate -t helloworld-dns.yaml

get-apiurl-sydney:
	aws cloudformation describe-stacks \
		--stack-name ${StackName} \
		--query 'Stacks[].Outputs[?OutputKey==`HelloWorldApi`]' \
		--output table \
		--region ${Sydney}

get-apiurl-singapo:
	aws cloudformation describe-stacks \
		--stack-name ${StackName} \
		--query 'Stacks[].Outputs[?OutputKey==`HelloWorldApi`]' \
		--output table \
		--region ${Singapo}


SingapoDomain=qz09wf8am2.execute-api.ap-southeast-1.amazonaws.com
SydneyDomain=n3f0l47ew7.execute-api.ap-southeast-2.amazonaws.com
request-singapo:
	curl https://${SingapoDomain}/prod/helloworld

request-sydney:
	curl https://${SydneyDomain}/prod/helloworld

test:
	echo aaaa


get-lambda-singapo:
	aws cloudformation describe-stacks \
		--stack-name ${StackName} \
		--query 'Stacks[].Outputs[?OutputKey==`GetHealthcheckFunctionName`]' \
		--output table \
		--region ${Singapo}

get-lambda-sydney:
	aws cloudformation describe-stacks \
		--stack-name ${StackName} \
		--query 'Stacks[].Outputs[?OutputKey==`GetHealthcheckFunctionName`]' \
		--output table \
		--region ${Sydney}		

SingapoFunctionName=dev-SHM-TestMultiRegion-GetHealthcheck-KF3ATIB1GLOU
SydneyFunctionName=dev-SHM-TestMultiRegion-GetHealthcheck-L4I9FUZOCINW

update-lambda-singapo:
	aws lambda update-function-configuration \
		--function-name dev-SHM-TestMultiRegion-GetHealthcheck-KF3ATIB1GLOU \
		--environment Variables="{STATUS=fail}" \
		--region ${Singapo}

	