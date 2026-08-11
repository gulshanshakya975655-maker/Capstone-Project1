const API_URL = "http://127.0.0.1:8000";


// ==========================================
// ELEMENTS
// ==========================================

const titleInput = document.getElementById("title");
const priorityInput = document.getElementById("priority");
const dueDateInput = document.getElementById("due_date");

const tasksContainer = document.getElementById("tasks");

const searchInput = document.getElementById("searchInput");
const priorityFilter = document.getElementById("priorityFilter");
const statusFilter = document.getElementById("statusFilter");

const totalTasks = document.getElementById("totalTasks");
const pendingTasks = document.getElementById("pendingTasks");
const completedTasks = document.getElementById("completedTasks");
const highPriorityTasks = document.getElementById("highPriorityTasks");

const taskForm = document.querySelector(".task-form");

const userForm = document.getElementById("userForm");
const userName = document.getElementById("userName");
const userEmail = document.getElementById("userEmail");
const usersContainer = document.getElementById("users");

const projectForm = document.getElementById("projectForm");
const projectName = document.getElementById("projectName");
const projectOwnerId = document.getElementById("projectOwnerId");
const projectsContainer = document.getElementById("projects");


let tasks = [];
let users = [];
let projects = [];


// ==========================================
// LOAD TASKS
// ==========================================

async function loadTasks() {

    try {

        const response = await fetch(`${API_URL}/tasks`);

        if (!response.ok) {
            throw new Error("Failed to load tasks");
        }

        tasks = await response.json();

        renderTasks();

    } catch (error) {

        console.error("Error loading tasks:", error);

        tasksContainer.textContent = "Unable to load tasks.";
    }
}


// ==========================================
// RENDER TASKS
// ==========================================

function renderTasks() {

    const searchText = searchInput.value
        .trim()
        .toLowerCase();

    const selectedPriority = priorityFilter.value;
    const selectedStatus = statusFilter.value;


    const filteredTasks = tasks.filter(function (task) {

        const matchesSearch =
            task.title.toLowerCase().includes(searchText);

        const matchesPriority =
            selectedPriority === "all" ||
            task.priority === selectedPriority;

        const matchesStatus =
            selectedStatus === "all" ||
            task.status === selectedStatus;

        return (
            matchesSearch &&
            matchesPriority &&
            matchesStatus
        );
    });


    tasksContainer.textContent = "";


    if (filteredTasks.length === 0) {

        const message = document.createElement("p");

        message.textContent = "No tasks found.";

        tasksContainer.appendChild(message);

    } else {

        filteredTasks.forEach(function (task) {

            const taskItem =
                document.createElement("div");

            taskItem.className = "task-item";


            const title =
                document.createElement("h3");

            title.textContent = task.title;


            const priority =
                document.createElement("p");

            priority.textContent =
                `Priority: ${task.priority}`;


            const dueDate =
                document.createElement("p");

            dueDate.textContent =
                `Due Date: ${task.due_date || "Not set"}`;


            const status =
                document.createElement("p");

            status.textContent =
                `Status: ${task.status}`;


            const actions =
                document.createElement("div");

            actions.className = "task-actions";


            // EDIT
            const editButton =
                document.createElement("button");

            editButton.textContent = "Edit";

            editButton.className = "edit-btn";

            editButton.addEventListener(
                "click",
                function () {
                    editTask(task.id);
                }
            );


            // COMPLETE
            const completeButton =
                document.createElement("button");

            completeButton.textContent =
                task.status === "completed"
                    ? "Mark Pending"
                    : "Complete";

            completeButton.className =
                "complete-btn";

            completeButton.addEventListener(
                "click",
                function () {
                    updateTaskStatus(
                        task.id,
                        task.status
                    );
                }
            );


            // DELETE
            const deleteButton =
                document.createElement("button");

            deleteButton.textContent = "Delete";

            deleteButton.className =
                "delete-btn";

            deleteButton.addEventListener(
                "click",
                function () {
                    deleteTask(task.id);
                }
            );


            actions.appendChild(editButton);
            actions.appendChild(completeButton);
            actions.appendChild(deleteButton);


            taskItem.appendChild(title);
            taskItem.appendChild(priority);
            taskItem.appendChild(dueDate);
            taskItem.appendChild(status);
            taskItem.appendChild(actions);


            tasksContainer.appendChild(taskItem);
        });
    }


    updateSummary();
}


