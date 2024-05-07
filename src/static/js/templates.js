var video_feed = document.getElementById('video_feed');
var button = document.getElementById('startStopButton');
var template_name = document.getElementById('template_name');
var system_log = document.querySelector('.system-log-text p');
    function clickStartStopButton() {
        button.click();
    }

    function saveTemplate() {
    var url = '/save_template';
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({name: template_name.value})
            }).then(response => response.json())
                .then(data => {
                    status = data.status;
                    if (status === 'error') {
                        system_log.innerHTML += 'Error saving template ' + template_name.value + '<br>';
                        system_log.innerHTML += 'Add screws to the sequence before saving<br>'
                        system_log.innerHTML += 'Please try again<br>';
                        return;
                    }else if (status === 'success') {
                        system_log.innerHTML += 'Template ' + template_name.value + ' saved successfully<br>';
                        template_name.value = '';
                    }
                });

    }

    button.onclick = function() {
        if (template_name.value === '') {
            alert('Please enter a template name');
            return;
        }
        if (button.innerHTML === 'Start') {
            video_feed.src = "/video_feed";
            button.innerHTML = 'Save';
            system_log.innerHTML += 'Started recording screwing sequence for template ' + template_name.value + '<br>';
            system_log.innerHTML += 'Click on the video feed to record screwing sequence<br>';
            video_feed.removeEventListener('click', clickStartStopButton);

        } else {
            button.innerHTML = 'Start';
            video_feed.src = src="static/images/background.jpg";
            system_log.innerHTML += 'Stopped recording screwing sequence for template ' + template_name.value + '<br>';
            video_feed.addEventListener('click', clickStartStopButton);
            saveTemplate();
            }

        }


    video_feed.addEventListener('click', function(event) {
        if (button.innerHTML === 'Start') {
            return;
        }
        var rect = event.target.getBoundingClientRect();
        var x = parseInt(event.clientX - rect.left);
        //adjust to 640x480 resolution
        x = x / rect.width * 640;
        x = parseInt(x);
        var y = parseInt(event.clientY - rect.top);
        y = y / rect.height * 480;
        y = parseInt(y);
        console.log('x: ' + x + ', y: ' + y);
        var selectedScrew = document.getElementById('screws').value;
        var url = '/coordinates';
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify([x, y, selectedScrew])
        }).then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                system_log.innerHTML += 'Screw No : ' + data + ' at (' + x + ', ' + y + ')<br>';
        });
    });


    window.onload = function() {
    video_feed.addEventListener('click', clickStartStopButton);
    }