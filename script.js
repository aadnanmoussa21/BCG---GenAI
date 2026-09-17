
    async function sendMessage() {
        const inputField = document.getElementById('userInput');
        const query = inputField.value.trim();
        if (!query) return;

        const chatBox = document.getElementById('chatBox');
        chatBox.innerHTML += `<div class="message user-message">${query}</div>`;
        inputField.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 
                    'Accept': 'application/json',
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify({ query: query })
            });

            if (!response.ok) {
                throw new Error(`Server status: ${response.status}`);
            }

            const data = await response.json();
            chatBox.innerHTML += `<div class="message bot-message">${data.response}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (error) {
            console.error("Fetch error:", error);
            chatBox.innerHTML += `<div class="message bot-message" style="color:red;">Error: ${error.message}</div>`;
        }
    }

    function handleKeyPress(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    }