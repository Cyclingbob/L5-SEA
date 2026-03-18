var project_id = window.location.pathname.split("/")[2]

var create_system_form = document.getElementById("create-system-form")
if (create_system_form) create_system_form.addEventListener("submit", event => {
    event.preventDefault() // Stop page reloading

    let name = event.target[0].value
    let category = event.target[1].value
    let description = event.target[2].value
    let project_id = event.target[4].value //3 is the submit button.

    fetch("/create-system", {
        method: "POST",
        body: JSON.stringify({ name, category, description, project_id }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            window.location = "/system/" + data.id
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

var rename_project_btn = document.getElementById("rename-project-btn")
if(rename_project_btn) rename_project_btn.addEventListener("click", () => {
    var newname = prompt("Enter a new name for this project")
    if (newname === null) return // user cancelled
    if(newname.length == 0 || newname.length > 254){
        return alert("Invalid name length")
    }
    fetch("/project/" + project_id + "/rename", {
        method: "PATCH",
        body: JSON.stringify({ name: newname }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            document.getElementById("project-name-h1").innerHTML = "Project: " + data.name
            alert("Renamed to " + data.name)
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})

var change_desc_btn = document.getElementById("change-description-btn")
if (change_desc_btn) change_desc_btn.addEventListener("click", () => {
    var desc = prompt("Enter a new description for this project", document.getElementById("project-description-p").innerText.substring("Description: ".length))
    if (desc === null) return // user cancelled
    if(desc.length == 0 || desc.length > 65535){
        return alert("Invalid description length")
    }
    fetch("/project/" + project_id + "/description", {
        method: "PATCH",
        body: JSON.stringify({ description: desc }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            document.getElementById("project-description-p").innerHTML = "Description: " + data.description
            alert("Changed description to " + data.description)
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})

var change_category_btn = document.getElementById("change-category-btn")
if(change_category_btn) change_category_btn.addEventListener("click", () => {
    var cat = prompt("Enter a new category for this project")
    if (cat === null) return // user cancelled
    if(cat.length == 0 || cat.length > 254){
        return alert("Invalid category length")
    }
    fetch("/project/" + project_id + "/category", {
        method: "PATCH",
        body: JSON.stringify({ category: cat }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            document.getElementById("change-category-p").innerHTML = "Category: " + data.category
            alert("Changed description to " + data.category)
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})

var delete_project_btn = document.getElementById("delete-project-btn")
if(delete_project_btn) delete_project_btn.addEventListener("click", () => {
    var sure = prompt("Are you sure you want to delete this project? Type \"yes\" to confirm.")
    if(sure != "yes"){
        return alert("Aborted delete.")
    }
    fetch("/project/" + project_id, {
        method: "DELETE",
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
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

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll(".add-project-user-btn").forEach(btn => {
        let user_id = btn.id.split("-")[3]

        btn.addEventListener('click', event => {
            var role = prompt("Enter a new role for this user")
            if (role === null) return // user cancelled
            if(role.length == 0 || role.length > 254){
                return alert("Invalid role length")
            }
            fetch(`/project/${project_id}/add-user/${user_id}`, {
                method: "POST",
                headers: {
                    'Content-Type': "application/json"
                },
                body: JSON.stringify({
                    role
                })
            }).then(res => res.json()).then(data => {
                if(data.success){
                    window.location = "/project/" + project_id
                } else {
                    if(data.error){
                        alert(data.error)
                    } else {
                        alert(JSON.stringify(data))
                    }
                }
            })
        })
    })
    document.querySelectorAll(".remove-project-user-btn").forEach(btn => {
        let user_id = btn.id.split("-")[3]

        btn.addEventListener('click', event => {
            fetch(`/project/${project_id}/del-user/${user_id}`, {
                method: "DELETE",
            }).then(res => res.json()).then(data => {
                if(data.success){
                    window.location = "/project/" + project_id
                } else {
                    if(data.error){
                        alert(data.error)
                    } else {
                        alert(JSON.stringify(data))
                    }
                }
            })
        })
    })
})
