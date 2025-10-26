#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

using namespace std;

// Course structure
struct Course {
    string courseNumber;
    string courseTitle;
    vector<string> prerequisites;
};

// Node structure
struct Node {
    Course course;
    Node* left;
    Node* right;

    Node(Course c) {
        course = c;
        left = nullptr;
        right = nullptr;
    }
};

// Binary Search Tree class
class CourseBST {
private:
    Node* root;

    // Method to insert node
    Node* insert(Node* node, Course course) {
        if (node == nullptr) {
            return new Node(course);
        }
        if (course.courseNumber < node->course.courseNumber) {
            node->left = insert(node->left, course);
        } else {
            node->right = insert(node->right, course);
        }
        return node;
    }

    // Performs in-order traversal
    void inOrder(Node* node) const {
        if (node != nullptr) {
            inOrder(node->left);
            cout << node->course.courseNumber << ": " << node->course.courseTitle << endl;
            inOrder(node->right);
        }
    }

    // Searches for a course
    Course* search(Node* node, const string& courseNumber) const {
        if (node == nullptr) return nullptr;

        if (courseNumber == node->course.courseNumber) {
            return &node->course;
        } else if (courseNumber < node->course.courseNumber) {
            return search(node->left, courseNumber);
        } else {
            return search(node->right, courseNumber);
        }
    }

    // Deletes nodes
    void destroy(Node* node) {
        if (node != nullptr) {
            destroy(node->left);
            destroy(node->right);
            delete node;
        }
    }

public:
    CourseBST() {
        root = nullptr;
    }

    ~CourseBST() {
        destroy(root);
    }

    void insert(Course course) {
        root = insert(root, course);
    }

    void printInOrder() const {
        inOrder(root);
    }

    Course* findCourse(const string& courseNumber) const {
        return search(root, courseNumber);
    }
};

// Splits a string by delimiter
vector<string> split(const string& line, char delimiter) {
    vector<string> tokens;
    stringstream ss(line);
    string token;
    while (getline(ss, token, delimiter)) {
        tokens.push_back(token);
    }
    return tokens;
}

// Loads courses into the BST
void loadCoursesFromFile(const string& filename, CourseBST& bst) {
    ifstream file(filename);
    string line;

    if (!file.is_open()) {
        cout << "Error: Could not open file '" << filename << "'." << endl;
        return;
    }

    while (getline(file, line)) {
        vector<string> tokens = split(line, ',');
        if (tokens.size() < 2) continue;

        Course course;
        course.courseNumber = tokens[0];
        course.courseTitle = tokens[1];
        for (size_t i = 2; i < tokens.size(); ++i) {
            course.prerequisites.push_back(tokens[i]);
        }
        bst.insert(course);
    }

    file.close();
    cout << "Courses successfully loaded!" << endl;
}

// Displays course details
void displayCourseInfo(const CourseBST& bst) {
    string courseNumber;
    cout << "Enter the course number: ";
    getline(cin, courseNumber);

    Course* course = bst.findCourse(courseNumber);
    if (course == nullptr) {
        cout << "Course not found" << endl;
        return;
    }

    cout << course->courseNumber << ": " << course->courseTitle << endl;
    if (course->prerequisites.empty()) {
        cout << "Prerequisites: None" << endl;
    } else {
        cout << "Prerequisites: ";
        for (const auto& prereq : course->prerequisites) {
            cout << prereq << " ";
        }
        cout << endl;
    }
}

// Displays menu
void showMenu() {
    cout << "\nMenu Options:\n";
    cout << "1. Load course data\n";
    cout << "2. Print course list\n";
    cout << "3. Print course information\n";
    cout << "9. Exit\n";
    cout << "Enter your choice: ";
}

// Main program
int main() {
    CourseBST bst;
    int choice;
    string filename;

    do {
        showMenu();
        cin >> choice;
        cin.ignore();

        switch (choice) {
            case 1:
                cout << "Load sample.csv? n to load your own csv file (y/n): ";
                char choice;
                cin >> choice;
                cin.ignore();

                string filename;
                if (tolower(choice) == 'y') {
                    filename = "sample.csv";
                    cout << "Loading sample file..." << endl;
                } else {
                    cout << "Enter the file name: ";
                    getline(cin, filename);
                }

    loadCoursesFromFile(filename, bst);
    break;

            case 2:
                cout << "\nCourse List:\n";
                bst.printInOrder();
                break;

            case 3:
                displayCourseInfo(bst);
                break;

            case 9:
                cout << "Exiting program, Goodbye!" << endl;
                break;

            default:
                cout << "Invalid choice. Please enter 1, 2, 3, or 9." << endl;
        }

    } while (choice != 9);

    return 0;
}
