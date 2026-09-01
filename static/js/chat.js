document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("chat-form");
    const input = document.getElementById("message");
    const messages = document.getElementById("chat-messages");
    const status = document.getElementById("chat-status");
    const sendButton = document.getElementById("send-button");

    const questionCategories =
        document.getElementById("question-categories");

    const questionList =
        document.getElementById("question-list");


    let questions = [];


    function getCookie(name) {

        let cookieValue = null;

        if (document.cookie && document.cookie !== "") {

            const cookies =
                document.cookie.split(";");

            for (let cookie of cookies) {

                cookie = cookie.trim();

                if (
                    cookie.substring(
                        0,
                        name.length + 1
                    ) === name + "="
                ) {

                    cookieValue =
                        decodeURIComponent(
                            cookie.substring(
                                name.length + 1
                            )
                        );

                    break;
                }
            }
        }

        return cookieValue;
    }


    const csrfToken =
        getCookie("csrftoken");


    function addMessage(text, type) {

        const message =
            document.createElement("div");

        message.className =
            `message ${type}-message`;


        const avatar =
            document.createElement("div");

        avatar.className =
            "message-avatar";


        const content =
            document.createElement("div");

        content.className =
            "message-content";


        const strong =
            document.createElement("strong");

        strong.textContent =
            type === "assistant"
                ? "Guide d'Hyrule"
                : "Vous";


        const paragraph =
            document.createElement("p");

        paragraph.textContent =
            text;


        content.appendChild(strong);
        content.appendChild(paragraph);


        message.appendChild(avatar);
        message.appendChild(content);


        messages.appendChild(message);


        messages.scrollTop =
            messages.scrollHeight;
    }


    async function loadQuestions() {

        try {

            const response =
                await fetch(
                    "/api/zelda-questions/"
                );


            if (!response.ok) {

                throw new Error(
                    "Impossible de charger les questions."
                );
            }


            const data =
                await response.json();


            questions =
                data.questions || [];


            createCategories();

            displayQuestions("Toutes");


        } catch (error) {

            console.error(
                "Erreur questions Zelda :",
                error
            );


            questionList.innerHTML = `
                <p class="question-error">
                    Impossible de charger les questions.
                </p>
            `;
        }
    }


    function createCategories() {

        const categories =
            [
                ...new Set(
                    questions
                        .map(
                            question =>
                                question.category
                        )
                        .filter(Boolean)
                )
            ]
            .sort();


        questionCategories.innerHTML = "";


        const allButton =
            document.createElement("button");

        allButton.type = "button";

        allButton.className =
            "question-category active";

        allButton.dataset.category =
            "Toutes";

        allButton.textContent =
            "Toutes";


        questionCategories.appendChild(
            allButton
        );


        categories.forEach(category => {

            const button =
                document.createElement("button");

            button.type = "button";

            button.className =
                "question-category";

            button.dataset.category =
                category;

            button.textContent =
                category;


            questionCategories.appendChild(
                button
            );

        });


        questionCategories
            .querySelectorAll(
                ".question-category"
            )
            .forEach(button => {

                button.addEventListener(
                    "click",
                    () => {

                        questionCategories
                            .querySelectorAll(
                                ".question-category"
                            )
                            .forEach(item => {

                                item.classList.remove(
                                    "active"
                                );

                            });


                        button.classList.add(
                            "active"
                        );


                        displayQuestions(
                            button.dataset.category
                        );

                    }
                );

            });

    }


    function displayQuestions(category) {

        questionList.innerHTML = "";


        const filteredQuestions =
            category === "Toutes"
                ? questions
                : questions.filter(
                    question =>
                        question.category === category
                );


        if (!filteredQuestions.length) {

            questionList.innerHTML = `
                <p class="question-empty">
                    Aucune question dans cette catégorie.
                </p>
            `;

            return;
        }


        filteredQuestions.forEach(question => {

            const card =
                document.createElement("button");


            card.type = "button";

            card.className =
                "question-card";


            card.dataset.question =
                question.question;


            const categoryElement =
                document.createElement("span");

            categoryElement.className =
                "question-card-category";

            categoryElement.textContent =
                question.category;


            const textElement =
                document.createElement("span");

            textElement.className =
                "question-card-text";

            textElement.textContent =
                question.question;


            card.appendChild(
                categoryElement
            );

            card.appendChild(
                textElement
            );


            card.addEventListener(
                "click",
                () => {

                    input.value =
                        question.question;

                    input.focus();

                    input.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });

                }
            );


            questionList.appendChild(card);

        });

    }


    form.addEventListener(
        "submit",
        async event => {

            event.preventDefault();


            const message =
                input.value.trim();


            if (!message) {
                return;
            }


            addMessage(
                message,
                "user"
            );


            input.value = "";


            status.textContent =
                "Le Guide d'Hyrule réfléchit…";


            sendButton.disabled =
                true;


            try {

                const response =
                    await fetch(
                        "/chat/api/",
                        {
                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json",

                                "X-CSRFToken":
                                    csrfToken

                            },

                            body:
                                JSON.stringify({
                                    message: message
                                })

                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        "Erreur du serveur."
                    );

                }


                addMessage(
                    data.answer,
                    "assistant"
                );


                status.textContent = "";


            } catch (error) {

                console.error(
                    "Erreur chatbot :",
                    error
                );


                addMessage(
                    "Impossible de contacter le Guide d'Hyrule pour le moment.",
                    "assistant"
                );


                status.textContent =
                    "Erreur de connexion au serveur.";


            } finally {

                sendButton.disabled =
                    false;

                input.focus();

            }

        }
    );


    loadQuestions();

});