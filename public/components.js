var create_component_form = document.getElementById("create-component-form")
create_component_form.addEventListener("submit", event => {
    event.preventDefault() // Stop page reloading

    let name = event.target[0].value
    let type = event.target[1].value
    let part_number = event.target[2].value
    let unit_cost = event.target[3].value

    fetch("/component", {
        method: "POST",
        body: JSON.stringify({ name, type, part_number, unit_cost }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            alert("Component was created!")
            window.location = "/component/" + data.id
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

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll(".delete-component-btn").forEach(btn => {
        let component_id = btn.id.split("-")[3]

        btn.addEventListener('click', event => {
            fetch(`/component/${component_id}`, {
                method: "DELETE"
            }).then(res => res.json()).then(data => {
                if(data.success){
                    window.location = "/components"
                } else {
                    alert(data.error)
                }
            })
        })
    })
})