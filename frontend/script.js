// ===========================
// DATA OPTIONS
// ===========================
const data = {
  gender: ["Men", "Women", "Boys", "Girls", "Unisex"],
  subcategory: [
    "apparel set",
    "bottomwear",
    "dress",
    "innerwear",
    "loungewear and nightwear",
    "saree",
    "socks",
    "topwear",
  ],
  articleType: [
    "baby dolls",
    "bath robe",
    "belts",
    "blazers",
    "booties",
    "boxers",
    "bra",
    "briefs",
    "camisoles",
    "capris",
    "churidar",
    "clothing set",
    "dresses",
    "dupatta",
    "innerwear vests",
    "jackets",
    "jeans",
    "jeggings",
    "jumpsuit",
    "kurta sets",
    "kurtas",
    "kurtis",
    "leggings",
    "lehenga choli",
    "lounge pants",
    "lounge shorts",
    "lounge tshirts",
    "nehru jackets",
    "night suits",
    "nightdress",
    "patiala",
    "rain jacket",
    "robe",
    "rompers",
    "salwar",
    "salwar and dupatta",
    "sarees",
    "shapewear",
    "shirts",
    "shorts",
    "shrug",
    "skirts",
    "stockings",
    "suits",
    "suspenders",
    "sweaters",
    "sweatshirts",
    "swimwear",
    "tights",
    "tops",
    "track pants",
    "tracksuits",
    "trousers",
    "trunk",
    "tshirts",
    "tunics",
    "waistcoat",
  ],
  baseColour: [
    "beige",
    "black",
    "blue",
    "brown",
    "burgundy",
    "charcoal",
    "coffee brown",
    "cream",
    "fluorescent green",
    "gold",
    "green",
    "grey",
    "grey melange",
    "khaki",
    "lavender",
    "lime green",
    "magenta",
    "maroon",
    "mauve",
    "multi",
    "mushroom brown",
    "mustard",
    "navy blue",
    "nude",
    "off white",
    "olive",
    "orange",
    "peach",
    "pink",
    "purple",
    "red",
    "rose",
    "rust",
    "sea green",
    "silver",
    "skin",
    "tan",
    "taupe",
    "teal",
    "turquoise blue",
    "white",
    "yellow",
  ],
  usage: [
    "casual",
    "ethnic",
    "formal",
    "sports",
    "smart casual",
    "party",
    "travel",
  ],
  kota: [
    "Jakarta Pusat",
    "Jakarta Utara",
    "Jakarta Selatan",
    "Jakarta Barat",
    "Jakarta Timur",
    "Kepulauan Seribu",
    "Bogor",
    "Depok",
    "Bekasi",
    "Tangerang",
    "Tangerang Selatan"
  ],
};

// ===========================
// BACKEND API URL
// ===========================
const API_BASE_URL = "http://localhost:5000";

// ===========================
// AUTOCOMPLETE DROPDOWNS
// ===========================
document.querySelectorAll(".autocomplete").forEach((input) => {
  const key = input.dataset.key;
  const dropdown = input.nextElementSibling;

  function render(items) {
    dropdown.innerHTML = "";
    items.forEach((item) => {
      const div = document.createElement("div");
      div.textContent = item;
      div.onclick = () => {
        input.value = item;
        dropdown.style.display = "none";
      };
      dropdown.appendChild(div);
    });
    dropdown.style.display = "block";
  }

  input.addEventListener("focus", () => {
    render(data[key]);
  });

  input.addEventListener("input", () => {
    const value = input.value.toLowerCase();
    const filtered = data[key].filter((item) =>
      item.toLowerCase().includes(value)
    );
    render(filtered);
  });

  document.addEventListener("click", (e) => {
    if (!input.parentElement.contains(e.target)) {
      dropdown.style.display = "none";
    }
  });
});

/* SEASON SELECTION */
let selectedSeason = null;
document.querySelectorAll(".season-options div").forEach((item) => {
  item.addEventListener("click", () => {
    document
      .querySelectorAll(".season-options div")
      .forEach((el) => el.classList.remove("active"));
    item.classList.add("active");
    selectedSeason = item.dataset.value;
  });
});

/* GPS LOCATION */
let userLocation = null; // Store lat/lon

document.getElementById("gps-btn").addEventListener("click", () => {
  const gpsBtn = document.getElementById("gps-btn");
  const cityInput = document.querySelector('[data-key="kota"]');

  if (!navigator.geolocation) {
    alert("Geolocation tidak didukung oleh browser anda.");
    return;
  }

  gpsBtn.disabled = true;
  gpsBtn.innerHTML = "⏳";
  cityInput.value = "Mencari lokasi...";

  navigator.geolocation.getCurrentPosition(
    (position) => {
      userLocation = {
        lat: position.coords.latitude,
        lon: position.coords.longitude
      };

      // Update UI
      cityInput.value = "Lokasi Saya (GPS)";
      gpsBtn.innerHTML = "✅";
      gpsBtn.disabled = false;

      // Reset after 3 seconds
      setTimeout(() => {
        gpsBtn.innerHTML = "📍";
      }, 3000);

      console.log("📍 Location acquired:", userLocation);
    },
    (error) => {
      console.error("Error getting location:", error);
      alert("Gagal mengambil lokasi. Pastikan GPS aktif dan izin diberikan.");
      gpsBtn.innerHTML = "📍";
      gpsBtn.disabled = false;
      cityInput.value = "";
      userLocation = null;
    }
  );
});

