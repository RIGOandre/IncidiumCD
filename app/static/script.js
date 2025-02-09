document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const searchResults = document.getElementById("searchResults");
    const selectedData = document.getElementById("selectedData");
    const selectedDataList = document.getElementById("selectedDataList");
    const predictButton = document.getElementById("predictButton");

    let selectedHotel = null;

    // buscar hotéis
    searchInput.addEventListener("input", async (event) => {
        const query = event.target.value.trim().toLowerCase(); // Converte a consulta para minúsculas
        if (!query) {
            searchResults.innerHTML = "";
            return;
        }

        try {
            // requisição Flask
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            const results = await response.json();

            // Exibir resultados
            searchResults.innerHTML = "";
            if (results.length === 0) {
                searchResults.innerHTML = "<div> No results found. </div>";
                return;
            }

            results.forEach(hotel => {
                const div = document.createElement("div");
                div.textContent = `${hotel.nome} - ${hotel.bairro_group}`;
                div.style.cursor = "pointer";
                div.addEventListener("click", () => {
                    selectedHotel = hotel;
                    displaySelectedData(hotel);
                });
                searchResults.appendChild(div);
            });
        } catch (error) {
            console.error("Erro ao buscar hotéis:", error);
        }
    });

    // exibir dados 
    function displaySelectedData(hotel) {
        selectedData.style.display = "block";
        selectedDataList.innerHTML = "";

        for (const [key, value] of Object.entries(hotel)) {
            const listItem = document.createElement("li");
            listItem.textContent = `${key}: ${value}`;
            selectedDataList.appendChild(listItem);
        }
    }

    //  dados para previsão
    predictButton.addEventListener("click", () => {
        if (!selectedHotel) {
            alert("Selecione um hotel primeiro.");
            return;
        }

        //  dados ao servidor Flask
        fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(selectedHotel)
        })
        .then(response => response.json())
        .then(data => {
            alert(`Preço Previsto: ${data.prediction}`);
        })
        .catch(error => {
            console.error("Erro ao enviar dados:", error);
        });
    });
});

