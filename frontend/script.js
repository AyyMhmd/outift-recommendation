const OPTIONS = {
  gender: ["Men", "Women", "Boys", "Girls", "Unisex"],
  subcategory: [
    "topwear",
    "bottomwear",
    "innerwear",
    "saree",
    "dress",
    "loungewear and nightwear",
    "apparel set",
    "socks",
  ],
  articletype: [
    "shirts",
    "jeans",
    "track pants",
    "tshirts",
    "tops",
    "bra",
    "sweatshirts",
    "kurtas",
    "waistcoat",
    "shorts",
    "briefs",
    "sarees",
    "innerwear vests",
    "dresses",
    "night suits",
    "skirts",
    "blazers",
    "kurta sets",
    "shrug",
    "trousers",
    "camisoles",
    "boxers",
    "dupatta",
    "capris",
    "bath robe",
    "tunics",
    "jackets",
    "trunk",
    "lounge pants",
    "sweaters",
    "tracksuits",
    "swimwear",
    "nightdress",
    "baby dolls",
    "leggings",
    "kurtis",
    "jumpsuit",
    "suspenders",
    "robe",
    "salwar and dupatta",
    "patiala",
    "stockings",
    "tights",
    "churidar",
    "lounge tshirts",
    "lounge shorts",
    "shapewear",
    "nehru jackets",
    "salwar",
    "jeggings",
    "rompers",
    "booties",
    "lehenga choli",
    "clothing set",
    "rain jacket",
    "belts",
    "suits",
  ],
  basecolour: [
    "navy blue",
    "blue",
    "black",
    "grey",
    "green",
    "purple",
    "white",
    "beige",
    "brown",
    "pink",
    "maroon",
    "red",
    "off white",
    "yellow",
    "charcoal",
    "multi",
    "magenta",
    "orange",
    "sea green",
    "cream",
    "peach",
    "olive",
    "burgundy",
    "grey melange",
    "rust",
    "rose",
    "lime green",
    "teal",
    "khaki",
    "lavender",
    "mustard",
    "coffee brown",
    "skin",
    "turquoise blue",
    "nude",
    "mauve",
    "mushroom brown",
    "tan",
    "gold",
    "taupe",
    "silver",
    "fluorescent green",
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
  season: ["fall", "summer", "winter", "spring"],
  style: ["0", "1", "2", "3", "4", "5"],
};

document.querySelectorAll(".select-box").forEach((box) => {
  const key = box.dataset.key;
  const data = OPTIONS[key];

  box.innerHTML = `
    <div class="relative">
      <input class="select-input" placeholder="${key}" />
      <div class="dropdown hidden"></div>
    </div>
  `;

  const input = box.querySelector("input");
  const dropdown = box.querySelector(".dropdown");

  const render = (list) => {
    dropdown.innerHTML = list
      .map((item) => `<div class="dropdown-item">${item}</div>`)
      .join("");
  };

  input.addEventListener("focus", () => {
    dropdown.classList.remove("hidden");
    render(data);
  });

  input.addEventListener("input", (e) => {
    const val = e.target.value.toLowerCase();
    render(data.filter((d) => d.toLowerCase().includes(val)));
  });

  dropdown.addEventListener("click", (e) => {
    if (e.target.classList.contains("dropdown-item")) {
      input.value = e.target.textContent;
      dropdown.classList.add("hidden");
    }
  });

  document.addEventListener("click", (e) => {
    if (!box.contains(e.target)) dropdown.classList.add("hidden");
  });
});
