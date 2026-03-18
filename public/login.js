var login_form = document.getElementById("login-form")
login_form.addEventListener("submit", event => {
    event.preventDefault() // Stop page reloading

    let email = event.target[0].value
    let password = event.target[1].value

    fetch("/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
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
