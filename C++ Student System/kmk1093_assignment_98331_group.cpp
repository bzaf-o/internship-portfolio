#include <iostream>
#include <fstream>
#include <vector>
#include <limits>

using namespace std;

// Functions used in the code 👇
// Counts how many student records are in data.txt
int countLines(const string& filename) {
    ifstream inputFile(filename); //Open file
    if (!inputFile.is_open()) { //Checks if file is open/exists, if not then return an error
        cerr << "Error opening file: " << filename << endl;
        return -1; // Error
    }

    // Proceed to increment lineCount if file is indeed open/exists
    int lineCount = 0;
    string line;
    while (getline(inputFile, line)) {
        lineCount++;
    }

    inputFile.close();
    return lineCount;
}

// Searches for a specific matric number and returns it
string searchMatricNo(vector<string> errors) {
    errors.clear(); //Ensures that any error messages from previous operations are deleted
    string x;
    cin >> x;
    cout << endl;
    return x;
}

// Display errors
void displayErrors(vector<string>& errors) {
    cout << "\n##################  Error occurred! ##################\n\n";
    // for loop to print the errors (e.g., invalid c++ marks, invalid matric number)
        for (int i = 0; i < errors.size(); i++) {
            cout << errors[i];
        }
}

// Validates choice for the prompt at the end of an operation which asks user if they want to repeat the operation or go back to the main menu
bool validReturnChoice(int x) {
    // x is the number that the user enters. 1 is to repeat the operation, 2 is to return to main menu
    if (x == 1 || x == 2) {
        return true;
        // Input is valid, returns true
    } else {
        cout << "\n####################################\n\nError: Invalid choice, please try again.\n";
        return false;
        // Input is not 1 or 2, returns false
    }
}

// Prompt user to repeat operation or go back to main menu
int returnOrAgain(int option) {
    int choice;
    bool validchoice = false;

    // While loop to repeat this function if the user enters a different number from 1 (repeat operation) or 2 (return to main menu)
    while (!validchoice) {
        cout << endl << "####################################\n\n";
        switch (option) {
            case 1:
                // Output for adding record
                cout << "Do you want to add another record or return to the main menu?\n\n1. Add another record\n2. Return to main menu\n\n>> ";
                cin >> choice;

                // Checks validity of choice
                validchoice = validReturnChoice(choice);

                break;

            case 2:
                // Output for viewing a record
                cout << "Do you want to view another record or return to the main menu?\n\n1. View another record\n2. Return to main menu\n\n>> ";
                cin >> choice;

                // Checks validity of choice
                validchoice = validReturnChoice(choice);
                break;

            case 3:
                // Output for editing a record
                cout << "Do you want to edit another record or return to the main menu?\n\n1. Edit another record\n2. Return to main menu\n\n>> ";
                cin >> choice;

                // Checks validity of choice
                validchoice = validReturnChoice(choice);
                break;

            case 4:
                // Output for deleting a record
                cout << "Do you want to find another record to delete or return to the main menu?\n\n1. Find another record to delete\n2. Return to main menu\n\n>> ";
                cin >> choice;

                // Checks validity of choice
                validchoice = validReturnChoice(choice);
                break;

            default:
                // Invalid choice (never happens because value of choice is determined by programmer)
                cout << "\n\n#################################### Invalid choice, please try again.\n\n";
                break;
        }
    }

    cout << endl;
    return choice;
}

