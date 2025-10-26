# Creates a flask front end web interface so users can operate the Course Manager program through the front end

from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from mongo_crud import CRUD
import csv
import io
import os
from werkzeug.exceptions import RequestEntityTooLarge


def get_mongo():
    global mongo
    try:
        if mongo is None:
            return default_mongo
    except Exception:
        pass
    return default_mongo


app = Flask(__name__)
app.secret_key = "supersecretkey"

# Created to limit CSV upload file size to 2 MB
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

# Use MongoDB Atlas if available
mongo_uri = os.getenv("MONGO_URI")

if mongo_uri:
    print("Connecting to MongoDB Atlas via MONGO_URI...")
    default_mongo = CRUD(db_name="webappDB", collection_name="courses")
else:
    print("No MONGO_URI found. Using local MongoDB connection.")
    # Connects to a default MongoDB database otherwise
    default_mongo = CRUD("webapp_user", "securepassword123", "webappDB",
                         "courses")

mongo = default_mongo


@app.route("/")
def index():
    """Lists all courses from the current MongoDB connection"""
    global mongo

    # Checks for a new user session
    if "visited" not in session:
        session["visited"] = True
        try:
            default_mongo.collection.delete_many({})
            print(" Cleared default MongoDB for new user session")
        except Exception as e:
            print(f"Could not clear default MongoDB: {e}")

    # Checks if user is logged in to their MongoDB database first
    if mongo is None:
        flash("Please connect to MongoDB first:")
        return redirect(url_for("connect"))

    # Shows courses
    courses = list(get_mongo().collection.find({}))
    return render_template("index.html", courses=courses)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Uploads CSV file and saves courses to MongoDB"""
    global mongo

    if mongo is None:
        mongo = default_mongo
        flash("Using default MongoDB database (webappDB):")

    if request.method == "POST":
        file = request.files["file"]

        # will prompt user for a .csv file if one was not entered
        if not file or not file.filename:
            flash("No file selected. Please upload a CSV file.")
            return redirect(url_for("upload"))

        if not file.filename.lower().endswith(".csv"):
            flash("Please upload a valid CSV file.")
            return redirect(url_for("upload"))

        # saves file temporarily
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        # limits number of rows to 1000
        max_rows = 1000
        inserted = 0

        # Loads the CSV and inserts into MongoDB
        with open(filepath, "r", newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i >= max_rows:
                    flash(
                        f"Upload limit reached ({max_rows} courses max). Subsequent rows are skipped"
                    )

                if len(row) < 2:
                    continue

                doc = {
                    "course_number":
                    row[0].strip(),
                    "course_title":
                    row[1].strip(),
                    "prerequisites":
                    [p.strip() for p in row[2:]] if len(row) > 2 else []
                }

                # Avoids duplicates
                existing = get_mongo().collection.find_one(
                    {"course_number": row[0]})
                if not existing:
                    mongo.create(doc)
                    inserted += 1

        flash(f"Uploaded {inserted} course(s) successfully!")
        return redirect(url_for("index"))

    return render_template("upload.html")


@app.route('/export')
def export_courses():
    """Exports all courses from the current MongoDB connection to CSV"""
    try:
        collection = get_mongo().collection
        courses = list(collection.find({}, {"_id": 0}))
    except Exception as e:
        flash(f"Error accessing database: {str(e)}")
        return redirect(url_for("index"))

    if not courses:
        flash("No courses to export.")
        return redirect(url_for('index'))

    # Creates CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Course Number", "Course Title", "Prerequisites"])

    for course in courses:
        prereqs = ", ".join(course.get("prerequisites", []))
        writer.writerow([
            course.get("course_number", ""),
            course.get("course_title", ""), prereqs
        ])

    output.seek(0)

    return Response(output,
                    mimetype="text/csv",
                    headers={
                        "Content-Disposition":
                        "attachment;filename=courses_export.csv"
                    })


@app.route("/use-sample", methods=["POST"])
def use_sample():
    """Loads sample.csv data into MongoDB"""
    global mongo

    sample_path = os.path.join(os.getcwd(), "sample.csv")

    if not os.path.exists(sample_path):
        flash("Sample file not found.")
        return redirect(url_for("index"))

    inserted = 0
    try:
        with open(sample_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 2:
                    continue

                doc = {
                    "course_number":
                    row[0].strip(),
                    "course_title":
                    row[1].strip(),
                    "prerequisites":
                    [p.strip() for p in row[2:]] if len(row) > 2 else []
                }

                existing = get_mongo().collection.find_one(
                    {"course_number": row[0]})
                if not existing:
                    get_mongo().create(doc)
                    inserted += 1

        flash(f"Loaded {inserted} sample course(s) successfully!")
    except Exception as e:
        flash(f"Error loading sample courses: {str(e)}")

    return redirect(url_for("index"))


# Allows users to delete a course on the front end
@app.route("/delete/<course_number>", methods=["POST"])
def delete_course(course_number):
    """Deletes a course from MongoDB by the course number"""
    try:
        result = get_mongo().collection.delete_one(
            {"course_number": course_number})
        if result.deleted_count > 0:
            flash(f"Deleted course: {course_number}")
        else:
            flash(f"No course found with number: {course_number}")
    except Exception as e:
        flash(f"Error deleting course: {str(e)}")
    return redirect(url_for("index"))


@app.route("/clear", methods=["POST"])
def clear_courses():
    """Deletes all courses from the current MongoDB collection."""
    try:
        result = get_mongo().collection.delete_many({})
        flash(f"Deleted {result.deleted_count} course(s) successfully.")
    except Exception as e:
        flash(f"Error clearing courses: {str(e)}")
    return redirect(url_for("index"))


@app.route("/edit/<course_number>", methods=["GET", "POST"])
def edit_course(course_number):
    """Displays and updates an existing course"""
    collection = get_mongo().collection
    course = collection.find_one({"course_number": course_number})

    if not course:
        flash(f"No course found with number: {course_number}")
        return redirect(url_for("index"))

    if request.method == "POST":
        new_title = (request.form.get("course_title") or "").strip()
        new_prereqs = (request.form.get("prerequisites") or "").strip()

        prereq_list = [p.strip()
                       for p in new_prereqs.split(",")] if new_prereqs else []

        try:
            collection.update_one({"course_number": course_number}, {
                "$set": {
                    "course_title": new_title,
                    "prerequisites": prereq_list
                }
            })
            flash(f"Course {course_number} updated successfully.")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Error updating course: {str(e)}")

    return render_template("edit.html", course=course)


# Allows users to connect to their local databases on their machines
@app.route("/connect", methods=["GET", "POST"])
def connect():
    """Allows users to connect to their MongoDB database"""
    global mongo

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        db_name = request.form.get("db_name", "").strip()
        collection_name = request.form.get("collection_name", "").strip()

        try:
            if not username or not db_name or not collection_name:
                raise ValueError(
                    "Missing required fields for MongoDB connection")

            temp_mongo = CRUD(username, password, db_name, collection_name)

            _ = temp_mongo.collection.database.list_collection_names()

            mongo = temp_mongo
            flash(f"Connected successfully to MongoDB database: '{db_name}'")

            return redirect(url_for("index"))

        except Exception as e:
            # defaults to default_mongo database instance if user connection fails
            mongo = default_mongo
            flash(
                f"Connection failed. Using default MongoDB instead. Error: {str(e)}"
            )
            return redirect(url_for("index"))

    return render_template("connect.html")


@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(e):
    flash("File is too large. Maximum allowed size is 2MB")
    return redirect(url_for("upload"))


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    port = int(os.environ.get("PORT", 81))
    app.run(host="0.0.0.0", port=port, debug=True)
