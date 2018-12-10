import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import csv
import glob




def read_all_csv_files(directory, columns, index_response_time):
     
    # Get all csv-files from directory
    filenames = glob.glob(directory)
    
    
    # Iterate over all files
    for filename in filenames:
    
        # Ausgabe
        print("Read file: " + str(filename))
        
        # Open csv-file
        with open(filename, 'r') as csvfile:
        
            # Read csv-file
            readCSV = csv.reader(csvfile, delimiter=';')
            
            # Laufvariable für Zeilen
            j=0
            
            # Vorherige Response Time
            response_time_old = -1
                       
            # Datensamples aus CSV-Datei zeilenweise auslesen
            for row in readCSV:
                
                response_time = row[index_response_time]
                
                # Überspringen, falls falls sich response time wiederholt oder gleich Infinity,
                if response_time != response_time_old and response_time != 'Infinity':
                
                    # Erste Zeile überspringen (Header-Zeile)
                    if j>0:
                        
                        # Zeile auslesen
                        for i in range( len(columns) ):
                            columns[i].append(row[i])
                                                
                    # Laufvariable inkrementieren
                    j=j+1
                    
                # Response-Time übernehmen
                response_time_old = response_time
                
            print("Anzahl der ausgelesenen Datensamples: " + str(j-1) ) 
            
            
    
   
    
def lists_to_numpy_array(columns, columns_format):
    
    temp = None
    out = None
    
    for i in range( len(columns) ):
        
        # Spalte ist vom Datentyp float
        if columns_format[i] == 'float':
            temp = np.array(columns[i], dtype=float)
            
        # Spalte ist vom Datentyp categorial (Kategorie)
        elif columns_format[i] == 'categorial':
            temp = to_one_hot(columns[i])
            

        # Spalte zur Output-Matrix hinzufügen
        if out is None:
            out = temp
            
        else:
            out = np.column_stack([out, temp])


    return out  





def to_one_hot(values):

    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)

    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    
    print(label_encoder.classes_)

    return onehot_encoded
    
    
    


def pareto_front_list_dumb(liste):
    
    print(len(liste))
    
    pareto_list = []

    cycle = 0
    
    for i in liste:    
        
        if is_pareto_list_dumb(i, liste) == True:
            pareto_list.append(i)
            
        print('Cycle ' + str(cycle) + ' / ' + str(len(liste)))
        cycle = cycle+1       
    
    return pareto_list
    
    
    

def is_pareto_list_dumb(d, liste):
    
    #return_is_pareto = True
    
    for i in liste: 
    
        if i[0] < d[0] and i[1] < d[1]:    
            #return_is_pareto = False
            return False
            
    #return return_is_pareto
    return True

    
    
    
def pareto_front_dumb(data):
    
    len_data = len(data)
    print(len_data)
    
    # Array indicating whether each point is Pareto efficient
    # 0: Point is pareto-efficient
    # 1: Point is not pareto-efficient
    is_efficient = np.zeros(len_data)
       
    
    for i in range(len_data):    
        
        if is_pareto_dumb(data[i,:], data) == True:
            is_efficient[i] = 0

        else:
            is_efficient[i] = 1

        print('Cycle ' + str(i))

        
    # Return indices for non-zero elements to eleminate non pareto-efficient points
    nonzero_indices = np.nonzero(is_efficient) 
    
    # Delete non-pareto points
    data_pareto = np.delete(data, nonzero_indices, axis=0)
    
    return data_pareto
    

    
    
def is_pareto_dumb(d, data):
    
    len_data = len(data)
    
    #return_is_pareto = True
    
    for i in range(len_data): 
    
        if data[i,0] < d[0] and data[i,1] < d[1]:    
            #return_is_pareto = False
            return False
            
    #return return_is_pareto
    return True


    
    
# Zum Testen
def get_random_pareto(count, radius):
       
    x = np.random.rand(count,1)*90 + 10
    y = np.random.rand(count,1)*90 + 10
    
    # Punkte entfernen
    for i in range(count):
        
        xi = x[i]
        yi = y[i]


        if (xi*xi + yi*yi < radius*radius):
            x[i] = 'inf'
            y[i] = 'inf'
            
    return (x,y)

    
    
def to_numpy(liste, index_column):
    
    out = np.zeros((len(liste), 1))
    
    k=0
    
    for i in liste:
        
        out[k] = i[index_column]

        k=k+1

    return out
    
    
    

    