// Checks the range of each mark, gives an error indicating which subject is invalid if there are any
bool rangeCheck(int x, int n, vector<string>& errors) {
    string subject;
    switch (n) { //Determines which subject will be printed in the error message
    case 1:
        subject = "C++";
        break;

    case 2:
        subject = "Psychology";
        break;
    
    case 3:
        subject = "Discrete Math";
        break;

    case 4:
        subject = "Cognitive Science";
        break;
    
    default:
        return false;
    }
    if (x < 0 || x > 100) {
        string error_ = "Error: Marks for " + subject + " should be between 0 and 100\n";
        errors.push_back(error_); //Adds the error message into the error vector
        return false;
    } else 
        return true;
}
// Prompt user to enter first name, matric number and marks for 4 subjects
void newRecord(string& name_, string& matricno_, int& mark1_, int& mark2_, int& mark3_, int& mark4_) {
    cout << "\nEnter student's first name:\n>> ";
    cin >> name_;

    cout << "\nEnter student matric number:\n>> ";
    cin >> matricno_;

    cout << "\nEnter marks for C++:\n>> ";
    cin >> mark1_;

    cout << "\nEnter marks for Psychology:\n>> ";
    cin >> mark2_;

    cout << "\nEnter marks for Discrete Math:\n>> ";
    cin >> mark3_;

    cout << "\nEnter marks for Cognitive Science:\n>> ";
    cin >> mark4_;
}

// Checks whether the matric number (not a negative number, does not previously exist) and marks (within range of 0 - 100) are valid 
bool checkValidity(string matricno_, int mark1_, int mark2_, int mark3_, int mark4_,vector<string>& errors, int type) {
    // int type: 1 = using in entering a new record, so it will include checking if the record previously existed
    // int type: 2 = using in updating a record, so it will not include checking if the record previously existed (in case user wants to update other information, just not the matric number)

    // Matric number checks
        bool goodmatricno = true;
        string error_;

        // Check if it's a negative number
        if (matricno_[0] == '-') {
            error_ = "Error: Matric number is negative, or contains a negative sign.\n";
            errors.push_back(error_); //Adds the error message into the error vector
            goodmatricno = false;
        } 

        if (type == 1) {
            // Check if matric number already exists in file
            ifstream inFile("data.txt");
            string existingMatricno;

            while (inFile >> existingMatricno) {
                if (existingMatricno == matricno_) {
                    error_ = "Error: Matric number already exists.\n";
                    errors.push_back(error_); //Adds the error message into the error vector
                    inFile.close();
                    goodmatricno = false;
                    break;
                }
            }
    inFile.close();
        }

    // Marks checks
        // Check if the marks entered are between 0 and 100 for each subject

        bool goodmark1 = rangeCheck(mark1_, 1, errors);
        bool goodmark2 = rangeCheck(mark2_, 2, errors);
        bool goodmark3 = rangeCheck(mark3_, 3, errors);
        bool goodmark4 = rangeCheck(mark4_, 4, errors);
    
    // If marks and matric numbers are all good/valid, then all entries are proven to be valid
    if (goodmark1 && goodmark2 && goodmark3 && goodmark4 && goodmatricno) {
        return true;
    } else {
        return false;
    }
}

// Converts marks into grades
    /*
    A = 80 - 100
    B = 60 - 79
    C = 50 - 59
    D = 40 - 49
    E = 30 - 39
    F = 0 - 29
    */

char convertGrades(int x) {
    if (x > 79) {
        return 'A';
    } else if (x > 59) {
        return 'B';
    } else if (x > 49) {
        return 'C';
    } else if (x > 39) {
        return 'D';
    } else if (x > 29) {
        return 'E';
    } else {
        return 'F';
    }
}

// Entering records into the file
void enterRecords(const string& name, const string& matricno, int mark1, char grade1,
                int mark2, char grade2, int mark3, char grade3, int mark4, char grade4) {
    ofstream outFile("data.txt", ios::app); // Open the file in append mode, so it will add a new record instead of overwriting previous ones

    if (outFile.is_open()) {
        // Write the records to the file in order of: matric number, name, C++ marks, C++ grades, and repeat for psychology, discrete math and cognitive science
        outFile << matricno << " " << name << " " << mark1 << " " << grade1 << " "
                << mark2 << " " << grade2 << " " << mark3 << " " << grade3 << " "
                << mark4 << " " << grade4 << "\n";

        outFile.close(); // Close the file after writing
    } else {
        // If data.txt doesn't exist/can't be opened
        cerr << "Error: Unable to open the file for writing.\n";
    }
}

