#Task for sending data to the ground station
#We're passed a state vector

from Tasks.template_task import task

class task(Task):
    priority = 1
    frequency = 1/10
    name = 'downlink'
    color = 'blue'

    schedule_later = True


    def senddata(self):
        pass

    async def main_task(self):
        if self.satellite.isRecieving:
            pass
        else:
            self.senddata(self.satellite.downlinkdata)
        