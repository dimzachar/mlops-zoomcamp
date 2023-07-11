All files on main folder are final. Replace with _q# for individual questions.

## Q1. Refactoring

- rename batch_q1.py to batch.py and move to main folder
- Run python batch.py 2022 02 after pipenv shell

## Q2. Installing pytest

- Both of the above options are correct

## Q3. Writing first unit test

- rename batch_q3.py to batch.py and move to main folder
- Run pytest -s tests

How many rows should be there in the expected dataframe?
- 3


## Q4. Mocking S3 with Localstack 

- docker-compose up -d

- aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration
- aws --endpoint-url=http://localhost:4566 s3 ls


In both cases we should adjust commands for localstack. Which option do we need to use for such purposes?

- `--endpoint-url`

## Make input and output paths configurable


```bash
export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
```

## Q5. Creating test data

- Copy and rename batch_q5.py and integration_test_q5.py

```bash
export S3_ENDPOINT_URL=http://localhost:4566
```
- Run python integration_test.py
- aws --endpoint-url=http://localhost:4566 s3 ls s3://nyc-duration/in/

What's the size of the file?

- 3667


## Q6. Finish the integration test

- Copy and rename batch_q6.py and integration_test_q6.py
- Run python integration_test.py

What's the sum of predicted durations for the test dataframe?

- 31.51

## Running the test (ungraded)

- docker-compose down
- chmod +x integration_test.sh
- Run ./integration_test.sh


## Submit the results

* Submit your results here: https://forms.gle/vi7k972SKLmpwohG8
* It's possible that your answers won't match exactly. If it's the case, select the closest one.
* You can submit your answers multiple times. In this case, the last submission will be used for scoring.

## Deadline

The deadline for submitting is 16 July (Sunday) 23:00 CEST. After that, the form will be closed.
