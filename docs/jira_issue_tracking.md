# Jira Issue Tracking

A Google Sheet which lays out the detailed status of Jira tasks to complete DWETL is located here: [DWETL Issues Overview](https://docs.google.com/spreadsheets/d/1R_MjQDrjYeBOVkO-wmQJ1lhYwyTagJ9YksCYtXauvew/edit#gid=0). This Sheet is the most helpful to see all of the remaining issues of DWETL and the status of each dimension in the process. 

During development, we are focusing on the Bibliographic Record Dimension, but other dimensions are being added through the end of the transformations step. 

**High level progress tracking:** 

| Step                                          | Status                                                       |
| --------------------------------------------- | ------------------------------------------------------------ |
| Error handling                                | Done for any database errors or DQ check errors that come up. Need more testing on different dimensions. More error writing may need to happen for other kinds of errors so that this table is more helpful for users. |
| Logging and report email                      | Done                                                         |
| Processed data handling. Move to `processed`. | Done. Needs tests.                                           |
| Load stage 1 tables                           | Done but needs testing for other dimensions besides the Bib_rec_dimension |
| Load stage 2 tables                           | Done but needs testing for other dimensions besides the Bib_rec_dimension |
| Preprocessing                                 | Done                                                         |
| Data Quality Checks                           | Done, but needs more specific dq checks for other dimensions besides the Bib_rec_dimension |
| Transformations                               | Done, but needs specific transform functions tested and implemented for other dimensions besides the Bib_rec_dimension |
| Load stage 3 tables                           | In progress                                                  |
| Z00, Z13, Z13u Record Alignment               | In review                                                    |
| Load Dimension table                          |                                                              |
| Load new records to the reporting database    |                                                              |





**Old issues:**

- [LIBILS-371](https://issues.umd.edu/browse/LIBILS-371)Set up test database for ETL development

- LIBILS-370 Refactor stage 1 file-equivalent load (Step 1) CREATED ALREADY

- LIBILS-375 Import one-to-one stage 1 tables to stage 2 tables (in_ values) (From Step 2) 

- LIBILS-376 Write tests for the import of bib_rec stage 1 tables to stage 2 tables (From Step 2)

- LIBILS-377 Import mai50 z35 library item event stage 1 table to stage 2 table (From Step 2)

- LIBILS-378 Import mai01 z00 and z39 Field stage 1 tables to bib_rec_z00_field stage 2 table (From Step 2)

- LIBILS-379 Develop and test process of getting z35 circulation data into z30 (From Step 4)

  

