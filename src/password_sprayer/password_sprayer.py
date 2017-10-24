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

    valid_logins = {}
    invalid_logins = {}
    yamldump = {}
    user_field = ""
    password_field = ""
    data = {}
    url = ""
    response_key = ""
    valid_response = ""

    def __init__(self, yaml_config):
        """
        Kick off the application
        """
        self.load_yaml(yaml_config)
        self.load_params()
        self.dump_yaml_output()

    def load_yaml(self, yaml_config):
        """"
        Load params from
        a YAML document
        """
        opendoc = open(yaml_config, "r")
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

            try:
                self.proxies = key['proxies']
            except KeyError:
                self.proxies = None

            try:
                self.methods = [m.lower().strip() for m in key['methods']]
            except KeyError:
                raise ValueError('Missing "methods" list')

            if key['data'] and key['data'] != None:
                data_vals = key['data']
                for k in data_vals:
                    self.data[k] = data_vals[k]

            if key['users'] and key['passwords']:
                for m in self.methods:
                    self.check_for_valid_logins(
                        key['users'], key['passwords'], m)
            else:
                keyError = 'users' if not key.get('users') else 'passwords'
                raise ValueError('Missing "{0}" list'.format(keyError))

    def check_for_valid_logins(self, users_list, passwords_list, method):
        """
        Using input parameters
        test target url/api
        with user + password
        to see if valid login
        """

        self.valid_logins[method] = {'users_pwd': []}
        self.invalid_logins[method] = {'users_pwd': []}

        for u in users_list:

            self.data[self.user_field] = u

            for p in passwords_list:

                self.data[self.password_field] = p
                requestMethod = getattr(requests, method, None)

                if requestMethod is None:
                    raise ValueError('Method "{method}" is not supported'.format(
                        method=repr(method)))

                data_key = 'params' if method == 'get' else 'data'
                req_params = {'url': self.url,
                              'proxies': self.proxies, data_key: self.data}

                r = requestMethod(**req_params)

                print "\nTrying password " + str(p)
                print "For user " + str(u)

                dictdata = json.loads(r.text)

                if dictdata[self.response_key] == self.valid_response:

                    print "Method is: " + method.upper()
                    print "Status code is: "+str(r.status_code)
                    print "Response message is: "+str(r.reason)
                    print "Valid password: "+p
                    self.valid_logins[method]['users_pwd'].append(
                        {'user': u, 'password': p})
                    break

                else:
                    print "Response message is: "+str(dictdata[self.response_key])
                    self.invalid_logins[method]['users_pwd'].append(
                        {'user': u, 'password': p})

    def dump_yaml_output(self):
        """
        Dump a lsit of valid and
        invalid login attempts to two separate
        docs
        """
        valid_logins_doc = file('valid_logins.yaml', 'w')
        yaml.dump(self.valid_logins, valid_logins_doc,
                  default_flow_style=False)

        invalid_logins_doc = file('invalid_users.yaml', 'w')
        yaml.dump(self.invalid_logins, invalid_logins_doc,
                  default_flow_style=False)
