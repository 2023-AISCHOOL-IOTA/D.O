// 채팅창
// 메시지를 추가할때!!
function addMessage(message, sender, id) {
  var chatBody = document.getElementById("chat-body");
  // 요소를 생성할때 div에 넣어서 만든다
  var messageContainer = document.createElement("div");
  var messageSender = document.createElement("div");
  var messageBubble = document.createElement("div");
  var messageTime = document.createElement("div");
  
  var messageName = document.createElement("div");
  // var userImage = document.createElement('div');
  // var chatbotImage = document.createElement('div');

  //TODO - 정연
  var aImage = document.createElement("div");

  // 클래스 생성해준다
  messageContainer.className = "message-container";

  //말풍선이랑 이름 묶을 컨테이너
  messageName.className = "message-name";

  messageBubble.className = "message-bubble";
  messageSender.className = "message-sender";
  messageTime.className = "message-time";
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
  if (sender === "user") {
    messageContainer.classList.add("user-message"); // 보내는 게 user이면 usermessage를 더해준다

    //TODO - 정연
    aaa = "user";
    aImage.innerHTML = `<img src="/static/images/${aaa}.png" alt="${aaa}">`;
  } else {
    messageContainer.classList.add("chatbot-message");

    //TODO - 정연
    aaa = "chatbot";
    aImage.innerHTML = `<img src="/static/images/${aaa}.png" alt="${aaa}">`;
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
  hours = hours < 10 ? "0" + hours : hours;
  minutes = minutes < 10 ? "0" + minutes : minutes;

  return hours + ":" + minutes;
}

// 초기 대화 시작 -> jinja2로 이걸 띄워야 해
setTimeout(function () {
  addMessage("안녕하세요! 어떤 도움이 필요하세요?", "DOBOT");
}, 500);
$("#toyou").click(function () {
  // 입력된 데이터 가져오기

  let inputData = $("#message-input").val(); // message-input의 값만 가져오기
  if (inputData !== "") {
    //  text 변수에 저장

    let text = $(".message-container");

    // text에 append해 요소 추가
    addMessage(inputData, "user");
    text.val("");
    var chatBody = document.getElementById("chat-body");
    chatBody.scrollTop = chatBody.scrollHeight;

    // fastapi의 BaseModel은 JSON 형식을 받는데 그냥 data로 보내면 오류남
    // contentType으로 JSON임을 알려주고 JSON.stringify로 데이터를 JSON으로 변환

    $.ajax({
      type: "post", // 어떤 방식으로 보낼지
      url: "http://127.0.0.1:8000/dobot", // 보낼 주소
      contentType: "application/json", // 서버에 JSON 형식임을 알려줌
      data: JSON.stringify({ data: [inputData, getTime()] }), // 데이터를 JSON 문자열로 변환

      // 성공적인 전송시 서버에서 반환된 response 받음
      success: function (response) {
        // 서버 응답을 성공하면 실행

        addMessage(response.processed_data, "DOBOT");
        
        var chatBody = document.getElementById("chat-body");
        chatBody.scrollTop = chatBody.scrollHeight;
      },

      error: function () {
        alert("실패");
      },
    });

    $("#message-input").val(""); // 입력 필드 새로고침
  }
});

// 엔터시 작동
$("#message-input").keyup(function (event) {
  if (event.key === "Enter") {
    // 입력된 데이터 가져오기

   let inputData = $("#message-input").val(); // message-input의 값만 가져오기
  if (inputData !== "") {
    //  text 변수에 저장

    let text = $(".message-container");

    // text에 append해 요소 추가
    addMessage(inputData, "user");
    var chatBody = document.getElementById("chat-body");
    chatBody.scrollTop = chatBody.scrollHeight;

    // fastapi의 BaseModel은 JSON 형식을 받는데 그냥 data로 보내면 오류남
    // contentType으로 JSON임을 알려주고 JSON.stringify로 데이터를 JSON으로 변환

    $.ajax({
      type: "post", // 어떤 방식으로 보낼지
      url: "http://127.0.0.1:8000/dobot", // 보낼 주소
      contentType: "application/json", // 서버에 JSON 형식임을 알려줌
      data: JSON.stringify({ data: [inputData, getTime()] }), // 데이터를 JSON 문자열로 변환

      // 성공적인 전송시 서버에서 반환된 response 받음
      success: function (response) {
        // 서버 응답을 성공하면 실행

       addMessage(response.processed_data, "DOBOT");
        var chatBody = document.getElementById("chat-body");
        chatBody.scrollTop = chatBody.scrollHeight;
      },

      error: function () {
        alert("실패");
      },
    });

    $("#message-input").val(""); // 입력 필드 새로고침
  }
}});