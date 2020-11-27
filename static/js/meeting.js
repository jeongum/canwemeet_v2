const root = document.getElementById('root');
const meeting_status = document.getElementById('meeting-status');
const meeting_title = document.getElementById('meeting-title');
const start_meeting = document.getElementById('start_meeting');
const end_meeting = document.getElementById('end_meeting');
let connected = false;
let room;
let socket;

function addLocalVideo() {
    Twilio.Video.createLocalVideoTrack().then(track => {
        let video = document.getElementById('local').firstChild;
        let trackElement = track.attach();
        video.appendChild(trackElement);
    });
};

function connectMeetingStatusHandler() {
    if (!connected) {
        let username = usernameInput;
        let roomname = roomnameInput;
        if (!username) {
            alert('Enter your name before connecting');
            return;
        }
        connect(username, roomname).then(() => {
            start_meeting.disabled = false;
            end_meeting.disabled = false;
        }).catch(() => {
            alert('Connection failed. Is the backend running?');
        });
    }
    else {
        disconnect();
        connected = false;
    }
};

function connect(username, roomname) {
    let promise = new Promise((resolve, reject) => {
        // get a token from the back end
        let data;
        fetch('/enter', {
            method: 'POST',
            body: JSON.stringify({'username': username,'roomname': roomname})
        }).then(res => res.json()).then(_data => {
            // join video call
            data = _data;
            return Twilio.Video.connect(data.token);
        }).then(_room => {
            room = _room;
            room.participants.forEach(participantConnected);
            room.on('participantConnected', participantConnected);
            room.on('participantDisconnected', participantDisconnected);
            connected = true;
            updateParticipantCount();
            resolve();
        }).catch(e => {
            console.log(e);
            reject();
        });
    });
    return promise;
};

function updateParticipantCount() {
    if (!connected)
        meeting_status.innerHTML = '대기 중';
    else
        meeting_status.innerHTML = (room.participants.size + 1) + '명 대기 중';
};

function participantConnected(participant) {
    let participantCount = room.participants.size;
    let className = 'participant-' + participantCount;
    let participantClass = document.getElementsByClassName(className);
    let participantDiv = participantClass[0];

    participantDiv.setAttribute('id', participant.sid);

    let tracksDiv = document.createElement('div');
    participantDiv.appendChild(tracksDiv);

    let labelDiv = document.createElement('div');
    labelDiv.setAttribute('class', 'label');
    labelDiv.innerHTML = participant.identity;
    participantDiv.appendChild(labelDiv);
    
    participant.tracks.forEach(publication => {
        if (publication.isSubscribed)
            trackSubscribed(tracksDiv, publication.track);
    });
    participant.on('trackSubscribed', track => trackSubscribed(tracksDiv, track));
    participant.on('trackUnsubscribed', trackUnsubscribed);

    updateParticipantCount();
};

function participantDisconnected(participant) {
    let participantDiv = document.getElementById(participant.sid);

    while(participantDiv.firstChild) {
        participantDiv.removeChild(participantDiv.firstChild);
    }

    participantDiv.setAttribute('id', ' ');
    updateParticipantCount();
};


function trackSubscribed(div, track) {
    let trackElement = track.attach();
    div.appendChild(trackElement);
};

function trackUnsubscribed(track) {
    track.detach().forEach(element => {
        element.remove()
    });
};

function disconnect() {
    room.disconnect();

    let participantDiv = document.getElementById(participant.sid);
    while(participantDiv.firstChild) {
        participantDiv.removeChild(participantDiv.firstChild);
    }

    connected = false;
    updateParticipantCount();
};

// real-time stt

socket = io.connect('http://' + document.domain + ':' + location.port + '/meetingroom');
socket.on('ready', function(){
    SpeechtoText()
});
socket.on('end',function(){
    socket.disconnect()
    location.href='/minute';
});

socket.on('receive_message',function(msg){
    let minute = document.getElementById('minute-content');
    let new_script = document.createElement('article');
    let received_name = decodeURIComponent(msg.name);
    let received_chat = decodeURIComponent(msg.data);

    if(received_name == usernameInput) {
        new_script.setAttribute('class', 'local');

        let new_script_chat = document.createElement('div');
        new_script_chat.setAttribute('class', 'local-chat');
        new_script_chat.innerHTML = received_chat;

        new_script.appendChild(new_script_chat);
    }
    else {
        new_script.setAttribute('class', 'participant');

        let new_script_name = document.createElement('div');
        new_script_name.setAttribute('class', 'participant-name');
        new_script_name.innerHTML = received_name;

        let new_script_chat = document.createElement('div');
        new_script_chat.setAttribute('class', 'participant-chat');
        new_script_chat.innerHTML = received_chat;

        new_script.appendChild(new_script_name);
        new_script.appendChild(new_script_chat);
    }

    minute.appendChild(new_script);

})

function startMeeting(event) {
    start_meeting.disabled = true
    end_meeting.disabled = false
    meeting_status.innerHTML = (room.participants.size + 1) + '명 참여 중';
    socket.emit('before_meeting')
};

function endMeeting(event) {
    end_meeting.disabled = true
    socket.emit('after_meeting')    
};

function SpeechtoText() {
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
        let today = new Date(); 
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        recognition.lang = "ko-KR";
        recognition.start();
        recognition.onresult = function(e) {
            for(let i = e.resultIndex, len = e.results.length; i < len; i++)
                if(e.results[i].isFinal)
                    transcript = e.results[i][0].transcript;
                    socket.emit('send_message', {
                        date:encodeURIComponent(today.toUTCString()),
                        name:encodeURIComponent(usernameInput),
                        data:encodeURIComponent(transcript)
                    })
        };
        recognition.onerror = function(e) {
            recognition.stop();
        }
    }
  }
  
meeting_title.innerHTML = roomnameInput;
connectMeetingStatusHandler();
addLocalVideo();
start_meeting.addEventListener('click', startMeeting);
end_meeting.addEventListener('click', endMeeting);
