var video_feed = document.getElementById('video_feed');
var button = document.getElementById('startStopButton');
var dropdown = document.getElementById('templates_dropdown');
var system_log = document.querySelector('.system-log-text p');
    function clickStartStopButton() {
        button.click();
    }

    button.onclick = function() {
        var selected = dropdown.options[dropdown.selectedIndex].value;
        console.log(selected);
        if (selected === 'none') {
            alert('Please select a template');
            return;
        }
        if (button.innerHTML === 'Start') {
            video_feed.src = "/video_feed";
            button.innerHTML = 'Stop';
            dropdown.disabled = true;
            video_feed.removeEventListener('click', clickStartStopButton);

        } else {
            dropdown.disabled = false;
            button.innerHTML = 'Start';
            video_feed.src = src="static/images/background.jpg";
            video_feed.addEventListener('click', clickStartStopButton);
        }
    };

    dropdown.addEventListener('change', function() {
        var selected = dropdown.options[dropdown.selectedIndex].value;
        if (selected === 'Select Template') {
            return;
        }
        var url = '/get_template';
        system_log.innerHTML = 'Template selected: ' + dropdown.options[dropdown.selectedIndex].text + '<br>';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({id: selected})
        }).then(response => response.json())
            .then(data => {
            console.log(data);
                for (var i = 0; i < data.screws.length; i++) {
                    system_log.innerHTML += 'Screw ' + (i + 1) + ': ' + data.screws[i][0] + ', ' + data.screws[i][1] + '<br>';
                }
                system_log.innerHTML += 'Template loaded successfully<br>';
                system_log.innerHTML += 'Please click start to start the sequence<br>';
            });
    });

    //onload fetch templates list from server and populate on the dropdown
    window.onload = function() {
    video_feed.addEventListener('click', clickStartStopButton);
        var url = '/template_list_details';
        fetch(url)
            .then(response => response.json())
            .then(data => {
                while (dropdown.options.length > 1) {
                    dropdown.remove(1);
                }
                var template = document.getElementById('templates');
                if (data.length === 0) {
                    var option = document.createElement('option');
                    option.value = '0';
                    option.text = 'No templates available';
                    option.disabled = true;
                    dropdown.add(option);
                    return;
                }
                for (var i = 0; i < data.length; i++) {
                    var option = document.createElement('option');
                    option.value = data[i].id;
                    option.text = data[i].name;
                    dropdown.add(option);
                }
            });
    };
