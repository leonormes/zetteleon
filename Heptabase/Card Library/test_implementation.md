# test_implementation

Based on the previous analysis and the provided source code, there are several opportunities to enhance the test suite for Hutch-bunny, particularly in the area of result modifiers. Here's a detailed review of the test implementation and suggested code changes, focusing on `test_return.py` and `test_demographics_distribution_query.py` where result modifiers are primarily tested, and `core/obfuscation.py` where the result modifiers are defined and used.

## Detailed Review of Existing Test Implementation

1. **`test_return.py`:**

- **`test_solve_availability_count_matches`**: This test verifies that the count returned by an Availability Query matches the expected count. It does so by running a query against a test database and asserting that the result matches a pre-defined value. The test implicitly uses environment variables, such as `LOW_NUMBER_SUPPRESSION_THRESHOLD` and `ROUNDING_TARGET`, but does not test various values of these directly

- **Limitations**: While this test confirms core functionality, it does not explicitly test edge cases, different database backends, or error handling related to the result modifiers

1. **`test_demographics_distribution_query.py`**:

- These tests check that Hutch-bunny can handle Distribution Queries for demographic data. They verify the format and content of the generated distribution results. This includes the correct application of result modifiers, such as number suppression and rounding

- **Limitations**: Similar to `test_return.py`, these tests may not cover all edge cases and do not extensively test error handling or the interaction of multiple modifiers. The test data and query logic could be more varied to cover a wider range of scenarios.

1. **`core/obfuscation.py`**:

- **`get_result_modifiers`**: This function is responsible for retrieving and applying the result modifiers based on environment variables. It uses `LOW_NUMBER_SUPPRESSION_THRESHOLD` and `ROUNDING_TARGET` and should be more explicitly tested to ensure correct behaviour based on different configurations.

- **`suppress_low_numbers`**: This function applies low number suppression logic. The logic should be tested for all different thresholds and against all data types.

- **`round_numbers`**: This function applies rounding logic. The logic should be tested for all different rounding targets and against all data types.

## Suggested Code Changes and Additional Tests

Based on the analysis, here are some specific code changes and additions to the tests that could be implemented to improve the quality and coverage:

1. **Explicit Environment Variable Testing**

- **Problem**: The existing tests use environment variables implicitly but do not verify how different values of these environment variables impact result modifiers.

- **Solution**: Create dedicated tests in both `test_return.py` and `test_demographics_distribution_query.py` that explicitly set and test different values for `LOW_NUMBER_SUPPRESSION_THRESHOLD` and `ROUNDING_TARGET`.

- **Code Changes:**

   - Modify existing tests or create new test functions that use `os.environ` to set the variables before running the query.

```sh
import os
from unittest import TestCase

class TestResultModifiers(TestCase):
def test_suppression_threshold_5(self):
    os.environ['LOW_NUMBER_SUPPRESSION_THRESHOLD'] = '5'
    # Run query that should return less than 5, assert it is suppressed to 0

def test_rounding_target_10(self):
    os.environ['ROUNDING_TARGET'] = '10'
    # Run query that should be rounded, assert result is rounded to nearest 10
```

1. **Edge Case Testing**

- **Problem**: Current tests don't specifically target edge cases such as queries that return no results, results that are equal to the threshold, or very large numbers.

- **Solution**: Add new tests that focus on specific edge cases by creating test cases to address each of the points identified in the previous response.

- **Code Changes**

   - Add new test functions in `test_return.py` to check the following cases:

      - Queries that return no results.

      - Queries that return results equal to the suppression threshold, such as a value of 5 if the threshold is 5, and ensure it is suppressed to 0.

      - Queries that return results with values at the rounding boundary, ensuring the result is correctly rounded. For example, if the rounding target is 10, ensure the value 15 is rounded to 20.

      - Tests to verify the behaviour when the `LOW_NUMBER_SUPPRESSION_THRESHOLD` or `ROUNDING_TARGET` is zero, negative, or invalid, such as non integer values like "abc".

1. **Database Backend Testing:**

- **Problem**: The existing tests do not cover multiple database backends. Hutch-bunny is expected to also support Trino

