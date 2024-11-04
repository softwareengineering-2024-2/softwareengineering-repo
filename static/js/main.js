function addNewTodoInput() {
    const addTodo = document.getElementById("add-todo");
    addTodo.style.display = "none";

    const todoList = document.getElementById("todo-list");
    const newTodoItem = document.createElement("li");
    newTodoItem.className = "todo-item";

    const inputField = document.createElement("input");
    inputField.type = "text";
    inputField.className = "todo-input";
    inputField.placeholder = "할 일을 입력하세요";
    inputField.addEventListener("keypress", function(event) {
        if (event.key === "Enter" && inputField.value.trim() !== "") {
            addTodoItem(inputField.value);
            newTodoItem.remove();
            addTodo.style.display = "block";
        }
    });

    newTodoItem.appendChild(inputField);
    todoList.appendChild(newTodoItem);
    inputField.focus();
}

function addTodoItem(text) {
    const todoList = document.getElementById("todo-list");

    const todoItem = document.createElement("li");
    todoItem.className = "todo-item";

    const todoText = document.createElement("span");
    todoText.className = "todo-text";
    todoText.innerText = text;

    const completeButton = document.createElement("button");
    completeButton.className = "todo-complete";
    completeButton.innerText = "완료";
    completeButton.onclick = function() {
        if (completeButton.innerText === "완료") {
            if (todoItem.querySelector(".todo-input")) {
                const editInput = todoItem.querySelector(".todo-input");
                todoText.innerText = editInput.value;
                todoItem.replaceChild(todoText, editInput);
                editButton.innerText = "수정";
            }
            todoText.style.textDecoration = "line-through";
            todoText.style.color = "grey";
            completeButton.innerText = "미완료";
            editButton.style.display = "none"; // 수정 버튼 숨김
        } else {
            todoText.style.textDecoration = "none";
            todoText.style.color = "black";
            completeButton.innerText = "완료";
            editButton.style.display = "inline"; // 수정 버튼 다시 표시
        }
    };

    const editButton = document.createElement("button");
    editButton.className = "todo-edit";
    editButton.innerText = "수정";
    editButton.onclick = function() {
        if (editButton.innerText === "수정") {
            const editInput = document.createElement("input");
            editInput.type = "text";
            editInput.className = "todo-input";
            editInput.value = todoText.innerText;

            editInput.addEventListener("keypress", function(event) {
                if (event.key === "Enter" && editInput.value.trim() !== "") {
                    todoText.innerText = editInput.value;
                    todoItem.replaceChild(todoText, editInput);
                    editButton.innerText = "수정";
                }
            });

            todoItem.replaceChild(editInput, todoText);
            editInput.focus();
            editButton.innerText = "저장";
        } else {
            const editInput = todoItem.querySelector(".todo-input");
            if (editInput && editInput.value.trim() !== "") {
                todoText.innerText = editInput.value;
                todoItem.replaceChild(todoText, editInput);
                editButton.innerText = "수정";
            }
        }
    };

    const deleteButton = document.createElement("button");
    deleteButton.className = "todo-delete";
    deleteButton.innerText = "삭제";
    deleteButton.onclick = function() {
        todoList.removeChild(todoItem);
    };

    todoItem.appendChild(todoText);
    todoItem.appendChild(editButton);
    todoItem.appendChild(completeButton);
    todoItem.appendChild(deleteButton);
    todoList.appendChild(todoItem);
}
