document.addEventListener("DOMContentLoaded", function(){

document.querySelector('#message').addEventListener("keyup", function(event) {
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    document.querySelector('#send').click();
    document.querySelector('#messages').scrollTop = document.querySelector('#messages').scrollHeight;
  }
});

var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.emit('join room', {'room': messages.dataset.chatid});
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelector('#send').onclick = () => {
                const messages = document.querySelector('#messages');
                const message = document.querySelector('#message');
                console.log(messages.dataset.chatid)
                socket.emit('message sent', {'message': message.value, 'room': messages.dataset.chatid});
                document.querySelector('#message').value=""
            };
        });

    // When a new vote is announced, add to the unordered list
    socket.on('newMessage', data => {
        const user = document.querySelector("#username").dataset.user
        let message = data.message

        const li = document.createElement('p');
        if(data['user'] == user){
            li.style = "padding-right: 10px;text-align: right;padding-left: 0;"
            li.innerHTML = `${message}`;
        }else if(data['user'] != user && data['user']!=undefined){
            li.style = "color:green"
            message=data['user']+": "+message
            li.innerHTML = `${message}`;
        }else if(data['user']==undefined && data['message'].includes(" has entered the room.") && !data['message'].includes(user)){
            document.querySelector("#newPar").innerHTML = message
            setTimeout(()=>{
                document.querySelector("#newPar").innerHTML=""
            },2000);
        }
        document.querySelector('#messages').append(li);
    });
});