// ===========================
// GET FORM VALUES
// ===========================
function getFormValues() {
  const cityInput = document.querySelector('[data-key="kota"]').value;

  // If GPS was used but city input cleared manually, reset userLocation
  if (cityInput !== "Lokasi Saya (GPS)" && userLocation) {
    // Optional: keep using GPS if user wants, but typically if they type a city, use the city.
    // For now, if they typed something else, we ignore GPS.
    userLocation = null;
  }

  return {
    gender: document.querySelector('[data-key="gender"]').value,
    subcategory: document.querySelector('[data-key="subcategory"]').value,
    articleType: document.querySelector('[data-key="articleType"]').value,
    baseColour: document.querySelector('[data-key="baseColour"]').value,
    usage: document.querySelector('[data-key="usage"]').value,
    city: userLocation ? null : cityInput, // If userLocation exists, city is optional/ignored by backend
    lat: userLocation ? userLocation.lat : null,
    lon: userLocation ? userLocation.lon : null,
    season: selectedSeason || "summer"
  };
}

// ===========================
// RENDER OUTFIT CARDS
// ===========================
function renderOutfitCards(recommendations, weather) {
  const cardsContainer = document.querySelector(".cards");
  cardsContainer.innerHTML = "";

  // Category display names and colors
  const categoryConfig = {
    top: { name: "Atasan", color: "#f472b6", textColor: "" },
    bottom: { name: "Bawahan", color: "#60a5fa", textColor: "blue-text" },
    outerwear: { name: "Outer", color: "#a78bfa", textColor: "purple-text" },
    footwear: { name: "Alas Kaki", color: "#34d399", textColor: "blue-dark-text" }
  };

  recommendations.forEach((rec) => {
    const config = categoryConfig[rec.category] || { name: rec.category, color: "#888", textColor: "" };

    // Skip if no recommendation (type is none and we don't want to show it)
    const showCard = rec.type !== "none" || rec.category === "outerwear";

    if (showCard) {
      const card = document.createElement("div");
      card.className = "outfit-card";

      const confidenceClass = rec.confidence >= 85 ? "" :
        rec.confidence >= 70 ? "blue-text" : "purple-text";

      const statusText = rec.confidence >= 85 ? "✓ Cocok" :
        rec.confidence >= 70 ? "✓ Trendy" : "✓ Opsional";

      card.innerHTML = `
        <div class="card-tag">${config.name}</div>
        <div class="img-container">
          ${rec.image ?
          `<img src="${rec.image}" alt="${rec.name}" onerror="this.src='https://via.placeholder.com/300x200?text=${encodeURIComponent(rec.name)}'">` :
          `<div class="no-image">Tidak diperlukan</div>`
        }
        </div>
        <div class="card-stats">
          <span class="percentage ${confidenceClass}">${rec.confidence}%</span>
          <span class="check ${confidenceClass}">${statusText}</span>
        </div>
        <p class="card-desc">${rec.reason}</p>
        <p class="card-name"><strong>${rec.name}</strong></p>
      `;

      cardsContainer.appendChild(card);
    }
  });
}

// ===========================
// RENDER WEATHER INFO
// ===========================
function renderWeatherInfo(weather) {
  // Check if weather info section exists, if not create it
  let weatherSection = document.getElementById("weather-info");

  if (!weatherSection) {
    const resultSection = document.getElementById("result-section");
    weatherSection = document.createElement("div");
    weatherSection.id = "weather-info";
    weatherSection.className = "weather-info-card";
    resultSection.insertBefore(weatherSection, resultSection.querySelector(".cards"));
  }

  const iconUrl = `https://openweathermap.org/img/wn/${weather.icon}@2x.png`;

  weatherSection.innerHTML = `
    <div class="weather-display">
      <img src="${iconUrl}" alt="Weather icon" class="weather-icon">
      <div class="weather-details">
        <h3>🌍 ${weather.city}</h3>
        <p class="temp">${weather.temperature}°C</p>
        <p class="desc">${weather.weather_desc}</p>
        <p class="humidity">💧 Kelembaban: ${weather.humidity}%</p>
        <p class="feels">🌡️ Terasa seperti: ${weather.feels_like}°C</p>
      </div>
    </div>
  `;
}

