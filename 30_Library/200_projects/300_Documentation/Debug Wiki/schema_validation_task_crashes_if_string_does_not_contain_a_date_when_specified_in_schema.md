---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:43Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: schema_validation_task_crashes_if_string_does_not_contain_a_date_when_specified_in_schema
type:
uid: 
updated: 
version:
---

## Schema Validation Task Crashes if String Does not Contain a Date when Specified in Schema

```sh
	
2024-11-12 20:29:33 validate-sql-dataset-template-d5nlm-validate-dataset-2045007817 anonymisation INFO Flattening schema {'DispensingID': {'identifier_type': 'DIRECT', 'data_type': 'STRING'}, 'DispensingDateTime': {'identifier_type': 'INDIRECT', 'data_type': 'DATE'}, 'Consultant': {'identifier_type': 'INDIRECT', 'data_type': 'STRING'}, 'Div': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}, 'Group': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}, 'DrugDescription': {'identifier_type': 'INDIRECT', 'data_type': 'STRING'}, 'QtyDispensed': {'identifier_type': 'NON_ID', 'data_type': 'FLOAT'}, 'DrugPackSize': {'identifier_type': 'NON_ID', 'data_type': 'FLOAT'}, 'DrugPackSizePrice': {'identifier_type': 'NON_ID', 'data_type': 'FLOAT'}, 'MedicationDispensedCost': {'identifier_type': 'NON_ID', 'data_type': 'FLOAT'}, 'DrugPackSizeTariffPrice': {'identifier_type': 'NON_ID', 'data_type': 'FLOAT'}, 'HighCostFlag': {'identifier_type': 'INDIRECT', 'data_type': 'STRING'}, 'NHSNumber': {'identifier_type': 'DIRECT', 'data_type': 'STRING'}, 'PTTitle': {'identifier_type': 'INDIRECT', 'data_type': 'STRING'}, 'PTSex': {'identifier_type': 'INDIRECT', 'data_type': 'STRING'}, 'DOB': {'identifier_type': 'INDIRECT', 'data_type': 'BIRTH_DATE'}, 'HIVFlag': {'identifier_type': 'INDIRECT', 'data_type': 'STRING'}, 'GenericName': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}, 'PAS_Flag': {'identifier_type': 'INDIRECT', 'data_type': 'STRING'}, 'Drug_tariff_price_for_item': {'identifier_type': 'NON_ID', 'data_type': 'FLOAT'}, 'Prescriber': {'identifier_type': 'INDIRECT', 'data_type': 'STRING'}, 'Specialty': {'identifier_type': 'INDIRECT', 'data_type': 'STRING'}, 'WARD': {'identifier_type': 'INDIRECT', 'data_type': 'STRING'}, 'AMPP': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}, 'AMP': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}, 'VMPP': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}, 'VMP': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}, 'Dose': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}, 'Warnings': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}, 'Generic_or_brand': {'identifier_type': 'INDIRECT', 'data_type': 'STRING'}, 'Form': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}, 'Unknown': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}, 'Blueteq': {'identifier_type': 'INDIRECT', 'data_type': 'STRING'}, 'Data_LogDate': {'identifier_type': 'INDIRECT', 'data_type': 'DATE'}, 'count': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}, 'follow_the_record': {'identifier_type': 'NON_ID', 'data_type': 'STRING'}}
2024-11-12 20:29:47.264	
Traceback (most recent call last):
2024-11-12 20:29:47.264	
  File "/app/.venv/bin/dataset_validator", line 8, in <module>
2024-11-12 20:29:47.264	
    sys.exit(run_as_script())
2024-11-12 20:29:47.264	
  File "/app/.venv/lib/python3.10/site-packages/src/cli/dataset_validation.py", line 41, in run_as_script
2024-11-12 20:29:47.264	
    main(args)
2024-11-12 20:29:47.264	
  File "/app/.venv/lib/python3.10/site-packages/src/cli/dataset_validation.py", line 26, in main
2024-11-12 20:29:47.264	
    dataset_validator.validate()
2024-11-12 20:29:47.264	
  File "/app/.venv/lib/python3.10/site-packages/src/data_validation/dataset_validator.py", line 30, in validate
2024-11-12 20:29:47.264	
    validator_instance.validate_column()
2024-11-12 20:29:47.264	
  File "/app/.venv/lib/python3.10/site-packages/src/data_validation/abstract_column_validator.py", line 39, in validate_column
2024-11-12 20:29:47.264	
    self._add_to_errors_if_not_valid(data_point=row[self.column_name], row_number=int(str(idx))+1)
2024-11-12 20:29:47.264	
  File "/app/.venv/lib/python3.10/site-packages/src/data_validation/abstract_column_validator.py", line 65, in _add_to_errors_if_not_valid
2024-11-12 20:29:47.264	
    if not self.datapoint_validation(data_point):
2024-11-12 20:29:47.264	
  File "/app/.venv/lib/python3.10/site-packages/src/data_validation/abstract_column_validator.py", line 55, in datapoint_validation
2024-11-12 20:29:47.264	
    return self._validate_data_point(data_point)
2024-11-12 20:29:47.264	
  File "/app/.venv/lib/python3.10/site-packages/src/data_validation/column_validators/birth_date_validator.py", line 13, in _validate_data_point
2024-11-12 20:29:47.265	
    date = parse(data_point).replace(tzinfo=utc)
2024-11-12 20:29:47.265	
  File "/app/.venv/lib/python3.10/site-packages/dateutil/parser/_parser.py", line 1368, in parse
2024-11-12 20:29:47.265	
    return DEFAULTPARSER.parse(timestr, kwargs)
2024-11-12 20:29:47.265	
  File "/app/.venv/lib/python3.10/site-packages/dateutil/parser/_parser.py", line 646, in parse
2024-11-12 20:29:47.265	
    raise ParserError("String does not contain a date: %s", timestr)
2024-11-12 20:29:47.265	
dateutil.parser._parser.ParserError: String does not contain a date:
```

