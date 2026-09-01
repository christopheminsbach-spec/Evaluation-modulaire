document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById(
        "chat-classique-form"
    );

    const input = document.getElementById(
        "chat-classique-message"
    );

    const messages = document.getElementById(
        "chat-messages"
    );

    const status = document.getElementById(
        "chat-classique-status"
    );

    const sendButton = document.getElementById(
        "chat-classique-send"
    );


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


    function escapeHTML(text) {

        const div =
            document.createElement("div");

        div.textContent = text;

        return div.innerHTML;
    }


    function addMessage(
        text,
        type
    ) {

        const message =
            document.createElement("div");

        message.className =
            `message ${type}-message`;


        const avatar =
            document.createElement("div");

        avatar.className =
            "message-avatar";


        const avatarImage =
            document.createElement("img");

        avatarImage.src =
            "/static/css/icons/sheikah-eye.svg";

        avatarImage.alt =
            type === "assistant"
                ? "Assistant"
                : "Vous";


        avatar.appendChild(
            avatarImage
        );


        const content =
            document.createElement("div");

        content.className =
            "message-content";


        const strong =
            document.createElement("strong");

        strong.textContent =
            type === "assistant"
                ? "Assistant"
                : "Vous";


        const paragraph =
            document.createElement("p");

        paragraph.innerHTML =
            escapeHTML(text).replace(
                /\n/g,
                "<br>"
            );


        content.appendChild(
            strong
        );

        content.appendChild(
            paragraph
        );


        message.appendChild(
            avatar
        );

        message.appendChild(
            content
        );


        messages.appendChild(
            message
        );


        messages.scrollTop =
            messages.scrollHeight;
    }


    form.addEventListener(
        "submit",
        async (event) => {

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
                "L'assistant réfléchit…";


            sendButton.disabled =
                true;


            try {

                const response =
                    await fetch(
                        "/chat-classique/api/",
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
                                    message:
                                        message
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


                status.textContent =
                    "";


            } catch (error) {

                console.error(
                    "Erreur chat classique :",
                    error
                );


                addMessage(
                    "Impossible de contacter l'assistant pour le moment.",
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


    messages.scrollTop =
        messages.scrollHeight;


    input.focus();

});