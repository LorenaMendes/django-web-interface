function enableAddStep(){
    var select = document.getElementById("stepSelect");
    var btn = document.getElementById("addStep");

    const step_type = select.options[select.selectedIndex].value;

    if (step_type == "default")
        btn.disabled = true;
    else
        btn.disabled = false;
}

function addNewStep(){
    const select = document.getElementById("stepSelect");
    const btn = document.getElementById("addStep");
    const new_id = "Step-" + genId() + "-";
    const step_type = select.value;
    if (step_type == "default"){
        return;
    }

    insertContainer(new_id, step_type);
    // insertStep(new_id, step_type);    
    btn.disabled = true;
    select.value = "default";
}

function insertContainer(new_id, step_type){
    const [htmlString, new_events] = getStepContainerHtml(new_id, step_type);

    const div = document.createElement('div');
    div.innerHTML = htmlString.trim();

    const stepsContainer = document.getElementById("stepsContainer");
    const stepContainer = document.getElementById("stepMenuContainer");
    stepsContainer.insertBefore(div.firstChild, stepContainer);

    for (var [id, fun, type] of new_events) {
        addEventListener(id, fun, type);
    }
}

function genId(length=8) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}