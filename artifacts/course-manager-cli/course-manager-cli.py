# Python version of the C++ CourseBST program
# Esteban Garcia
# SNHU

# Imports mongo_crud.py file to load and use CRUD functionality with a database
from mongo_crud import CRUD
# Uses getpass to hide user password when authenticating to a mongoDB database
from getpass import getpass

# Creates a Course Class and adds an init method to initialize a course
class Course:
    def __init__(self, course_number, course_title, prerequisites=None):
        self.course_number = course_number
        self.course_title = course_title
        self.prerequisites = prerequisites if prerequisites else []

# Creates a node that is added to the binary search tree
class Node:
    def __init__(self, course):
        self.course = course
        self.left = None
        self.right = None
        self.height = 1

# Uses an AVL Tree to save courses in program
class CourseBST:
    def __init__(self):
        self.root = None

    # Utility methods for AVL tree
    def _height(self, node):
        return node.height if node else 0

    def _balance(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    # Adds rotations for AVL tree
    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        return x

   # Creates an insert function to insert courses in tree
    def _insert(self, node, course):
        if not node:
            return Node(course)

        if course.course_number < node.course.course_number:
            node.left = self._insert(node.left, course)
        elif course.course_number > node.course.course_number:
            node.right = self._insert(node.right, course)
        else:
            # skips if it is a duplicate course
            return node

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._balance(node)

        # Rotates tree based on where it is unbalanced
        if balance > 1 and course.course_number < node.left.course.course_number:
            return self._rotate_right(node)
        
        if balance < -1 and course.course_number > node.right.course.course_number:
            return self._rotate_left(node)
    
        if balance > 1 and course.course_number > node.left.course.course_number:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
    
        if balance < -1 and course.course_number < node.right.course.course_number:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, course):
        self.root = self._insert(self.root, course)

    # prints courses in alphabetic and numerical order
    def print_in_order(self):
        def _in_order(node):
            if node:
                _in_order(node.left)
                print(f"{node.course.course_number}: {node.course.course_title}")
                _in_order(node.right)
        _in_order(self.root)

    # finds a course based on the course_number
    def find_course(self, course_number):
        def _search(node, course_number):
            if not node:
                return None
            if course_number == node.course.course_number:
                return node.course
            elif course_number < node.course.course_number:
                return _search(node.left, course_number)
            else:
                return _search(node.right, course_number)
        return _search(self.root, course_number)


def split(line, delimiter):
    """Splits a line into tokens."""
    return [token.strip() for token in line.split(delimiter)]


def load_courses_from_file(filename, bst):
    """Loads courses from a CSV file into the AVL tree."""
    try:
        with open(filename, 'r') as file:
            for line in file:
                tokens = split(line.strip(), ',')
                if len(tokens) < 2:
                    continue

                course_number = tokens[0]
                course_title = tokens[1]
                prerequisites = tokens[2:] if len(tokens) > 2 else []

                course = Course(course_number, course_title, prerequisites)
                bst.insert(course)

        print("Courses successfully loaded and balanced with AVL Tree!")
    except FileNotFoundError:
        print(f"Error: Could not open file '{filename}'.")


def display_course_info(bst):
    """Displays detailed information about a specific course."""
    course_number = input("Enter the course number: ").strip()
    course = bst.find_course(course_number)

    if not course:
        print("Course not found.")
        return
    print(f"{course.course_number}: {course.course_title}")
    if not course.prerequisites:
        print("Prerequisites: None")
    else:
        print("Prerequisites:", ", ".join(course.prerequisites))


def show_menu():
    """Displays the main menu."""
    print("\nMenu Options:")
    print("1. Load course data from CSV")
    print("2. Load courses from MongoDB")
    print("3. Print course list")
    print("4. Print course information")
    print("5. Save courses to MongoDB")
    print("6. Update a course in MongoDB")
    print("7. Delete a course from MongoDB")
    print("9. Exit")

