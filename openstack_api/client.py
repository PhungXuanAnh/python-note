from authenticate import Authenticate
from flavor import Flavor
from image import Image
from orchestration.heat import Heat

class Client(object):
    def __init__(self,  OS_AUTH_URL, OS_PROJECT_NAME, OS_USERNAME, OS_PASSWORD):
        
        self.auth = Authenticate(OS_AUTH_URL, OS_PROJECT_NAME, OS_USERNAME, OS_PASSWORD)
        self.flavor = Flavor(self.auth.get_token_id(), self.auth.get_compute_admin_url())
        self.image = Image(self.auth.get_token_id(), self.auth.get_image_admin_url())
        self.heat = Heat(self.auth.get_token_id(), self.auth.get_orchestration_admin_url())
        
