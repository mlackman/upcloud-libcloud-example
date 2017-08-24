import sys

from libcloud.compute.drivers import upcloud
from libcloud.compute.deployment import ScriptDeployment
from libcloud.compute.base import NodeAuthSSHKey

private_ssh_key_file = 'path to private ssh key, example /home/somebody/.ssh/id_rsa'
ssh_key='public ssh key'

if len(sys.argv) != 3:
    print('Change also private_ssh_key_file and ssh_key')
    print('usage: python deploy.py username password')
    sys.exit(-1)

username = sys.argv[1]
password = sys.argv[2]

driver = upcloud.UpcloudDriver(username, password)
image = [image  for image in driver.list_images() if image.name.startswith('Ubuntu')][0]
size = [size for size in driver.list_sizes() if size.name=='1xCPU-1GB'][0]
location = [location for location in driver.list_locations() if location.name.startswith('Helsinki')][0]

script = ScriptDeployment('echo "testing testing" > output.txt')

auth = NodeAuthSSHKey(ssh_key)
node = driver.deploy_node(ssh_key=private_ssh_key_file,
        ssh_username=username,
        deploy=script, image=image, size=size, location=location, name='testing',
        auth=auth)
print(node.public_ips)


