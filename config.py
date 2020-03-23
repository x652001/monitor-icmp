import configparser

class Config():
    def __init__(self,config='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(filenames=config)
        self.site_list = self.config.sections()
        self.site_list.remove('global')

    def get_global(self):
        global_set_dict = {}
        global_set_dict['fping_path'] = self.config['global']['fping_path']
        global_set_dict['fping_count'] = self.config['global']['fping_count']
        global_set_dict['fping_interval'] = self.config['global']['fping_interval']
        global_set_dict['pushgateway_url'] = self.config['global']['pushgateway_url']
        global_set_dict['job_name'] = self.config['global']['job_name']
        global_set_dict['max_processes'] = self.config['global']['max_processes']
        # Log
        print("===Load Global Config===")
        print(global_set_dict)
        return global_set_dict
        
    def get_site(self):
        project_dict = {}
        host_dict = {}
        tag_dict = {}
        for section in self.site_list:
            project_dict['%s' % section ] = self.config[section]['project']
            host_dict['%s' % section ] = self.config[section]['host']
            tag_dict['%s' % section ] = self.config[section]['tag']
        # Log
        print("===Load Site Config===")
        print(project_dict)
        print(host_dict)
        print(tag_dict)

        return project_dict,host_dict,self.site_list,tag_dict


if __name__ == "__main__":
    test = Config()
    a,b,c,d = test.get_site()
    print(a)
    print(b)
    print(c)
    print(d)
    e = test.get_global()
    print(e)

    

