import unittest
import pandas as pd
from datetime import datetime
import batch

def dt(hour, minute, second=0):
    return datetime(2022, 1, 1, hour, minute, second)

class TestPrepareData(unittest.TestCase):
    def test_prepare_data(self):
        
        categorical = ['PUlocationID', 'DOlocationID']
        # Define test input
        data = [
            (None, None, dt(1, 2), dt(1, 10)),
            (1, None, dt(1, 2), dt(1, 10)),
            (1, 2, dt(2, 2), dt(2, 3)),
            (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
            (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
            (3, 4, dt(1, 2, 0), dt(2, 2, 1)),     
        ]


        columns = ['PUlocationID', 'DOlocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']

        df = pd.DataFrame(data, columns=columns)

        df_actual = batch.prepare_data(df, categorical)

        data_expected = [
            ('-1', '-1', 8.0),
            ('1', '-1', 8.0),
            ('1', '2', 1.0),
        ]
        
        columns_test = ['PUlocationID', 'DOlocationID', 'duration']
        df_expected = pd.DataFrame(data_expected, columns=columns_test)
        
        print("Number of rows in the expected dataframe:", df_expected.shape[0])


        self.assertTrue(df_actual['PUlocationID'].equals(df_expected['PUlocationID']))
        self.assertTrue(df_actual['DOlocationID'].equals(df_expected['DOlocationID']))
        self.assertAlmostEqual((df_actual['duration'] - df_expected['duration']).abs().sum(), 0, places=6)

if __name__ == '__main__':
    unittest.main()