// ==========================================
// UPDATE SUMMARY
// ==========================================

function updateSummary() {

    const total = tasks.length;

    const pending =
        tasks.filter(function (task) {
            return task.status === "pending";
        }).length;

    const completed =
        tasks.filter(function (task) {
            return task.status === "completed";
        }).length;

    const highPriority =
        tasks.filter(function (task) {
            return task.priority === "high";
        }).length;


    totalTasks.textContent = total;
    pendingTasks.textContent = pending;
    completedTasks.textContent = completed;
    highPriorityTasks.textContent = highPriority;
}


// ==========================================
// CREATE TASK
// ==========================================

async function createTask() {

    const title =
        titleInput.value.trim();

    const priority =
        priorityInput.value;

    const dueDate =
        dueDateInput.value;


    if (!title) {

        alert("Please enter a task title.");

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/tasks`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    title: title,

                    priority: priority,

                    due_date: dueDate || null,

                    status: "pending",

                    project_id: 1
                })
            }
        );


        if (!response.ok) {

            const errorData =
                await response.json();

            alert(
                errorData.detail ||
                "Failed to create task."
            );

            return;
        }


        const newTask =
            await response.json();


        tasks.push(newTask);


        titleInput.value = "";

        priorityInput.value = "medium";

        dueDateInput.value = "";


        renderTasks();


    } catch (error) {

        console.error(
            "Error creating task:",
            error
        );

        alert(
            "Backend server is not reachable."
        );
    }
}


// ==========================================
// EDIT TASK
// ==========================================

async function editTask(taskId) {

    const task =
        tasks.find(function (item) {
            return item.id === taskId;
        });


    if (!task) {
        return;
    }


    const newTitle =
        prompt(
            "Enter new task title:",
            task.title
        );


    if (newTitle === null) {
        return;
    }


    const trimmedTitle =
        newTitle.trim();


    if (!trimmedTitle) {

        alert(
            "Task title cannot be empty."
        );

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/tasks/${taskId}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    title: trimmedTitle
                })
            }
        );


        if (!response.ok) {

            alert(
                "Failed to update task."
            );

            return;
        }


        const updatedTask =
            await response.json();


        tasks =
            tasks.map(function (item) {

                if (item.id === taskId) {
                    return updatedTask;
                }

                return item;
            });


        renderTasks();


    } catch (error) {

        console.error(
            "Error updating task:",
            error
        );
    }
}


// ==========================================
// UPDATE TASK STATUS
// ==========================================

async function updateTaskStatus(
    taskId,
    currentStatus
) {

    const newStatus =
        currentStatus === "completed"
            ? "pending"
            : "completed";


    try {

        const response = await fetch(
            `${API_URL}/tasks/${taskId}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    status: newStatus
                })
            }
        );


        if (!response.ok) {

            const errorData =
                await response.json();

            alert(
                errorData.detail ||
                "Failed to update task status."
            );

            return;
        }


        const updatedTask =
            await response.json();


        tasks =
            tasks.map(function (task) {

                if (task.id === taskId) {
                    return updatedTask;
                }

                return task;
            });


        renderTasks();


    } catch (error) {

        console.error(
            "Error updating task status:",
            error
        );

        alert(
            "Unable to update task status."
        );
    }
}


// ==========================================
// DELETE TASK
// ==========================================

