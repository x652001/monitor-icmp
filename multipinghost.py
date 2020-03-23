import multiprocessing
from pinghost import PingHost
from pushgateway import PushGateway

class MultiPingHost():
    def __init__(self,site_list,host_dict,project_dict,global_set_dict,tag_dict):
        # Define what site need to be test
        # Section name from config.ini
        self.site_list = site_list
        # Host which need to be ping from config.ini
        self.host_dict = host_dict
        # Project name in each host from config.ini 
        self.project_dict = project_dict
        # Tag name in each host from config.ini
        self.tag_dict = tag_dict
        # Global settings from config.ini
        self.global_set_dict = global_set_dict
        # Define the multi process number by site_list quantity
        if len(self.site_list) > int(global_set_dict['max_processes']):
            self.process_num = int(global_set_dict['max_processes'])
        else:
            self.process_num = len(self.site_list)
        # Init the fping
        self.pinghost = PingHost(fping_path=global_set_dict['fping_path'],ping_count=global_set_dict['fping_count']) 
        # Init the pushgateway API request
        self.pushgateway = PushGateway(job_name=global_set_dict['job_name'],url=global_set_dict['pushgateway_url'])

    # Get ICMP latency & loss packet values & Send data to pushgateway by API
    def add(self,site,ip,project,tag):
        # Get icmp latency & loss packet
        loss,latency = self.pinghost.ping(ip)
        # Send metric & value to pushgateway
        self.pushgateway.senddata(
            metrics='icmp_packet_latency_avg', 
            value=latency, 
            instance=site, 
            project=project, 
            tag = tag, 
            host = ip
            )
        self.pushgateway.senddata(
            metrics='icmp_packet_loss', 
            value=loss, 
            instance=site, 
            project=project,
            tag = tag,
            host = ip
            )
        return

    # Multi Process 
    def ping_multi(self):
        host_list = []
        for site in self.site_list:
            host_list.append((site,self.host_dict[site],self.project_dict[site],self.tag_dict[site]))
        pool = multiprocessing.Pool(processes=self.process_num)
        pool.starmap(self.add,host_list)
        pool.close()
        pool.join()


if __name__ == "__main__":
    global_set_dict = {
        'fping_path': "'/usr/local/bin/fping'", 
        'fping_count': '10', 
        'pushgateway_url': '192.168.66.100:9091', 
        'job_name': 'guardian_icmp', 
        'max_processes': '30'
        }
    site_list = ['google', 'yahoo']
    host_dict = {'google': 'www.google.com', 'yahoo': 'www.yahoo.com'}
    project_dict = {'google': 'project_test', 'yahoo': 'project_test'}
    tag_dict = {'google': 'Taiwan', 'yahoo': 'Taiwan', 'pchome': 'Taiwan'}
    test = MultiPingHost(
        site_list=site_list, 
        host_dict=host_dict, 
        project_dict=project_dict, 
        global_set_dict=global_set_dict,
        tag_dict = tag_dict
        )
    test.ping_multi()

    pass
