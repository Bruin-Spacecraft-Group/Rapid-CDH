class task(Task):
    priority = 1
    frequency = 1/10
    name = 'flight loop'
    color = 'blue'

    schedule_later = True

    async def main_task(self):
        if self.satellite.comms_is_recieving_beacon:
            pass
        elif self.satellite.eps_batt_soc < EPS_BATT_LOW:
            # run the task to point ADCS to the sun
            pass
        elif self.satellite.eps_batt_soc > EPS_BATT_MIN_THRUST and
             self.satellite.time > self.satellite.comms_thrust_window_begin and
             self.satellite.time < self.satellite.comms_thrust_window_end:
            print("prop enters thrust")
            # run the task to tell prop to enter THRUST MODE