async function deleteTask(taskId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this task?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/tasks/${taskId}`,
            {
                method: "DELETE"
            }
        );


        if (!response.ok) {

            alert(
                "Failed to delete task."
            );

            return;
        }


        tasks =
            tasks.filter(function (task) {
                return task.id !== taskId;
            });


        renderTasks();


    } catch (error) {

        console.error(
            "Error deleting task:",
            error
        );
    }
}


// ==========================================
// LOAD USERS
// ==========================================

async function loadUsers() {

    try {

        const response =
            await fetch(`${API_URL}/users`);


        if (!response.ok) {
            throw new Error("Failed to load users");
        }


        users =
            await response.json();


        renderUsers();


    } catch (error) {

        console.error(
            "Error loading users:",
            error
        );

        usersContainer.textContent =
            "Unable to load users.";
    }
}


// ==========================================
// RENDER USERS
// ==========================================

function renderUsers() {

    usersContainer.textContent = "";


    if (users.length === 0) {

        const message =
            document.createElement("p");

        message.textContent =
            "No users found.";

        usersContainer.appendChild(message);

        return;
    }


    users.forEach(function (user) {

        const userItem =
            document.createElement("div");

        userItem.className =
            "task-item";


        const name =
            document.createElement("h3");

        name.textContent =
            user.name;


        const email =
            document.createElement("p");

        email.textContent =
            `Email: ${user.email}`;


        const id =
            document.createElement("p");

        id.textContent =
            `User ID: ${user.id}`;


        // ACTIONS
        const actions =
            document.createElement("div");

        actions.className =
            "task-actions";


        // EDIT USER
        const editButton =
            document.createElement("button");

        editButton.textContent =
            "Edit";

        editButton.className =
            "edit-btn";

        editButton.addEventListener(
            "click",
            function () {
                editUser(user.id);
            }
        );


        // DELETE USER
        const deleteButton =
            document.createElement("button");

        deleteButton.textContent =
            "Delete";

        deleteButton.className =
            "delete-btn";

        deleteButton.addEventListener(
            "click",
            function () {
                deleteUser(user.id);
            }
        );


        actions.appendChild(editButton);
        actions.appendChild(deleteButton);


        userItem.appendChild(name);
        userItem.appendChild(email);
        userItem.appendChild(id);
        userItem.appendChild(actions);


        usersContainer.appendChild(userItem);
    });
}
// ==========================================
// EDIT USER
// ==========================================

async function editUser(userId) {

    const user = users.find(function (item) {
        return item.id === userId;
    });

    if (!user) {
        return;
    }

    const newName = prompt(
        "Enter new user name:",
        user.name
    );

    if (newName === null) {
        return;
    }

    const newEmail = prompt(
        "Enter new email:",
        user.email
    );

    if (newEmail === null) {
        return;
    }

    const name = newName.trim();
    const email = newEmail.trim();

    if (!name || !email) {
        alert("Name and email cannot be empty.");
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/users/${userId}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    email: email
                })
            }
        );

        if (!response.ok) {

            const errorData =
                await response.json();

            alert(
                errorData.detail ||
                "Failed to update user."
            );

            return;
        }

        const updatedUser =
            await response.json();

        users = users.map(function (item) {

            if (item.id === userId) {
                return updatedUser;
            }

            return item;
        });

        renderUsers();

    } catch (error) {

        console.error(
            "Error updating user:",
            error
        );

        alert(
            "Unable to update user."
        );
    }
}


// ==========================================
// DELETE USER
// ==========================================

async function deleteUser(userId) {

    const confirmed = confirm(
        "Are you sure you want to delete this user?"
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/users/${userId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {

            const errorData =
                await response.json();

            alert(
                errorData.detail ||
                "Failed to delete user."
            );

            return;
        }

        users = users.filter(function (user) {
            return user.id !== userId;
        });

        renderUsers();

    } catch (error) {

        console.error(
            "Error deleting user:",
            error
        );

        alert(
            "Unable to delete user."
        );
    }
}

// ==========================================
// CREATE USER
// ==========================================

async function createUser(event) {

    event.preventDefault();


    const name =
        userName.value.trim();

    const email =
        userEmail.value.trim();


    if (!name || !email) {

        alert(
            "Please enter name and email."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/users`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        email: email
                    })
                }
            );


        if (!response.ok) {

            const errorData =
                await response.json();

            alert(
                errorData.detail ||
                "Failed to create user."
            );

            return;
        }


        const newUser =
            await response.json();


        users.push(newUser);


        userName.value = "";

        userEmail.value = "";


        renderUsers();


    } catch (error) {

        console.error(
            "Error creating user:",
            error
        );

        alert(
            "Backend server is not reachable."
        );
    }
}


