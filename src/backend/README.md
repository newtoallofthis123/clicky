# Routes

## /add \[POST\]

This function takes in the patient's information from a POST request and stores it in the patient_info dictionary.

The patient_info dictionary contains the following information:

1. name
2. age
3. gender
4. problems
5. diagnosis
6. conditions
7. description
8. mediciness
9. status
10. doctor
11. info (phone, email and address)
12. time
13. hash
14. key
    The add_to_db() function is then called and the patient_info dictionary is passed as an argument. The function then returns the patient_info dictionary.