// Display a record
void displayRecord(const string& findmatricno) {
ifstream inputFile("data.txt");

if (!inputFile.is_open()) { //Check if file exists/is open
    cerr << "Error opening file!\n";
    return;
}

// Temporary variables for each component of student records
string name, matricno;
char grade1, grade2, grade3, grade4;
int mark1, mark2, mark3, mark4;

bool found = false; //Check for when program has found the same matric number as the user wants to display

while (inputFile >> matricno >> name >> mark1 >> grade1 >> mark2 >> grade2 >> mark3 >> grade3 >> mark4 >> grade4) {
    if (matricno == findmatricno) {
        found = true;

        // Display record of matching matric number
        cout << "Name: " << name << "\nMatric number: " << matricno
            << "\nC++ grades: " << mark1 << " (" << grade1 << ")\nPsychology grades: " << mark2 << " (" << grade2 << ")"
            << "\nDiscrete Math grades: " << mark3 << " (" << grade3 << ")\nCognitive Science grades: " << mark4 << " (" << grade4 << ")\n";
        
        return;
    }
}

if (found == false) { //If matric number isn't found in the file, then output this error
    cerr << "Error: Matric number not found.\n";
}

inputFile.close();
}

// Searches for whether or not a record exists in the data.txt file
bool searchRecord(string findmatricno) {
    // Open file to search for matric number
    ifstream inputFile("data.txt");

    // Check if file doesn't exist, in which it will return as false
    if (!inputFile.is_open()) {
        cerr << "Error opening file.\n";
        return false;
    }

    // If file does exist, then variables that will store info extracted from file
    string matricnoFromFile;
    string student;
    float marks1, marks2, marks3, marks4;
    char grade1, grade2, grade3, grade4;
    bool found = false;

    // Loop through the file to find the matric number that user is looking for
    while (inputFile >> matricnoFromFile) {
        inputFile >> student >> marks1 >> grade1 >> marks2 >> grade2 >> marks3 >> grade3 >> marks4 >> grade4;

        // Check if the current matricno matches the searchmatricno
        if (matricnoFromFile == findmatricno) {
            cout << "#################################### Matric number found in the file! ####################################\n";
            found = true;
            break;
        }
    }

    if (!found) {
        cerr << "Error: Matric number you entered doesn't exist.\n";
    }
    inputFile.close();
    return found;
}

// Updates marks when editing records
int updateMarks(const string& input, int newmark, int mark) {
    if (!input.empty()) { //Checks if new mark that user entered is empty
        newmark = stoi(input);
        return newmark;
    } else {
        // Reset cin and ignores any remaining characters in the input buffer up to a newline character ('\n') This helps in discarding invalid input and preparing for a fresh input
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        return mark;
    }
}

