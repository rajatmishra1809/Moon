// static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    const htmlElement = document.documentElement;
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeToggleIcon = document.getElementById('theme-toggle-icon');

    // Load theme preference from localStorage or default to light
    const currentTheme = localStorage.getItem('theme') || 'light';
    if (currentTheme === 'dark') {
        htmlElement.classList.add('dark');
        htmlElement.classList.remove('light');
        themeToggleIcon.classList.remove('fa-sun', 'text-yellow-300');
        themeToggleIcon.classList.add('fa-moon', 'text-blue-300');
    } else {
        htmlElement.classList.add('light');
        htmlElement.classList.remove('dark');
        themeToggleIcon.classList.remove('fa-moon', 'text-blue-300');
        themeToggleIcon.classList.add('fa-sun', 'text-yellow-300');
    }

    // Toggle theme on button click
    themeToggleBtn.addEventListener('click', () => {
        if (htmlElement.classList.contains('light')) {
            htmlElement.classList.remove('light');
            htmlElement.classList.add('dark');
            themeToggleIcon.classList.remove('fa-sun', 'text-yellow-300');
            themeToggleIcon.classList.add('fa-moon', 'text-blue-300');
            localStorage.setItem('theme', 'dark');
        } else {
            htmlElement.classList.remove('dark');
            htmlElement.classList.add('light');
            themeToggleIcon.classList.remove('fa-moon', 'text-blue-300');
            themeToggleIcon.classList.add('fa-sun', 'text-yellow-300');
            localStorage.setItem('theme', 'light');
        }
    });

    // --- Zodiac Prediction Logic ---
    // This function is called from the onclick attribute in zodiac.html
    window.getZodiacPrediction = async (signKey) => {
        const modal = document.getElementById('prediction-modal');
        const modalSignName = document.getElementById('modal-sign-name');
        const modalPredictionText = document.getElementById('modal-prediction-text');

        try {
            const response = await fetch(`/get_zodiac_prediction/${signKey}`);
            const data = await response.json();

            if (data.success) {
                // Capitalize the first letter of the sign key for display
                const displaySignName = signKey.charAt(0).toUpperCase() + signKey.slice(1);
                modalSignName.textContent = `${displaySignName} - Today's Insight`;
                modalPredictionText.textContent = data.prediction;
                modal.classList.remove('hidden'); // Show the modal
            } else {
                console.error("Failed to get zodiac prediction:", data.message);
                // In a real app, you'd show a user-friendly message here, not an alert.
                // For simplicity, we just log to console.
            }
        } catch (error) {
            console.error("Error fetching zodiac prediction:", error);
        }
    };

    // Close modal when close button is clicked
    const closeModalBtn = document.getElementById('close-modal');
    if (closeModalBtn) { // Check if the element exists (only on zodiac.html)
        closeModalBtn.addEventListener('click', () => {
            document.getElementById('prediction-modal').classList.add('hidden');
        });
        // Close modal when clicking outside of it
        document.getElementById('prediction-modal').addEventListener('click', (e) => {
            if (e.target.id === 'prediction-modal') {
                e.target.classList.add('hidden');
            }
        });
    }

    // --- Tarot Card Logic ---
    // This function is called from the onclick attribute in tarot.html
    window.drawTarotCard = async () => {
        const drawnCardDisplay = document.getElementById('drawn-card-display');
        const drawnCardImage = document.getElementById('drawn-card-image');
        const drawnCardName = document.getElementById('drawn-card-name');
        const drawnCardMeaning = document.getElementById('drawn-card-meaning');
        const cardSelectionArea = document.getElementById('card-selection-area');
        const drawAgainBtn = document.getElementById('draw-again-btn');

        // Hide card selection area and drawn card display initially
        cardSelectionArea.classList.add('hidden');
        drawnCardDisplay.classList.add('hidden');
        drawAgainBtn.classList.add('hidden');


        // Add a loading state or spinner if you want visual feedback during fetch
        // For example, display a "Drawing card..." text

        try {
            const response = await fetch('/draw_tarot_card');
            const data = await response.json();

            drawnCardImage.src = data.image_url;
            drawnCardImage.alt = data.name;
            drawnCardName.textContent = data.name;
            drawnCardMeaning.textContent = data.meaning;

            // Show the drawn card display and the "Draw Again" button
            drawnCardDisplay.classList.remove('hidden');
            drawAgainBtn.classList.remove('hidden');

        } catch (error) {
            console.error("Error drawing tarot card:", error);
            // Re-show the card selection area if an error occurs
            cardSelectionArea.classList.remove('hidden');
            // Display an error message to the user in the UI (e.g., a div for messages)
            // For simplicity, just logging here.
        }
    };

    // Resets the tarot card display to allow drawing a new card
    window.resetTarot = () => {
        const drawnCardDisplay = document.getElementById('drawn-card-display');
        const cardSelectionArea = document.getElementById('card-selection-area');
        const drawAgainBtn = document.getElementById('draw-again-btn');

        drawnCardDisplay.classList.add('hidden'); // Hide drawn card
        drawAgainBtn.classList.add('hidden'); // Hide draw again button
        cardSelectionArea.classList.remove('hidden'); // Show card selection area
    };
});
