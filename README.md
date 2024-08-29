# AI Call Agent

## Description

## Functional Requirements
1. Read CSV file (see **Data Section** for content and format) iteratively to obtain calls to be processed.
2. Format AI prompt using the current call record and place call (See **Configuration Section** for complete details ). <p>
If the call recipient can not be reached, retry the number of times specified in the overall configuration file. 
3. Write the results of the call to an output file indicating one of the following results:
    - Call successful
    - Recipient could not be reached. Call retry scheduled.
    - Recipient could not be reached
## Setup 
Setup for the application can be accomplished by using the information here.

### Programming language
Python
### Calling API
- [Bland Home](https://www.bland.ai/)
- [Bland API](https://docs.bland.ai/api-v1/post/calls)

### Environment
- Environment variables: [^1]

    ```
    BLANDAI_AUTH_KEY=<YOUR_BLANDAI_AUTH_KEY>
    BLANDAI_PHONE_NUMBER=<YOUR MOBIL PHONE NUMBER>

    ```
[^1]: *Setting items like API keys and phone numbers as environment variables maintain privacy for the purposes of this project insomuch as they are not exposed in code or configuration files. Depending on your OS, you can set these in your environment shell scripts or as a volitile setting at the command line prior to agent execution.*

### Configuration
Call API. 
- Call API  configuration allows for setting parameters including:
    -  Caller voice selection
        - Interuption threshold
        - LLM model
            - Base
            - Enhanced
            - Turbo
        -  Transfer phone number
        - Answered_By Enabled
        - Start time
            - When to begin prcessing the file.
        - Record
            - Record the phone call if the recipient is reached
        - Max_duration
            - Set a maximum duration for the call in minutes.
        - Additional parameters (key-value pairs)
            - Parameters are key pieces of information you want your agent to know and never forget. For example, a key could be "reservation_time" and its corresponding value could be "8pm on August 21, 2023".
        - Prompt.
            - Prompt specific configuration allows for setting and tuning NLP call specific parameters including:
                - Task
                - Example (Few-Shot Learning)


## Data
There are two main data files:
1. Office Data <br>
Office List with transfer numbers. <br>
Office data will include:
    - Office Name
    - Dynamic transfer numbers

    **Example:**
    ```
    {
        "office_name": "xyz_clinic",
        "transfer_list": {
            "default": "+12223334444"
         }
    }
    ```
2. Call data <br>
Call Data for the application will include the following columns:
    - Recipient Office
    - Recipient Last Name
    - Recipient First Name
    - Recipient Phone Number

The office name from the Call data will be matched with the office name from the Office data.

Format:
The Office data and Call data will initially be defined as CSV files.

## Running the agent
To run the agent:
```
python caller_agent.py -mode=<runmode> -row_num=<row_number>
```
runmode: 
- one 
    - single call. \<default\> 
- batch
    - batch mode.

row_num: (1 - default)
- \<integer\> 
    - ones (1) based row number from the  Call Data file. If the row does not exist, a user friendly message will be displayed.

    If the runmode is not specified, Row_num is ignored, even if specified.