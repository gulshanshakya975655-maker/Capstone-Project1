console.log("TaskFlow script.js loaded");

// const API_URL = "http://127.0.0.1:8000";
const API_URL = "https://capstone-project1-ovg9.onrender.com";

// =====================================================
// ELEMENTS
// =====================================================

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

const quickAddForm = document.getElementById("quickAddForm");
const quickAddInput = document.getElementById("quickAddInput");
const quickAddResult = document.getElementById("quickAddResult");

let tasks = [];
let users = [];
let projects = [];


// =====================================================
// CACHE
// =====================================================

const TASK_CACHE_KEY = "taskflow_tasks_cache";
const USER_CACHE_KEY = "taskflow_users_cache";
const PROJECT_CACHE_KEY = "taskflow_projects_cache";


function saveCache(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
        console.error("Cache save error:", error);
    }
}


function loadCache(key) {
    try {
        const data = localStorage.getItem(key);

        if (!data) {
            return null;
        }

        return JSON.parse(data);
    } catch (error) {
        console.error("Cache load error:", error);
        return null;
    }
}


// =====================================================
// ERROR / SUCCESS HELPERS
// =====================================================

function showFieldError(input, message) {

    if (!input) {
        return;
    }

    input.classList.add("input-error");

    let errorElement =
        input.parentElement.querySelector(".field-error");

    if (!errorElement) {

        errorElement = document.createElement("div");

        errorElement.className = "field-error";

        input.parentElement.insertBefore(
            errorElement,
            input.nextSibling
        );
    }

    errorElement.textContent = message;
    errorElement.classList.add("show");
}


function clearFieldError(input) {

    if (!input) {
        return;
    }

    input.classList.remove("input-error");

    const errorElement =
        input.parentElement.querySelector(".field-error");

    if (errorElement) {
        errorElement.textContent = "";
        errorElement.classList.remove("show");
    }
}


function showSuccess(container, message) {

    if (!container) {
        return;
    }

    container.textContent = message;
    container.className = "success-message";

    setTimeout(function () {

        container.textContent = "";
        container.className = "";

    }, 2500);
}


// =====================================================
// AUTH
// =====================================================

const token = localStorage.getItem("taskflow_token");

if (!token) {
    console.warn("No login token found.");
}


// =====================================================
// LOGOUT BUTTON
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    const btn = document.getElementById("logoutBtn");

    if (!btn) {
        console.log("Logout button not found");
        return;
    }

    btn.addEventListener("click", function (event) {

        event.preventDefault();

        console.log("Logout button clicked");

        localStorage.removeItem("taskflow_token");
        localStorage.removeItem("task_cache");
        localStorage.removeItem("user_cache");
        localStorage.removeItem("project_cache");

        window.location.href = "auth.html";
    });

});


// =====================================================
// LOAD TASKS
// =====================================================

async function loadTasks() {

    const cachedTasks = loadCache(TASK_CACHE_KEY);

    if (Array.isArray(cachedTasks)) {

        tasks = cachedTasks;

        renderTasks();
    }

    try {

        const response =
            await fetch(API_URL + "/tasks");

        if (!response.ok) {

            throw new Error(
                "Failed to load tasks"
            );
        }

        tasks = await response.json();

        saveCache(
            TASK_CACHE_KEY,
            tasks
        );

        renderTasks();

    } catch (error) {

        console.error(
            "Error loading tasks:",
            error
        );

        if (!cachedTasks && tasksContainer) {

            tasksContainer.textContent =
                "Unable to load tasks.";
        }
    }
}


// =====================================================
// RENDER TASKS
// =====================================================

