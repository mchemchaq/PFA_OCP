const FASTAPI_URL = "http://localhost:8000"; // Ensure this matches your backend URL

let fullContractText = null; // Stores the full text for chatbot

document.addEventListener("DOMContentLoaded", () => {
    const pdfUpload = document.getElementById("pdfUpload");
    const extractButton = document.getElementById("extractButton");
    const uploadStatus = document.getElementById("uploadStatus");
    const loadingIndicator = document.getElementById("loadingIndicator");
    const extractedDataDisplay = document.getElementById("extractedData");
    const downloadCsvButton = document.getElementById("downloadCsvButton");

    const chatMessages = document.getElementById("chatMessages");
    const chatInput = document.getElementById("chatInput");
    const sendMessageButton = document.getElementById("sendMessageButton");
    const chatStatus = document.getElementById("chatStatus");

    // --- File Upload and Extraction ---
    extractButton.addEventListener("click", async () => {
        const file = pdfUpload.files[0];
        if (!file) {
            uploadStatus.className = "status-message error";
            uploadStatus.textContent = "Please select a PDF file first.";
            return;
        }

        uploadStatus.textContent = ""; // Clear previous status
        extractedDataDisplay.innerHTML = ""; // Clear previous results
        downloadCsvButton.style.display = 'none';
        fullContractText = null; // Reset full contract text

        loadingIndicator.style.display = 'block'; // Show loading

        const formData = new FormData();
        formData.append("pdf_file", file);

        try {
            const response = await fetch(`${FASTAPI_URL}/extract/`, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const extracted = data.extracted_data;
            fullContractText = data.full_text; // Store for chatbot

            uploadStatus.className = "status-message success";
            uploadStatus.textContent = "Information extracted successfully!";
            
            displayExtractedData(extracted);
            setupDownloadCsv(extracted, file.name);
            
            chatStatus.className = "status-message success";
            chatStatus.textContent = "Chatbot enabled! You can now ask questions about the contract.";
            chatInput.disabled = false;
            sendMessageButton.disabled = false;

        } catch (error) {
            uploadStatus.className = "status-message error";
            uploadStatus.textContent = `Error: ${error.message}. Please ensure the backend is running.`;
            chatStatus.className = "status-message error";
            chatStatus.textContent = "Chatbot disabled due to extraction error.";
            chatInput.disabled = true;
            sendMessageButton.disabled = true;
        } finally {
            loadingIndicator.style.display = 'none'; // Hide loading
        }
    });

    function displayExtractedData(data) {
        let html = `
            <div><strong>Contract Number:</strong> ${data["Contract Number"] || 'Not found'}</div>
            <div><strong>Client:</strong> ${data["Client"] || 'Not found'}</div>
            <div><strong>Supplier:</strong> ${data["Supplier"] || 'Not found'}</div>
            <div><strong>Object:</strong> ${data["Object"] || 'Not found'}</div>
            <div><strong>Total Amount:</strong> ${data["Total Amount"] || 'Not found'}</div>
            <div><strong>Currency:</strong> ${data["Currency"] || 'Not found'}</div>
            <div><strong>Location:</strong> ${data["Location"] || 'Not found'}</div>
            <h3>Complete Results Table</h3>
            <table>
                <thead>
                    <tr>
                        <th>Contract Number</th>
                        <th>Client</th>
                        <th>Supplier</th>
                        <th>Object</th>
                        <th>Date</th>
                        <th>Total Amount</th>
                        <th>Currency</th>
                        <th>Location</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>${data["Contract Number"] || 'N/A'}</td>
                        <td>${data["Client"] || 'N/A'}</td>
                        <td>${data["Supplier"] || 'N/A'}</td>
                        <td>${data["Object"] || 'N/A'}</td>
                        <td>${data["Date"] || 'N/A'}</td>
                        <td>${data["Total Amount"] || 'N/A'}</td>
                        <td>${data["Currency"] || 'N/A'}</td>
                        <td>${data["Location"] || 'N/A'}</td>
                    </tr>
                </tbody>
            </table>
        `;
        extractedDataDisplay.innerHTML = html;
    }

    function setupDownloadCsv(data, fileName) {
        const headers = ["Contract Number", "Client", "Supplier", "Object", "Date", "Total Amount", "Currency", "Location"];
        const row = headers.map(header => JSON.stringify(data[header] || "")).join(",");
        const csvContent = "data:text/csv;charset=utf-8," + headers.join(",") + "\n" + row;
        
        downloadCsvButton.href = encodeURI(csvContent);
        downloadCsvButton.download = `contract_info_${fileName.replace(".pdf", ".csv")}`;
        downloadCsvButton.style.display = 'block';
    }


    // --- Chatbot Functionality ---
    sendMessageButton.addEventListener("click", handleChat);
    chatInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            handleChat();
        }
    });

    function addMessageToChat(message, role) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message", role);
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom
    }

    async function handleChat() {
        const prompt = chatInput.value.trim();
        if (!prompt) return;

        if (!fullContractText) {
            chatStatus.className = "status-message error";
            chatStatus.textContent = "Please upload a PDF and extract information first.";
            return;
        }

        addMessageToChat(prompt, "user");
        chatInput.value = ""; // Clear input

        chatStatus.textContent = "AI is thinking...";
        chatStatus.className = "status-message success"; // Temporarily use success for thinking
        sendMessageButton.disabled = true; // Disable until response

        try {
            const response = await fetch(`${FASTAPI_URL}/chat/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    full_contract_text: fullContractText,
                    question: prompt,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            const answer = data.answer || "Sorry, I couldn't find a direct answer to that question in the document.";
            addMessageToChat(answer, "assistant");
            chatStatus.textContent = ""; // Clear status
            chatStatus.className = "status-message"; // Reset class
        } catch (error) {
            chatStatus.className = "status-message error";
            chatStatus.textContent = `Error during chat: ${error.message}`;
            addMessageToChat(`Error: ${error.message}`, "assistant");
        } finally {
            sendMessageButton.disabled = false; // Re-enable send button
            chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom again
        }
    }

    // Initial state for chatbot: disabled until contract is extracted
    chatInput.disabled = true;
    sendMessageButton.disabled = true;
    chatStatus.className = "status-message warning";
    chatStatus.textContent = "Upload a PDF and extract information to enable the chatbot.";
});