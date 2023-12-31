function goBack() {
    console.log('뒤로가기 버튼 클릭');
}

// 채팅창
// 메시지를 추가할때!!
function addMessage(message, sender) {
    var chatBody = document.getElementById('chat-body');
    // 요소를 생성할때 div에 넣어서 만든다
    var messageContainer = document.createElement('div');
    var messageSender = document.createElement('div');
    var messageBubble = document.createElement('div');
    var messageTime = document.createElement('div');

    var messageName = document.createElement("div");
    // var userImage = document.createElement('div');
    // var chatbotImage = document.createElement('div');


    //TODO - 정연
    var aImage = document.createElement("div");
    


    // 클래스 생성해준다
    messageContainer.className = 'message-container';

    //말풍선이랑 이름 묶을 컨테이너
    messageName.className = "message-name";

    messageBubble.className = 'message-bubble';
    messageSender.className = 'message-sender';
    messageTime.className = 'message-time';
    // userImage.className = 'user-image';
    // chatbotImage.className = 'chatbot-image';
    
    //TODO - 정연
    aaa = "chatbot";
    aImage.className = `${aaa}-image`;

    // 매개변수 지정
    messageBubble.textContent = message;
    messageSender.textContent = sender;
    messageTime.textContent = getTime(); // 현재 시간을 얻어옴
    
    // 이미지 지정
    // userImage.innerHTML = '<img src="/images/user.png" alt="user">';
    // chatbotImage.innerHTML = '<img src="/images/logo.png" alt="logo">';
    messageName.appendChild(messageSender);
    messageName.appendChild(messageBubble);
    
    // messageContainer에 각 요소들을 넣겠다~
    messageContainer.appendChild(aImage);
    // messageContainer.appendChild(messageBubble);
    // messageContainer.appendChild(messageSender);
    messageContainer.appendChild(messageName);
    messageContainer.appendChild(messageTime);

 
    // messageContainer.appendChild(userImage);

    // 사용자와 챗봇에 따라 클래스를 추가
    if (sender === 'user') {
        messageContainer.classList.add('user-message');  // 보내는 게 user이면 usermessage를 더해준다

        //TODO - 정연
        aaa = "user";    
        aImage.innerHTML = `<img src="/images/${aaa}.png" alt="${aaa}">`;
       
    } else {
        messageContainer.classList.add('chatbot-message');

        //TODO - 정연
        aaa = "chatbot"; 
        aImage.innerHTML = `<img src="/images/${aaa}.png" alt="${aaa}">`;

    }



    // if (sender === 'user') {
    //     chatBody.appendChild(messageContainer);
    // } else {
    //     chatBody.insertBefore(messageContainer, chatBody.firstChild);
    // }

    // (메시지를 보낼때마다) chatBody에 messageContainer를 붙이겠다
    chatBody.appendChild(messageContainer);

    


    // perfect scrollbar
    chatBody.scrollTop = chatBody.scrollHeight;
}

// 현재 시간 함수
function getTime() {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();

    // 시간 형식을 맞추기 위해 0을 추가
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;

    return hours + ':' + minutes;
}
// 로딩이 필요할때 id 가 loading 인 div를 보이게 하고 로딩이 끝나면 감춤

// 입력창
// 메시지를 보낼때 
function sendMessage() {
    var messageInput = document.getElementById('message-input');
    var message = messageInput.value;

    if (message.trim() !== '') {
        addMessage(message, 'user');
        simulateChatbotResponse(message);
        messageInput.value = '';
    }
}

// 사용자의 메시지에 대한 챗봇의 응답을 시뮬레이트 예시
function simulateChatbotResponse(userMessage) {
    var chatbotResponse = (userMessage.includes('안녕') ? '안녕하세요!' : '죄송합니다. 이해하지 못했습니다.'); 
                                              // 삼항연산자이다! 안녕하세요 -> 안녕, 그 외 -> 이해하지 못했습니다.
    addMessage(chatbotResponse, 'DOBOT');
    
}

// Enter 키를 누를 때 sendMessage 함수 호출
document.getElementById('message-input').addEventListener('keyup', function (event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// 초기 대화 시작 -> jinja2로 이걸 띄워야 해
setTimeout(function () {
    addMessage('안녕하세요! 어떤 도움이 필요하세요?', 'DOBOT');
}, 500);
