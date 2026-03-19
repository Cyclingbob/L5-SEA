var system_id = window.location.pathname.split("/")[2]

var rename_system_btn = document.getElementById("rename-system-btn")
rename_system_btn.addEventListener("click", () => {
    var newname = prompt("Enter a new name for this system")
    if (newname === null) return // user cancelled
    if(newname.length == 0 || newname.length > 254){
        return alert("Invalid name length")
    }
    fetch("/system/" + system_id + "/rename", {
        method: "PATCH",
        body: JSON.stringify({ name: newname }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            document.getElementById("system-name-h1").innerHTML = "System: " + data.name
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
change_desc_btn.addEventListener("click", () => {
    var desc = prompt("Enter a new description for this system", document.getElementById("system-description-p").innerText.substring("Description: ".length))
    if (desc === null) return // user cancelled
    if(desc.length == 0 || desc.length > 65535){
        return alert("Invalid description length")
    }
    fetch("/system/" + system_id + "/description", {
        method: "PATCH",
        body: JSON.stringify({ description: desc }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            document.getElementById("system-description-p").innerHTML = "Description: " + data.description
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
change_category_btn.addEventListener("click", () => {
    var cat = prompt("Enter a new category for this system")
    if (cat === null) return // user cancelled
    if(cat.length == 0 || cat.length > 254){
        return alert("Invalid category length")
    }
    fetch("/system/" + system_id + "/category", {
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

var delete_system_btn = document.getElementById("delete-system-btn")
if(delete_system_btn) delete_system_btn.addEventListener("click", () => { // Not present for non-admins
    var sure = prompt("Are you sure you want to delete this system? Type \"yes\" to confirm.")
    if(sure != "yes"){
        return alert("Aborted delete.")
    }
    fetch("/system/" + system_id, {
        method: "DELETE",
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            alert("System was deleted!")
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
    fetch("/components.json").then(res => res.json()).then(data => {
        fetch(`/system-components/${system_id}.json`).then(res => res.json()).then(systemData => {
            components = data.components
            system_components = systemData.components

            // document.querySelectorAll(".cb-a-checkbox").forEach(cb => {
            //     cb.addEventListener('change', event => {
            //         boxChecked(event, "a", components, system_components)
            //     })
            // })

            // document.querySelectorAll(".cb-b-checkbox").forEach(cb => {
            //     cb.addEventListener('change', event => {
            //         boxChecked(event, "b", components, system_components)
            //     })
            // })
        });    
    })

    document.querySelectorAll(".add-component-btn").forEach(btn => {
        let component_id = btn.id.split("-")[2]

        btn.addEventListener('click', event => {
            fetch(`/system/${system_id}/add-component/${component_id}`, {
                method: "POST"
            }).then(res => res.json()).then(data => {
                if(data.success){
                    alert("System Component was added to the system!")
                    window.location = "/system/" + system_id
                } else {
                    alert(data.error)
                }
            })
        })
    })

    document.querySelectorAll('.remove-component-btn').forEach(btn => {
        let system_component_id = btn.id.split("-")[2]

            btn.addEventListener('click', event => {
            fetch(`/system/remove-component/${system_component_id}`, {
                method: "DELETE"
            }).then(res => res.json()).then(data => {
                if(data.success){
                    alert("System Component was removed from the system")
                    window.location = "/system/" + system_id
                } else {
                    alert(data.error)
                }
            })
        })
    })

    create_connection_form = document.getElementById("connection-builder")
    create_connection_form.addEventListener("submit", event => {
        event.preventDefault() // Stop page reloading

        let system_component_a = event.target[0].value
        let system_component_b = event.target[1].value
        let component_a_label = event.target[2].value
        let component_b_label = event.target[3].value

        fetch("/connection", {
            method: "POST",
            body: JSON.stringify({ system_component_a, system_component_b, component_a_label, component_b_label }),
            headers: {
                'Content-Type': "application/json"
            }
        })
        .then(res => res.json())
        .then(data => {
            if(data.success){
                alert("Added new connection!")
                window.location = window.location.href // reload to update list
            } else {
                if(data.error){
                    alert(data.error)
                } else {
                    alert("Did not receive data from server")
                }
            }
        })
    })

    document.querySelectorAll(".remove-connection-btn").forEach(btn => {

        let connection_id = btn.id.split("-")[2]
        btn.addEventListener('click', event => {
            var sure = prompt("Are you sure you want to delete this system connection? Type \"yes\" to confirm.")
            if(sure != "yes"){
                return alert("Aborted delete.")
            }
            fetch(`/connection/${connection_id}`, {
                method: "DELETE"
            }).then(res => res.json()).then(data => {
                if(data.success){
                    alert("System Connection was removed")
                    window.location = "/system/" + system_id
                } else {
                    alert(data.error)
                }
            })
        })
    })
})