# aws cloudformation package \
#     --template-file helloworld-sam.yaml \
# 	--output-template-file /tmp/cf-helloworld-sam.yaml \
# 	--s3-bucket <your bucket in us-east-1> \
# 	--region us-east-1

# aws cloudformation deploy \
#     --template-file /tmp/cf-helloworld-sam.yaml \
# 	--stack-name multiregionhelloworld \
# 	--capabilities CAPABILITY_IAM \
# 	--region us-east-1

# aws cloudformation package \
#     --template-file helloworld-sam.yaml \
# 	--output-template-file /tmp/cf-helloworld-sam.yaml \
# 	--s3-bucket <your bucket in us-west-2> \
# 	--region us-west-2

# aws cloudformation deploy \
#     --template-file /tmp/cf-helloworld-sam.yaml \
# 	--stack-name multiregionhelloworld \
# 	--capabilities CAPABILITY_IAM \
# 	--region us-west-2


StackName=dev-SHM-TestMultiRegion
Sydney=ap-southeast-2
Singapo=ap-southeast-1

package-sydney:
	# find . -regex '^.*\(__pycache__\|\.py[co]\)$' -delete
	sam package \
	    --template-file helloworld-sam.yaml \
	    --output-template-file packaged.yaml \
		--s3-bucket test-xuananh-multi-region-sedney \
		--s3-prefix ${StackName} \
		--region ${Sydney}

package-singapo:
	# find . -regex '^.*\(__pycache__\|\.py[co]\)$' -delete
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
		--region ${Sydney} \
		--debug	

deploy-singapo:
	sam deploy \
	    --template-file packaged.yaml \
		--stack-name ${StackName} \
		--capabilities CAPABILITY_IAM \
		--region ${Singapo} \
		--debug

create-sydney: package-sydney deploy-sydney

create-singapo: package-singapo deploy-singapo

test-singapo:
	curl https://o5o4l439qa.execute-api.ap-southeast-1.amazonaws.com/prod/helloworld

test-sydney:
	curl https://ncbf3cwdy8.execute-api.ap-southeast-2.amazonaws.com/prod/helloworld