def prompt_for_user_and_pass():
    print("\n--- MongoDB Connection Setup ---")
    username = input("Enter MongoDB username (leave blank for no authentication): ").strip()
    password = getpass("Enter MongoDB password (leave blank if none exists): ").strip()

    if username and password:
        return CRUD(username, password, "coursesDB", "courses")
    else:
        return CRUD("coursesDB", "courses")


def save_courses_to_mongodb(bst, mongo):
    """Saves courses to MongoDB in sorted (in numerical order) order."""
    def _save(node):
        if node:
            # Visit the leftmost node to get smallest course number
            _save(node.left)

            # Checks if the courses already exists in the database
            existing = mongo.collection.find_one(
                {"course_number": node.course.course_number}
            )

            if existing:
                print(f"Skipped pre-existing course in database: {node.course.course_number}")
            else:
              # Insert new course document
              doc = {
                  "course_number": node.course.course_number,
                  "course_title": node.course.course_title,
                  "prerequisites": node.course.prerequisites
              }

            mongo.create(doc)
            # Visit the right subtree for the larger course numbers
            _save(node.right)

    _save(bst.root)
    print("Courses have been saved to MongoDB in alphabetical and numerical order.")


def load_courses_from_mongodb(mongo, bst):
    documents = mongo.read({})
    for doc in documents:
        course = Course(
            doc["course_number"],
            doc["course_title"],
            doc.get("prerequisites", [])
        )
        bst.insert(course)
    print("Courses loaded from MongoDB and balanced with an AVL Tree!")


def update_course_db(mongo):
    """Updates a course directly in the MongoDB collection."""
    course_number = input("Enter the course number to update: ").strip()
    new_title = input("Enter the new course title (leave blank to keep current): ").strip()
    new_prereqs = input("Enter the new prerequisites (comma-separated, leave blank to keep current): ").strip()

    new_data = {}
    if new_title:
        new_data["course_title"] = new_title
    if new_prereqs:
        new_data["prerequisites"] = [p.strip() for p in new_prereqs.split(",")]

    if new_data:
        updated_count = mongo.update({"course_number": course_number}, new_data)
        if updated_count > 0:
            print(f"{updated_count} course(s) updated successfully.")
        else:
            print("No matching course was found.")
    else:
        print("No updates were provided.")


def delete_mongo_course(mongo):
    """Deletes a course directly in MongoDB"""
    course_number = input("Enter the course number to delete: ").strip()
    deleted_count = mongo.delete({"course_number": course_number})
    if deleted_count > 0:
        print(f"{deleted_count} course(s) deleted successfully.")
    else:
        print("No matching course found.")


def main():
    bst = CourseBST()
    mongo = None

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if not choice.isdigit():
            print("Please enter a number (1, 2, 3, or 9).")
            continue

        if choice == '1':
            sample_or_no = input("Load sample.csv? n to load your own csv file (y/n)").strip()
            if sample_or_no.strip() == "y":
                filename = "sample.csv"
                load_courses_from_file(filename, bst)
            else:
                filename = input("Enter the file name (including the extension): ").strip()
                load_courses_from_file(filename, bst)

        elif choice == '2':
            # Triggered if user tries to access MongoDB without being authenticated to a database first
            if mongo is None:
                mongo = prompt_for_user_and_pass()
            load_courses_from_mongodb(mongo, bst)

        elif choice == '3':
            print("\nCourse List (Balanced AVL Order):")
            bst.print_in_order()

        elif choice == '4':
            display_course_info(bst)

        elif choice == '5':
            # Triggered if user tries to access MongoDB without being authenticated to a databse first
            if mongo is None:
                mongo = prompt_for_user_and_pass()
            save_courses_to_mongodb(bst, mongo)

        elif choice == '6':
            # Triggered if user tries to access MongoDB without being authenticated to a databse first
            if mongo is None:
                mongo = prompt_for_user_and_pass()
            update_course_db(mongo)

        elif choice == '7':
            # Triggered if user tries to access MongoDB without being authenticated to a databse first
            if mongo is None:
                mongo = prompt_for_user_and_pass()
            delete_mongo_course(mongo)

        elif choice == '9':
            print("Exiting program, Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 9.")


if __name__ == "__main__":
    main()