function renderTasks() {

    if (!tasksContainer) {
        return;
    }

    const searchText =
        searchInput
            ? searchInput.value.trim().toLowerCase()
            : "";

    const selectedPriority =
        priorityFilter
            ? priorityFilter.value
            : "all";

    const selectedStatus =
        statusFilter
            ? statusFilter.value
            : "all";


    const filteredTasks =
        tasks.filter(function (task) {

            const taskTitle =
                String(task.title || "")
                    .toLowerCase();

            const matchesSearch =
                taskTitle.includes(searchText);

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

        const message =
            document.createElement("p");

        message.textContent =
            "No tasks found.";

        tasksContainer.appendChild(message);

    } else {

        filteredTasks.forEach(function (task) {

            const taskItem =
                document.createElement("div");

            taskItem.className =
                "task-item";


            const title =
                document.createElement("h3");

            title.textContent =
                task.title;


            const priority =
                document.createElement("p");

            priority.textContent =
                "Priority: " +
                task.priority;


            const dueDate =
                document.createElement("p");

            dueDate.textContent =
                "Due Date: " +
                (task.due_date || "Not set");


            const status =
                document.createElement("p");

            status.textContent =
                "Status: " +
                task.status;


            const actions =
                document.createElement("div");

            actions.className =
                "task-actions";


            // EDIT
            const editButton =
                document.createElement("button");

            editButton.type = "button";
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

            completeButton.type = "button";

            if (task.status === "completed") {
                completeButton.textContent =
                    "Mark Pending";
            } else {
                completeButton.textContent =
                    "Complete";
            }

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

            deleteButton.type = "button";
            deleteButton.textContent = "Delete";
            deleteButton.className = "delete-btn";

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


// =====================================================
// TASK SUMMARY
// =====================================================

function updateSummary() {

    const total =
        tasks.length;

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


    if (totalTasks) {
        totalTasks.textContent = total;
    }

    if (pendingTasks) {
        pendingTasks.textContent = pending;
    }

    if (completedTasks) {
        completedTasks.textContent = completed;
    }

    if (highPriorityTasks) {
        highPriorityTasks.textContent =
            highPriority;
    }
}


// =====================================================
// CREATE TASK
// =====================================================

async function createTask() {

    if (!titleInput) {
        return;
    }

    const title =
        titleInput.value.trim();

    const priority =
        priorityInput
            ? priorityInput.value
            : "medium";

    const dueDate =
        dueDateInput
            ? dueDateInput.value
            : "";


    clearFieldError(titleInput);


    if (!title) {

        showFieldError(
            titleInput,
            "Task title is required."
        );

        titleInput.focus();

        return;
    }


    try {

        const response =
            await fetch(
                API_URL + "/tasks",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        title: title,
                        priority: priority,
                        due_date:
                            dueDate || null,
                        status: "pending",

                        // Your current HTML does not
                        // have project selection.
                        project_id: 1
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            showFieldError(
                titleInput,
                data.detail ||
                    "Failed to create task."
            );

            return;
        }


        tasks.push(data);

        saveCache(
            TASK_CACHE_KEY,
            tasks
        );


        titleInput.value = "";


        if (priorityInput) {
            priorityInput.value = "medium";
        }


        if (dueDateInput) {
            dueDateInput.value = "";
        }


        clearFieldError(titleInput);

        renderTasks();

    } catch (error) {

        console.error(
            "Error creating task:",
            error
        );

        showFieldError(
            titleInput,
            "Backend server is not reachable."
        );
    }
}


// =====================================================
// EDIT TASK
// =====================================================

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
        return;
    }


    try {

        const response =
            await fetch(
                API_URL +
                "/tasks/" +
                taskId,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        title:
                            trimmedTitle
                    })
                }
            );


        if (!response.ok) {
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


        saveCache(
            TASK_CACHE_KEY,
            tasks
        );


        renderTasks();

    } catch (error) {

        console.error(
            "Error updating task:",
            error
        );
    }
}


// =====================================================
// UPDATE TASK STATUS
// =====================================================

async function updateTaskStatus(
    taskId,
    currentStatus
) {

    let newStatus;

    if (currentStatus === "completed") {
        newStatus = "pending";
    } else {
        newStatus = "completed";
    }


    try {

        const response =
            await fetch(
                API_URL +
                "/tasks/" +
                taskId,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        status:
                            newStatus
                    })
                }
            );


        if (!response.ok) {
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


        saveCache(
            TASK_CACHE_KEY,
            tasks
        );


        renderTasks();

    } catch (error) {

        console.error(
            "Error updating task:",
            error
        );
    }
}