// Reads file to update/edit records
void updateRecord(string matricno_find, vector<string>& errors) {
        ifstream inputFile("data.txt");
        ofstream tempFile("temp.txt"); //temporary file to hold new/edited values

        if (inputFile.is_open() && tempFile.is_open()) {
            // variables to hold info from file
            string newName, name, newMatricno, matricno, input;
            char grade1, grade2, grade3, grade4;
            int newMark1, newMark2, newMark3, newMark4, mark1, mark2, mark3, mark4;

            bool found = false, validmarks = false;

            // Loop through file to find line with the matric number that user inputs
            while (inputFile >> matricno >> name >> mark1 >> grade1 >> mark2 >> grade2 >> mark3 >> grade3 >> mark4 >> grade4) {
                if (matricno == matricno_find) { //Record that user is looking for has been found
                    found = true;

                    // Display current record
                    cout << "\n#################################### Current Record ####################################\n\n";
                    displayRecord(matricno_find);

                    // Prompt user to update information
                    cout << "\n#################################### Update Records ####################################\n\n";
                    cout << "Enter new name (Press Enter to keep the existing value):\n>> ";
                    cin.ignore(); // Ignore newline character from previous input
                    getline(cin, newName);
                    if (newName.empty())
                        newName = name;

                    cout << "\nEnter new matric number (Press Enter to keep the existing value):\n>> ";
                    getline(cin, newMatricno);
                    if (newMatricno.empty())
                        newMatricno = matricno;

                    cout << "\nEnter new marks for C++ (Enter current value to keep the existing value: " << mark1 << ")\n>> ";
                    cin >> input;
                    newMark1 = updateMarks(input, newMark1, mark1); //Calls function that checks whether the input is the same as the existing value or a new one

                    cout << "\nEnter new marks for Psychology (Enter current value to keep the existing value: " << mark2 << ")\n>> ";
                    cin >> input;
                    newMark2 = updateMarks(input, newMark2, mark2); //Calls function that checks whether the input is the same as the existing value or a new one

                    cout << "\nEnter new marks for Discrete Math (Enter current value to keep the existing value: " << mark3 << ")\n>> ";
                    cin >> input;
                    newMark3 = updateMarks(input, newMark3, mark3); //Calls function that checks whether the input is the same as the existing value or a new one

                    cout << "\nEnter new marks for Cognitive Science (Enter current value to keep the existing value: " << mark4 << ")\n>> ";
                    cin >> input;
                    newMark4 = updateMarks(input, newMark4, mark4); //Calls function that checks whether the input is the same as the existing value or a new one

                    // Checks whether the new matric number and name are valid, and tells the function that we are not checking for whether or not the matric number already exists (by entering 2)
                    validmarks = checkValidity(newMatricno, newMark1, newMark2, newMark3, newMark4, errors, 2);

                    if (validmarks == true) { //Marks and matric number are all good to go, will only update the file if all inputs are valid
                        // Write the updated record to the temporary file
                        tempFile << newMatricno << " " << newName << " " << newMark1 << " " << convertGrades(newMark1) << " "
                                << newMark2 << " " << convertGrades(newMark2) << " " << newMark3 << " " << convertGrades(newMark3) << " "
                                << newMark4 << " " << convertGrades(newMark4) << "\n";

                        cout << "\nRecord updated successfully!\n";
                    } else { //Marks and/or matric number aren't valid
                        found = false;
                        displayErrors(errors);
                    }
                } else { //
                    // Write unchanged records to the temporary file
                    tempFile << matricno << " " << name << " " << mark1 << " " << grade1 << " "
                            << mark2 << " " << grade2 << " " << mark3 << " " << grade3 << " "
                            << mark4 << " " << grade4 << "\n";
                }
            }

            // Close files before removing and renaming
            inputFile.close();
            tempFile.close();

            // Replace the original file with the temporary file only if all inputs are valid
            if (found && validmarks) {
                remove("data.txt");
                rename("temp.txt", "data.txt");
            }
        } else {
            cerr << "Error: Unable to open files for reading/writing.\n";
        }
}

//Function to find and delete a record
void deleteRecord(string matricdelete) {
    ifstream inputFile("data.txt");
    ofstream tempFile("temp.txt");

    if (inputFile.is_open() && tempFile.is_open()) {
        // Variables to hold info from file
        string matricno, name;
        char grade1, grade2, grade3, grade4;
        int mark1, mark2, mark3, mark4;

        while (inputFile >> matricno >> name >> mark1 >> grade1 >> mark2 >> grade2 >> mark3 >> grade3 >> mark4 >> grade4) {
            if (matricno == matricdelete) {
                // Found student record that user wants to delete
                continue;
            }

            // Write unchanged records to the temporary file
            tempFile << matricno << " " << name << " " << mark1 << " " << grade1 << " "
                    << mark2 << " " << grade2 << " " << mark3 << " " << grade3 << " "
                    << mark4 << " " << grade4 << "\n";
        }

        cout << "Record with matric number " << matricdelete << " deleted successfully!\n";

        // Close files before removing and renaming
        inputFile.close();
        tempFile.close();

        // Replace the original file with the temporary file
        remove("data.txt");
        rename("temp.txt", "data.txt");
    } else {
        cout << "Error: Unable to open files for reading/writing.\n";
    }
}

