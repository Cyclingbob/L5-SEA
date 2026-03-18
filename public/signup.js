var signup_form = document.getElementById("signup-form")
signup_form.addEventListener("submit", event => {
    event.preventDefault() // Stop page reloading

    let first_name = event.target[0].value
    let surname = event.target[1].value
    let email = event.target[2].value
    let password = event.target[3].value

    fetch("/signup", {
        method: "POST",
        body: JSON.stringify({ first_name, surname, email, password }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            window.location = "/"
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})
