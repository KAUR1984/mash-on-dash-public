"use strict";

function addPluginCard(plugin_name, parent_id) {
    // ajax call on data.json file to retrieve the given plugin attributes

    const xhttp = new XMLHttpRequest();

    xhttp.onload = function () {
        const json_response_text = this.responseText;
        console.log("Response: " + json_response_text);
        const json_object = JSON.parse(json_response_text);

        console.log("Parameter plugin name: " + plugin_name.toLowerCase());

        // search for the plugin name in json list of plugins
        for (let i = 0; i < json_object.allPlugins.length; i++) {

            let parameter_plugin = plugin_name.toLowerCase();
            let current_plugin_name = json_object.allPlugins[i].pluginname.toLowerCase();

            console.log("current plugin name in data.json file: " + current_plugin_name)

            if (current_plugin_name === parameter_plugin) {
                // add a new card when clicking on the api links. Workflow btn clicked = 0 as workflow button was not clicked (the api name (link) was clicked)
                let new_plugin_card_id = add_workflow_card(0, false, parent_id, json_object.allPlugins[i]);
                console.log("printing new plugin card id: " + new_plugin_card_id);

                // add the plugin info to the new card
                let plugin_div = document.createElement("div");

                // get the first element of the selected input. Only 1 data source is allowed atm.
                // Might extend the functionality for incorporating multiple input sources in the future. TODO

                let get_first_input_source = 0;

                // document.getElementsByClassName("plugin-name")[get_first_input_source].innerHTML =
                //     json_object.allPlugins[i].pluginname.toString();
                //
                // document.getElementsByClassName("plugin-url")[get_first_input_source].innerHTML =
                //     json_object.allPlugins[i].homePageUrl.toString();
                //
                // document.getElementsByClassName("chosen-plugin-name")[get_first_input_source].innerHTML =
                //     json_object.allPlugins[i].pluginname.toString();

                for (let k = 0; k < json_object.allPlugins[i].methods.length; k++) {

                    let curr_method_object = json_object.allPlugins[i].methods[k];

                    let plugin_job_div = document.createElement("div");
                    plugin_job_div.id = curr_method_object.methodName + "-expand-card-div";
                    plugin_job_div.innerHTML = '<a onclick="expandCard(\'' + curr_method_object.methodName + '\')" class="plugin-card-link row ms-0"><div class="card border mt-2 w-95" style="box-shadow: none"><div class="row ms-0 mt-3"><div class="card col-4 rounded-2 p-0" style="width: 26px; height: 26px; box-shadow: none"><i class="material-icons" style="color: darkslategray; font-size: 25px">expand_more</i></div><div class="text-dark text-md col text-bold">' + toSpacedTitle(curr_method_object.methodName) + '</div></div><div class="text-xs text-dark ms-4 ps-2 pt-1 mb-2">' + curr_method_object.methodDescription + '</div></div></a>';

                    // document.getElementsByClassName(current_plugin_name+"-jobs")[get_first_input_source]
                    //     .append(plugin_job_div);
                    let plugin_card_id = current_plugin_name.replace(/\s/g, '') + "-jobs";
                    console.log("Printing plugin_card_id : " + plugin_card_id);
                    document.getElementById(plugin_card_id).append(plugin_job_div);
                }
            }
        }
    }

    xhttp.open("GET", "http://127.0.0.1:5000/static/data.json", true);
    xhttp.send();
}

let previousPluginMethodName = "";

function expandCard(method_name) {
    let existing_input_field = document.getElementById(method_name + "-input-div");

    if ((previousPluginMethodName !== method_name) && (existing_input_field == null)) {

        let input_div = document.createElement("div");
        input_div.id = method_name + "-input-div";

        // create another ajax call, js function and have the btn and the input, remove the form. and have another ajax TODO
        input_div.innerHTML = '<form class="row align-items-center justify-content-center" method="post" onsubmit="setFlag()" action="http://127.0.0.1:5000/other-pages/create-a-workflow"><div class="form-group border rounded-2 my-4 w-90"><input type="text" required name="' + method_name + '-input-string" class="form-control" placeholder="Input String..."></div></div><div class="row align-content-end justify-content-end"><button type="submit" onclick="setFlag()" class="btn-info mb-3 me-3 w-lg-10 w-md-15 text-center rounded-2">Continue</button></form>';

        document.getElementById(method_name + "-expand-card-div")
            .children.item(0).children.item(0)
            .append(input_div);
    }

    previousPluginMethodName = method_name;
}

function setFlag() {
    console.log("SetFlag() method is being called");
    sessionStorage.setItem("pressed_continue_btn", "true");
}

function toSpacedTitle(input_string) {
    input_string = input_string.split(/(?=[A-Z])/).join(" ");       // split based on capital letters
    console.log(input_string);

    return input_string.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    })
}

// https://stackoverflow.com/questions/4793604/how-to-insert-an-element-after-another-element-in-javascript-without-using-a-lib
function insertAfter(newNode, referenceParentNode) {
    referenceParentNode.parentNode.insertBefore(newNode, referenceParentNode.nextSibling);
}
