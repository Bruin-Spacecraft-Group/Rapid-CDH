#Task for sending data to the ground station
#We're passed a state vector

from Tasks.template_task import task

class Comms_downlink_task(Task):
    priority = 1
    frequency = 1/10
    name = 'downlink'
    color = 'blue'

    schedule_later = True


    def senddata(self):
        print('comms is sending data')

    async def main_task(self):
        if self.satellite.isRecieving:
            print('comms is in receive mode')
        else:
            self.senddata(self.satellite.downlinkdata)
        