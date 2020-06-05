function showBlock(clicked_id){
    
    var blocks = document.getElementsByClassName('block');
    for (var i = 0; i < blocks.length; i++)
    blocks[i].setAttribute('hidden', true);
    
    var blockId = clicked_id + "-block";
    var block = document.getElementById(blockId);
    block.removeAttribute('hidden');
    
    
    var buttons = document.getElementsByClassName('button-block');
    for (var i = 0; i < buttons.length; i++)
        buttons[i].classList.remove('active');
    document.getElementById(clicked_id).classList.add('active');
}

function submit(){
    document.getElementById("myForm").submit();
}

function detailCaptcha(){
    var mainSelect = document.getElementById("id_captcha");
    const captcha_type = mainSelect.options[mainSelect.selectedIndex].value;
    var captchaDiv = document.getElementById("captchaDiv");
    
    if(captcha_type == "none") captchaDiv.innerHTML = ``
    else if(captcha_type == "image"){
        captchaDiv.innerHTML = `
        <div id="ir_image">
            <br /><label for="img_url" class="requiredField">
                Image URL or Xpath <span class="asteriskField">*</span>
            </label>
            <input class="form-control" name="img_url" id="img_url" type="text" required/>
        </div>
    `;
    } else if(captcha_type == "sound"){
        captchaDiv.innerHTML = `
            <div id="ir_image">
                <br /><label for="sound_url" class="requiredField">
                    Sound URL or Xpath <span class="asteriskField">*</span>
                </label>
                <input class="form-control" name="sound_url" id="sound_url" type="text" required/>
            </div>
        `;
    }
}

function detailIpRotationType(){
    var ipSelect = document.getElementById("ip_type");
    const ip_rotation_type = ipSelect.options[ipSelect.selectedIndex].value;
    var extra_div = document.getElementById("ip_type_div");

    if(ip_rotation_type == 'tor'){
        extra_div.innerHTML = `
        <br /><label for="tor_password" class="requiredField">
            Tor Password<span class="asteriskField">*</span>
        </label>
        <input class="form-control" name="tor_password" id="tor_password" type="text" required/>
        `
    } else {
        extra_div.innerHTML = `
        <br /><label for="proxy_list" class="requiredField">
            Proxy List File<span class="asteriskField">*</span>
        </label>
        <div class="custom-file">
            <input name="proxy_list" type="file" class="custom-file-input" id="proxy_list">
            <label class="custom-file-label" for="proxy_list">Choose file</label>
        </div>
        `
    }
}

function detailAntiblock(){
    var mainSelect = document.getElementById("id_antiblock");
    const antiblock_type = mainSelect.options[mainSelect.selectedIndex].value;
    var antiblockDiv = document.getElementById("antiblockDiv");
    
    if(antiblock_type == "none") antiblockDiv.innerHTML = ``
    if(antiblock_type == "ip"){
        antiblockDiv.innerHTML = `
        <div id="ir_rotation">
            <br /><label for="id_source_name" class="requiredField">
                IP Rotation Type<span class="asteriskField">*</span>
            </label>
            <select class="custom-select" id="ip_type" name="ip_type" onchange=detailIpRotationType()>
                <option value="tor" selected>Tor</option>
                <option value="proxy">Proxy list</option>
            </select>
            <div id="ip_type_div"></div>
            <br /><label for="max_reqs_per_ip" class="requiredField">
                Max requisitions per IP<span class="asteriskField">*</span>
            </label>
            <input class="form-control" name="max_reqs_per_ip" id="max_reqs_per_ip" type="number" required/>
            <br /><label for="max_reuse_rounds" class="requiredField">
                Max reuse rounds<span class="asteriskField">*</span>
            </label>
            <input class="form-control" name="max_reuse_rounds" id="max_reuse_rounds" type="number" required/>
        </div>
        `;
        detailIpRotationType();
    } else if (antiblock_type == "user_agent"){
        
        antiblockDiv.innerHTML = `
        <div id="user_agent">
            <br /><label for="reqs_per_user_agent" class="requiredField">
                Requests per User Agent<span class="asteriskField">*</span>
            </label>
            <input class="form-control" name="reqs_per_user_agent" id="reqs_per_user_agent" type="number" required/>
            <br /><label for="user_agents_file" class="requiredField">
                User Agents File<span class="asteriskField">*</span>
            </label>
            <div class="custom-file">
                <input type="file" class="custom-file-input" name="user_agents_file" id="user_agents_file">
                <label class="custom-file-label" for="user_agents_file">Choose file</label>
            </div>
        </div>
        `;
    } else if(antiblock_type == "delay"){
        
        antiblockDiv.innerHTML = `
        <div id="delay">
            <br /><label for="delay_secs" class="requiredField">
                Delay in seconds<span class="asteriskField">*</span>
            </label>
            <input class="form-control" name="delay_in_secs" id="delay_secs" type="number" required/>
            <br /><div class="form-check form-text">
                <input class="form-check-input" type="radio" name="delay_type" id="random_delay" value="random" checked>
                <label class="form-check-label" for="random_delay">Random delay</label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="delay_type" id="fixed_delay" value="fixed">
                <label class="form-check-label" for="fixed_delay">Fixed delay</label>
            </div>
        </div>
        `;
    } else if(antiblock_type == "cookies"){
        
        antiblockDiv.innerHTML = `
        <div id="cookies">
            <br /><label for="cookies_file" class="requiredField">
                Cookies File<span class="asteriskField">*</span>
            </label>
            <div class="input-group">
                <div class="custom-file">
                    <input type="file" class="custom-file-input" id="cookies_file" name="cookies_file">
                    <label class="custom-file-label" for="cookies_file">Choose file</label>
                </div>
            </div>
            <br /><div class="custom-control custom-checkbox">
                <input type="checkbox" class="custom-control-input" id="persist_cookies" name="persist_cookies">
                <label class="custom-control-label" for="persist_cookies">Persist Cookies</label>
            </div>
        </div>
        `;
    }
}