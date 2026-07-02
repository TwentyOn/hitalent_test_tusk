const typeField = document.getElementById('typeField')
const categoryField = document.getElementById('categoryField')

typeField.addEventListener('change', typeChange)
categoryField.innerHTML = '<option value selected>выберите тип</option>'


async function typeChange(event) {
    response = await fetch(`http://127.0.0.1:8000/api/dictionary/type/${typeField.value}/categories/`, {
        method: 'GET'
    })
    if (response.ok) {
        body = await response.json()
        categoryField.innerHTML = '<option value selected>---------</option>'
        for (let key in body) {
            const option = document.createElement('option')
            option.value = key
            option.textContent = body[key]
            categoryField.appendChild(option)
        }
    }
}