
document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/users")
    .then(res => res.json())
    .then(users => {
      const tbody = document.querySelector("#usersTable tbody")
      users.forEach(u => {
        const row = document.createElement("tr")
        row.innerHTML = `<td>${u.id}</td><td>${u.nombre_completo}</td><td>${u.curp || "No ingresada"}</td><td>${u.rfc || "No ingresada"}</td>`
        tbody.appendChild(row)
      })
    })
})
