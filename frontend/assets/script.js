const API_URL = "/api/v1/events";

async function loadValentines() {
  const container = document.getElementById("valentinesList");

  container.innerHTML = `
    <div class="loader-wrapper">
      <div class="loader"></div>
      <p class="loader-text">Загружаем валентинки...</p>
    </div>
  `;

  try {
    const res = await fetch(API_URL);
    const data = await res.json();

    container.innerHTML = "";

    if (data.length === 0) {
      container.innerHTML = `<p class="empty-text">Пока нет опубликованных валентинок 💔</p>`;
      return;
    }

    data.forEach(val => {
      const card = document.createElement("div");
      card.classList.add("card");

      const date = val.dispatch_date
        ? new Date(val.dispatch_date).toLocaleDateString("ru-RU", { day: "numeric", month: "long", year: "numeric" })
        : "";

      card.innerHTML = `
        <p>❤️ ${val.text}</p>
        <div class="card-footer">
          <span class="author">— ${val.author_email}</span>
          <span class="date">${date}</span>
        </div>
      `;

      container.appendChild(card);
    });

  } catch (err) {
    container.innerHTML = `<p class="empty-text">Не удалось загрузить валентинки ⚠️</p>`;
    console.log("Ошибка загрузки валентинок:", err);
  }
}

async function submitValentine() {
  const text = document.getElementById("message").value.trim();
  const authorEmail = document.getElementById("author_email").value.trim();
  const recipientEmail = document.getElementById("email").value.trim();
  const type = document.querySelector('input[name="type"]:checked').value;
  const isPublic = type === "public";

  if (!text) { alert("Введите текст валентинки 💌"); return; }
  if (!authorEmail) { alert("Введите ваш email 💌"); return; }
  if (!recipientEmail) { alert("Введите email получателя 💌"); return; }

  const dispatch_date = new Date().toISOString().slice(0, 19).replace("T", " ");

  const formData = new FormData();
  formData.append("text", text);
  formData.append("author_email", authorEmail);
  formData.append("recipient_email", recipientEmail);
  formData.append("dispatch_date", dispatch_date);
  formData.append("is_public", isPublic);

  const responseMessage = document.getElementById("responseMessage");
  const btn = document.querySelector("button");

  btn.disabled = true;
  btn.textContent = "Отправляем...";

  try {
    const res = await fetch(API_URL, { method: "POST", body: formData });

    if (res.ok) {
      responseMessage.innerText = isPublic ? "Валентинка опубликована 💕" : "Валентинка отправлена на почту 💌";
      responseMessage.style.color = "#d4185f";

      document.getElementById("message").value = "";
      document.getElementById("author_email").value = "";
      document.getElementById("email").value = "";

      loadValentines();
    } else {
      const err = await res.json();
      responseMessage.innerText = "Ошибка: " + (err.detail || "Что-то пошло не так");
      responseMessage.style.color = "#c0392b";
    }

  } catch (err) {
    responseMessage.innerText = "Ошибка соединения с сервером ⚠️";
    responseMessage.style.color = "#c0392b";
  } finally {
    btn.disabled = false;
    btn.textContent = "Отправить 💌";
  }
}

document.addEventListener("DOMContentLoaded", loadValentines);
