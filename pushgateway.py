import requests
import time

class PushGateway():
    def __init__(self,job_name,url='localhost:9091'):
        # Init the pushgateway API url
        self.url = 'http://%s/metrics/job/%s' % (url,job_name)

    def senddata(self, metrics, value, instance, project = None, tag = None, host = None):
        # Add instance Tag
        full_url = self.url + '/instance/%s' % instance
        # Add Tag label
        if project != None:
            full_url += '/project/%s' % project 
        if tag != None:
            full_url += '/tag/%s' % tag
        if host != None:
            full_url += '/host/%s' % host
        # Metric key & value 
        data = '%s %s\n' % (metrics,value)
        # Print Log
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(full_url)
        print('%s = %s' % (instance,data))
        # Post data to pushgateway API
        res = requests.post(url = full_url,data=data)
        return res
        


if __name__ == "__main__":
    url = '192.168.66.100:9091'
    test = PushGateway(url=url,job_name='guardian')
    #test.senddata(metrics='test_metrics',value=12,instance='web002',project='testproject3',tag='Hello2')
    test.senddata(metrics='test_metrics',value=12,instance='web003')