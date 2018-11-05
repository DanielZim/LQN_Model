import sys
sys.path.append('../../Utils')
import numpy as np
import lqn
import time
import myUtils as utils


# Daten initialisieren
pofod                   = []
cost                    = []
response_time           = []
rate_cpu1               = [] 
rate_cpu2               = []
rate_cpu3               = []
assembled_component     = []
allocation_C1           = []
allocation_C2           = []
allocation_C3           = []



columns = [cost, response_time, pofod, rate_cpu1, rate_cpu2, rate_cpu3, assembled_component, 
           allocation_C1, allocation_C2, allocation_C3]
          
          
# Read all csv-files in given directory
utils.read_all_csv_files("peropteryx_import/*.csv", columns, index_response_time=1)  


print(len(columns))

# LQN-Instanz initialisieren
mylqn = lqn.Lqn()




# Zeitmessung
timestamp1 = time.time()

#for i in range(len(cost)):
N = len(cost)
     
for i in range(N):
    
    # CPU rates
    rate1 = float(rate_cpu1[i])
    rate2 = float(rate_cpu2[i])
    rate3 = float(rate_cpu3[i])
    
    # Assembled Component
    if assembled_component[i] == 'BookingSystem (ID: _ZZH7IC6IEd-Jla2o7wkBzQ)':
        ac = 'Booking'
    elif assembled_component[i] == 'QuickBooking (ID: __VPcQOtlEd-m3_hR0FtH3Q)':
        ac = 'QuickBooking'
    else:
        ac = None
    
    # Allocation C1 
    if allocation_C1[i] == 'Server1 (ID: _g7HJEC6MEd-Jla2o7wkBzQ)':
        a1 = 'S1'
    elif allocation_C1[i] == 'server2 (ID: _h3wXgC6MEd-Jla2o7wkBzQ)':
        a1 = 'S2'
    elif allocation_C1[i] == 'Server3 (ID: _vxqJwS6QEd-pNfzbJsur0g)':
        a1 = 'S3'
    else:
        a1 = None
        
    # Allocation C2 
    if allocation_C2[i] == 'Server1 (ID: _g7HJEC6MEd-Jla2o7wkBzQ)':
        a2 = 'S1'
    elif allocation_C2[i] == 'server2 (ID: _h3wXgC6MEd-Jla2o7wkBzQ)':
        a2 = 'S2'
    elif allocation_C2[i] == 'Server3 (ID: _vxqJwS6QEd-pNfzbJsur0g)':
        a2 = 'S3'
    else:
        a2 = None
        
    # Allocation C3
    if allocation_C3[i] == 'Server1 (ID: _g7HJEC6MEd-Jla2o7wkBzQ)':
        a3 = 'S1'
    elif allocation_C3[i] == 'server2 (ID: _h3wXgC6MEd-Jla2o7wkBzQ)':
        a3 = 'S2'
    elif allocation_C3[i] == 'Server3 (ID: _vxqJwS6QEd-pNfzbJsur0g)':
        a3 = 'S3'
    else:
        a3 = None
        
        
    #rt = mylqn.evaluate_fitness(7.345, 6.223, 4.543, 'Booking', 'S1', 'S2', 'S3')
    (costs, rt) = mylqn.evaluate_fitness(rate1, rate2, rate3, ac, a1, a2, a3)
    
    out = str(rt) + " - " + str(response_time[i]) + '-' + str(rate1) + '-' + str(rate2) + '-' + str(rate3) + '-' + a1 + '-' + a2 + '-' + a3 + '-' + ac
    
    if float(rt) != float(response_time[i]):   
        print(out)

    if i%100 == 0:
        print(i)



# Zeitmessung
timestamp2 = time.time()
diff = timestamp2 - timestamp1



print ("This took %.2f seconds" % diff)