// ==========================================
// LOAD PROJECTS
// ==========================================

async function loadProjects() {

    try {

        const response =
            await fetch(
                `${API_URL}/projects`
            );


        if (!response.ok) {
            throw new Error(
                "Failed to load projects"
            );
        }


        projects =
            await response.json();


        renderProjects();


    } catch (error) {

        console.error(
            "Error loading projects:",
            error
        );

        projectsContainer.textContent =
            "Unable to load projects.";
    }
}


// ==========================================
// RENDER PROJECTS
// ==========================================

function renderProjects() {

    projectsContainer.textContent = "";


    if (projects.length === 0) {

        const message =
            document.createElement("p");

        message.textContent =
            "No projects found.";

        projectsContainer.appendChild(message);

        return;
    }


    projects.forEach(function (project) {

        const projectItem =
            document.createElement("div");

        projectItem.className =
            "task-item";


        const name =
            document.createElement("h3");

        name.textContent =
            project.name;


        const owner =
            document.createElement("p");

        owner.textContent =
            `Owner ID: ${project.owner_id}`;


        const id =
            document.createElement("p");

        id.textContent =
            `Project ID: ${project.id}`;


        // ACTIONS
        const actions =
            document.createElement("div");

        actions.className =
            "task-actions";


        // EDIT PROJECT
        const editButton =
            document.createElement("button");

        editButton.textContent =
            "Edit";

        editButton.className =
            "edit-btn";

        editButton.addEventListener(
            "click",
            function () {
                editProject(project.id);
            }
        );


        // DELETE PROJECT
        const deleteButton =
            document.createElement("button");

        deleteButton.textContent =
            "Delete";

        deleteButton.className =
            "delete-btn";

        deleteButton.addEventListener(
            "click",
            function () {
                deleteProject(project.id);
            }
        );


        actions.appendChild(editButton);
        actions.appendChild(deleteButton);


        projectItem.appendChild(name);
        projectItem.appendChild(owner);
        projectItem.appendChild(id);
        projectItem.appendChild(actions);


        projectsContainer.appendChild(
            projectItem
        );
    });
}

// ==========================================
// EDIT PROJECT
// ==========================================

async function editProject(projectId) {

    const project = projects.find(function (item) {
        return item.id === projectId;
    });

    if (!project) {
        return;
    }

    const newName = prompt(
        "Enter new project name:",
        project.name
    );

    if (newName === null) {
        return;
    }

    const name = newName.trim();

    if (!name) {
        alert("Project name cannot be empty.");
        return;
    }

    const newOwnerId = prompt(
        "Enter owner user ID:",
        project.owner_id
    );

    if (newOwnerId === null) {
        return;
    }

    const ownerId = Number(newOwnerId);

    if (!ownerId) {
        alert("Please enter a valid owner ID.");
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/projects/${projectId}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    owner_id: ownerId
                })
            }
        );

        if (!response.ok) {

            const errorData =
                await response.json();

            alert(
                errorData.detail ||
                "Failed to update project."
            );

            return;
        }

        const updatedProject =
            await response.json();

        projects = projects.map(function (item) {

            if (item.id === projectId) {
                return updatedProject;
            }

            return item;
        });

        renderProjects();

    } catch (error) {

        console.error(
            "Error updating project:",
            error
        );

        alert("Unable to update project.");
    }
}


