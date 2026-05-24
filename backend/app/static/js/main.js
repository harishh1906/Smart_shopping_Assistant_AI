/* ==========================================================================
   SMART SHOPPING ASSISTANT - CLIENT SIDE APP INTERACTION CONTROLLER
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Asynchronously Load AI Generated Marketing Copy on Details page
    const aiDescElement = document.getElementById("generated-description");
    if (aiDescElement) {
        const productId = aiDescElement.dataset.productId;
        if (productId) {
            fetch(`/generate_description/${productId}`)
                .then(response => {
                    if (!response.ok) throw new Error("Failed to fetch description");
                    return response.json();
                })
                .then(data => {
                    // Update layout
                    aiDescElement.innerHTML = `<p class="ai-text-glow">${data.description}</p>`;
                })
                .catch(error => {
                    console.error("❌ Description Engine Exception:", error);
                    aiDescElement.innerText = "The selected clothing item represents a stylish choice from our premium brand catalog. Tailored to fit modern lifestyles and provide long-lasting comfort.";
                });
        }
    }

    // 2. Setup smooth hover micro-interactions
    const cards = document.querySelectorAll(".product-card");
    cards.forEach(card => {
        card.addEventListener("mouseenter", () => {
            card.style.transform = "translateY(-6px)";
        });
        card.addEventListener("mouseleave", () => {
            card.style.transform = "translateY(0)";
        });
    });

    // 3. Prevent multiple form submissions by loading state indicators
    const searchForm = document.querySelector(".search-form");
    if (searchForm) {
        searchForm.addEventListener("submit", () => {
            const submitBtn = searchForm.querySelector("button[type='submit']");
            if (submitBtn) {
                submitBtn.innerHTML = `Searching...`;
                submitBtn.disabled = true;
            }
        });
    }
});
