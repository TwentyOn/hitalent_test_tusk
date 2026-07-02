const typeField = document.getElementById('typeField')
const categoryField = document.getElementById('categoryField')
const subCategoryField = document

typeField.addEventListener('change', typeChange)
categoryField.innerHTML = '<option value selected>выберите тип</option>'


async function typeChange(event) {
    cur_option = typeField.options[typeField.selectedIndex].text
    if (cur_option !== '---------') {
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
    } else {
        categoryField.innerHTML = '<option value selected>выберите тип</option>'
    }

}