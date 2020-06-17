// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
    modal.style.display = "none";
    }
}

$(document).on('click', '.confirm-delete', function () {
    $("#confirmDeleteModal").attr("caller-id", $(this).attr("id"));
});

$(document).on('click', '#confirmDeleteButtonModal', function () {
    var caller = $("#confirmDeleteButtonModal").closest(".modal").attr("caller-id");
    window.location = $("#".concat(caller)).attr("href");
});

function defineIcon(section, isValid){
    var sectionId = '#' + section + '-valid-icon';
    if (isValid) {
        $(sectionId).removeClass('fa-warning').addClass('fa-check');
    } else {
        $(sectionId).removeClass('fa-check').addClass('fa-warning');
    }
    enableCreateButton();
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
                case 'none':
                    defineIcon(section, true);
                    break;
                case 'ip':
                    if(! (document.getElementById('id_max_reqs_per_ip').value.length > 0 &&
                    document.getElementById('id_max_reuse_rounds').value.length > 0)){
                        defineIcon(section, false);
                        return;
                    }
                    
                    var bool = true;
                    switch(subsection2){
                        case 'proxy':
                            bool = document.getElementById('id_proxy_list').value.length == 0 ? boo&true : bool&false;
                            break;
                    }
                    defineIcon(section, bool);
                    break;
                case 'user_agent':
                    if( document.getElementById('id_reqs_per_user_agent').value.length > 0
                    && document.getElementById('id_user_agents_file').value.length > 0){
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
                    if( document.getElementById('id_cookies_file').value.length > 0){
                        defineIcon(section, true);
                    }
                    else  defineIcon(section, false);
                    break;
            }
            break;
        case 'captcha':
            var isValid = true;
            if(document.getElementById("id_has_webdriver").checked && document.getElementById("id_webdriver_path").value.length <= 0){
                defineIcon(section, false);
                break;
            }
            switch(subsection1){
                case 'image':
                    isValid = document.getElementById('id_img_xpath').value.length > 0;
                    break;
                case 'sound':
                    isValid = document.getElementById('id_sound_xpath').value.length > 0;
                    break;
            }
            defineIcon(section, isValid);
            break;
    }

}

function enableCreateButton(){
    var blocks = document.getElementsByClassName('valid-icon');
    var isValid = true;
    for(var i=0; i< blocks.length; i++){
        if(blocks[i].classList.contains('fa-warning')){
            isValid = false;
            break;
        }
    }
    
    var button = document.getElementById('createButton');
    if(button.classList.contains('list-group-item-valid') && !isValid){
        button.classList.remove('list-group-item-valid');
        button.classList.add('list-group-item-invalid');
    } else if(isValid){
        button.classList.remove('list-group-item-invalid');
        button.classList.add('list-group-item-valid');
    }

}

function setNavigation(){
    var path = window.location.pathname;
    path = path.replace(/\/$/, "");
    path = decodeURIComponent(path);
    
    $(".navbar-nav li a").each(function () {
        var href = $(this).attr('href');
        if (path.substring(0, href.length) === href) {
            $(this).closest('li').addClass('active');
        }
    });
}

$(document).ready(function() {    
    setNavigation();
    
    $('input').on('blur keyup', function() {
        var inputName = $(this).attr('name');
        switch(inputName){
            case 'source_name':
            case 'base_url':
                defineValid('basic-info');
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
            case 'img_xpath':
                defineValid('captcha', 'image');
                break;
            case 'sound_xpath':
                defineValid('captcha', 'sound');
                break;
            case 'webdriver_path':
                defineValid('captcha');
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

function detailWebdriverType(){
    var webdriverBool = document.getElementById("id_has_webdriver");
    document.getElementById("webdriver_path_div").hidden = !webdriverBool.checked;
    
}

function detailCaptcha(){
    var mainSelect = document.getElementById("id_captcha");
    const captcha_type = mainSelect.options[mainSelect.selectedIndex].value;
    
    document.getElementById('webdriver').hidden = captcha_type == 'none' ? true : false;

    var contents = document.getElementsByClassName("content-div");
    for (const i in contents)
        contents[i].hidden = true;
    document.getElementById(captcha_type).hidden = false;
    
    defineValid('captcha', captcha_type);
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
    
    defineValid('antiblock', antiblock_type);
}

function detailCrawlerType(){
    var mainSelect = document.getElementById("id_crawler_type");
    const crawler_type = mainSelect.options[mainSelect.selectedIndex].value;
    
    var contents = document.getElementsByClassName("content-div");
    for (const i in contents)
        contents[i].hidden = true;
    document.getElementById(crawler_type).hidden = false;
    
    defineValid('crawler_type', crawler_type);
}

function runScript(id) {
    $.ajax({
        url: '../manage_crawl/' + id, //The URL you defined in urls.py
        success: function(data) {
          //If you wish you can do additional data manipulation here.
          
        }

    });
}

function runDelete(id) {
    $.ajax({
        url: '../../delete/' + id, //The URL you defined in urls.py
        success: function(data) {
          //If you wish you can do additional data manipulation here.
          
        }

    });
}
