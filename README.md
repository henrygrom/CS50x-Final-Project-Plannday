# PlannDay - A Task Management Web Application

## What is PlannDay?
PlannDay is a flask based task management web application. The user interface divides the tasks into three schedule (Morning, Afternoon, and Evening tasks). This encourages the user to plan the flow of the day. PlannDay web application is built with [Python Flask](https://flask.palletsprojects.com/en/3.0.x/), [Flask-WTF](https://wtforms.readthedocs.io/en/3.1.x/), and [CS50 SQL](https://cs50.readthedocs.io/libraries/cs50/python/). PlannDay web application is designed with HTML, [Tailwind CSS](https://tailwindcss.com/docs/installation), and JavaScript.

### [Click here to see short demo.](https://youtu.be/R5JEKMtcAMc)

## How to use PlannDay?
#### Registration Page
1. Navigate to registration page.
2. Fill the registration form correctly then click the register button.
3. Upon successful registraton, you will be redirected to homepage.

#### Login Page
1. If you already have an account, go to login page.
2. Login in your credentials then click the login button.
3. If you don't have an account, there is a link to registration page.

#### Home Page
1. Tasks are displayed in three views: Morning, Afternoon, and Before Bed.
2. Each view has an "Add Task" button that opens a modal.
3. In the modal, fill in the task details, then click "Save" to submit. To discard changes, click "Cancel" to close the modal.
4. Once a task is in view, you can mark it as complete by clicking the checkbox.
5. Use the "Completed" button to navigate to the Completed Tasks tab and review your accomplished tasks.
6. Click the "Logout" button to log your account out.

#### Completed Task Page
1. The interface is similar to homepage with small changes.
2. To permanently delete tasks that are completed, click the "Clear" button. This will open a modal to confirm this action.
3. Uncheck the checkbox to change the status of the task.

## How was Plannday created?
## app.py
This is the main file that contains most of the logic to run the web application.

### Routes
- **Task Creation:**
The **_index_** route handles task creation, allowing users to input details of the task such as title and description. Upon submission, the tasks are stored in the database using CS50 SQL syntax. Lastly, it redirects the user back to the homepage.

- **Task Status Updates:**
The **_update_task_status_** route handles the dynamic status updates. The trigger for this route are the checkboxes. The status changes are reflected in the database.

- **Task Deletion:**
The **_delete_tasks_** route handles the permanent deletion of completed tasks. Users can clear completed tasks for a specific schedule, triggering the removal of record from the database.

- **Homepage:**
The default **_'/'_** route displays the tasks categorized into morning, afternoon, and evening schedule. The user can add, modify and navigate to completed task tab in this route.

- **Completed Tasks Page:**
The **_completed_tasks_** route displays the completed tasks, categorized by schedule. Users can review their completed tasks and make actions such as clear and uncheck in this separate view.

- **Logout**:
The **_logout_** route handles user logout functionality. It clears the current session then redirect the user to the login page.

## auth.py
This file manages user authentication, handling both login and register functionalities.

### Routes
- **Login:**
The **_login_** route handles the user login. It presents a form for users to enter their credentials. Upon successful login, users are redirected to the homepage. Unsuccessful login attempts show error messages to help the user.

- **Register:**
The **_register_** route manages user registration. It presents a form for users to enter their details such as full name, username, and password. Upon successful registration, new users are added to the database and redirected to the homepage.

- **Login Required Decorator:**
The **_login_required_** decorator ensures that certain routes are accessible only to authenticated users.

## forms.py
This file contains form classes neccessary for user interaction and task management. These forms are implemented using WTForms extension. It handles the validation and data processing logic of user login, registration, and task creation.

### RegistrationForm Fields and Validators:
- **first_name:** Records user's first name, ensuring it contains letters only.
- **last_name:** Records user's last name, ensuring it contains letters only.
- **username:** Accepts username with character and length limitations. It also ensures no username is duplicated.
- **password:** Records user's password, ensuring it meets security criteria.
- **password_confirmation:** Ensures the user correctly enter its password.

### LoginForm Fields and Validators:
- **username:** Captures the user's username for the main app to check if the user exist.
- **password:** Records user's password for the main app to check if the password hash matches the record in the database.

### TaskForm Fields and Validators:
- **task_title:** Records the title of the task ensuring the field is not empty and does not exceed a specified length.
- **task_description:** Records the description of the task ensuring it does not exceed the specified length.
- **task_schedule:** Provides a dropdown selection of the schedule of the task. It has a validator to ensure task schedule is a valid option.

## HTML Templates
### Layout
The **_layout.html_** serves as the base of the web application. It includes the navigation bar and necessary head and meta tags. I used Tailwind CSS framework to design the entire web app to my taste. I used this framework because I think it is much easier and faster to design my web app with this framework.

### auth
- **login.html:** The login page template allows the user to log in with their username and password.
- **register.html:** The register page allows the user to create account by providing their details.

### main
- **index.html:** The homepage template displays the task categorized by schedule, morning, afternoon, and evening. Users can add new tasks or mark existing tasks complete. I added simple animation to Add Task button to make the web app interactive. I used modal task forms to modernize the design of my web app and allow the user to focus on existing tasks.

- **completedtask.html** The completed task page displays the completed tasks much like the homepage. The difference is the Add Task button is replaced with Clear button to clear the task view.

## JavaScript

### completedtask
This is the file that contains the JavaScript for the completed task page. It consists of two functions that makes the page dynamic.
- **Dynamic Checkboxes:** This allows the status of tasks to be dynamically change using the checkbox. When a checkbox with the name "task-checkbox" is changed, the script sends an AJAX request to update the task status. It retrieves the task ID and checked status, sends them to the server, and updates the task status without refreshing the page.

- **Clear Button:** This allows the confirmation modal to appear when the Clear button is clicked. Upon confirmation of action, it sends an AJAX request to delete tasks for a specific schedule then reloads the page.

### scripts
This is the file that contains the JavaScript for the homepage. It consists of four functions that makes the page interactive and dynamic.
- **Modal Task Form:** This allows the task form modal to appear when the Add Task button is clicked. It also allows the user to close the modal when the the cancel button is clicked.

- **Task Schedule Autofill:** This autofills of the task schedule field in the TaskForm. It retrieves the schedule value from the clicked button then sets the value of hidden form field of task schedule.

- **Strikethrough Effect:** This adds a strikethrough effect to the parent element of the tasks when the checkbox is checked, and removes it if unchecked.

- **Dynamic Checkboxes:** The same logic from completed task script is applied for this function except it updates the status of the task to a different value.

## Special Thanks
### [CS50x 2023](https://cs50.harvard.edu/x/2023/)




