// "use strict";
//
// let number = 2;
// let list_of_cards = [];
//
// // add initial elements
// let card_0 = document.getElementById("card0");         // choose input card
// let card_1 = document.getElementById("card1");         // Processing card
// let card_1000 = document.getElementById("card1000");   // output card, max. 1000 cards are allowed
//
// list_of_cards.push(card_0, card_1, card_1000);
//
// function updateSerialNumber() {
//     let processing_tab_elements = document.getElementsByClassName("processingtab");
//     let counter = 1;
//     for (let i = 0; i < processing_tab_elements.length; i++) {
//         // console.log("Printing processing tab_element id: " + processing_tab_elements[i].id);
//
//         // assign the new id of the current card
//         processing_tab_elements[i].id = "processingtabheading" + counter.toString();
//
//         // insert the serial number for the card; "afterbegin" parameter docs - https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML
//         let card_heading = document.getElementById("processingtabheading" + counter.toString());
//
//         // remove the existing card heading
//         card_heading.innerHTML = "";
//
//         // update the heading with the latest serial number (after adding more cards, serial numbers need to be updated
//         if (processing_tab_elements[i].id === "processingtabheading1") {
//             card_heading.insertAdjacentHTML('afterbegin', counter.toString() + ". Input");
//         } else if (processing_tab_elements[i].id === `processingtabheading${processing_tab_elements.length}`) {
//             card_heading.insertAdjacentHTML('afterbegin', counter.toString() + ". Output");
//         } else {
//             console.log("hi Processing " + processing_tab_elements[i].id);
//             card_heading.insertAdjacentHTML('afterbegin', counter.toString() + ". Processing");
//         }
//         counter++;
//     }
// }
//
// function add_workflow_card(workflow_btn_id) {
//
//     let card = document.createElement("div");
//     let add_workflow_btn = document.createElement("div");
//
//     // empty processing card
//     // card.innerHTML = "<div><div class='row mt-6'> <div class='card' style='background-color: #C7CCD0'> <div class='card-header p-0 pt-0' style='background-color: #C7CCD0'> <h4 class='mb-0'> <div class='row d-inline-flex'> <div class='card' style='background-color: #272628; width:62px; height:52px'> <i class='draw-icon-sizing text-light material-icons opacity-10 mt-1 ms-0 md-light' style='font-size: 40px'>extension</i> </div> <span class='processingtab col mt-2 mb-2' style='color: black'> Processing </span> </div> </h4> </div> </div> </div> <div class='row'> <div class='card min-height-100'></div> </div> </div>";
//
//     // card.innerHTML = '<div id="card1"><div class="row mt-6"><div class="card" style="background-color: #C7CCD0"><div class="card-header p-0 pt-0" style="background-color: #C7CCD0"><h4 class="mb-0"><div class="row d-inline-flex"><div class="card" style="background-color: #272628; width: 62px; height: 52px"><i class="draw-icon-sizing text-light material-icons opacity-10 mt-1 ms-0 md-light" style="font-size: 40px">extension</i></div><span class="processingtab col mt-2 mb-2" style="color: black">Processing</span></div></h4></div></div></div>\n<div class="row "><div class="card min-height-100"><div class="row justify-content-center"><div class="col-md-5 mt-3 mb-4 me-6"><span class="text-bold">Choose from existing plugins:</span><div class="input-group input-group-outline mt-3 mb-3 me-4"><label class="form-label">Search API plugins...</label><input type="text" class="form-control"></div><div class="row"><div class="col">"{% for list_item in first_eight_list_of_default_plugins %}"<li class="row mx-1 mb-1 my-3" style="list-style-type: none"><div class="card rounded-2 p-0" style="width: 22px; height: 22px"><i class="material-icons" style="color: darkslategray">draw</i></div><script>let plugin_name = "{{list_item}}"</script><a class="col text-bold" href="#btn1" onclick="retrievePluginInfo(plugin_name)">"{{ list_item }}"</a></li>"{% endfor %}"</div><div class="col">"{% for list_item in last_eight_list_of_default_plugins %}"<li class="row mx-1 mb-1 my-3" style="list-style-type: none"><div class="card rounded-2 p-0" style="width: 22px; height: 22px"><i class="material-icons" style="color: darkslategray">draw</i></div><script>let plugin_name = "{{list_item}}"</script><a class="col text-bold" href="#btn1" onclick="retrievePluginInfo(plugin_name)">"{{ list_item }}"</a></li>"{% endfor %}"</div></div><span class="row text-sm align-items-center justify-content-center mt-5 font-italic font-weight-light">and "{{number_of_plugins_left}}" more...</span></div><div class="col-md-6 text-bold border-start mt-3 ps-4 mb-3"><span class="ps-4">Choose Input:</span><div class="row min-height-100 mx-4 card mt-3" style="background-color: #F0F2F5"><h6 class="mt-3">1. From API</h6><hr class="mt-0 w-95 ms-2"><span class="ms-2 text-sm">Select APIs from existing plugins:</span><div class="pe-md-3 mt-3 ms-2"><div class="input-group input-group-outline me-4 w-90"><label class="form-label">Search API plugins...</label><input type="text" class="form-control"></div></div><br></div><div class="row min-height-100 mx-4 card my-4" style="background-color: #F0F2F5"><h6 class="mt-3">2. From Local Files</h6><hr class="mt-0 w-95 ms-2"><span class="ms-2 text-sm">Upload files from your local computer:</span><div class="row align-items-center justify-content-center"><label for="file-upload" class="col-sm-5 align-items-center justify-content-center custom-file-upload mt-4 mb-0 text-light bold text-center">Upload</label></div><input id="file-upload1" type="file"/><span class="text-center text-sm mb-3">.csv, .json, .txt</span></div><div class="row min-height-100 mx-4 card my-4" style="background-color: #F0F2F5"><h6 class="mt-3">3. From online database</h6><hr class="mt-0 w-95 ms-2"><span class="ms-2 text-sm">Input URL of the online data source:</span><div class="pe-md-3 mt-3"><div class="input-group input-group-outline ms-2 mb-4 w-90"><label class="form-label">Enter URL...</label><input type="text" class="form-control"></div></div></div></div></div></div></div></div>'
//     // card.innerHTML = '<div id="card1"><div class="row mt-6"><div class="card" style="background-color: #C7CCD0"><div class="card-header p-0 pt-0" style="background-color: #C7CCD0"><h4 class="mb-0"><div class="row d-inline-flex"><div class="card" style="background-color: #272628; width: 62px; height: 52px"><i class="draw-icon-sizing text-light material-icons opacity-10 mt-1 ms-0 md-light" style="font-size: 40px">extension</i></div><span class="processingtab col mt-2 mb-2" style="color: black">Processing</span></div></h4></div></div></div>\n<div class="row "><div class="card min-height-100"><div class="row justify-content-center"><div class="col-md-5 mt-3 mb-4 me-6"><span class="text-bold">Choose from existing plugins:</span><div class="input-group input-group-outline mt-3 mb-3 me-4"><label class="form-label">Search API plugins...</label><input type="text" class="form-control"></div><div class="row"><div class="col">{% for list_item in first_eight_list_of_default_plugins %}<li class="row mx-1 mb-1 my-3" style="list-style-type: none"><div class="card rounded-2 p-0" style="width: 22px; height: 22px"><i class="material-icons" style="color: darkslategray">draw</i></div><script>let plugin_name = "{{list_item}}"</script><a class="col text-bold" href="#btn1" onclick="retrievePluginInfo(plugin_name)">{{ list_item }}</a></li>{% endfor %}</div><div class="col">{% for list_item in last_eight_list_of_default_plugins %}<li class="row mx-1 mb-1 my-3" style="list-style-type: none"><div class="card rounded-2 p-0" style="width: 22px; height: 22px"><i class="material-icons" style="color: darkslategray">draw</i></div><script>let plugin_name = \'{{list_item}}\'</script><a class="col text-bold" href="#btn1" onclick="retrievePluginInfo(plugin_name)">{{ list_item }}</a></li>{% endfor %}</div></div><span class="row text-sm align-items-center justify-content-center mt-5 font-italic font-weight-light">and {{number_of_plugins_left}} more...</span></div><div class="col-md-6 text-bold border-start mt-3 ps-4 mb-3"><span class="ps-4">Choose Input:</span><div class="row min-height-100 mx-4 card mt-3" style="background-color: #F0F2F5"><h6 class="mt-3">1. From API</h6><hr class="mt-0 w-95 ms-2"><span class="ms-2 text-sm">Select APIs from existing plugins:</span><div class="pe-md-3 mt-3 ms-2"><div class="input-group input-group-outline me-4 w-90"><label class="form-label">Search API plugins...</label><input type="text" class="form-control"></div></div><br></div><div class="row min-height-100 mx-4 card my-4" style="background-color: #F0F2F5"><h6 class="mt-3">2. From Local Files</h6><hr class="mt-0 w-95 ms-2"><span class="ms-2 text-sm">Upload files from your local computer:</span><div class="row align-items-center justify-content-center"><label for="file-upload" class="col-sm-5 align-items-center justify-content-center custom-file-upload mt-4 mb-0 text-light bold text-center">Upload</label></div><input id="file-upload1" type="file"/><span class="text-center text-sm mb-3">.csv, .json, .txt</span></div><div class="row min-height-100 mx-4 card my-4" style="background-color: #F0F2F5"><h6 class="mt-3">3. From online database</h6><hr class="mt-0 w-95 ms-2"><span class="ms-2 text-sm">Input URL of the online data source:</span><div class="pe-md-3 mt-3"><div class="input-group input-group-outline ms-2 mb-4 w-90"><label class="form-label">Enter URL...</label><input type="text" class="form-control"></div></div></div></div></div></div></div></div>'
//     card.innerHTML = '<div><div class="row mt-6"><div class="card" style="background-color: #C7CCD0"><div class="card-header p-0 pt-0" style="background-color: #C7CCD0"><h4 class="mb-0"><div class="row d-inline-flex"><div class="card" style="background-color: #272628; width: 62px; height: 52px"><i class="draw-icon-sizing text-light material-icons opacity-10 mt-1 ms-0 md-light" style="font-size: 40px">extension</i></div><span class="processingtab col mt-2 mb-2" style="color: black">Processing</span></div></h4></div></div></div>\n<div class="row "><div class="card min-height-100"><div class="row justify-content-center"><div class="col-md-5 mt-3 mb-4 me-6"><span class="text-bold">Choose from existing plugins:</span><div class="input-group input-group-outline mt-3 mb-3 me-4"><label class="form-label">Search API plugins...</label><input type="text" class="form-control"></div><div class="row"><div class="col">{% for list_item in first_eight_list_of_default_plugins %}<li class="row mx-1 mb-1 my-3" style="list-style-type: none"><div class="card rounded-2 p-0" style="width: 22px; height: 22px"><i class="material-icons" style="color: darkslategray">draw</i></div>  <a class="col text-bold" href="#btn1" onclick="retrievePluginInfo(plugin_name)">{{ list_item }}</a></li>{% endfor %}</div><div class="col">{% for list_item in last_eight_list_of_default_plugins %}<li class="row mx-1 mb-1 my-3" style="list-style-type: none"><div class="card rounded-2 p-0" style="width: 22px; height: 22px"><i class="material-icons" style="color: darkslategray">draw</i></div><a class="col text-bold" href="#btn1" onclick="retrievePluginInfo(plugin_name, -1)">{{ list_item }}</a></li>{% endfor %}</div></div><span class="row text-sm align-items-center justify-content-center mt-5 font-italic font-weight-light">and {{number_of_plugins_left}} more...</span></div><div class="col-md-6 text-bold border-start mt-3 ps-4 mb-3"><span class="ps-4">Choose Input:</span><div class="row min-height-100 mx-4 card mt-3" style="background-color: #F0F2F5"><h6 class="mt-3">1. From API</h6><hr class="mt-0 w-95 ms-2"><span class="ms-2 text-sm">Select APIs from existing plugins:</span><div class="pe-md-3 mt-3 ms-2"><div class="input-group input-group-outline me-4 w-90"><label class="form-label">Search API plugins...</label><input type="text" class="form-control"></div></div><br></div><div class="row min-height-100 mx-4 card my-4" style="background-color: #F0F2F5"><h6 class="mt-3">2. From Local Files</h6><hr class="mt-0 w-95 ms-2"><span class="ms-2 text-sm">Upload files from your local computer:</span><div class="row align-items-center justify-content-center"><label for="file-upload" class="col-sm-5 align-items-center justify-content-center custom-file-upload mt-4 mb-0 text-light bold text-center">Upload</label></div><input id="file-upload1" type="file"/><span class="text-center text-sm mb-3">.csv, .json, .txt</span></div><div class="row min-height-100 mx-4 card my-4" style="background-color: #F0F2F5"><h6 class="mt-3">3. From online database</h6><hr class="mt-0 w-95 ms-2"><span class="ms-2 text-sm">Input URL of the online data source:</span><div class="pe-md-3 mt-3"><div class="input-group input-group-outline ms-2 mb-4 w-90"><label class="form-label">Enter URL...</label><input type="text" class="form-control"></div></div></div></div></div></div></div></div>'
//
//     // add_workflow_btn.innerHTML = "<div class=\"my-0\"><hr class=\"mt-0\" width=\"1\" size=\"70\" style=\"z-index: 0; position: absolute; margin-left: auto; margin-right: auto; text-align: center; left: 0; right: 0;\"><div class=\"text-center align-items-center mt-3\" style=\"z-index: 1; position: absolute; margin-left: auto; margin-right: auto; text-align: center; left: 0; right: 0;\"><a onclick=\"add_workflow_card(number)\"><i class=\"row material-icons justify-content-center opacity-10 text-dark \" style=\"font-size: 35px; fill: black; position: relative\">add_circle</i></a></div></div>";
//     add_workflow_btn.innerHTML = '<div class="my-0"><hr class="mt-0" width="1" size="70" style="z-index: 0; position: absolute; margin-left: auto; margin-right: auto; text-align: center; left: 0; right: 0;"><div class="text-center align-items-center mt-3" style="z-index: 1; position: absolute; margin-left: auto; margin-right: auto; text-align: center; left: 0; right: 0;"><a onclick="add_workflow_card(id_counter)"><i class="row material-icons justify-content-center opacity-10 text-dark " style="font-size: 35px; fill: black; position: relative">add_circle</i></a></div></div>';
//
//
//     card.id = "card" + id_counter;
//     add_workflow_btn.id = "btn" + (id_counter + 1);
//
//     card.append(add_workflow_btn);
//
//     console.log("number: " + id_counter + " Card ID: " + card.id + " Btn Id: " + add_workflow_btn.id);
//     console.log("card+(number-1): card" + (workflow_btn_id-1).toString());
//
//     // document.body.append(card);
//     let curr_parent_card = document.getElementById("card" + (workflow_btn_id-1).toString());
//     curr_parent_card.append(card);
//
//     // add the newest card in between the two cards (where the plus button was clicked)
//     let parent_card_idx = list_of_cards.findIndex(
//         element => element.getAttribute('id') === curr_parent_card.getAttribute('id'));
//
//     // insert the newly card after the parent card
//     list_of_cards.splice(parent_card_idx+1, 0, card);
//     list_of_cards.join();
//
//     // update the serial numbers in front of the cards.
//     updateSerialNumber();
//     list_of_cards.forEach(element => console.log(element));
//
//     id_counter++;
// }