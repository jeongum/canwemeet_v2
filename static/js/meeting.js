const root = document.getElementById('root');
const meeting_status = document.getElementById('meeting-status');
const meeting_title = document.getElementById('meeting-title');
const start_stt = document.getElementById('start_stt');
const end_stt = document.getElementById('end_stt');
let connected = false;
let room;

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
            start_stt.disabled = false;
            end_stt.disabled = false;
        }).catch(() => {
            alert('Connection failed. Is the backend running?');
        });
    }
    else {
        disconnect();
        start_stt.disabled = true;
        end_stt.disabled = true;
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

meeting_title.innerHTML = roomnameInput;
addLocalVideo();
connectMeetingStatusHandler();