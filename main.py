from config import Config
from multipinghost import MultiPingHost
import time


class Main():
    def __init__(self):
        # Log
        print("Starting")
        # Get config
        config = Config()
        project_dict,host_dict,site_list,tag_dict = config.get_site()
        global_set_dict = config.get_global()
        self.fping_interval = int(global_set_dict['fping_interval'])
        # put config
        self.multipinghost = MultiPingHost(
            site_list = site_list, 
            host_dict = host_dict, 
            tag_dict= tag_dict,
            project_dict = project_dict, 
            global_set_dict = global_set_dict,
            )
    
    def run(self):
        while True:
            self.multipinghost.ping_multi()
            time.sleep(self.fping_interval)


if __name__ == "__main__":
    version_str = """
    #####################
    #   Guardian ICMP   #
    #####################
    # Author - Sam      #
    # Date - 2019/08/07 #
    # Version - v0.1    #
    #####################
    """
    print(version_str)
    app = Main()
    app.run()