### ParserError in Birth Date Validation

Description:

The Birth Date Validator encountered an error while processing a dataset. The error arises when attempting to parse a value in the 'DOB' column that does not conform to a recognized date format. This issue occurred during the execution of the `validate_column` function within the `Birth_Date_Validator` class.

Relevant Code Snippet:

Python

```python
# ... within Birth_Date_Validator._validate_data_point
date = parse(data_point).replace(tzinfo=utc) 
```

Error Message:

```python
dateutil.parser._parser.ParserError: String does not contain a date: 
```

Cause:

The `dateutil.parser.parse` function is unable to interpret the data point encountered in the 'DOB' column as a valid date. This could be due to various reasons, including:

- Empty or missing value: The 'DOB' field for the record might be blank or missing.
- Incorrect format: The date might be provided in a format not recognized by the parser (e.g., 'DD-MM-YYYY' instead of 'YYYY-MM-DD').
- Invalid characters: The data point might contain non-date characters or extraneous whitespace.

Solution:

1. Data Cleansing: Before validation, implement a data cleansing step to:
    - Remove any leading or trailing whitespace from the 'DOB' column.
    - Handle missing values by either assigning a default date or excluding the record from processing.
2. Format Standardization: Ensure all dates in the 'DOB' column adhere to a consistent, supported format. Consider using a dedicated date formatting library to preprocess the data.
3. Error Handling: Modify the `_validate_data_point` function to include error handling for `ParserError`. This could involve:
    - Logging the invalid data point and row number for further investigation.
    - Providing a more informative error message to the user.
    - Allowing the user to specify the expected date format as a parameter.

Related Information:

Note: The exact solution will depend on the specific data format and business requirements. Further analysis of the dataset and the invalid data point is recommended to determine the most appropriate course of action.
