import glob
#import lxml.etree.ElementTree as etree
from lxml import etree
import time
import numpy as np
import subprocess
from datetime import datetime

class Lqn:
        
    
    def __init__(self):
    
        self.__file_dictionary__ = {}
        
        self.__temp_output_path__ = 'C:/Volumes/Daten/PalladioTests/workspace/Output/'

        # Read all files in given directory and initialize dictionary
        self.__read_all_files__(self.__file_dictionary__, directory='model_templates/*.lqxo' )
        
        
        
        
    def __read_all_files__(self, filename, directory): 

        # Get all csv-files from given directory
        filenames = glob.glob(directory)
           
        # Iterate over all files
        for filename in filenames:
            
            # Open lqxo-file
            xml_tree = etree.parse(filename)
        
            dictionary_index = self.__get_dictionary_index__(filename)
                      
            self.__file_dictionary__[dictionary_index] = xml_tree 

            # Ausgabe
            #print("Read file: " + str(filename))
            #print("Code: " + dictionary_index)

            
            
    def __get_dictionary_index__(self, filename): 
    
        for i1 in range(1,4):
            for i2 in range(1,4):
                for i3 in range(1,4):
                    
                    s = "S" + str(i1) + "_S" + str(i2) + "_S" + str(i3)
                    
                    s_Booking = "Booking_"+s
                    s_QuickBooking = "QuickBooking_"+s
                    
                    if s_QuickBooking in filename:
                        return "QB_"+s
                        
                    if s_Booking in filename:
                        return "B_"+s                 
                        
        return 'Not found'

                        
        
    def __read_response_time_from_resultFile___(self, filename):
        
        response_time = -1
        
        try:
            # Open lqxo-output-file
            xml_tree = etree.parse(self.__temp_output_path__ + filename)
        except OSError as e:
            #print("Fehlerausgabe: " + str(e))
            return -1
            
            
         # Parse XML 
        xml_root = xml_tree.getroot()
        
        # Iterate over all "processor"-nodes
        for xml_processor in xml_root.findall('processor'): 
            
            # UsageScenario_defaultUsageScenario_1_Processor
            if xml_processor.get('name') == 'UsageScenario_defaultUsageScenario_1_Processor':
        
                xml_task = xml_processor.find('task')
                xml_entry = xml_task.find('entry') 
                xml_result_entry = xml_entry.find('result-entry') 
                            
                response_time = xml_result_entry.get('phase1-service-time')

                
        return response_time
         
         
                        
                        
    def __generate_lqn_model__(self, rate_CPU1, rate_CPU2, rate_CPU3, assembled_component, allocation_C1, allocation_C2, allocation_C3):
        
        # Build index-string for dictionary call
        dictionary_index = allocation_C1 + '_' + allocation_C2 + '_' + allocation_C3
        
        if assembled_component == "Booking":
            dictionary_index = "B_" + dictionary_index
        elif assembled_component == "QuickBooking":
            dictionary_index = "QB_" + dictionary_index
        else:
            print("Error: string not found")
        
            
        # Get xml-data from dictionary
        xml_tree = self.__file_dictionary__[dictionary_index]
        

        # TODO deepcopy (necessary?)

        # Parse XML 
        xml_root = xml_tree.getroot()
        
        # Iterate over all "processor"-nodes
        for xml_processor in xml_root.findall('processor'):           
                    
            
            # Server 1
            if xml_processor.get('name') == 'Server1_CPU_Processor':
                
                self.__xml_subroutine__(xml_processor, rate_CPU1)                       
                
            # Server 2
            if xml_processor.get('name') == 'server2_CPU_Processor':
                
                self.__xml_subroutine__(xml_processor, rate_CPU2)
                            
            # Server 3
            if xml_processor.get('name') == 'Server3_CPU_Processor':
                
                self.__xml_subroutine__(xml_processor, rate_CPU3)
                        
        
        return xml_tree
        
        
    
        
    def __xml_subroutine__(self, xml_processor, rate_CPU):
        
        rounding = 12        
        
        xml_task = xml_processor.find('task')
                
        # Iterate over all "entry"-nodes
        for xml_entry in xml_task.findall('entry'):     
            

            # Booking and Quickbooking-----------------------------------------------------------------
            
            # InternalAction_action__vGuakC6JEd-Jla2o7wkBzQ_34_50 
            if xml_entry.get('name') == 'InternalAction_action__vGuakC6JEd-Jla2o7wkBzQ_34_50_Entry':
                
                xml_entry_phase_activities = xml_entry.find('entry-phase-activities')                                            
                xml_activity = xml_entry_phase_activities.find('activity')            
                xml_activity.set('host-demand-mean', str(round(4.0/rate_CPU,rounding)))
                
            
            # InternalAction_bankPayment__QG_9kC6KEd-Jla2o7wkBzQ2_910_110
            if xml_entry.get('name') == 'InternalAction_bankPayment__QG_9kC6KEd-Jla2o7wkBzQ2_910_110_Entry':
                
                xml_entry_phase_activities = xml_entry.find('entry-phase-activities')                                
                xml_activity = xml_entry_phase_activities.find('activity')                               
                xml_activity.set('host-demand-mean', str(round(3.0/rate_CPU,rounding)))
                
                                
            # InternalAction_CCpayment__QS5rkC6KEd-Jla2o7wkBzQ2_910_110
            if xml_entry.get('name') == 'InternalAction_CCpayment__QS5rkC6KEd-Jla2o7wkBzQ2_910_110_Entry':
                
                xml_entry_phase_activities = xml_entry.find('entry-phase-activities')                                
                xml_activity = xml_entry_phase_activities.find('activity')                                
                xml_activity.set('host-demand-mean', str(round(4.0/rate_CPU,rounding)))
                
            
                # InternalAction_aName__QG_9kC6KEd-Jla2o7wkBzQ_910_110
            if xml_entry.get('name') == 'InternalAction_aName__QG_9kC6KEd-Jla2o7wkBzQ_910_110_Entry':
                
                xml_entry_phase_activities = xml_entry.find('entry-phase-activities')                                
                xml_activity = xml_entry_phase_activities.find('activity')                                
                xml_activity.set('host-demand-mean', str(round(3.0/rate_CPU,rounding)))
                
            
            # Booking only-------------------------------------------------------------------------------
                
             # InternalAction_aName__HcazEC6KEd-Jla2o7wkBzQ_67_80
            if xml_entry.get('name') == 'InternalAction_aName__HcazEC6KEd-Jla2o7wkBzQ_67_80_Entry':
                
                xml_entry_phase_activities = xml_entry.find('entry-phase-activities')                                
                xml_activity = xml_entry_phase_activities.find('activity')                                
                xml_activity.set('host-demand-mean', str(round(5.0/rate_CPU,rounding)))
                
                
            # Quickbooking only---------------------------------------------------------------------------
            
            # InternalAction_checkCache__c1GMgOtmEd-m3_hR0FtH3Q_67_80
            if xml_entry.get('name') == 'InternalAction_checkCache__c1GMgOtmEd-m3_hR0FtH3Q_67_80_Entry':
                
                xml_entry_phase_activities = xml_entry.find('entry-phase-activities')                                
                xml_activity = xml_entry_phase_activities.find('activity')                                
                xml_activity.set('host-demand-mean', str(round(0.5/rate_CPU,rounding)))
                
                            
            # InternalAction_determineCheapest__fEh4gOtmEd-m3_hR0FtH3Q_67_80
            if xml_entry.get('name') == 'InternalAction_determineCheapest__fEh4gOtmEd-m3_hR0FtH3Q_67_80_Entry':
                
                xml_entry_phase_activities = xml_entry.find('entry-phase-activities')                                
                xml_activity = xml_entry_phase_activities.find('activity')                                
                xml_activity.set('host-demand-mean', str(round(2.5/rate_CPU,rounding)))
        
                        
                     

    def __calculate_costs_numpy_adapter__(self, rate_CPU1, rate_CPU2, rate_CPU3, assembled_component, allocation_C1, allocation_C2, allocation_C3):

        rate_CPU1_np = np.array([rate_CPU1])
        rate_CPU2_np = np.array([rate_CPU2])
        rate_CPU3_np = np.array([rate_CPU3])
        
        if allocation_C1 == 'S1':
            allocation_C1_np = np.array([0])
        elif allocation_C1 == 'S2':
            allocation_C1_np = np.array([1])
        elif allocation_C1 == 'S3':
            allocation_C1_np = np.array([2])
            
        if allocation_C2 == 'S1':
            allocation_C2_np = np.array([0])
        elif allocation_C2 == 'S2':
            allocation_C2_np = np.array([1])
        elif allocation_C2 == 'S3':
            allocation_C2_np = np.array([2])
            
        if allocation_C3 == 'S1':
            allocation_C3_np = np.array([0])
        elif allocation_C3 == 'S2':
            allocation_C3_np = np.array([1])
        elif allocation_C3 == 'S3':
            allocation_C3_np = np.array([2])
            
        if assembled_component == 'Booking':
            assembled_component_np = np.array([0])
        elif assembled_component == 'QuickBooking':
            assembled_component_np = np.array([1])
            
        costs = self.calculate_costs(rate_CPU1_np, rate_CPU2_np, rate_CPU3_np, assembled_component_np, allocation_C1_np, allocation_C2_np, allocation_C3_np, 1)
        
        return costs


        
    def evaluate_fitness_list(self, argument_list):
        
        return self.evaluate_fitness(argument_list[0], argument_list[1], argument_list[2], argument_list[3], argument_list[4], argument_list[5], argument_list[6])
        
               
    
    def evaluate_fitness(self, rate_CPU1, rate_CPU2, rate_CPU3, assembled_component, allocation_C1, allocation_C2, allocation_C3):
        
        
        lqn_input_xml = self.__generate_lqn_model__(rate_CPU1, rate_CPU2, rate_CPU3, assembled_component, allocation_C1, allocation_C2, allocation_C3)
        
        date = datetime.now().strftime("%Y-%m-%d_%H%M%S_%f")
            
        inputFile_name  = date  + '.in.lqxo'           
        resultFile_name = date  + '.out.lqxo'
        
                
        # Input-Datei für LQN-Solver speichern
        lqn_input_xml.write(self.__temp_output_path__ + inputFile_name)    

        
        # Kommando-String für Aufruf des lqns-Kommandozeilentools
        command = "lqns -x -o" + self.__temp_output_path__ + resultFile_name + " " + self.__temp_output_path__ + inputFile_name
        
        # Ausgabe auf der Konsole unterdrücken
        command += " 2> nul"
        
        #print (command)
        
        # Execute LQN-solver
        subprocess.call(command, shell=True)
        
        
        # Response-Time aus lqns-result-file extrahieren
        response_time_string = self.__read_response_time_from_resultFile___(resultFile_name)
        response_time = float(response_time_string)
        
        # Calculate costs
        costs = self.__calculate_costs_numpy_adapter__(rate_CPU1, rate_CPU2, rate_CPU3, assembled_component, allocation_C1, allocation_C2, allocation_C3)
        costs = float(costs)
        
        return (costs, response_time)
            
            
        
    
    def calculate_costs(self, rate_cpu1, rate_cpu2, rate_cpu3, assembled_component, allocation_C1, allocation_C2, allocation_C3, N): 
        
        costs_cpu1 = np.zeros(N)
        costs_cpu2 = np.zeros(N)
        costs_cpu3 = np.zeros(N)
        component_costs = np.zeros(N)
        
        for i in range(N):
        
            # Costs cpu1
            if allocation_C1[i] == 0 or allocation_C2[i] == 0 or allocation_C3[i] == 0:
                costs_cpu1[i] = 0.7665*((rate_cpu1[i]/2)**6.2539)+145
            else:
                costs_cpu1[i] = 0
                
            # Costs cpu2
            if allocation_C1[i] == 2 or allocation_C2[i] == 2 or allocation_C3[i] == 2:
                costs_cpu2[i] = 0.7665*((rate_cpu2[i]/2)**6.2539)+145
            else:
                costs_cpu2[i] = 0
        
            # Costs cpu3
            if allocation_C1[i] == 1 or allocation_C2[i] == 1 or allocation_C3[i] == 1:
                costs_cpu3[i] = 0.7665*((rate_cpu3[i]/2)**6.2539)+145
            else:
                costs_cpu3[i] = 0
    
            # Component costs
            if assembled_component[i] == 0:
                component_costs[i] = 550
            else:
                component_costs[i] = 750
            
        return costs_cpu1 + costs_cpu2 + costs_cpu3 + component_costs
                
        