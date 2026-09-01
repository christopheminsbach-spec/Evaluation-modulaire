document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("locationMapModal");
    const modalWindow = document.querySelector(".location-map-window");

    const modalName = document.getElementById("modalLocationName");
    const modalRegion = document.getElementById("modalLocationRegion");

    const modalMap = document.getElementById("modalLocationMap");
    const modalLink = document.getElementById("modalLocationLink");

    const closeButton = document.getElementById("closeLocationMap");
    const overlay = document.querySelector(".location-map-overlay");

    const buttons = document.querySelectorAll(
        ".world-location-marker, .world-list-item"
    );


    // =====================================================
    // OUVERTURE
    // =====================================================

    function openLocation(button) {

        const name = button.dataset.locationName;
        const region = button.dataset.locationRegion;
        const map = button.dataset.locationMap;
        const url = button.dataset.locationUrl;

        if (!map) {
            console.error("Aucune carte définie pour :", name);
            return;
        }


        // Informations
        modalName.textContent = name;
        modalRegion.textContent = `Région : ${region}`;


        // =================================================
        // CARTE
        // =================================================

        let mapPath = map;

        /*
         * Si Django retourne :
         * maps/necluda.jpg
         *
         * on ajoute /static/
         */

        if (!mapPath.startsWith("/")) {
            mapPath = `/static/${mapPath}`;
        }

        modalMap.src = mapPath;

        modalMap.alt = `Carte de ${name}`;


        // =================================================
        // LIEN VERS LES QUÊTES
        // =================================================

        modalLink.href = url;


        // =================================================
        // OUVERTURE MODALE
        // =================================================

        modal.classList.remove("is-map-visible");

        modal.setAttribute("aria-hidden", "false");

        document.body.style.overflow = "hidden";

        modal.classList.add("is-open");


        // =================================================
        // ANIMATION DE LA CARTE
        // =================================================

        setTimeout(() => {

            modal.classList.add("is-map-visible");

        }, 250);
    }


    // =====================================================
    // BOUTONS
    // =====================================================

    buttons.forEach((button) => {

        button.addEventListener("click", () => {

            openLocation(button);

        });

    });


    // =====================================================
    // FERMETURE
    // =====================================================

    function closeLocation() {

        modal.classList.remove("is-map-visible");

        setTimeout(() => {

            modal.classList.remove("is-open");

            modal.setAttribute("aria-hidden", "true");

            document.body.style.overflow = "";

            modalMap.src = "";

        }, 300);
    }


    closeButton.addEventListener(
        "click",
        closeLocation
    );


    overlay.addEventListener(
        "click",
        closeLocation
    );


    // =====================================================
    // ESC
    // =====================================================

    document.addEventListener("keydown", (event) => {

        if (
            event.key === "Escape" &&
            modal.classList.contains("is-open")
        ) {

            closeLocation();

        }

    });

});