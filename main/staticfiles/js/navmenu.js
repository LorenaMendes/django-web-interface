function defineIcon(section, isValid){
    var sectionId = '#' + section + '-valid-icon';
    if (isValid) {
        $(sectionId).removeClass('fa-warning').addClass('fa-check');
    } else {
        $(sectionId).removeClass('fa-check').addClass('fa-warning');
    }
}

function defineValid(section, subsection1 = '', subsection2 = ''){
    switch(section){
        case 'basic-info':
            if( document.getElementById('id_source_name').value.length > 0 &&
                document.getElementById('id_base_url').value.length > 0
            ) defineIcon(section, true);
            else defineIcon(section, false);
            break;
        case 'antiblock':
            switch(subsection1){
                case 'ip':
                    if(! (document.getElementById('id_max_reqs_per_ip').value.length > 0 &&
                    document.getElementById('id_max_reuse_rounds').value.length > 0)){
                        defineIcon(section, false);
                        return;
                    }
                    
                    var bool = true;
                    switch(subsection2){
                        case 'tor':
                            bool = document.getElementById('id_tor_password').value.length > 0 ? bool&true : bool&false;
                            break;
                        case 'proxy':
                            bool = document.getElementById('id_proxy_list').files.length == 0 ? boo&true : bool&false;
                            break;
                    }
                    defineIcon(section, bool);
                    break;
                case 'user_agent':
                    if( document.getElementById('id_reqs_per_user_agent').value.length > 0
                    && document.getElementById('id_user_agents_file').files.length > 0){
                        defineIcon(section, true);
                    }
                    else defineIcon(section, false);
                    break;
                case 'delay':
                    if( document.getElementById('id_delay_secs').value.length > 0)
                        defineIcon(section, true);
                    else defineIcon(section, false);
                    break;
                case 'cookies':
                    if( document.getElementById('id_cookies_file').files.length > 0){
                        defineIcon(section, true);
                    }
                    else  defineIcon(section, false);
                    break;
            }
            break;
    }

}

$(document).ready(function() {
    
    $('input').on('blur keyup', function() {
        var inputName = $(this).attr('name');
        switch(inputName){
            case 'source_name':
            case 'base_url':
                defineValid('basic-info');
                break;
            case 'tor_password':
                defineValid('antiblock', 'ip', 'tor');
                break;
            case 'proxy_list':
                defineValid('antiblock', 'ip', 'proxy');
                break;
            case 'max_reqs_per_ip':
            case 'max_reuse_rounds':
                defineValid('antiblock', 'ip');
                break;
            case 'reqs_per_user_agent':
            case 'user_agents_file':
                defineValid('antiblock', 'user_agent');
                break;
            case 'delay_secs':
                defineValid('antiblock', 'delay');
                break;
            case 'cookies_file':
                defineValid('antiblock', 'cookies');
                break;

        }

    });
});

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
        
    } else if(captcha_type == "sound"){
        
    }
}

function detailIpRotationType(){
    var ipSelect = document.getElementById("id_ip_type");
    
    const ip_rotation_type = ipSelect.options[ipSelect.selectedIndex].value;
    
    document.getElementById("tor_div").hidden = true;
    document.getElementById("proxy_div").hidden = true;
    
    var id = ip_rotation_type + "_div";
    document.getElementById(id).hidden = false;    
}

function detailAntiblock(){
    var mainSelect = document.getElementById("id_antiblock");
    const antiblock_type = mainSelect.options[mainSelect.selectedIndex].value;

    var contents = document.getElementsByClassName("content-div");
    for (const i in contents)
        contents[i].hidden = true;
    document.getElementById(antiblock_type).hidden = false;

    console.log("tipo: " + antiblock_type);
    defineValid('antiblock', antiblock_type);
}