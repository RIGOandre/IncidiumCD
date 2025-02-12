document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const searchResults = document.getElementById("searchResults");
    const popup = document.getElementById("popup");
    const closePopup = document.getElementById("closePopup");
    const popupDataList = document.getElementById("popupDataList");
    const predictButton = document.getElementById("predictButton");

    let selectedHotel = null;

    //  buscar hotéis
    searchInput.addEventListener("input", async (event) => {
        const query = event.target.value.trim().toLowerCase();
        if (!query) {
            searchResults.innerHTML = "";
            return;
        }

        try {
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            const results = await response.json();

            searchResults.innerHTML = "";
            if (results.length === 0) {
                searchResults.innerHTML = "<div>No results found.</div>";
                return;
            }

            results.forEach(hotel => {
                const div = document.createElement("div");
                div.textContent = `${hotel.nome} - ${hotel.bairro_group}`;
                div.style.cursor = "pointer";
                div.addEventListener("click", () => {
                    selectedHotel = hotel;
                    openPopup(hotel);
                });
                searchResults.appendChild(div);
            });
        } catch (error) {
            console.error("Erro ao buscar hotéis:", error);
        }
    });

    // Abrir o pop-up
    function openPopup(hotel) {
        popupDataList.innerHTML = ""; // Limpa o conteúdo anterior

        for (const [key, value] of Object.entries(hotel)) {
            const formattedKey = key
                .replace(/_/g, " ")
                .split(" ")
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(" ");

            const listItem = document.createElement("li");
            listItem.textContent = `${formattedKey}: ${value}`;
            popupDataList.appendChild(listItem);
        }

        popup.style.display = "block"; // Mostra o pop-up
    }

    // Fechar o pop-up com confirmação de preço
    closePopup.addEventListener("click", () => {
        if (!selectedHotel) {
            alert("Selecione um hotel primeiro.");
            return;
        }

        // Enviar dados para previsão
        fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(selectedHotel)
        })
        .then(response => response.json())
        .then(data => {
            // confirmação de preço  SweetAlert2
            Swal.fire({
                title: `<strong>The Expected Price Is ${data.prediction}</strong>`,
                icon: "success",
                html: `
                   <h4>What do you think about this price? </h4>
                `,
                showCloseButton: true,
                showCancelButton: true,
                focusConfirm: false,
                confirmButtonText: `
                  <i class="fa fa-thumbs-up"></i> Great!
                `,
                confirmButtonAriaLabel: "Thumbs up, great!",
                cancelButtonText: `
                Not Great!
                `,
            }).then((result) => {
                closeAllPopups();
            });
        })
        .catch(error => {
            console.error("Erro ao enviar dados:", error);
        });
    });

    // Fechar o pop-up ao clicar fora 
    window.addEventListener("click", (event) => {
        if (event.target === popup) {
            popup.style.display = "none";
        }
    });

    // Enviar dados para previsão
    predictButton.addEventListener("click", () => {
        if (!selectedHotel) {
            alert("Selecione um hotel primeiro.");
            return;
        }

        fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(selectedHotel)
        })
        .then(response => response.json())
        .then(data => {
            Swal.fire({
                title: `<strong>The expected price is ${data.prediction}</strong>`,
                icon: "success",
                html: `
                   <h4>What do you think about this price? </h4>
                `,
                showCloseButton: true,

                focusConfirm: false,
                confirmButtonText: `
                  <i class="fa fa-thumbs-up"></i> Great!
                `,
                confirmButtonAriaLabel: "Thumbs up, great!",

                
            }).then((result) => {

                closeAllPopups();
            });
        })
        .catch(error => {
            console.error("Erro ao enviar dados:", error);
        });
    });

    function closeAllPopups() {
        popup.style.display = "none";

        Swal.close();
    }
});