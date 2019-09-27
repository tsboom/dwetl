# WIP - Work-In-Progress

## Introduction

This document provided information about the "wip" branch, which contains some
work-in-progress code that might be useful in the future.

This document should _not_ be added to the main repository, it is strictly
informational for the changes in this branch.

The changes in this branch are initial "sketches" of the following:

1) Loading "stage 1" tables into "stage 2" tables

2) A proof-of-concept of showing that a "data quality" object can use be created
fro JSON information from the Excel spreadsheet, using currying/partial
functions to validate a given input.

**Note:** These changes have not been extensively tested, and so are likely not
suitable AS-IS for production use.
 
## Stage 1 to Stage 2 Loading

The following files provide the "sketch" of loading a Stage 1 table into a
Stage 2 table.

* load_stage_2.py
* dwetl/processor/copy_stage1_to_stage2.py
* tests/processor/test_copy_stage1_to_stage2.py

These files demonstrate copying the following tables:

* 'dw_stg_1_mai01_z00' to 'dw_stg_2_bib_rec_z00'
*  'dw_stg_1_mai50_z30' to 'dw_stg_2_lbry_item_z30'

Assuming that the "Stage 1" tables have been populated, the script can be run
using:

```
> python load_stage_2 <PROCESSING_CYCLE_ID>
```

where \<PROCESSING_CYCLE_ID> is the processing cycle id used to load the
Stage 1 tables. For example, if the processing cycle id is "1", the command
would be:

```
> python load_stage_2 1
```

The majority of the work is done by the "CopyStage1ToStage2" class in the
"dwetl/processor/copy_stage1_to_stage2.py" file.

## Data Quality Object Proof-of-Concept

The following files provide a basic proof-of-concept of creating a object
from the "data quality" JSON stanza of the Excel spreadsheet:

* data_quality_info.py
* tests/test_data_quality_info.py

The "DataQuality" class in the "data_quality_info.py" demonstrates that it is
possible to take the "data_quality" stanza from one of the JSON files in
the "table_config" directory, and use it to construct an object that can
perform the validation using the "specific_dq_function" and
"specific_dq_function_param_1" values specified in the stanza.

The class uses currying (also known as "partial application") to construct a
new object that uses the "specific_dq_function" and
"specific_dq_function_param_1" (if any) to perform a validation via the
"validate" method.

Note: Python has "functools.partial, which would have been used, except that
it requires that the functions used in "specific_dq_function" have their
parameters arranged so that the "input" parameter is last, instead of first.

The "tests/test_data_quality_info.py" shows some example of validating input
based on JSON stanzas.