// ===========================
// API CALLS
// ===========================
async function getRecommendations(formData) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/recommend`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching recommendations:", error);
    throw error;
  }
}

async function getWeather(city) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/weather?city=${encodeURIComponent(city)}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching weather:", error);
    throw error;
  }
}

// ===========================
// SHOW ERROR MESSAGE
// ===========================
function showError(message) {
  const resultSection = document.getElementById("result-section");
  resultSection.style.display = "block";
  resultSection.innerHTML = `
    <div class="error-message">
      <h2>⚠️ Oops!</h2>
      <p>${message}</p>
      <p>Pastikan backend server sudah berjalan di <code>http://localhost:5000</code></p>
    </div>
  `;
  resultSection.scrollIntoView({ behavior: 'smooth' });
}

// ===========================
// SHOW LOADING STATE
// ===========================
function showLoading(button) {
  button.disabled = true;
  button.innerHTML = `
    <span class="spinner"></span> Mencari rekomendasi...
  `;
}

function hideLoading(button) {
  button.disabled = false;
  button.innerText = "Find Outfit Recommendations";
}

// ===========================
// MAIN BUTTON HANDLER
// ===========================
document.querySelector(".btn-primary").addEventListener("click", async () => {
  const button = document.querySelector(".btn-primary");
  const resultSection = document.getElementById("result-section");

  // Get form values
  const formData = getFormValues();

  // Validate required fields
  if (!formData.gender) {
    alert("Silakan pilih Gender terlebih dahulu!");
    return;
  }

  if (!formData.city && (!formData.lat || !formData.lon)) {
    alert("Silakan pilih Kota atau gunakan GPS!");
    return;
  }

  // Show loading
  showLoading(button);

  try {
    // Call API
    const result = await getRecommendations(formData);

    if (result.success) {
      // Reset result section
      resultSection.innerHTML = `
        <h2 class="result-title">✨ Recommended Outfits</h2>
        <p class="result-subtitle">Rekomendasi outfit berdasarkan preferensi dan cuaca saat ini:</p>
        <div id="weather-info"></div>
        <div class="cards"></div>
      `;

      // Render weather info
      renderWeatherInfo(result.weather);

      // Render outfit cards
      renderOutfitCards(result.recommendations, result.weather);

      // Show result section
      resultSection.style.display = "block";

      // Scroll to results
      resultSection.scrollIntoView({ behavior: 'smooth' });
    } else {
      showError(result.error || "Terjadi kesalahan saat memproses rekomendasi.");
    }
  } catch (error) {
    console.error("Error:", error);
    showError("Tidak dapat terhubung ke server. Pastikan backend sudah berjalan.");
  } finally {
    hideLoading(button);
  }
});

// ===========================
// ADDITIONAL STYLES (Injected)
// ===========================
const additionalStyles = document.createElement("style");
additionalStyles.textContent = `
  .weather-info-card {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 25px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  }

  .weather-display {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .weather-icon {
    width: 80px;
    height: 80px;
  }

  .weather-details h3 {
    margin: 0 0 5px;
    color: #4b3f5d;
  }

  .weather-details .temp {
    font-size: 32px;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(90deg, #f472b6, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .weather-details .desc {
    text-transform: capitalize;
    margin: 5px 0;
    color: #666;
  }

  .weather-details .humidity,
  .weather-details .feels {
    margin: 3px 0;
    font-size: 14px;
    color: #777;
  }

  .card-name {
    margin-top: 8px;
    font-size: 14px;
    color: #4b3f5d;
  }

  .no-image {
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f0f0f0;
    border-radius: 12px;
    color: #888;
    font-size: 14px;
  }

  .error-message {
    text-align: center;
    padding: 40px;
    background: rgba(255, 200, 200, 0.8);
    border-radius: 18px;
  }

  .error-message h2 {
    color: #c53030;
  }

  .error-message code {
    background: #fff;
    padding: 4px 8px;
    border-radius: 4px;
  }

  .spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid #fff;
    border-radius: 50%;
    border-top-color: transparent;
    animation: spin 0.8s linear infinite;
    margin-right: 8px;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .btn-primary:disabled {
    opacity: 0.8;
    cursor: not-allowed;
  }

  .season-options div.active {
    background: linear-gradient(90deg, #f472b6, #a78bfa);
    color: white;
    border-radius: 12px;
  }

  @media (max-width: 768px) {
    .cards {
      grid-template-columns: repeat(2, 1fr);
    }
    
    .weather-display {
      flex-direction: column;
      text-align: center;
    }
  }

  @media (max-width: 480px) {
    .cards {
      grid-template-columns: 1fr;
    }
  }
`;
document.head.appendChild(additionalStyles);

// ===========================
// INIT: Check Backend Status
// ===========================
async function checkBackendStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/`);
    const data = await response.json();
    console.log("✅ Backend connected:", data);
  } catch (error) {
    console.warn("⚠️ Backend not available. Please start the Flask server.");
  }
}

// Check on page load
checkBackendStatus();
