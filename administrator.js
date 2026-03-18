var create_project_form = document.getElementById("create-project-form")
create_project_form.addEventListener("submit", event => {
    event.preventDefault() // Stop page reloading

    let name = event.target[0].value
    let category = event.target[1].value
    let description = event.target[2].value

    fetch("/create-project", {
        method: "POST",
        body: JSON.stringify({ name, category, description }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            window.location = "/project/" + data.id
            // alert(data.id)
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})

var create_user_form = document.getElementById("create-user-form")
create_user_form.addEventListener("submit", event => {
    event.preventDefault() // Stop page reloading

    let first_name = event.target[0].value
    let surname = event.target[1].value
    let email = event.target[2].value
    let password = event.target[3].value

    fetch("/create-user", {
        method: "POST",
        body: JSON.stringify({ first_name, surname, email, password }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            window.location = "/user/" + data.id
            // alert(data.id)
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})
