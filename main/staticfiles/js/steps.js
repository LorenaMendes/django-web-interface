function ShowIframe() {

    var iframe_element = document.getElementById("myIframe");
    
    if (iframe_element.style.display === "none"){
        iframe_element.style.display = "block";
        document.getElementById("myButton").innerText = "Hide Website";
    }
    else{
        iframe_element.style.display = "none";
        document.getElementById("myButton").innerText = "Show Website";
    }
}

function enableAddStep(){
    var select = document.getElementById("stepMenu");
    var btn = document.getElementById("addStep");

    const step_type = select.options[select.selectedIndex].value;

    if (step_type == "default")
        btn.disabled = true;
    else
        btn.disabled = false;
}

function addNewStep(){
    const select = document.getElementById("stepMenu");
    const btn = document.getElementById("addStep");
    const new_id = "Step-" + genId() + "-";
    const step_type = select.value;
    if (step_type == "default"){
        return;
    }

    insertContainer(new_id, step_type);
    insertStep(new_id, step_type);    
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

function getStepContainerHtml(new_id, step_type){
    const new_container_id = new_id + "Container";
    return [
        `
        <div class=\"stepContainer row\" id=\"${new_container_id}\" stepType="${step_type}">
            <div class=\"col-1 indentContainer\"></div>
            <div class=\"col\">
                <div class=\"stepStuff row\">
                </div>
                <div class=\"row justify-content-end manageSteps\">
                    <div class=\"col-2\">Gerenciar Passo:</div>
                    <div class=\"col-1\">
                        <span
                            id=\"dedent${new_container_id}\"
                            class=\"badge badge-light clickableSpan\"
                        >
                            <img src=\"{% static \"icons/arrow-left-black.svg\" %}\" alt=\"Selecionar\"></img>
                        </span>
                    </div>
                    <div class=\"col-1\">
                        <span
                            id=\"indent${new_container_id}\"
                            class=\"badge badge-light clickableSpan\"
                        >
                        <img src=\"{% static \"icons/arrow-right-black.svg\" %}\" alt=\"Selecionar\"></img>
                        </span>
                    </div>
                    <div class=\"col-1\">
                        <span
                            id=\"moveStepUp${new_container_id}\"
                            class=\"badge badge-light clickableSpan\"
                        >
                        <img src=\"{% static \"icons/arrow-up-black.svg\" %}\" alt=\"Selecionar\"></img>
                        </span>
                    </div>
                    <div class=\"col-1\">
                        <span
                            id=\"moveStepDown${new_container_id}\"
                            class=\"badge badge-light clickableSpan\"
                        >
                        <img src=\"/home/lorena/Django/interface/main/staticfiles/icons/arrow-down-black.svg\" alt=\"Selecionar\"></img>
                        </span>
                    </div>
                    <div class=\"col-1\">
                        <span
                            id=\"deleteElement${new_container_id}\"
                            class=\"badge badge-light clickableSpan\"
                        >
                        <img src=\"{% static \"x.svg\" %}\" alt=\"Selecionar\"></img>
                        </span>
                    </div>
                </div>
            </div>
        </div>    
        `, 
        [
            ["dedent"+new_container_id, function(){dedentStep(new_container_id);}, "click"], 
            ["indent"+new_container_id, function(){indentStep(new_container_id);}, "click"], 
            ["moveStepUp"+new_container_id, function(){moveStepUp(new_container_id);}, "click"], 
            ["moveStepDown"+new_container_id, function(){moveStepDown(new_container_id);}, "click"], 
            ["deleteElement"+new_container_id, function(){deleteElement(new_container_id);}, "click"], 

        ]
    ];
}

function insertStep(new_id, step_type) {
    var inner_elements = ""
    if (step_type == "default") {
        console.log("ERROR: Received default option. Should not fall here")
        return "";
    } else if (step_type == "click") {
        [inner_elements, new_events] = getClickStepHtml(new_id);
    } else if (step_type == "select") {
        [inner_elements, new_events] = getSelectStepHtml(new_id);
    } else if (step_type == "table") {
        [inner_elements, new_events] = getSaveTableHtml(new_id);
    } else if (step_type == "save") {
        [inner_elements, new_events] = getSaveInfoHtml(new_id);
    } else if (step_type == "iframe") {
        [inner_elements, new_events] = getIFrameStepHtml(new_id);
    } else if (step_type == "download") {
        [inner_elements, new_events] = getDownloadHtml(new_id);
    } else if (step_type == "pages") {
        [inner_elements, new_events] = getPaginationHtml(new_id);
    } else if (step_type == "captcha") {
        [inner_elements, new_events] = getCaptchaHtml(new_id);
    } else if (step_type == "if") {
        [inner_elements, new_events] = getIfHtml(new_id);
    } else {
        console.log("Invalid option of step. Returning.");
        return;
    }
    document.querySelector("#" + new_id + "Container > div.col > div.stepStuff").innerHTML = inner_elements.trim();

    for (var [id, fun, type] of new_events) {
        addEventListener(id, fun, type);
    }
}

function getClickStepHtml(new_id){
    const [xpath_html, xpath_events] = getXpathHtml("", new_id, "");

    // envent target, function, event type
    var events = [].concat(xpath_events);

    console

    var html = `
        <div class=\"col\">
            <div class=\"row\">
                <div class=\"col\">
                    <strong>Clique em um elemento</strong>
                </div>
                <div class=\"col-3\">
                    id: ${new_id}
                </div>
            </div>
    ` + xpath_html + `
        </div>    
    `;

    return [html, events];
}

function getSelectStepHtml(new_id){
    var is_filled_dynamically = new_id + "IsFilledDynamically";
    var filled_after_step = new_id + "FilledAfterStep";
    var options_to_ignore = new_id + "OptionToIgnore";

    const [xpath_html, xpath_events] = getXpathHtml("", new_id, "");

    // envent target, function, event type
    var events = [
        [is_filled_dynamically, function () {toggleElement(filled_after_step);}, "change"],
    ].concat(xpath_events);

    var html = `
        <div class=\"col\">
            <div class=\"row\">
                <div class=\"col\">
                    <strong>Selecione opção</strong>
                </div>
                <div class=\"col-3\">
                    id: ${new_id}
                </div>
            </div>
            ` + xpath_html + `
            <div class=\"row\">
                <div class=\"col\">
                    <div class=\"custom-control custom-switch\">
                        <input type=\"checkbox\" class=\"custom-control-input\" id=\"${is_filled_dynamically}\">
                        <label class=\"custom-control-label\" for=\"${is_filled_dynamically}\">Preenchido dinamicamente?</label>
                    </div>
                </div>
            </div>
            <div class=\"row\" id=\"${filled_after_step}\" style=\"display: none;\">
                <label class=\"col-4\">
                    <img src=\"icons/corner-down-right.svg\" alt=\"\"> Preenchido depois do passo:
                </label>
                <input type=\"text\" class=\"col-4\" placeholder=\"Step-...-\" id=\"${new_id}FilledAfterStep\">
            </div>
            <div class=\"row\">
                <label class=\"col-3\">
                    <img src=\"icons/corner-down-right.svg\" alt=\"\">
                    Ignorar opções:
                </label>
                <input type=\"text\" class=\"col\" placeholder=\"cidade 1;cidade 2;(...)\" id=\"${options_to_ignore}\">
                <div class="col-1">
                    <span class=\"badge badge-light clickableSpan\">
                        <img src=\"icons/help-circle.svg\" alt=\"Como usar\">
                    </span>
                </div>
            </div>
        </div>   
    `;

    return [html, events];
}

function getSaveTableHtml(new_id){
    var xpath_id = new_id + "XpathInput";
    var save_content_table = new_id + "SaveContentTable";
    var file_name = new_id + "FileName";
    var overwrite_file = new_id + "OverwriteFile";
    var append_to_file = new_id + "AppendToFile";
    
    const [xpath_html, xpath_events] = getXpathHtml(xpath_id, "", "Xpath para tabela");

    // envent target, function, event type
    var events = [
        [xpath_id, function () { askTable(save_content_table, xpath_id); }, "input"],
    ].concat(xpath_events);

    var html = `
        <div class=\"col\">
            <div class=\"row\">
                <div class=\"col\">
                    <strong>Salve a tabela</strong>
                </div>
                <div class=\"col-3\">
                    id: ${new_id}
                </div>
            </div>
            ` + xpath_html + `
            <div class=\"row\">
                <div class=\"col\">
                    Selecione a tabela (tag table no html). As linhas serão casadas usando xpath + "/tbody[1]/tr[1, 2, ...]".
                </div>
            </div>

            <div class=\"row\">
                <div class=\"col\">
                    Preview:
                </div>
            </div>
            <div class=\"row\">
                <div class=\"col\">
                    <div class=\"tableWrapperScrollY my-custom-scrollbar\">
                        <table class=\"table\" id=\"${save_content_table}\">
                        </table>
                    </div>
                </div>
            </div>

            <div class=\"row\">
                <div class=\"col\">
                    <label>Nome do arquivo</label>
                    <input type=\"text\" class=\"form-control\" placeholder=\"./(...)\" id=\"${file_name}\">
                </div>
            </div>

            <div class=\"row\">
                <div class=\"col\">
                    <form>
                        <div class=\"custom-control custom-radio\">
                            <input type=\"radio\" id=\"${overwrite_file}\" name=\"customRadio\" class=\"custom-control-input\" checked>
                            <label class=\"custom-control-label\" for=\"${overwrite_file}\">Sobrescrever arquivo se ja
                                existe</label>
                        </div>
                        <div class=\"custom-control custom-radio\">
                            <input type=\"radio\" id=\"${append_to_file}\" name=\"customRadio\" class=\"custom-control-input\">
                            <label class=\"custom-control-label\" for=\"${append_to_file}\">Adicionar dados ao final do arquivo
                                (se já existir)</label>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    `;
    
    return [html, events];
}

function getIFrameStepHtml(new_id){
    const [xpath_html, xpath_events] = getXpathHtml("", new_id, "");

    // envent target, function, event type
    var events = [].concat(xpath_events);

    var html = `
        <div class=\"col\">
            <div class=\"row\">
                <div class=\"col\"><strong>Mude para o iframe</strong></div>
            </div>
            <div class=\"col-3\">
                id: ${new_id}
            </div>
            ` + xpath_html + `
        </div>    
    `;

    return [html, events];
}

function getDownloadHtml(new_id){
    var folder_address = new_id = "FolderAddress";

    const [xpath_html, xpath_events] = getXpathHtml("", new_id, "");

    // envent target, function, event type
    var events = [].concat(xpath_events);

    var html = `
        <div class=\"col\">
            <div class=\"row\">
                <div class=\"col\">
                    <strong>Baixe o arquivo</strong>
                </div>
                <div class=\"col-3\">
                    id: ${new_id}
                </div>
            </div>
            ` + xpath_html + `
            <div class=\"row\">
                <div class=\"col\">
                    <label>Salvar na pasta</label>
                    <input type=\"text\" class=\"form-control\" placeholder=\"./(...)\" id=\"${folder_address}\">
                </div>
            </div>
        </div>        
    `;

    return [html, events];
}

function getPaginationHtml(new_id){
    const [xpath_htmlNextPageBtn, xpath_eventsNextPageBtn] = getXpathHtml(
        new_id + "NextPageBtn", "", "Xpath para botão de próxima página")
    const [xpath_htmlMaxPagesInfo, xpath_eventsMaxPagesInfo] = getXpathHtml(
        new_id + "MaxPagesInfo", "", "Xpath para número máximo de páginas")

    // envent target, function, event type
    var events = [].concat(xpath_eventsNextPageBtn).concat(xpath_eventsMaxPagesInfo);

    var html = `
        <div class=\"col\">
            <!--  -->
            <div class=\"row\">
                <div class=\"col\">
                    <strong>Para cada página</strong>
                </div>
                <div class=\"col-3\">
                    id: ${new_id}
                </div>
            </div>
            ` + xpath_htmlNextPageBtn + `
            ` + xpath_htmlMaxPagesInfo + `
        </div>
    `;

    return [html, events];
}

function getCaptchaHtml(new_id) {
    const [xpath_html, xpath_events] = getXpathHtml("", new_id, "");

    // envent target, function, event type
    var events = [].concat(xpath_events);

    var html = `
        <div class=\"col\">
            <div class=\"row\">
                <div class=\"col\">
                    <strong>Quebre o captcha</strong>
                </div>

                <div class=\"col-3\">
                    id: ${new_id}
                </div>
            </div>
            ` + xpath_html + `
        </div>
    `;

    return [html, events];
}

function getIfHtml(new_id){
    const [xpath_html, xpath_events] = getXpathHtml("", new_id, "");
    var if_detect = new_id + "IfDetect";
    // envent target, function, event type
    var events = [].concat(xpath_events);

    var html = `
        <div class=\"col\">
            <div class=\"row\">
                <div class=\"col\">
                    <strong>Se detectar elemento</strong>
                </div>

                <div class=\"col-3\">
                    id: ${new_id}
                </div>
            </div>

            <div class=\"row\">
                <div class=\"col\">
                    <div class=\"custom-control custom-switch\">
                        <input type=\"checkbox\" class=\"custom-control-input\" id=\"${if_detect}\">
                        <label class=\"custom-control-label\" for=\"${if_detect}\">
                            Se marcado, funcionará como 'se detectar'. Se não marcado, 'se não detectar'
                        </label>
                    </div>
                </div>
            </div>

            ` + xpath_html + ` 
        </div>
    `;

    return [html, events];
}

function getSaveInfoHtml(new_id) {
    var events = [
        [`${new_id}AddInfoBtn`, function () { // Adds info to be collected
            console.log("AddInfoBtn clicked")
            const select = document.getElementById(`${new_id}AddInfoSelect`);
            const info_type = select.options[select.selectedIndex].value;
            console.log("calling add Info with:", new_id, info_type);
            addInfo(new_id, info_type);
            select.value = "default";
            var btn = document.getElementById(`${new_id}AddInfoBtn`);
            btn.disabled = true;
        }, "click"],
        [`${new_id}AddInfoSelect`, function(){
            // disables 'AddInfoBtn' if value select is the default
            // enables otherwise
            var select = document.getElementById(`${new_id}AddInfoSelect`);
            var btn = document.getElementById(`${new_id}AddInfoBtn`);

            if (select.options[select.selectedIndex].value == "default")
                btn.disabled = true;
            else
                btn.disabled = false;
        }, "change"]
    ];

    var html = `
        <div class=\"col\">
            <div class=\"row\">
                <div class=\"col\">
                    <strong>Salve informações</strong>
                </div>
                <div class=\"col-3\">
                    id: ${new_id}
                </div>
            </div>

            <div class=\"row\">
                <div class=\"col\">
                    <label>Nome do arquivo</label>
                    <input type=\"text\" class=\"form-control\" placeholder=\"./(...)\" id=\"${new_id}FileName\">
                </div>
            </div>

            <div class=\"row\">
                <div class=\"col\">
                    <form>
                        <div class=\"custom-control custom-radio\">
                            <input type=\"radio\" id=\"${new_id}OverwriteFile\" name=\"customRadio\" class=\"custom-control-input\" checked>
                            <label class=\"custom-control-label\" for=\"${new_id}OverwriteFile\">Sobrescrever arquivo se ja
                                existe</label>
                        </div>
                        <div class=\"custom-control custom-radio\">
                            <input type=\"radio\" id=\"${new_id}AppendToFile\" name=\"customRadio\" class=\"custom-control-input\">
                            <label class=\"custom-control-label\" for=\"${new_id}AppendToFile\">Adicionar dados ao final do arquivo
                                (se já existir)</label>
                        </div>
                    </form>
                </div>
            </div>

            <div class=\"row\">
                <div class=\"col\" id=\"${new_id}InfoContainer\">
                    <div class="row" id="${new_id}Dummy"></div>
                </div>
            </div>

            <div class=\"row\" style=\"border-top: 1px dotted gray\">
                <div class=\"col\">
                    Adicionar informação:
                </div>
            </div>
            <div class=\"row\">
                <div class=\"col\">
                    <select class=\"custom-select\" id=\"${new_id}AddInfoSelect\">
                        <option selected value=\"default\">Selecione o tipo de informação</option>
                        <option value=\"href\">href</option>
                        <option value=\"attr\">atributos do elemento</option>
                        <option value=\"txt\">texto do elemento</option>
                    </select>
                </div>
            </div>
            <div class=\"row\">
                <div class=\"col\">
                    <button class=\"btn btn-primary\" type=\"button\" id=\"${new_id}AddInfoBtn\" disabled>Adicionar</button>
                </div>
            </div>
        </div>
    `;

    return [html, events];
}

function getXpathHtml(xpath_id="", new_id="", label=""){
    if(xpath_id == "" && new_id == "")
        throw new InvalidOperationException(errors.InvalidArgumentException );
    else if(xpath_id == "")
        xpath_id = new_id + "XpathInput";

    console.log("getXpathHtml: xpath_id: " + xpath_id);

    if(label == "")
        label = "xpath";

    var events = [
        [xpath_id + "SelectSpanDefault", function () {
            selectXpathSpan(xpath_id + "SelectSpan");
            readXpath(xpath_id); 
        }, "click"],
        [xpath_id + "CopySpan", function () { copyInputText(xpath_id); }, "click"],
    ]

    var html = `
        <!-- begin xpath -->
        <div class=\"row\">
            <div class=\"col\"><label>${label}:</label></div>
        </div>
        <form>
            <div class=\"form-row\">
                <div class=\"col-1\">
                    <span
                        class=\"badge badge-light clickableSpan\"
                        id=\"${xpath_id}SelectSpan\"
                    >
                        <img src=\"{static \'icons/mouse-pointer-gray.svg\'}\" alt=\"Selecionar\" 
                            style=\"display: block; padding: 5px; margin: 0px auto;\"
                            id=\"${xpath_id}SelectSpanDefault\">
                        <img src=\"icons/mouse-pointer-white.svg\" alt=\"Selecionar\" 
                            style=\"display: none; padding: 5px; margin: 0px auto;\" 
                            id=\"${xpath_id}SelectSpanSelected\">
                    </span>
                </div>
                <div class=\"col-6\">
                    <input type=\"text\" class=\"form-control\" placeholder=\"xpath para elemento\" id=\"${xpath_id}\">
                </div>
                <div class=\"col-1\">
                    <button class="btn btn-primary" type="button" id=\"${xpath_id}CopySpan\">Copiar</button>
                </div>
                <div class=\"col-1\">
                    <span class=\"badge badge-light clickableSpan\">
                        <img src=\"icons/help-circle.svg\" alt=\"Como usar\">
                    </span>
                </div>
            </div>
        </form>
        <!-- end xpath -->
    `;

    return [html, events]
}

function genJson() {
    var steps_container = document.getElementById("stepsContainer");
    var steps = steps_container.children;

    var root_step = {
        type: "root",
        depth: 0,
        children: [],
        name: document.getElementById("collectorName").value,
        max_requests_per_seconds: document.getElementById("maxRequestsPerSecond").value,
        rotate_address: document.getElementById("rotateAddress").checked,
        max_requests_per_ip: document.getElementById("maxResquestsPerAddress").value
    };
    var depth_stack = [root_step];
    var stack_top = depth_stack[depth_stack.length - 1];
    for (var step of steps) {
        var step_container_id = step.getAttribute("id");
        if(step_container_id == "stepMenuContainer"){
            continue;
        }
        var depth = getIndentationLevel(step_container_id);
        if (depth > stack_top['depth'] + 1) {
            document.getElementById("configJson").value = "Identação incorreta!!";
            return;
        }
        else while (stack_top.depth >= depth) {
            depth_stack.pop();
            stack_top = depth_stack[depth_stack.length - 1];
        }

        var new_step = getStepConfig(step_container_id);
        new_step["depth"] = depth;
        new_step["id"] = document.querySelector("#" + step_container_id + 
            "> div.col > div.stepStuff.row > div > div:nth-child(1) >" + 
            "div.col-3").textContent.replace("id:", "").trim();
        new_step["children"] = [];

        stack_top.children.push(new_step);
        depth_stack.push(new_step);
        stack_top = depth_stack[depth_stack.length - 1];
    }
    document.getElementById("configJson").value = JSON.stringify(root_step);
}

function copyInputText(){
    // console.log("copying input from " + input_id);
    const el = document.getElementById("configJson");
    el.select();
    document.execCommand('copy');
}