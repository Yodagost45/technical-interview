import nmea_parser
import pytest
import pandas as pd


def test_parse_file_1():
    print("Test 1 -------------------------------------------------------")
    print("Testing no exceptions on good input")
    csv_filename = "test_1_csv"
    try:
        nmea_parser.parse_file("output", csv_filename)
    except:
        assert False
        return False
    
    #Check the output of the first two locations
    df = pd.read_csv(csv_filename)
    #print("post csv:")
    #print(df)
    
    for index, row in df.iterrows():
        print(row['lat'], row['lon'], row['hae'], row['timestamp'])
        assert row['lat'] == 51.5772666667 and row['lon'] == -1.31025 and row['hae'] == 0.0 and row['timestamp'] == '2026-01-29T14:57:56.345Z'
        break
    print("Passed")

def test_parse_file_2():
    print("Test 2 -------------------------------------------------------")
    print("Testing missing lines, expecting exception")
    with pytest.raises(Exception) as e_info:
        nmea_parser.parse_file("output_test_2", "test_2_csv")
    print(e_info.value)
    print("Passed")
    assert str(e_info.value) == "nmea file in unexpected format - should be GGA, then GSA, then RMC"

def test_parse_file_3():
    print("Test 3 -------------------------------------------------------")
    print("Testing missing latitude, expecting exception")
    with pytest.raises(Exception) as e_info:
        nmea_parser.parse_file("output_test_3", "test_3_csv")
        print(e_info)
        print("Passed")
    print(e_info.value)
    print("Passed")
    assert str(e_info.value) == "Message GPRMC invalid checksum 69 - should be 70."
    
def test_parse_file_4():
    print("Test 4 -------------------------------------------------------")
    print("Testing missing longitude, expecting exception")
    with pytest.raises(Exception) as e_info:
        nmea_parser.parse_file("output_test_4", "test_4_csv")
        print(e_info)
        print("Passed")
    print(e_info.value)
    print("Passed")
    assert str(e_info.value) == "Message GPRMC invalid checksum 6A - should be 73."
    
def test_parse_file_5():
    print("Test 5 -------------------------------------------------------")
    print("Testing file not found, expecting exception")
    with pytest.raises(Exception) as e_info:
        nmea_parser.parse_file("file_that_doesnt_exist", "test_5_csv")
        print("Passed")
        print(e_info)
        
        print("Passed")
    print(e_info.value)
    print("Passed")
    assert str(e_info.value) == "File does not exist."

test_parse_file_1()
test_parse_file_2()
test_parse_file_3()
test_parse_file_4()
test_parse_file_5()