const taskInput = document.getElementById("task-input");
const taskList = document.getElementById("task-list");
const addTaskForm = document.getElementById("add-task-form");

function addTask(task) {
  console.log(task)
  const li = document.createElement("li");
  li.id = `task-${task.id}`;
  li.classList.toggle("completed", task.completed);
  const textSpan = document.createElement("span");
  textSpan.textContent = task.title;
  li.appendChild(textSpan);
  const deleteButton = document.createElement("button");
  deleteButton.textContent = "Delete";
  deleteButton.addEventListener("click", function () {
    deleteTask(task.id);
  });
  li.appendChild(deleteButton);
  const completedCheckbox = document.createElement("input");
  completedCheckbox.type = "checkbox";
  completedCheckbox.checked = task.completed;
  completedCheckbox.addEventListener("change", function () {
    updateTask(task.id, completedCheckbox.checked);
  });
  li.insertBefore(completedCheckbox, textSpan);
  taskList.appendChild(li);
}

function addTaskToServer(text) {
  fetch("http://localhost:8000/api/tasks", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ title: text, completed: false }),
  })
    .then((response) => response.json())
    .then((data) => {
      addTask(data);
    })
    .catch((error) => console.error(error));
}

function deleteTaskFromServer(id) {
  fetch(`http://localhost:8000/api/tasks/${id}`, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .catch((error) => console.error(error));
}

function deleteTask(id) {
  const li = document.getElementById(`task-${id}`);
  li.remove();
  deleteTaskFromServer(id);
}

function updateTaskOnServer(id, completed) {
  fetch(`http://localhost:8000/api/tasks/${id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ completed: completed }),
  })
    .then((response) => response.json())
    .catch((error) => console.error(error));
}

function updateTask(id, completed) {
  const li = document.getElementById(`task-${id}`);
  li.classList.toggle("completed", completed);
  updateTaskOnServer(id, completed);
}

function getTasksFromServer() {
  fetch("http://localhost:8000/api/tasks")
    .then((response) => response.json())
    .then((data) => {
      data.forEach(addTask);
    })
    .catch((error) => console.error(error));
}

addTaskForm.addEventListener("submit", function (event) {
  event.preventDefault();
  console.log(event)
  const text = taskInput.value.trim();
  console.log(taskInput)
  console.log(text)
  if (text !== "") {
    addTaskToServer(text);
    taskInput.value = "";
  }
});

getTasksFromServer();
