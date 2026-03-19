var user_id = window.location.pathname.split("/")[2]

var rename_user_btn = document.getElementById("rename-user-btn")
rename_user_btn.addEventListener("click", () => {
    var first_name = prompt("Enter a new first name")
    if (first_name === null) return // user cancelled
    if(first_name.length == 0 || first_name.length > 254){
        return alert("Invalid first name length")
    }
    var surname = prompt("Enter a new first name")
    if (surname === null) return // user cancelled
    if(surname.length == 0 || surname.length > 254){
        return alert("Invalid first name length")
    }
    fetch("/user/" + user_id + "/rename", {
        method: "PATCH",
        body: JSON.stringify({ first_name, surname }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            document.getElementById("user-name-h1").innerHTML = "User: " + data.first_name + " " + data.surname
            alert("Renamed user to " + data.first_name + " " + data.surname)
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})

var change_email_btn = document.getElementById("change-email-btn")
change_email_btn.addEventListener("click", () => {
    var email = prompt("Enter a new email address for this user")
    if (email === null) return // user cancelled
    if(email.length == 0 || email.length > 254){
        return alert("Invalid email length")
    }
    fetch("/user/" + user_id + "/email", {
        method: "PATCH",
        body: JSON.stringify({ email }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            document.getElementById("change-email-p").innerHTML = "Email: " + data.email
            alert("Changed email to " + data.email)
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})

var change_password_btn = document.getElementById("change-password-btn")
change_password_btn.addEventListener("click", () => {
    var pass = prompt("Enter a new password for this user")
    if (pass === null) return // user cancelled
    if(pass.length == 0 || pass.length > 254){
        return alert("Invalid password length")
    }
    fetch("/user/" + user_id + "/password", {
        method: "PATCH",
        body: JSON.stringify({ password: pass }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            alert("Changed password successfully!")
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})

var delete_user_btn = document.getElementById("delete-user-btn")
delete_user_btn.addEventListener("click", () => {
    var sure = prompt("Are you sure you want to delete this user? Type \"yes\" to confirm.")
    if(sure != "yes"){
        return alert("Aborted delete.")
    }
    fetch("/user/" + user_id, {
        method: "DELETE",
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            alert("User was deleted!")
            window.location = "/admin"
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})