// =====================================================
// DELETE TASK
// =====================================================

async function deleteTask(taskId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this task?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                API_URL +
                "/tasks/" +
                taskId,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {
            return;
        }


        tasks =
            tasks.filter(function (task) {
                return task.id !== taskId;
            });


        saveCache(
            TASK_CACHE_KEY,
            tasks
        );


        renderTasks();

    } catch (error) {

        console.error(
            "Error deleting task:",
            error
        );
    }
}


// =====================================================
// LOAD USERS
// =====================================================

async function loadUsers() {

    const cachedUsers =
        loadCache(
            USER_CACHE_KEY
        );


    if (Array.isArray(cachedUsers)) {

        users = cachedUsers;

        renderUsers();
    }


    try {

        const response =
            await fetch(
                API_URL + "/users"
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load users"
            );
        }


        users =
            await response.json();


        saveCache(
            USER_CACHE_KEY,
            users
        );


        renderUsers();

    } catch (error) {

        console.error(
            "Error loading users:",
            error
        );


        if (!cachedUsers &&
            usersContainer) {

            usersContainer.textContent =
                "Unable to load users.";
        }
    }
}


// =====================================================
// RENDER USERS
// =====================================================

function renderUsers() {

    if (!usersContainer) {
        return;
    }


    usersContainer.textContent = "";


    if (users.length === 0) {

        const message =
            document.createElement("p");

        message.textContent =
            "No users found.";

        usersContainer.appendChild(
            message
        );

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
            "Email: " +
            user.email;


        const id =
            document.createElement("p");

        id.textContent =
            "User ID: " +
            user.id;


        const actions =
            document.createElement("div");

        actions.className =
            "task-actions";


        const editButton =
            document.createElement("button");

        editButton.type = "button";
        editButton.textContent = "Edit";
        editButton.className = "edit-btn";


        editButton.addEventListener(
            "click",
            function () {
                editUser(user.id);
            }
        );


        const deleteButton =
            document.createElement("button");

        deleteButton.type = "button";
        deleteButton.textContent = "Delete";
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


        usersContainer.appendChild(
            userItem
        );
    });
}


// =====================================================
// CREATE USER
// =====================================================

async function createUser(event) {

    event.preventDefault();


    const name =
        userName.value.trim();

    const email =
        userEmail.value.trim();


    clearFieldError(userName);
    clearFieldError(userEmail);


    if (!name) {

        showFieldError(
            userName,
            "User name is required."
        );

        userName.focus();

        return;
    }


    if (!email) {

        showFieldError(
            userEmail,
            "User email is required."
        );

        userEmail.focus();

        return;
    }


    if (!userEmail.checkValidity()) {

        showFieldError(
            userEmail,
            "Please enter a valid email address."
        );

        userEmail.focus();

        return;
    }


    try {

        const response =
            await fetch(
                API_URL + "/users",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        email: email
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            showFieldError(
                userEmail,
                data.detail ||
                    "Failed to create user."
            );

            return;
        }


        users.push(data);


        saveCache(
            USER_CACHE_KEY,
            users
        );


        userName.value = "";
        userEmail.value = "";


        renderUsers();

    } catch (error) {

        console.error(
            "Error creating user:",
            error
        );


        showFieldError(
            userEmail,
            "Backend server is not reachable."
        );
    }
}


// =====================================================
// EDIT USER
// =====================================================

