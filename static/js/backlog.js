new Sortable(document.getElementById("userstoryLists"), {
  group: "shared",
  animation: 150,
  onEnd: function () {
    checkEmptyBacklogs();
  },
});

function initializeSortableBacklogBoxes() {
  document
    .querySelectorAll(".user-stories")
    .forEach(function (backlogUserStories) {
      new Sortable(backlogUserStories, {
        group: "shared",
        animation: 150,
        filter: ".backlog-title-wrapper", // title-wrapper 드래그 제외
        preventOnFilter: false, // 제외한 요소의 기본 동작 유지
        onAdd: function (event) {
          checkEmptyBacklogs();
        },
        onEnd: function () {
          checkEmptyBacklogs();
        },
      });
    });
}

initializeSortableBacklogBoxes();

function allowDrop(event) {
  event.preventDefault();
}

function drag(event) {
  event.dataTransfer.setData(
    "story_id",
    event.target.getAttribute("data-story-id")
  );
}

function drop(event) {
  event.preventDefault();
  const story_id = event.dataTransfer.getData("story_id");
  const storyElement = document.querySelector(
    `.user-story[data-story-id='${story_id}']`
  );

  if (storyElement) {
    const backlogBox = event.target.closest(".backlog-box");
    const backlogUserStories = event.target.closest(".user-stories");

    if (backlogBox) {
      // Find the .user-stories container inside the backlog box
      const userStoriesContainer = backlogBox.querySelector(".user-stories");

      // If .user-stories container exists, append the story element to it
      if (userStoriesContainer) {
        userStoriesContainer.appendChild(storyElement);
      } else {
        // If .user-stories doesn't exist, create it and append the story
        const newUserStoriesContainer = document.createElement("div");
        newUserStoriesContainer.classList.add("user-stories");
        newUserStoriesContainer.appendChild(storyElement);
        backlogBox.appendChild(newUserStoriesContainer);
      }
    } else {
      // If no backlog box is found, handle creating a new one if needed (this logic can be customized)
      const newBacklogBox = createNewBacklogBox();
      const userStoriesContainer = document.createElement("div");
      userStoriesContainer.classList.add("user-stories");
      userStoriesContainer.appendChild(storyElement);
      newBacklogBox.appendChild(userStoriesContainer);
      document.getElementById("backlogs").appendChild(newBacklogBox);
      initializeSortableBacklogBoxes();
    }

    checkEmptyBacklogs();
  }
}

function createNewBacklogBox() {
  const backlogBox = document.createElement("div");
  backlogBox.classList.add("backlog-box");
  backlogBox.setAttribute("data-backlog-id", Date.now());

  // 백로그 제목과 삭제 버튼을 하나로 묶을 컨테이너 생성
  const titleWrapper = document.createElement("div");
  titleWrapper.classList.add("backlog-title-wrapper");

  const inputField = document.createElement("input");
  inputField.type = "text";
  inputField.placeholder = "백로그 이름 입력";

  const deleteButton = document.createElement("button");
  deleteButton.innerText = "x";
  deleteButton.onclick = () => {
    const backlogId = backlogBox.getAttribute("data-backlog-id");
    if (backlogId) {
      // Move the user stories back to user-container
      const userStories = backlogBox.querySelectorAll(".user-story");
      userStories.forEach((story) => {
        document.getElementById("userstoryLists").appendChild(story);
      });
    }
    backlogBox.remove(); // Remove the backlog box
    checkEmptyBacklogs(); // Check for any empty backlog boxes to remove
  };

  // titleWrapper에 input과 deleteButton을 추가
  titleWrapper.appendChild(inputField);
  titleWrapper.appendChild(deleteButton);

  // backlogBox에 titleWrapper 추가
  backlogBox.appendChild(titleWrapper);

  document.getElementById("backlogs").appendChild(backlogBox);
  return backlogBox;
}

function checkEmptyBacklogs() {
  document.querySelectorAll(".backlog-box").forEach(function (box) {
    if (box.querySelectorAll(".user-story").length === 0) {
      const backlogId = box.getAttribute("data-backlog-id");
      if (backlogId) {
        deleteBacklog(backlogId, false);
      }
      box.remove();
    }
  });
}

function saveBacklogGroup() {
  const backlogGroups = Array.from(
    document.querySelectorAll(".backlog-box")
  ).map((box) => {
    const backlogName = box.querySelector("input").value.trim();
    const storyIds = Array.from(box.querySelectorAll(".user-story")).map(
      (story) => story.getAttribute("data-story-id")
    );
    const backlogId = box.getAttribute("data-backlog-id");
    return { backlogName, storyIds, backlogId };
  });

  const unassignedStoryIds = Array.from(
    document.querySelectorAll(".userstoryLists .user-story")
  ).map((story) => story.getAttribute("data-story-id"));

  for (const group of backlogGroups) {
    if (!group.backlogName) {
      alert("모든 백로그에는 이름이 필요합니다. 이름을 입력해 주세요.");
      return;
    }
  }

  fetch("/backlog/product_backlog/save_groups", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ backlogGroups, unassignedStoryIds }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("백로그 목록이 저장되었습니다.");
        location.reload();
      } else {
        alert("백로그 목록 저장에 실패하였습니다.");
      }
    });
}

function deleteBacklog(backlogId, shouldReload = true) {
  fetch(`/backlog/product_backlog/delete/${backlogId}`, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      if (shouldReload) {
        location.reload();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("서버와의 통신 중 문제가 발생했습니다.");
    });
}

document.querySelectorAll(".user-story").forEach((element) => {
  element.addEventListener("dragstart", drag);
});
