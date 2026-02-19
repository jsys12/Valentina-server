const API_URL = "http://localhost:8000/api/valentines";

// Загрузка опубликованных валентинок
async function loadValentines() {
  try {
    const res = await fetch(API_URL);
    const data = await res.json();

    const container = document.getElementById("valentinesList");
    container.innerHTML = "";

    data.forEach(val => {
      const card = document.createElement("div");
      card.classList.add("card");

      card.innerHTML = `
        <p>❤️ ${val.message}</p>
        <p class="author">— ${val.name}</p>
        <p class="date">${val.created_at}</p>
      `;

      container.appendChild(card);
    });

  } catch (err) {
    console.log("Backend not connected yet");
  }
}

// Отправка формы
async function submitValentine() {

  const message = document.getElementById("message").value;
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const type = document.querySelector('input[name="type"]:checked').value;

  if (!message) {
    alert("Введите текст валентинки 💌");
    return;
  }

  const payload = {
    message: message,
    name: type === "public" ? name : null,
    email: type === "anonymous" ? email : null,
    is_anonymous: type === "anonymous"
  };

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    await res.json();

    const responseMessage = document.getElementById("responseMessage");

    if (type === "anonymous") {
      responseMessage.innerText = "Валентинка отправлена на почту 💌";
      responseMessage.style.color = "green";
    } else {
      responseMessage.innerText = "Валентинка опубликована 💕";
      responseMessage.style.color = "green";
    }

    document.getElementById("message").value = "";
    document.getElementById("name").value = "";
    document.getElementById("email").value = "";

    loadValentines();

  } catch (err) {
    const responseMessage = document.getElementById("responseMessage");
    responseMessage.innerText = "Ошибка соединения с сервером ⚠️";
    responseMessage.style.color = "red";
  }
}

document.addEventListener("DOMContentLoaded", loadValentines);