//Function to display all records so far
void displayAll() {
ifstream inputFile("data.txt");

if (inputFile.is_open()) {
    string name, matricno, grade1, grade2, grade3, grade4;
    int mark1, mark2, mark3, mark4;

    while (inputFile >> matricno >> name >> mark1 >> grade1 >> mark2 >> grade2 >> mark3 >> grade3 >> mark4 >> grade4) {
        cout << "\nName: " << name << "\nMatric number: " << matricno
            << "\nC++ grades: " << mark1 << " (" << grade1 << ")\nPsychology grades: " << mark2 << " (" << grade2 << ")"
            << "\nDiscrete Math grades: " << mark3 << " (" << grade3 << ")\nCognitive Science grades: " << mark4 << " (" << grade4 << ")\n";
    }

    inputFile.close();
} else {
    cout << "Error: Unable to open the file for reading.\n";
}
}

int main () {
    // Variable and vector declaration
        // Student records
        vector <string> name, matricno;
        vector <int> mark1, mark2, mark3, mark4; //C++, Psychology, Discrete Math, Cognitive Science
        vector <char> grade1, grade2, grade3, grade4;

        // Temporary student records
        string name_, matricno_;
        int mark1_, mark2_, mark3_, mark4_;
        char grade1_, grade2_, grade3_, grade4_;

        // Misc
        int choice, cont;
        vector <string> errors;
        string data = "data.txt";
        bool recordexist;
        string matricno_find;

    /* Main Menu (based on number user enters)
    1 - Enter new record
    2 - Find and display existing record
    3 - Find and update a record
    4 - Find and delete a record
    5 - Display all records
    6 - Exit program
    */

   mainmenu:
   while (true) {
   cout << "\n################## Student Information System ##################\n\n" << "Welcome to the Student Information System! Please enter the corresponding number for which operation you'd like to do.\n\n" << "1. Enter new student record\n2. Search for an existing record and display it\n3. Search for an existing record and update it\n4. Search for a student record and delete it\n5. Display all current student records\n6. Exit the program\n\n>> ";
   cin >> choice;
   cout << endl;

    if (choice == 1) { //Enters new student records [Tiffany]
        newrecord:
        errors.clear(); //Clears errors from previous operations
        // Prompt user to enter new records
        cout << "################## New Student Record ##################\n";
        newRecord(name_, matricno_, mark1_, mark2_, mark3_, mark4_);

        // Check if user input (marks and matric numbers specifically) are valid
        bool valid = checkValidity(matricno_, mark1_, mark2_, mark3_, mark4_, errors, 1);

        // Once passed validity check, convert marks to grades and put all records into a new line on the file
        if (valid == true) {
            // Converts marks into grades
            grade1_ = convertGrades(mark1_);
            grade2_ = convertGrades(mark2_);
            grade3_ = convertGrades(mark3_);
            grade4_ = convertGrades(mark4_);

            // Enter the temporary records into the file to become permanent records
            enterRecords(name_, matricno_, mark1_, grade1_, mark2_, grade2_, mark3_, grade3_, mark4_, grade4_);

            // Display the recently added record and return to menu
            cout << "\n################## Added Record Successfully! ##################\n\n";
            displayRecord(matricno_);
        } else {
            // Call function to display errors
            displayErrors(errors);
        }
        // Function to ask whether want to add another record or return to main menu
        cont = returnOrAgain(1);
        if (cont == 1)
            goto newrecord;
        else
            goto mainmenu;

    } else if (choice == 2) { //Display an existing student's records [Marie]
        display:
        cout << "################## Display Student Record ##################";
        
        // Ask for matric number to identify which record to edit
        cout << "\n\nEnter matric number of student record to display:\n\n>> ";
        matricno_find = searchMatricNo(errors);

        // Check if matric number exists in file records
        bool recordexists = searchRecord(matricno_find);

        if (recordexists) {
            // If found, display all the info from that line.
            cout << endl;
            displayRecord(matricno_find);
        } 
        // If not found, there will be an error message from the searchRecord function

        // Ask if user wants to find another matric number or go back to main menu
        cont = returnOrAgain(2);
        if (cont == 1)
            goto display;
        else
            goto mainmenu;

    } else if (choice == 3) { //Update/edit an existing student's records [Nazlifah]
        update:

        cout << "################## Update Student Record ##################\n\n";

        // Ask for matric number to identify which record to edit
        cout << "Enter matric number of student record to edit:\n\n>> ";
        matricno_find = searchMatricNo(errors);

        // Check if matric number exists in the file data.txt
        bool recordexist = searchRecord(matricno_find);

        if (recordexist == true) {
            // If record exists, then prompt user to update the record information
            updateRecord(matricno_find, errors);

            if (errors.empty()) {
                // Display the newly edited information if there are no errors
                cout << endl;
                displayRecord(matricno_find);
            } else {
                // If there are errors, display this prompt after displaying the errors
                cout << "\nNo changes made. Edit this record again with valid values to make any changes.\n";
            }
        } else {
            cout << "";
        }

        // Prompt user to update another record or go back to the main menu
        cont = returnOrAgain(3);
        if (cont == 1)
            goto update;
        else
            goto mainmenu;

    } else if (choice == 4) { //Delete student record [Balqis]
        deleterecord:
        int del;
        cout << "\n################## Delete Student Record ##################\n\n";
        // Enter matricno to be found
        cout << "Enter matric number of student record to delete:\n\n>> ";
        matricno_find = searchMatricNo(errors);

        // Consume newline character from the input buffer
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        // Checks if record exists in file data.txt
        recordexist = searchRecord(matricno_find);

        if (recordexist) {
            // If found, display the record
            cout << "\nRecord found!\n\n";
            displayRecord(matricno_find);

            while (true) { //Loop to repeat this prompt if the user enters an invalid choice (not 1 or 2)
            cout << "\nAre you sure you want to delete this record?\n\n1. Yes\n2. No\n\n>> ";
            cin >> del;
            if (del == 2) {

                cout << "\nStudent record not deleted.\n";
                break;

            } else if (del == 1) {

                cout << "Deleting...\n\n";

                deleteRecord(matricno_find);

                cout << "Record deleted!";
                break;

            } else {

                cout << "\nInvalid choice, please try again.\n";
                cin.clear();
                cin.ignore();

            }
            }
        }

        //Prompt to repeat operation or go back to main menu
        cont = returnOrAgain(4);
        if (cont == 1)
            goto deleterecord;
        else
            goto mainmenu;

    } else if (choice == 5) { //Display all existing records [Owen]
        displayall:
        // Call function to display all existing records
        int totalrecords = countLines("data.txt");

        cout << "################## Displaying Current Student Records ##################\n\n";
        if (totalrecords != 1)
            cout << "There are currently " << totalrecords << " student records:\n";
        else
            cout << "There is currently " << totalrecords << " student record:\n";

        displayAll();
        cout << endl;

        // Immediately goes to main menu as it would be irrelevant to ask whether user would want to repeat this operation
        goto mainmenu;

    } else if (choice == 6) { //Exiting the program

        // Say bye-bye and return 0;
        cout << "################## Exiting Program. Bye bye! ##################\n\n";
        break;

    } else { //User enters any other option aside from 1 to 6
        cout << "###########################################\n\nInvalid choice selected. Please try again.\n";
        cin.clear(); // Clear the cin for any errors
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        continue;
    }
    }
    return 0;

}

/* Important!

54 68 69 73 20 63 6F 64 65 20 77 61 73 20 6D 61 64 65 20 62 79 20 42 61 6C 71 69 73 20 5A 61 66 69 72 61 68 20 28 39 38 33 33 31 29 27 73 20 67 72 6F 75 70 2C 20 61 6E 64 20 69 66 20 74 68 65 72 65 20 61 72 65 20 6F 74 68 65 72 73 20 77 68 6F 20 63 6F 70 69 65 64 20 74 68 69 73 20 6D 65 73 73 61 67 65 20 77 69 74 68 6F 75 74 20 6B 6E 6F 77 69 6E 67 20 77 68 61 74 20 74 68 69 73 20 6D 65 61 6E 73 2C 20 74 68 65 6E 20 74 68 65 79 20 68 61 76 65 20 63 6F 70 69 65 64 20 6F 75 72 20 63 6F 64 65 2E


*/