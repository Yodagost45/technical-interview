#from nmea import input_stream, data_frame
import pytest
import pandas as pd
from pynmeagps import NMEAReader
from pathlib import Path


def parse_file(nmea_filename, output_csv_filename):
    # Import nmea data
    # Convert to CSV
    # Save csv file and output file name, according to name input
    if not nmea_filename.endswith('.nmea'):
        nmea_filename = nmea_filename + '.nmea'


    csv_array = []
    my_file = Path(nmea_filename)
    #print(my_file.is_file())
    if my_file.is_file():
        with open(nmea_filename, 'rb') as stream:
            nmr = NMEAReader(stream, nmeaonly=True, validate=1 or 2, quitonerror=2 )
            
            counter = [0, 0]
            for raw_data, parsed_data in nmr: 
                #print(parsed_data)
                #print(raw_data)
                #print(parsed_data.msgID)
                match parsed_data.msgID:
                    case "GGA":
                        csv_array.append([])
                        if counter[1] != 0:
                            raise Exception("nmea file in unexpected format - should be GGA, then GSA, then RMC") 
                        counter[1] += 1
                        csv_array[counter[0]].append(parsed_data.lat)
                        csv_array[counter[0]].append(parsed_data.lon)
                        #print(parsed_data.lat)
                        #print(parsed_data.lon)

                        #print(parsed_data.alt)
                        #print(parsed_data.sep)
                        hae = parsed_data.alt - parsed_data.sep
                        #print("HAE: " + str(hae))
                        csv_array[counter[0]].append(hae)

                    case "GSA":
                        #print("GSA")
                        if counter[1] != 1:
                            raise Exception("nmea file in unexpected format - should be GGA, then GSA, then RMC") 
                        counter[1] += 1
                    case "RMC":
                        #print("RMC")
                        if counter[1] != 2:
                            raise Exception("nmea file in unexpected format - should be GGA, then GSA, then RMC") 
                        counter[1] = 0
                        datetime = str(parsed_data.date) + "T" + str(parsed_data.time)
                        datetime = datetime[:-3]
                        datetime += "Z"
                        #print(datetime)
                        csv_array[counter[0]].append(datetime)
                        counter[0] += 1
        #print(csv_array)
                    

        #output and save as csv
        df = pd.DataFrame(
            csv_array,
            columns=["lat", "lon", "hae", "timestamp"]
        )
        
        df.to_csv(output_csv_filename, index=False)
    else:
        #File does not exist
        print("hi")
        raise Exception("File does not exist.")

#def test_parse_file():

    #assert parse_file()

