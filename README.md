Make sure you have `Python >= 3.12` and `mysql-connector-python` package installed. If not, use `pip install mysql-connector-python` to install that package.

This is just my school project regarding my acquired knowledge of Python in my 2 years of learning in my school.
Feel free to improve it or whatever.

NOTE: I took some help from the internet to make the `formatting.py` for making it look nicer.

# ArrayMaxMin Program Flowchart

This flowchart explains the logic of the ArrayMaxMin program that finds the maximum and minimum values in an array of 10 numbers.

```mermaid
flowchart TD
    Start --> DeclareArray["Declare array arr of size 10"]
    DeclareArray --> DeclareVars["Declare variables i, max, min"]
    DeclareVars --> CreateScanner["Create Scanner object"]
    CreateScanner --> ShowPrompt["Display 'Enter 10 numbers:'"]
    ShowPrompt --> InitI["Initialize i = 0"]
    InitI --> CheckI{"Is i < 10?"}
    CheckI -- Yes --> ReadInput["Read arr[i] from user input"]
    ReadInput --> IncrementI["Increment i"]
    IncrementI --> CheckI
    CheckI -- No --> InitMaxMin["Initialize max = min = arr[0]"]
    InitMaxMin --> InitLoopI["Initialize i = 1"]
    InitLoopI --> CheckLoopI{"Is i < arr.length?"}
    CheckLoopI -- Yes --> CheckMax{"Is arr[i] > max?"}
    CheckMax -- Yes --> UpdateMax["max = arr[i]"]
    CheckMax -- No --> CheckMin{"Is arr[i] < min?"}
    UpdateMax --> CheckMin
    CheckMin -- Yes --> UpdateMin["min = arr[i]"]
    CheckMin -- No --> IncrementLoopI["Increment i"]
    UpdateMin --> IncrementLoopI
    IncrementLoopI --> CheckLoopI
    CheckLoopI -- No --> DisplayMax["Display 'Maximum number is: ' + max"]
    DisplayMax --> DisplayMin["Display 'Minimum number is: ' + min"]
    DisplayMin --> End
```

## Code Explanation

1. **Initialization**:
   - Create an integer array of size 10
   - Initialize variables for iteration and storing max/min values
   - Set up Scanner for user input

2. **Input Phase**:
   - Prompt user to enter 10 numbers
   - Read each number into the array using a loop

3. **Processing Phase**:
   - Assume the first element is both max and min
   - Iterate through the remaining elements
   - Update max if a larger element is found
   - Update min if a smaller element is found

4. **Output Phase**:
   - Display the maximum value
   - Display the minimum value