// ==========================================
// DELETE PROJECT
// ==========================================

async function deleteProject(projectId) {

    const confirmed = confirm(
        "Are you sure you want to delete this project?"
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/projects/${projectId}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {

            const errorData =
                await response.json();

            alert(
                errorData.detail ||
                "Failed to delete project."
            );

            return;
        }

        projects = projects.filter(function (project) {
            return project.id !== projectId;
        });

        renderProjects();

    } catch (error) {

        console.error(
            "Error deleting project:",
            error
        );

        alert("Unable to delete project.");
    }
}
// ==========================================
// CREATE PROJECT
// ==========================================

async function createProject(event) {

    event.preventDefault();


    const name =
        projectName.value.trim();

    const ownerId =
        Number(projectOwnerId.value);


    if (!name || !ownerId) {

        alert(
            "Please enter project name and owner ID."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/projects`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        owner_id: ownerId
                    })
                }
            );


        if (!response.ok) {

            const errorData =
                await response.json();

            alert(
                errorData.detail ||
                "Failed to create project."
            );

            return;
        }


        const newProject =
            await response.json();


        projects.push(newProject);


        projectName.value = "";

        projectOwnerId.value = "";


        renderProjects();


    } catch (error) {

        console.error(
            "Error creating project:",
            error
        );

        alert(
            "Backend server is not reachable."
        );
    }
}


// ==========================================
// TASK FORM
// ==========================================

if (taskForm) {

    taskForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            createTask();
        }
    );
}


// ==========================================
// USER FORM
// ==========================================

if (userForm) {

    userForm.addEventListener(
        "submit",
        createUser
    );
}


// ==========================================
// PROJECT FORM
// ==========================================

if (projectForm) {

    projectForm.addEventListener(
        "submit",
        createProject
    );
}


// ==========================================
// SEARCH
// ==========================================

if (searchInput) {

    searchInput.addEventListener(
        "input",
        function () {
            renderTasks();
        }
    );
}


// ==========================================
// PRIORITY FILTER
// ==========================================

if (priorityFilter) {

    priorityFilter.addEventListener(
        "change",
        function () {
            renderTasks();
        }
    );
}


// ==========================================
// STATUS FILTER
// ==========================================

if (statusFilter) {

    statusFilter.addEventListener(
        "change",
        function () {
            renderTasks();
        }
    );
}


// ==========================================
// START APPLICATION
// ==========================================

loadTasks();

loadUsers();

loadProjects();

// ==========================================
// AI QUICK-ADD
// ==========================================

const quickAddForm = document.getElementById("quickAddForm");
const quickAddInput = document.getElementById("quickAddInput");
const quickAddResult = document.getElementById("quickAddResult");

if (quickAddForm) {

    quickAddForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const description =
                quickAddInput.value.trim();

            if (!description) {
                alert("Please enter a task description.");
                return;
            }

            try {

                const response = await fetch(
                    `${API_URL}/tasks/quick-add`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            description: description,
                            project_id: 1
                        })
                    }
                );

                const data =
                    await response.json();

                if (!response.ok) {

                    console.error(
                        "Quick-Add error:",
                        data
                    );

                    alert(
                        data.detail
                            ? JSON.stringify(data.detail)
                            : "Quick-Add failed."
                    );

                    return;
                }

                console.log(
                    "Quick-Add success:",
                    data
                );

                quickAddResult.textContent =
                    "✅ Task created successfully!";

                quickAddInput.value = "";

                await loadTasks();

            } catch (error) {

                console.error(
                    "Quick-Add error:",
                    error
                );

                alert(
                    "Unable to connect to backend."
                );
            }
        }
    );
}