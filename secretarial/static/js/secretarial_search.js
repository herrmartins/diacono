import {
  getCookie
} from './get_cookie.js';

const categoryDisplayNames = {
  minutes: 'Atas',
  templates: 'Modelos de Atas',
  users: 'Usuários',
  members: 'Membros'

};

document.addEventListener("DOMContentLoaded", function() {
  var searchForm = document.getElementById("search-form");
  searchForm.addEventListener("submit", function(event) {
    event.preventDefault();

    let searchCriterion = document.getElementById("searched").value;
    let searchCategory = document.querySelector("select").value;
    let apiUrl = "/api/search";
    let fieldsToDisplay = [];

    fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          category: searchCategory,
          searched: searchCriterion,
        }),
      })
      .then(function(response) {
        if (!response.ok) {
          throw new Error("Erro na resposta de requisição...");
        }
        return response.json();
      })
      .then(function(data) {
        let resultsContainer = document.getElementById("search_result");
        resultsContainer.innerHTML = "";

        let container = document.createElement("div");
        container.classList.add("container");

        let row = document.createElement("div");
        row.classList.add("row", "justify-content-center");

        let col = document.createElement("div");
        col.classList.add("col-10");

        let card = document.createElement("div");
        card.classList.add("card", "my-4");

        let cardBody = document.createElement("div");
        cardBody.classList.add("card-body");

        let categoryDisplayName = categoryDisplayNames[searchCategory] || searchCategory;

        let categoryHeader = document.createElement("p");
        categoryHeader.classList.add("fs-5", "fw-bold", "mb-3", "d-block");
        categoryHeader.textContent = "Categoria: " + categoryDisplayName;

        cardBody.appendChild(categoryHeader);
        cardBody.appendChild(document.createElement("hr"));

        if (data.length === 0) {
          let noResultsMessage = document.createElement("p");
          noResultsMessage.textContent = "Não há resultados para este critério de busca.";
          cardBody.appendChild(noResultsMessage);
        } else {
          let resultList = document.createElement("ul");
          resultList.classList.add("list-group");

          data.forEach(function(item) {
            let displayFields = "";
            if (searchCategory === "minutes") {
              displayFields = `Presidente: ${item.president} | Data: ${item.meeting_date}`;

              let link = document.createElement("a");
              link.textContent = "Ver Ata";
              link.href = `/secretarial/meeting/detail/${item.id}`;

              let listItem = document.createElement("li");
              listItem.classList.add("list-group-item");
              listItem.appendChild(document.createTextNode(displayFields + " "));
              listItem.appendChild(link);

              resultList.appendChild(listItem);
            } else if (searchCategory === "templates") {
              displayFields = item.title;
            } else if (searchCategory === "users" || searchCategory === "members") {
              displayFields = `${item.first_name} ${item.last_name}`;
            }
          });

          cardBody.appendChild(resultList);
        }

        card.appendChild(cardBody);
        col.appendChild(card);
        row.appendChild(col);
        container.appendChild(row);
        resultsContainer.appendChild(container);
      })
      .catch(function(error) {
        console.error("Error:", error);
      });
  });
});