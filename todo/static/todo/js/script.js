function del(btn) {
    if (!confirm("Are you sure??")) return;
    let mydata = { id: btn.dataset.id };
    var json_upload = "json_val=" + JSON.stringify(mydata);
    var xhr = new XMLHttpRequest();
    xhr.onload = () => {
      document.querySelector(`#task${btn.dataset.id}`).remove();
    };
    xhr.open("POST", "{% url 'del_task' %}");
    xhr.setRequestHeader(
      "Content-type",
      "application/x-www-form-urlencoded"
    );
    xhr.send(json_upload);
  }
  function mark(btn) {
    let mydata = { id: btn.dataset.id, mark: btn.dataset.mark };
    var json_upload = "json_val=" + JSON.stringify(mydata);
    var xhr = new XMLHttpRequest();
    xhr.onload = () => {
      if (btn.dataset.mark == "True") {
        btn.style.backgroundColor = "white";
        btn.dataset.mark = "False";
      } else {
        btn.style.backgroundColor = "green";
        btn.dataset.mark = "True";
      }
    };
    xhr.open("POST", "{% url 'mark_task' %}");
    xhr.setRequestHeader(
      "Content-type",
      "application/x-www-form-urlencoded"
    );
    // let data_json = JSON.parse(data);
    // console.log(data_json);
    xhr.send(json_upload);
  }
  document.querySelectorAll(".mark").forEach((c) => {
    if (c.dataset.mark == "True") c.style.backgroundColor = "green";
  });
  function add_task() {
    document.querySelector(".add-task").style.display = "flex";
  }
  function close_add_task() {
    document.querySelector(".add-task").style.display = "none";
  }
  document
    .querySelector("#add-task-form")
    .addEventListener("submit", (e) => {
      e.preventDefault();
      var form = e.target;
      var data = new FormData(form);
      var request = new XMLHttpRequest();
      request.onload = () => {
        if (request.status == 200) {
          newadd = JSON.parse(request.response);
          console.log(request.response);
          document.querySelector(".tasks").insertAdjacentHTML(
            "beforeend",
            `<div id="task${newadd.new_task.id}" class="task">
      <div class="task_top">
      <h4>Pr.-${newadd.new_task.priority}</h4>
      <h4>${newadd.new_task.date}</h4>
    </div>
    <div class="section">
      <img src="${newadd.new_task.img}" alt="This is an image" class="task_img" />
      <h3>${newadd.new_task.title}</h3>
    </div>
    <div class="button">
      <button
      style="background-color:white;"
        onclick="mark(this)"
        data-mark="${newadd.new_task.status}"
        data-id="${newadd.new_task.id}"
        id="task${newadd.new_task.id}mark"
        class="mark"
      ></button>
      <div id="task${newadd.new_task.id}open" class="open">
        <button
          style="background-color: rgba(211, 211, 24, 0.959)"
          id="task${newadd.new_task.id}open"
          class="open butt"
        ><a href="{% url 'open' task.id %}">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></button>
        <button
          style="background-color: rgba(207, 54, 54, 0.829)"
          id="task${newadd.new_task.id}del"
          class="del butt"
          data-id="${newadd.new_task.id}"
          onclick="del(this)"
        ><a href="#" style="pointer-events: none;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></button>
      </div>
    </div>
  </div>`
          );
          form.reset();
          document.querySelector(".add-task").style.display = "none";
        }
      };
      request.open("POST", "{% url 'add_task' %}");
      request.send(data);
    });