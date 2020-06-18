# Create WLD
import sys
import os
import time
sys.path.append(os.path.abspath(__file__ + '/../../'))
from Utils.utils import Utils


class CreateDomain:
    def __init__(self):
        print('Create Domain')
        self.utils = Utils(sys.argv)
        self.hostname = sys.argv[1]

    def create_workload_domain(self):
        # validations
        data = self.utils.read_input(os.path.abspath(__file__ + '/../') + '/domain_creation_spec_vxrail.json')
        validations_url = 'https://' + self.hostname + '/v1/domains/validations'
        response = self.utils.post_request(data, validations_url)
        print ('Validatin started for domain. The valdidation id is: ' + response['id'])
        validate_poll_url = 'https://' + self.hostname + '/v1/domains/validations/' + response['id']
        print ('Polling on validation api ' + validate_poll_url)
        time.sleep(10)
        validation_status = self.utils.poll_on_id(validate_poll_url, False)
        print('Validate domain ended with status: ' + validation_status)
        if validation_status != 'SUCCEEDED':
            print ('Validation Failed.')
            exit(1)

        # Domain Creation
        domain_creation_url = 'https://' + self.hostname + '/v1/domains'
        response = self.utils.post_request(data, domain_creation_url)
        print ('Creating Domain...')
        task_url = 'https://' + self.hostname + '/v1/tasks/' + response['id']
        print ("Domain creation task completed with status:  " + self.utils.poll_on_id(task_url, True))

if __name__ == "__main__":
    CreateDomain().create_workload_domain()

