function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", function() {
  var searchForm = document.getElementById("search-form");
  searchForm.addEventListener("submit", function(event) {
    event.preventDefault();

    var searchCriterion = document.getElementById("searched").value;
    var searchCategory = document.querySelector("select").value;
    var apiUrl = "";
    var fieldsToDisplay = [];
    console.log("OPÇÃO É: ", searchCategory)
    if (searchCategory === "minutes") {
      apiUrl = "http://127.0.0.1:8000/api/minutes";
      fieldsToDisplay = ["president", "meeting_date"];
    } else if (searchCategory === "templates") {
      apiUrl = "http://127.0.0.1:8000/api/templates";
      fieldsToDisplay = ["title"];
    } else if (searchCategory === "users") {
      apiUrl = "http://127.0.0.1:8000/api/users";
      fieldsToDisplay = ["first_name", "last_name"];
    } else if (searchCategory === "members") {
      apiUrl = "http://127.0.0.1:8000/api/members";
      fieldsToDisplay = ["first_name", "last_name"];
    }

    fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        searched: searchCriterion,
      }),
    })
      .then(function(response) {
        if (!response.ok) {
          throw new Error("Erro na resposta da requisição...");
        }
        return response.json();
      })
      .then(function(data) {
        var results = data.map(function(item) {
          var displayFields = fieldsToDisplay.map(function(field) {
            return item[field];
          });
          return '<p class="fw-light">' + displayFields.join(" ") + '</p>';
        }).join("");
        document.getElementById("search_result").innerHTML = results;
      })
      .catch(function(error) {
        console.error("Erro:", error);
      });
  });
});