- **Solution**: Modify the test setup to include testing with Trino in addition to PostgreSQL. This may require setting up a testing environment for Trino and modifying test database connection logic.

- **Code Changes**:

   - Implement a way to configure the tests with different database connection parameters through environment variables or a configuration file.

   - Add test cases that use Trino connection parameters.

1. **Error Handling**

- **Problem**: The tests do not explicitly test how errors are handled by result modifiers, particularly in the function `get_result_modifiers` in `obfuscation.py`, that might occur during configuration or application of result modifiers.

- **Solution**: Create tests that intentionally use invalid configurations to verify that appropriate errors are logged or raised.

- **Code Changes:**

   - Modify the `get_result_modifiers` method in `core/obfuscation.py` to raise exceptions when invalid values are encountered (like non-integers or negative numbers).

   - Add test cases in `test_return.py` and `test_demographics_distribution_query.py` to verify that such errors are correctly raised.

   - Add test cases to verify correct logging if exceptions are not raised, but logged instead.

1. **Performance Testing**

- **Problem**: There are currently no tests to assess the performance impact of result modifiers.

- **Solution**: Develop performance tests that measure the execution time of queries with and without result modifiers, and against datasets of different sizes.

- **Code Changes**:

   - Create a new script (e.g., `test_performance.py`) that includes tests to measure the execution time of queries with result modifiers.

   - Use `timeit` or similar to measure performance of queries with and without filters.

   - Track resource consumption as well as execution time to identify potential bottlenecks.

1. **Filter Combination Testing:**

- **Problem:** Tests do not explicitly test the interaction between low number suppression and rounding to ensure they are applied in the correct sequence.

- **Solution:** Implement a new test that specifically checks if suppression takes precedence when both are enabled.

- **Code Changes:**

   - Create a test function that configures both `LOW_NUMBER_SUPPRESSION_THRESHOLD` and `ROUNDING_TARGET`, with values set such that the correct filter order can be validated.

   - Assert that the suppression is applied first, so a number under the threshold is suppressed to zero, even if it is on the rounding boundary.

1. **Automated Test Data Generation**

- **Problem**: The existing tests rely on a static test database, which may not fully cover all edge cases and scenarios.

- **Solution**: Implement a mechanism to generate test data dynamically, with edge cases and varying data volumes.

- **Code Changes**:

   - Create a function that can generate a test database with different scenarios and varying number of data records.

   - Modify the test setup to call this function before tests are run, ensuring new test datasets are generated.

1. **Integration Testing**

- **Problem**: The tests do not fully verify the interaction of the result modifiers with other components of Hutch-bunny

- **Solution**: Develop integration tests that verify the interaction of the result modifiers with other components of Hutch-bunny, such as the database connection, query execution, and result packaging.

- **Code Changes**

   - Develop test cases to explicitly test the complete end-to-end query pipeline.

   - This can involve calling query executors with the result modifiers enabled, and ensuring the correct outputs are observed.

## Example Code Implementation

Here's a snippet illustrating a new test in `test_return.py` to address edge cases for suppression:

```sh
import os
from unittest import TestCase
from hutch_bunny.core.execute_query import execute_query

class TestResultModifiers(TestCase):

def test_suppression_threshold_edge_case(self):
    os.environ['LOW_NUMBER_SUPPRESSION_THRESHOLD'] = '5'
    query = {
        "analysis": "availability",
        "filters": {},
    }
    result = execute_query(query)
    self.assertEqual(result['count'], 0) # assert value suppressed to 0
```

This test explicitly sets the suppression threshold and ensures that when the result is equal to this threshold, it is correctly suppressed to zero.

Here's an example of a test to confirm proper behaviour if the environment variable is not an integer:

```sh
import os
from unittest import TestCase
from hutch_bunny.core.obfuscation import get_result_modifiers

class TestObfuscation(TestCase):
def test_invalid_suppression_threshold(self):
    os.environ['LOW_NUMBER_SUPPRESSION_THRESHOLD'] = 'abc'
    with self.assertRaises(ValueError):
          get_result_modifiers() # assert error is raised
```

This test explicitly sets the suppression threshold to an invalid value, and asserts that a ValueError is raised as expected.