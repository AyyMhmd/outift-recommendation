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
  style: ["0", "1", "2", "3", "4", "5"],
};

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

// hasil untuk output
// Fungsi untuk menampilkan hasil saat tombol diklik
document.querySelector(".btn-primary").addEventListener("click", () => {
    const resultSection = document.getElementById("result-section");
    
    // Memberikan efek loading sederhana
    document.querySelector(".btn-primary").innerText = "Searching...";
    
    setTimeout(() => {
        resultSection.style.display = "block";
        document.querySelector(".btn-primary").innerText = "Find Outfit Recommendations";
        
        // Scroll otomatis ke hasil
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }, 800);
});
