document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm")
    const dashboard = document.querySelector(".dashboard")
    const tableBody = document.querySelector("#usersTable tbody")
    const searchInput = document.getElementById("searchInput")
  
    if (loginForm) {
      loginForm.addEventListener("submit", async (e) => {
        e.preventDefault()
        const formData = new FormData(loginForm)
        const response = await fetch("/login", {
          method: "POST",
          body: formData
        })
        if (response.redirected) {
          window.location.href = response.url
        } else {
          document.getElementById("loginError").textContent = "Acceso denegado"
        }
      })
    }
  
    async function loadUsers() {
      const res = await fetch("/api/users")
      const users = await res.json()
      renderTable(users)
      searchInput.addEventListener("input", () => {
        const filtered = users.filter(u => u.nombre_completo.toLowerCase().includes(searchInput.value.toLowerCase()) || u.id.toString().includes(searchInput.value))
        renderTable(filtered)
      })
    }
  
    function renderTable(data) {
      tableBody.innerHTML = ""
      data.forEach(u => {
        const tr = document.createElement("tr")
        tr.innerHTML = `
          <td>${u.id}</td>
          <td>${u.nombre_completo}</td>
          <td>${u.curp || "No ingresada"}</td>
          <td>${u.rfc || "No ingresada"}</td>
          <td><button onclick="openUser(${u.id}, '${u.nombre_completo}')">+</button></td>
        `
        tableBody.appendChild(tr)
      })
    }
  
    window.openUser = function(id, nombre) {
      document.getElementById("infoNombre").textContent = `Usuario: ${nombre} (ID: ${id})`
      document.getElementById("uploadDocForm").dataset.userid = id
      document.getElementById("userDetails").classList.remove("hidden")
    }
  
    const uploadForm = document.getElementById("uploadDocForm")
    if (uploadForm) {
      uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault()
        const form = new FormData(uploadForm)
        form.append("user_id", uploadForm.dataset.userid)
        const res = await fetch("/upload/document", {
          method: "POST",
          body: form
        })
        const result = await res.json()
        document.getElementById("docResultado").textContent = JSON.stringify(result, null, 2)
      })
    }
  
    if (dashboard) loadUsers()
  })
  