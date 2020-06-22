document.addEventListener('DOMContentLoaded',
    function () {
        var crawler_id = document.getElementById("crawler_id").innerText.trim();

        var instance_id = document.getElementById("last_instance_id").innerText.trim();
        if(instance_id == "None")
            return;

        var last_as_running = document.getElementById("instance_running").innerText.trim() == "True";

        if(last_as_running){
            document.getElementById("stderr_tail").innerText = "";
            tail_logs(instance_id);
            setTimeout(() => {
                console.log("last as running. Checking if still running...");
                var text = document.getElementById("stderr_tail").innerText.trim();
                console.log("last log: " + text);

                setTimeout(() => {
                    console.log("10s passed, checking log again...");
                    tail_logs(instance_id);
                    console.log("new log: " + document.getElementById("stderr_tail").innerText.trim());
                    if (text == document.getElementById("stderr_tail").innerText.trim()) {
                        console.log("It is not running anymore.");
                        set_instance_to_not_running(crawler_id, instance_id);
                    }
                    else {
                        console.log("It is still running");
                        set_to_running(crawler_id, instance_id);
                        tail_f_logs(instance_id);
                    }
                }, 5000);
            }, 5000);
        }
        else{
            set_to_not_running(crawler_id);
            tail_logs(instance_id);
        }
    },
    false
);

function tail_logs(instance_id){
    // calls tail log view and set logs
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            if(response["out"].lenght == 0){
                document.getElementById("stdout_tail").innerText = response["out"]
            }
            else{
                document.getElementById("stdout_tail").innerText = "Empty file."
            }
            document.getElementById("stdout_tail_update").innerText = "last update: " + response["time"]
            document.getElementById("stderr_tail").innerText = response["err"]
            document.getElementById("stderr_tail_update").innerText = "last update: " + response["time"]
        }
    };
    xhr.open("GET", "/tail_log_file/" + instance_id, true);
    xhr.send();
}

function tail_f_logs(instance_id){
    console.log("tail_f_logs");
    // Calls tail_logs every 5 seconds
    // setInterval(
    //     function(){ tail_logs(instance_id);},
    //     5000
    // ); 
}

function set_instance_to_not_running(crawler_id, instance_id){
    window.location.replace("/detail/stop_crawl/" + crawler_id + "/" + instance_id);
}

function set_to_not_running(crawler_id){
    document.getElementById("status_badge").innerHTML = `
        Status: <span class="badge badge-warning">Not running</span>    
    `;
    document.getElementById("run_button").innerHTML = "Run";
    document.getElementById("run_button").setAttribute("href", "/detail/run_crawl/" + crawler_id);
    document.getElementById("stop_button").classList.add("disabled");
    document.getElementById("stop_button").innerHTML = "Stop";
} 

function set_to_running(crawler_id, instance_id){
    document.getElementById("status_badge").innerHTML = `
        Status: <span class="badge badge-success">Running</span>    
    `;
    document.getElementById("run_button").innerHTML = "Run";
    document.getElementById("run_button").classList.add("disabled");
    document.getElementById("stop_button").innerHTML = "Stop";
    document.getElementById("stop_button").setAttribute("href", "/detail/stop_crawl/", crawler_id, instance_id);
}
