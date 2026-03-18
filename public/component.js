var component_id = window.location.pathname.split("/")[2]

var rename_component_btn = document.getElementById("rename-component-btn")
rename_component_btn.addEventListener("click", () => {
    var newname = prompt("Enter a new name for this component")
    if (newname === null) return // user cancelled
    if(newname.length == 0 || newname.length > 254){
        return alert("Invalid name length")
    }
    fetch("/component/" + component_id + "/rename", {
        method: "PATCH",
        body: JSON.stringify({ name: newname }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            document.getElementById("component-name-h1").innerHTML = "Component: " + data.name
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

var change_type_btn = document.getElementById("change-type-btn")
change_type_btn.addEventListener("click", () => {
    var desc = prompt("Enter a new type for this component")
    if (desc === null) return // user cancelled
    if(desc.length == 0 || desc.length > 254){
        return alert("Invalid type length")
    }
    fetch("/component/" + component_id + "/type", {
        method: "PATCH",
        body: JSON.stringify({ type: desc }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            document.getElementById("component-type-p").innerHTML = "Type: " + data.type
            alert("Changed type to " + data.type)
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})

var change_part_number_btn = document.getElementById("change-part-number-btn")
change_part_number_btn.addEventListener("click", () => {
    var pn = prompt("Enter a new category for this system")
    if (pn === null) return // user cancelled
    if(pn.length == 0 || pn.length > 254){
        return alert("Invalid part number length")
    }
    fetch("/component/" + component_id + "/part-number", {
        method: "PATCH",
        body: JSON.stringify({ part_number: pn }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            document.getElementById("component-part-number-p").innerHTML = "Part Number: " + data.part_number
            alert("Changed part_number to " + data.part_number)
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})

var change_unit_cost_btn = document.getElementById("change-unit-cost-btn")
change_unit_cost_btn.addEventListener("click", () => {
    var uc = prompt("Enter a new unit cost for this system")
    if (uc === null) return // user cancelled
    uc = uc.trim()
    var parsed = parseFloat(uc)

    if (uc.length === 0 || Number.isNaN(parsed) || !Number.isFinite(parsed)) {
        return alert("Not a valid float!")
    }

    fetch("/component/" + component_id + "/unit-cost", {
        method: "PATCH",
        body: JSON.stringify({ unit_cost: parseFloat(uc) }),
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            document.getElementById("component-unit-cost-p").innerHTML = "Unit Cost: £" + data.unit_cost
            alert("Changed unit cost to £" + data.unit_cost)
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})


var delete_component_btn = document.getElementById("delete-component-btn")
delete_component_btn.addEventListener("click", () => {
    var sure = prompt("Are you sure you want to delete this system? Type \"yes\" to confirm.")
    if(sure != "yes"){
        return alert("Aborted delete.")
    }
    fetch("/component/" + component_id, {
        method: "DELETE",
        headers: {
            'Content-Type': "application/json"
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            window.location = "/components"
        } else {
            if(data.error){
                alert(data.error)
            } else {
                alert("Did not receive data from server")
            }
        }
    })
})
