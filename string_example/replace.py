sample_string = "192.168.0.1"

print sample_string.replace(".","_")

Fname = "John"
Lname = "Doe"
Age = "24"


# PYTHON 2
test1 = '%s is %s years old' % ("Mar", "1")
print(test1)


# PYTHON 3
print ('{} {} is {} years old.'.format(Fname, Lname, Age))

print ('{0} {1} is {2} years old.'.format(Fname, Lname, Age))

print ('{0} {1} is {0} years old.'.format(Fname, Lname, Age))

ONBOARD_RUN_CMD = 'sudo docker run -d \ \n' \
                    '--name {containerName}-{hostPort} \ \n' \
                    '--hostname {containerHostName}-{hostPort} \ \n' \
                    '-e "SERVICE_5000_NAME=onboard-microservice" \ \n' \
                    '-p 0.0.0.0:{hostPort}:{containerPort} \ \n' \
                    '-v {hostLogDir}:{absolutePathContainerLogDir} \ \n' \
                    '-v {hostConfigDir}:{absolutePathContainerConfigDir} \ \n' \
                    '-v {hostSourceDir}:{absolutePathContainerSourceDir} \ \n' \
                    '{image}:{tag} {cmd}' \

# docker run --name "container_name" --hostname "container_hostname" --net=host -p <host_port:container_port> -v <host_dir>:<absolute_container_path> image_name:tag

print (ONBOARD_RUN_CMD.format(containerName                  = "onboard-microservice",
                             containerHostName              = "onboard_microservice",
                             hostPort                       = "10000",
                             containerPort                  = "5000",
                             hostLogDir                     = "~/validium_log",
                             absolutePathContainerLogDir    = "/root/validium_log",
                             hostConfigDir                  = "~/validium-nsb-backend/validium/common/config/service_onboard.conf",
                             absolutePathContainerConfigDir = "/etc/validium/service.conf",
                             hostSourceDir                  = "~/validium-nsb-backend",
                             absolutePathContainerSourceDir = "/root/validium-nsb-backend",
                             image                          = "shark.viosoft.com/onboard-microservice",
                             tag                            = "0.4",
                             cmd                            = '/bin/bash -c ~/validium-nsb-backend/validium/microservices/onboad/onboard_microservice.sh'
                            ))