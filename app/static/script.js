document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const searchResults = document.getElementById("searchResults");
    const popup = document.getElementById("popup");
    const closePopup = document.getElementById("closePopup");
    const popupDataList = document.getElementById("popupDataList");
    const predictButton = document.getElementById("predictButton");

    const SEARCH_DELAY = 250; // ms de espera antes de consultar o servidor

    let selectedHotel = null;
    let searchTimer = null;
    let inFlight = null; // cancela a busca anterior quando outra comeca

    // Campos que nao interessam na ficha do anuncio.
    const HIDDEN_FIELDS = new Set(["id", "host_id"]);

    function formatLabel(key) {
        return key
            .replace(/_/g, " ")
            .split(" ")
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(" ");
    }

    function formatValue(value) {
        return value === null || value === undefined || value === "" ? "—" : value;
    }

    function renderResults(results) {
        searchResults.innerHTML = "";

        if (results.length === 0) {
            const empty = document.createElement("div");
            empty.className = "no-results";
            empty.textContent = "No results found.";
            searchResults.appendChild(empty);
            return;
        }

        results.forEach(hotel => {
            const item = document.createElement("div");
            item.className = "result-item";
            item.textContent = `${hotel.nome} - ${hotel.bairro_group}`;
            item.setAttribute("role", "option");
            item.tabIndex = 0;

            const select = () => openPopup(hotel);
            item.addEventListener("click", select);
            item.addEventListener("keydown", event => {
                if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    select();
                }
            });

            searchResults.appendChild(item);
        });
    }

    async function runSearch(query) {
        if (inFlight) {
            inFlight.abort();
        }
        inFlight = new AbortController();

        try {
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`, {
                signal: inFlight.signal
            });
            if (!response.ok) {
                throw new Error(`Servidor respondeu ${response.status}`);
            }
            renderResults(await response.json());
        } catch (error) {
            if (error.name !== "AbortError") {
                console.error("Erro ao buscar hotéis:", error);
            }
        }
    }

    searchInput.addEventListener("input", event => {
        const query = event.target.value.trim();

        clearTimeout(searchTimer);
        if (!query) {
            searchResults.innerHTML = "";
            return;
        }

        // Sem o debounce cada tecla digitada virava uma requisição.
        searchTimer = setTimeout(() => runSearch(query), SEARCH_DELAY);
    });

    function openPopup(hotel) {
        selectedHotel = hotel;
        popupDataList.innerHTML = "";

        Object.entries(hotel)
            .filter(([key]) => !HIDDEN_FIELDS.has(key))
            .forEach(([key, value]) => {
                const listItem = document.createElement("li");
                listItem.textContent = `${formatLabel(key)}: ${formatValue(value)}`;
                popupDataList.appendChild(listItem);
            });

        popup.hidden = false;
        predictButton.focus();
    }

    function closeAllPopups() {
        popup.hidden = true;
        if (window.Swal) {
            Swal.close();
        }
    }

    // O X fecha o pop-up. Antes ele disparava a previsão junto, o que fazia
    // o alerta de preço aparecer justamente quando se queria sair da tela.
    closePopup.addEventListener("click", closeAllPopups);

    window.addEventListener("click", event => {
        if (event.target === popup) {
            closeAllPopups();
        }
    });

    document.addEventListener("keydown", event => {
        if (event.key === "Escape" && !popup.hidden) {
            closeAllPopups();
        }
    });

    predictButton.addEventListener("click", async () => {
        if (!selectedHotel) {
            Swal.fire({ icon: "info", title: "Selecione um hotel primeiro." });
            return;
        }

        predictButton.disabled = true;
        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(selectedHotel)
            });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `Servidor respondeu ${response.status}`);
            }

            await Swal.fire({
                title: `<strong>The expected price is ${data.prediction}</strong>`,
                icon: "success",
                html: "<h4>What do you think about this price?</h4>",
                showCloseButton: true,
                focusConfirm: false,
                confirmButtonText: '<i class="fa fa-thumbs-up"></i> Great!',
                confirmButtonAriaLabel: "Thumbs up, great!"
            });
            closeAllPopups();
        } catch (error) {
            console.error("Erro ao enviar dados:", error);
            Swal.fire({
                icon: "error",
                title: "Não foi possível calcular a previsão",
                text: error.message
            });
        } finally {
            predictButton.disabled = false;
        }
    });
});
