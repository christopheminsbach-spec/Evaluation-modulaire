document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("message");
  const messages = document.getElementById("chat-messages");
  const status = document.getElementById("chat-status");
  const sendButton = document.getElementById("send-button");
  const typing = document.getElementById("chat-typing");

  const questionsList = document.getElementById("questions-list");
  const questionsEmpty = document.getElementById("questions-empty");
  const questionsCount = document.getElementById("questions-count");
  const questionSearch = document.getElementById("question-search");
  const questionCategory = document.getElementById("question-category");

  const exportButton = document.getElementById("export-pdf-button");
  if (exportButton) {
    exportButton.addEventListener("click", function (event) {
      event.preventDefault();

      fetch("/chat/classique/")
        .then((response) => response.json())
        .then((data) => {
          window.location.href = `/chat/export/${data.conversation_id}/`;
        });
    });
  }

  const QUESTIONS_API = "/api/zelda-questions/";
  const CHAT_API = "/chat/api/";

  let questions = [];

  function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
  }

  function getCookie(name) {
    const cookies = document.cookie.split(";");

    for (const cookie of cookies) {
      const trimmed = cookie.trim();

      if (trimmed.startsWith(`${name}=`)) {
        return decodeURIComponent(trimmed.substring(name.length + 1));
      }
    }

    return null;
  }

  function scrollMessagesToBottom() {
    if (!messages) {
      return;
    }

    messages.scrollTop = messages.scrollHeight;
  }

  function setStatus(text = "", type = "") {
    if (!status) {
      return;
    }

    status.textContent = text;
    status.className = "chat-status";

    if (type) {
      status.classList.add(type);
    }
  }

  function setLoading(loading) {
    if (input) {
      input.disabled = loading;
    }

    if (sendButton) {
      sendButton.disabled = loading;
    }

    if (typing) {
      typing.hidden = !loading;
    }
  }

  function addUserMessage(text) {
    const messageElement = document.createElement("div");

    messageElement.className = "message user-message";

    messageElement.innerHTML = `
            <div class="message-avatar">
                <img
                    src="/static/css/icons/master-sword.svg"
                    alt="Joueur"
                >
            </div>

            <div class="message-content">
                <strong>Vous</strong>
                <p>${escapeHtml(text)}</p>
            </div>
        `;

    messages.appendChild(messageElement);

    scrollMessagesToBottom();
  }

  function addAssistantMessage(text) {
    const messageElement = document.createElement("div");

    messageElement.className = "message assistant-message";

    const formattedText = escapeHtml(text)
      .replace(/\n\n/g, "</p><p>")
      .replace(/\n/g, "<br>");

    messageElement.innerHTML = `
            <div class="message-avatar">
                <img
                    src="/static/css/icons/sheikah-eye.svg"
                    alt="Guide d'Hyrule"
                >
            </div>

            <div class="message-content">
                <strong>Guide d'Hyrule</strong>
                <p>${formattedText}</p>
            </div>
        `;

    messages.appendChild(messageElement);

    scrollMessagesToBottom();
  }

  function renderQuestions() {
    if (!questionsList) {
      return;
    }

    const searchValue = (questionSearch?.value || "").trim().toLowerCase();

    const categoryValue = (questionCategory?.value || "").trim().toLowerCase();

    const filteredQuestions = questions.filter((item) => {
      const questionText = String(item.question || "").toLowerCase();

      const category = String(item.category || "").toLowerCase();

      const matchesSearch =
        !searchValue ||
        questionText.includes(searchValue) ||
        category.includes(searchValue);

      const matchesCategory = !categoryValue || category === categoryValue;

      return matchesSearch && matchesCategory;
    });

    questionsList.innerHTML = "";

    if (questionsCount) {
      questionsCount.textContent = `${filteredQuestions.length} question${filteredQuestions.length > 1 ? "s" : ""}`;
    }

    if (questionsEmpty) {
      questionsEmpty.hidden = filteredQuestions.length !== 0;
    }

    filteredQuestions.forEach((item, index) => {
      const button = document.createElement("button");

      button.type = "button";
      button.className = "question-item";

      const id = item.id ?? index + 1;
      const question = item.question ?? "";
      const category = item.category ?? "";

      button.innerHTML = `
                <span class="question-number">
                    ${String(id).padStart(2, "0")}
                </span>

                <span class="question-text">
                    ${escapeHtml(question)}

                    ${
                      category
                        ? `<span class="question-category">${escapeHtml(category)}</span>`
                        : ""
                    }
                </span>
            `;

      button.addEventListener("click", () => {
        selectQuestion(question);
      });

      questionsList.appendChild(button);
    });
  }

  function populateCategories() {
    if (!questionCategory) {
      return;
    }

    const categories = [
      ...new Set(questions.map((item) => item.category).filter(Boolean)),
    ].sort((a, b) =>
      String(a).localeCompare(String(b), "fr", {
        sensitivity: "base",
      }),
    );

    questionCategory.innerHTML = `
            <option value="">
                Toutes les catégories
            </option>
        `;

    categories.forEach((category) => {
      const option = document.createElement("option");

      option.value = category;
      option.textContent = category;

      questionCategory.appendChild(option);
    });
  }

  function selectQuestion(question) {
    if (!input) {
      return;
    }

    input.value = question;

    input.focus();

    input.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
    });

    setStatus("Question ajoutée au champ du chat.", "success");

    setTimeout(() => {
      setStatus("");
    }, 2500);
  }

  async function loadQuestions() {
    try {
      if (questionsList) {
        questionsList.innerHTML = `
                    <div class="catalog-loading">
                        <div class="catalog-spinner"></div>
                        <span>
                            Chargement du catalogue...
                        </span>
                    </div>
                `;
      }

      const response = await fetch(QUESTIONS_API, {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
        credentials: "same-origin",
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP ${response.status}`);
      }

      const data = await response.json();

      if (Array.isArray(data)) {
        questions = data;
      } else if (Array.isArray(data.questions)) {
        questions = data.questions;
      } else {
        questions = [];
      }

      populateCategories();
      renderQuestions();
    } catch (error) {
      console.error("Erreur lors du chargement des questions :", error);

      if (questionsList) {
        questionsList.innerHTML = `
                    <div class="catalog-loading">
                        <span>
                            Impossible de charger le catalogue.
                        </span>
                    </div>
                `;
      }

      if (questionsCount) {
        questionsCount.textContent = "Catalogue indisponible";
      }
    }
  }

  async function sendMessage(message) {
    const csrfToken = getCookie("csrftoken");

    const headers = {
      "Content-Type": "application/json",
      Accept: "application/json",
    };

    if (csrfToken) {
      headers["X-CSRFToken"] = csrfToken;
    }

    const response = await fetch(CHAT_API, {
      method: "POST",
      headers,
      credentials: "same-origin",
      body: JSON.stringify({
        message: message,
      }),
    });

    let data;

    try {
      data = await response.json();
    } catch {
      throw new Error("Le serveur a retourné une réponse invalide.");
    }

    if (!response.ok) {
      throw new Error(data.error || `Erreur HTTP ${response.status}`);
    }

    return data;
  }

  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      const message = input?.value.trim();

      if (!message) {
        return;
      }

      addUserMessage(message);

      input.value = "";

      setStatus("");
      setLoading(true);

      try {
        const data = await sendMessage(message);

        const answer =
          data.answer || "Je n'ai pas réussi à générer une réponse.";

        addAssistantMessage(answer);

        setStatus("Réponse du Guide d'Hyrule reçue.", "success");
      } catch (error) {
        console.error("Erreur du chat :", error);

        addAssistantMessage(
          "Désolé, le Guide d'Hyrule n'est pas disponible pour le moment.",
        );

        setStatus(error.message || "Une erreur est survenue.", "error");
      } finally {
        setLoading(false);

        if (input) {
          input.focus();
        }
      }
    });
  }

  if (questionSearch) {
    questionSearch.addEventListener("input", renderQuestions);
  }

  if (questionCategory) {
    questionCategory.addEventListener("change", renderQuestions);
  }

  loadQuestions();

  scrollMessagesToBottom();
});
