const modal = document.getElementById("artifact-modal");
const modalTitle = document.getElementById("artifact-title");
const githubLink = document.getElementById("github-link");
const demoLink = document.getElementById("demo-link");
const closeBtn = document.querySelector(".close");

// When an artifact is clicked
document.querySelectorAll(".artifact-link").forEach(link => {
  link.addEventListener("click", (e) => {
    e.preventDefault();

    const title = e.target.innerText;
    const github = e.target.getAttribute("data-github");
    const demo = e.target.getAttribute("data-demo");

    modalTitle.textContent = title;
    githubLink.href = github;

    // If there's a demo link, show the "Run Artifact" button, otherwise hide it
    if (demo) {
      demoLink.href = demo;
      demoLink.style.display = "inline-block";
    } else {
      demoLink.style.display = "none";
    }

    modal.style.display = "flex";
  });
});

// Close modal
closeBtn.onclick = function() {
  modal.style.display = "none";
};

// Close when clicking outside modal
window.onclick = function(event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
};

// enhancements modal logic
document.addEventListener("DOMContentLoaded", () => {
  const enhancementModal = document.getElementById("enhancement-modal");
  const enhancementTitle = document.getElementById("enhancement-title");
  const enhancementScrollbox = document.getElementById("enhancement-scrollbox");
  const enhancementClose = enhancementModal.querySelector(".close");

  const enhancementText = {
    software: `
      <p>
        For this enhancement, I first planned what changes I wanted to make to this program to create a more advanced and user-friendly application. I created a to-do list and decided on creating the following changes:  
        Change programming language from C++ to Python; This was done to demonstrate proficiency in more than one programming language. Add more detailed comments to program. Create not only an enhanced CLI app but a front-end interface that accomplishes the same as the CLI app. Design a faster course loading algorithm like an AVL tree. Allow for database functionality instead of forcing users to only be able to load and save to CSV files
      </p>
         
      <p>
        This shows my detailed planning before I began to actually program the concepts. When changing the program to Python from C++, I had to rely at times on Python documentation as I was not as familiar with Python as I was in C++. However, this reliance on documentation not only strengthened my familiarity with the language but my confidence in designing programs in this language, and I was able to appreciate the many advantages it had, but also the disadvantages, such as being slower than C++.  
      </p>
      <p>
        When creating the web app to allow users to access the same functions as the CLI app but on the front end, I used Flask, a web framework for Python. I detailed routes in my main Flask file titled app.py, added the proper imports needed such as CRUD actions from my mongo_crud.py file, as well as functionality to allow the use of HTML templates with the Flask interface. The routes were created by accounting for edge cases and possible errors that could occur.  
      </p>
      <p>
        I also made sure to create limitations for the user to make the app more secure. Limitations such as the max size of the CSV file being 2 MB. This was done to prevent a user knowingly or unknowingly crashing the app since the app’s memory would be overwhelmed. I also created HTML templates to display the necessary information to the user on the front end. Without these templates, the app would not be able to be a fully functional web interface app since no information would be displayed to the user online. I created four HTML files that each dealt with a separate page of the program.  
      </p>
      <p>
        The file that displayed the home page to the user was index.html and used a combination of HTML code to add headings, the main course table, and links to the other pages, but also load Flask flash messages, like when a user successfully loads courses from a CSV file or deletes courses. I also created a styles.css file that styled the HTML code, to make it more visually appealing to the user. 
      </p>
    `,
    algorithms: `
      <p>
        In the CLI version of my project, I implemented an AVL tree to replace the original binary search tree in the original project. This change ensured that the loading of courses would be faster with this new data structure since it is self-balancing unlike a binary search tree. In a tree that is not self-balancing, the tree can quickly become skewed to one side of the tree or the other, and this results in search speeds of O(n). By balancing the tree so that it is always –1 or +1 from each node, we eliminate this and a speed of O(log n) is achieved. 
      </p>
      <p>
        In the web version of my project, I transitioned from implementing an AVL tree data structure to a more scalable but equally fast data structure used by MongoDB. This change not only maintained algorithm efficiency but also made the data more persistent and scalable. MongoDB already handles insertion, deletion, and search operations with their internal B-tree indexes, which provide equal speed as an AVL tree, but they allow data to be persistent across user sessions. I also implemented algorithms to validate input, filter duplicates in courses, iterating through MongoDB results, and converting lists into comma separated strings when a user exports to a CSV file. 
      </p>
    `,
    databases: `
      <p>
        Finally, in this final enhancement I created database functionality in both my CLI and web-based app. In my original CLI app, there was no database functionality that allowed a user to load or save courses to a database. The only way they could load and save courses was from a CSV file. So, then I decided to allow a user to load from a database as well, thus not limiting their options.  
      </p>
      <p>
        First, the program checks if a user is authenticated to a database before they can do anything else. Once they are it calls a function called load_courses_from_mongodb(mongo, bst), which then reads through each document in the collection. For each document, a new node is created in the AVL tree, just as it would from a CSV file, and all the database documents are saved in this tree just like they would be if a user loaded from a CSV file instead.
      </p>
      <p>
        I also created the ability for a user to update or delete a course right from the database. This was accomplished by once again verifying if they are authenticated to a database and then prompting the user for the course number to update as well as the prerequisite. It then checks if new data was given and then directly updates the course in MongoDB using the command mongo.update with whatever new data was given. 
      </p>
      <p>
        For my web app, I still relied on the mongo_crud.py file, which includes the database actions of creating, reading, updating, and deleting. This time, however, it was implemented in the Flask web interface to allow for the front-end interface. I created a default MongoDB instance titled webappDB, and a default user and password for the user. If a user wished to authenticate their own database, they could, but this default database was created for those that wished to use the app database to manipulate their courses.  
      </p>
      <p>
        The function index in app.py shows all courses from the current MongoDB connection if there are any. It also creates a new user session each time a user opens the page. The upload function takes courses from an uploaded CSV file and saves them to the app database. The code limits the number of rows to 1000 to not overload the site. Those courses that exceed the limit are then skipped, and a flash message is shown to the user, making them aware of why they were skipped. The function also disallows duplicated by checking if the course is already in the database, and if it is present, this course is not added. Finally, the function use_sample uses a sample.csv file that is included in the project directory to load courses to the database and display them on the front-end interface to the user. This is done in case the user simply wants to test the functionality without having a CSV or database ready to load the courses to the front-end. 
      </p>
      <p>
        All these planned enhancements were met in my final project and thus show my progress as a programmer since I first began creating this project in module one. As I was refining this artifact in this category, I was learning and refining important concepts like designing a program before building it, debugging, testing edge cases, thinking about the user experience, working with MongoDB, and much more. Some challenges I faced were in remaining patient when my program would give an error or behave in an unexpected way. I also learned to use available resources not only those that were provided in the capstone course but also in forums and documentation. Using these resources is also part of what makes a good programmer, since sometimes you will need outside help when encountering topics, you aren’t familiar with. 
      </p>
    `
  };

  // Open the appropriate enhancement modal based on what the user clicked
  document.querySelectorAll(".enhancement-link").forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const key = e.currentTarget.getAttribute("data-enhancement");
      const title = e.currentTarget.innerText;

      enhancementTitle.textContent = title;
      enhancementScrollbox.innerHTML = enhancementText[key] || "<p>No content available.</p>";

      enhancementModal.style.display = "flex";
      document.body.style.overflow = "hidden";
    });
  });

  // Close handlers
  const closeEnhancement = () => {
    enhancementModal.style.display = "none";
    document.body.style.overflow = "";
  };

  enhancementClose.addEventListener("click", closeEnhancement);
  window.addEventListener("click", (event) => {
    if (event.target === enhancementModal) closeEnhancement();
  });
  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeEnhancement();
  });
});
