document.addEventListener(
    "DOMContentLoaded",
    () => {


        const form =
            document.getElementById(
                "chat-form"
            );


        const input =
            document.getElementById(
                "message"
            );


        const messages =
            document.getElementById(
                "chat-messages"
            );


        const status =
            document.getElementById(
                "chat-status"
            );


        const exportButton =
            document.getElementById(
                "export-pdf"
            );


        const questionList =
            document.getElementById(
                "question-list"
            );


        const searchInput =
            document.getElementById(
                "question-search"
            );


        const categoryFilter =
            document.getElementById(
                "category-filter"
            );



        let conversation_id =
            window.conversationId || null;



        let questions = [];




        // ===============================
        // CSRF DJANGO
        // ===============================

        function getCookie(name){

            let value = null;


            document.cookie
                .split(";")
                .forEach(cookie=>{


                    cookie =
                    cookie.trim();



                    if(
                        cookie.startsWith(
                            name + "="
                        )
                    ){

                        value =
                        decodeURIComponent(
                            cookie.substring(
                                name.length + 1
                            )
                        );

                    }


                });


            return value;

        }





        // ===============================
        // AJOUT MESSAGE
        // ===============================

        function addMessage(
            text,
            type
        ){


            if(!messages)
                return;



            const div =
            document.createElement(
                "div"
            );


            div.className =
            "message " + type;



            div.innerHTML =
            `
            <strong>
            ${
                type === "user-message"
                ?
                "Vous"
                :
                "Guide d'Hyrule"
            }
            </strong>

            <p>
            ${text}
            </p>
            `;



            messages.appendChild(
                div
            );


            messages.scrollTop =
            messages.scrollHeight;


        }






        // ===============================
        // ENVOI MESSAGE CHAT
        // ===============================

        async function sendMessage(
            text
        ){


            if(!text)
                return;



            addMessage(
                text,
                "user-message"
            );



            input.value = "";



            status.innerHTML =
            "Le Guide consulte les archives d'Hyrule...";



            try{


                const response =
                await fetch(

                    "/chat/api/",

                    {

                        method:"POST",


                        headers:{

                            "Content-Type":
                            "application/json",


                            "X-CSRFToken":
                            getCookie(
                                "csrftoken"
                            )

                        },


                        body:
                        JSON.stringify({

                            message:text,


                            conversation_id:
                            conversation_id

                        })

                    }

                );




                const data =
                await response.json();




                if(!response.ok){

                    throw new Error(
                        data.error ||
                        "Erreur serveur"
                    );

                }





                if(
                    data.conversation_id
                ){

                    conversation_id =
                    data.conversation_id;



                    window.conversationId =
                    conversation_id;



                    if(exportButton){

                        exportButton.disabled =
                        false;



                        exportButton.onclick =
                        ()=>{


                            window.location.href =
                            "/chat/pdf/"
                            +
                            conversation_id
                            +
                            "/";


                        };

                    }

                }





                addMessage(
                    data.answer,
                    "assistant-message"
                );



                status.innerHTML="";



            }

            catch(error){


                console.error(
                    error
                );


                status.innerHTML =
                "Erreur de connexion au Guide d'Hyrule.";


                addMessage(
                    "Impossible de contacter le Guide.",
                    "assistant-message"
                );


            }


        }






        // ===============================
        // FORMULAIRE CHAT
        // ===============================


        if(form){


            form.addEventListener(
                "submit",
                (event)=>{


                    event.preventDefault();



                    sendMessage(
                        input.value.trim()
                    );


                }
            );


        }







        // ===============================
        // CHARGEMENT QUESTIONS ZELDA
        // ===============================

        async function loadQuestions(){


            try{


                const response =
                await fetch(
                    "/api/zelda-questions/"
                );



                const data =
                await response.json();



                questions =
                data.questions || [];



                buildCategories();


                displayQuestions(
                    questions
                );


            }


            catch(error){


                console.error(
                    error
                );


                if(questionList){

                    questionList.innerHTML =
                    "Impossible de charger les archives Zelda.";

                }


            }


        }






        // ===============================
        // CREATION CATEGORIES
        // ===============================

        function buildCategories(){


            if(!categoryFilter)
                return;



            categoryFilter.innerHTML =
            `
            <option value="">
            Toutes les catégories
            </option>
            `;



            const categories =
            [
                ...new Set(
                    questions.map(
                        q=>q.category
                    )
                )
            ];



            categories.forEach(
                category=>{


                    const option =
                    document.createElement(
                        "option"
                    );



                    option.value =
                    category;



                    option.textContent =
                    category;



                    categoryFilter.appendChild(
                        option
                    );


                }
            );


        }






        // ===============================
        // AFFICHAGE QUESTIONS
        // ===============================

        function displayQuestions(
            list
        ){


            if(!questionList)
                return;



            questionList.innerHTML="";



            list.forEach(
                item=>{


                    const button =
                    document.createElement(
                        "button"
                    );



                    button.className =
                    "catalog-question";



                    button.innerHTML =
                    `
                    <strong>
                    ${item.category}
                    </strong>

                    <br>

                    ${item.question}
                    `;



                    button.onclick =
                    ()=>{


                        sendMessage(
                            item.question
                        );


                    };



                    questionList.appendChild(
                        button
                    );


                }
            );


        }







        // ===============================
        // RECHERCHE
        // ===============================


        if(searchInput){


            searchInput.addEventListener(
                "input",
                ()=>{


                    const value =
                    searchInput.value
                    .toLowerCase();



                    displayQuestions(

                        questions.filter(
                            q=>

                            q.question
                            .toLowerCase()
                            .includes(value)

                        )

                    );


                }
            );


        }








        // ===============================
        // FILTRE CATEGORIE
        // ===============================


        if(categoryFilter){


            categoryFilter.addEventListener(
                "change",
                ()=>{


                    const value =
                    categoryFilter.value;



                    if(!value){

                        displayQuestions(
                            questions
                        );

                        return;

                    }



                    displayQuestions(

                        questions.filter(
                            q=>

                            q.category === value

                        )

                    );


                }
            );


        }






        // ===============================
        // QUESTIONS PRESENTES DANS HTML
        // ===============================


        document
        .querySelectorAll(
            ".question-card"
        )
        .forEach(
            card=>{


                card.addEventListener(
                    "click",
                    ()=>{


                        const question =
                        card.dataset.question;



                        if(input){

                            input.value =
                            question;


                            form.dispatchEvent(
                                new Event(
                                    "submit"
                                )
                            );

                        }


                    }
                );


            }
        );





        // ===============================
        // DEMARRAGE
        // ===============================

        loadQuestions();


    }
);