async function editUser(userId) {

    const user =
        users.find(function (item) {
            return item.id === userId;
        });


    if (!user) {
        return;
    }


    const newName =
        prompt(
            "Enter new user name:",
            user.name
        );


    if (newName === null) {
        return;
    }


    const newEmail =
        prompt(
            "Enter new email:",
            user.email
        );


    if (newEmail === null) {
        return;
    }


    const name =
        newName.trim();

    const email =
        newEmail.trim();


    if (!name || !email) {
        return;
    }


    try {

        const response =
            await fetch(
                API_URL +
                "/users/" +
                userId,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        email: email
                    })
                }
            );


        if (!response.ok) {
            return;
        }


        const updatedUser =
            await response.json();


        users =
            users.map(function (item) {

                if (item.id === userId) {
                    return updatedUser;
                }

                return item;
            });


        saveCache(
            USER_CACHE_KEY,
            users
        );


        renderUsers();

    } catch (error) {

        console.error(
            "Error updating user:",
            error
        );
    }
}


// =====================================================
// DELETE USER
// =====================================================

async function deleteUser(userId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this user?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                API_URL +
                "/users/" +
                userId,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {
            return;
        }


        users =
            users.filter(function (user) {
                return user.id !== userId;
            });


        saveCache(
            USER_CACHE_KEY,
            users
        );


        renderUsers();

    } catch (error) {

        console.error(
            "Error deleting user:",
            error
        );
    }
}


// =====================================================
// LOAD PROJECTS
// =====================================================

async function loadProjects() {

    const cachedProjects =
        loadCache(
            PROJECT_CACHE_KEY
        );


    if (Array.isArray(cachedProjects)) {

        projects =
            cachedProjects;

        renderProjects();
    }


    try {

        const response =
            await fetch(
                API_URL + "/projects"
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load projects"
            );
        }


        projects =
            await response.json();


        saveCache(
            PROJECT_CACHE_KEY,
            projects
        );


        renderProjects();

    } catch (error) {

        console.error(
            "Error loading projects:",
            error
        );


        if (!cachedProjects &&
            projectsContainer) {

            projectsContainer.textContent =
                "Unable to load projects.";
        }
    }
}


// =====================================================
// RENDER PROJECTS
// =====================================================

function renderProjects() {

    if (!projectsContainer) {
        return;
    }


    projectsContainer.textContent = "";


    if (projects.length === 0) {

        const message =
            document.createElement("p");

        message.textContent =
            "No projects found.";

        projectsContainer.appendChild(
            message
        );

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
            "Owner ID: " +
            project.owner_id;


        const id =
            document.createElement("p");

        id.textContent =
            "Project ID: " +
            project.id;


        const actions =
            document.createElement("div");

        actions.className =
            "task-actions";


        const editButton =
            document.createElement("button");

        editButton.type = "button";
        editButton.textContent = "Edit";
        editButton.className =
            "edit-btn";


        editButton.addEventListener(
            "click",
            function () {
                editProject(project.id);
            }
        );


        const deleteButton =
            document.createElement("button");

        deleteButton.type = "button";
        deleteButton.textContent = "Delete";
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


// =====================================================
// CREATE PROJECT
// =====================================================

async function createProject(event) {

    event.preventDefault();


    const name =
        projectName.value.trim();

    const ownerId =
        Number(projectOwnerId.value);


    clearFieldError(projectName);
    clearFieldError(projectOwnerId);


    if (!name) {

        showFieldError(
            projectName,
            "Project name is required."
        );

        projectName.focus();

        return;
    }


    if (!ownerId || ownerId <= 0) {

        showFieldError(
            projectOwnerId,
            "Please enter a valid owner ID."
        );

        projectOwnerId.focus();

        return;
    }


    try {

        const response =
            await fetch(
                API_URL + "/projects",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        owner_id: ownerId
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            showFieldError(
                projectOwnerId,
                data.detail ||
                    "Failed to create project."
            );

            return;
        }


        projects.push(data);


        saveCache(
            PROJECT_CACHE_KEY,
            projects
        );


        projectName.value = "";
        projectOwnerId.value = "";


        renderProjects();

    } catch (error) {

        console.error(
            "Error creating project:",
            error
        );


        showFieldError(
            projectOwnerId,
            "Backend server is not reachable."
        );
    }
}


// =====================================================
// EDIT PROJECT
// =====================================================

async function editProject(projectId) {

    const project =
        projects.find(function (item) {
            return item.id === projectId;
        });


    if (!project) {
        return;
    }


    const newName =
        prompt(
            "Enter new project name:",
            project.name
        );


    if (newName === null) {
        return;
    }


    const name =
        newName.trim();


    if (!name) {
        return;
    }


    const newOwnerId =
        prompt(
            "Enter owner user ID:",
            project.owner_id
        );


    if (newOwnerId === null) {
        return;
    }


    const ownerId =
        Number(newOwnerId);


    if (!ownerId || ownerId <= 0) {
        return;
    }


    try {

        const response =
            await fetch(
                API_URL +
                "/projects/" +
                projectId,
                {
                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        owner_id: ownerId
                    })
                }
            );


        if (!response.ok) {
            return;
        }


        const updatedProject =
            await response.json();


        projects =
            projects.map(function (item) {

                if (item.id === projectId) {
                    return updatedProject;
                }

                return item;
            });


        saveCache(
            PROJECT_CACHE_KEY,
            projects
        );


        renderProjects();

    } catch (error) {

        console.error(
            "Error updating project:",
            error
        );
    }
}


