
StackName=dev-SHM-TestMultiRegion
Sydney=ap-southeast-2
Singapo=ap-southeast-1
Region1TargetDomainName=d-j6ein3i4kd.execute-api.ap-southeast-1.amazonaws.com
Region2TargetDomainName=d-m7ull8gzaj.execute-api.ap-southeast-2.amazonaws.com
HostedZoneId=Z3NEZJXMZLM0JX
MultiregionDomainName=devapi.inslifeguard.com

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
	REGION=${Sydney} python base_path_mapping.py create

undeploy-sydney:
	aws cloudformation delete-stack --stack-name ${StackName} --region ${Sydney}

create-singapo: package-singapo deploy-singapo
	REGION=${Singapo} python base_path_mapping.py create

create-base-path-singapo:
	REGION=${Singapo} python base_path_mapping.py create

undeploy-singapo:
	aws cloudformation delete-stack --stack-name ${StackName} --region ${Singapo}

test-singapo:
	curl https://o5o4l439qa.execute-api.ap-southeast-1.amazonaws.com/prod/helloworld

test-sydney:
	curl https://ncbf3cwdy8.execute-api.ap-southeast-2.amazonaws.com/prod/helloworld


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


test-dns:
	curl https://devapi.inslifeguard.com/v1/helloworld/

validate:
	sam validate -t helloworld-dns.yaml