import subprocess
import sys

# Using fping from shell to check icmp latancy 
class PingHost():
    def __init__(self,fping_path='/usr/local/sbin/fping',ping_count=5):
        # Define the fping path in shell
        self.fping_path = fping_path
        # Set the fping's ping count
        self.ping_count = str(ping_count)

    # Get icmp latency & loss with IP
    def ping(self,ipaddr):
        # Get fping's stdout (this variable type is byte) 
        res = subprocess.Popen(
            '%s -c%s %s 2>&1' % (self.fping_path,self.ping_count,ipaddr), 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            ).communicate()[0]
        # Change the variable type to str from byte
        # Makesure can change this str into list
        result = res.decode().replace('%,', '').replace('/',' ').split('\n')[-2]
        # Get ICMP latency average
        try: 
            icmp_packet_latency_avg = float(result.split(' ')[-2])
        except ValueError:
            icmp_packet_latency_avg = -1
        # Get ICMP loss
        try: 
            icmp_packet_loss = float(result.split(' ')[-8])
        except ValueError:
            icmp_packet_loss = -1
        except IndexError:
            icmp_packet_loss = -1
        # 
        return icmp_packet_loss,icmp_packet_latency_avg


if __name__ == "__main__":
    test = PingHost(fping_path='/usr/local/bin/fping',ping_count=10)
    a,b = test.ping('www.google.com')
    print('icmp packet loss: ' + str(a) + '%')
    print('icmp packet latency avg: ' + str(b) +'ms')