// =====================================================
// DELETE PROJECT
// =====================================================

async function deleteProject(projectId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this project?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                API_URL +
                "/projects/" +
                projectId,
                {
                    method: "DELETE"
                }
            );


        if (!response.ok) {
            return;
        }


        projects =
            projects.filter(function (project) {
                return project.id !== projectId;
            });


        saveCache(
            PROJECT_CACHE_KEY,
            projects
        );


        renderProjects();

    } catch (error) {

        console.error(
            "Error deleting project:",
            error
        );
    }
}


// =====================================================
// AI QUICK ADD
// =====================================================

if (quickAddForm) {

    quickAddForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            const description =
                quickAddInput.value.trim();


            clearFieldError(
                quickAddInput
            );


            if (!description) {

                showFieldError(
                    quickAddInput,
                    "Please enter a task description."
                );

                quickAddInput.focus();

                return;
            }


            try {

                const response =
                    await fetch(
                        API_URL +
                        "/tasks/quick-add",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({
                                description:
                                    description,

                                // Current HTML has
                                // no project selector.
                                project_id: 1
                            })
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    showFieldError(
                        quickAddInput,
                        data.detail
                            ? JSON.stringify(
                                data.detail
                            )
                            : "Quick-Add failed."
                    );

                    return;
                }


                quickAddInput.value = "";

                clearFieldError(
                    quickAddInput
                );


                showSuccess(
                    quickAddResult,
                    "Task created successfully!"
                );


                await loadTasks();

            } catch (error) {

                console.error(
                    "Quick-Add error:",
                    error
                );


                showFieldError(
                    quickAddInput,
                    "Unable to connect to backend."
                );
            }
        }
    );
}


// =====================================================
// FORM EVENTS
// =====================================================

if (taskForm) {

    taskForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            createTask();
        }
    );
}


if (userForm) {

    userForm.addEventListener(
        "submit",
        createUser
    );
}


if (projectForm) {

    projectForm.addEventListener(
        "submit",
        createProject
    );
}


// =====================================================
// SEARCH
// =====================================================

if (searchInput) {

    searchInput.addEventListener(
        "input",
        renderTasks
    );
}


if (priorityFilter) {

    priorityFilter.addEventListener(
        "change",
        renderTasks
    );
}


if (statusFilter) {

    statusFilter.addEventListener(
        "change",
        renderTasks
    );
}


// =====================================================
// START APPLICATION
// =====================================================

loadTasks();
loadUsers();
loadProjects();

console.log("TaskFlow application started");


