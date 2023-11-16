function addMessage(message, sender) {
  var chatBody = document.getElementById("chat-body");
  var messageContainer = document.createElement("div");
  var messageBubble = document.createElement("div");
  var messageSender = document.createElement("div");
  var messageTime = document.createElement("div");
  var botContainer = document.getElementById("first");
  messageContainer.className = "message-container";
  messageBubble.className = "message-bubble";
  messageSender.className = "message-sender";
  messageTime.className = "message-time";

  messageBubble.textContent = message;
  messageSender.textContent = sender;
  // 현재 시간을 얻어옴

  messageContainer.appendChild(messageBubble);
  messageContainer.appendChild(messageSender);
  messageContainer.appendChild(messageTime);

  // 시간을 나타내는 요소를 생성해서 메시지 컨테이너에 추가합니다.
  var timeElement = document.createElement("div");
  timeElement.className = "message-time";
  timeElement.textContent = getTime();
  messageContainer.appendChild(timeElement);

  var botContainer = document.getElementById("bot");

  if (botContainer) {
    // 'bot' 아이디를 가진 div 태그가 존재하는 경우
    botContainer.classList.add("user-message");
    // 해당 div 태그에 'user-message' 클래스를 추가합니다.
  } else {
    messageContainer.classList.add("chatbot-message");
  }
  chatBody.appendChild(messageContainer);

  chatBody.scrollTop = chatBody.scrollHeight;
}
function getTime() {
  var now = new Date();
  var hours = now.getHours();
  var minutes = now.getMinutes();

  // 시간 형식을 맞추기 위해 0을 추가
  hours = hours < 10 ? "0" + hours : hours;
  minutes = minutes < 10 ? "0" + minutes : minutes;

  return hours + ":" + minutes;
}

// 초기 대화 시작
setTimeout(function () {
  addMessage("안녕하세요! 어떤 도움이 필요하세요?", "DOBOT");
}, 500);
// 버튼 클릭 이벤트 처리
$("#toyou").click(function () {
  // 입력된 데이터 가져오기

  let inputData = $("#message-input").val(); // message-input의 값만 가져오기
  if (inputData !== "") {
    //  text 변수에 저장

    let text = $(".message-container");

    // text에 append해 요소 추가
    text.append(
      '<div class = "message-bubble" id = "user" >' +
        "<div class='user-message'>" +
        inputData +
        "</div>" +
        "</div>" +
        "<div class = 'message-sender'id = 'u2'>" +
        "나" +
        "</div>" +
        "<div class ='message-time' id = 'u' >" +
        getTime() +
        "</div>"
    );

    // fastapi의 BaseModel은 JSON 형식을 받는데 그냥 data로 보내면 오류남
    // contentType으로 JSON임을 알려주고 JSON.stringify로 데이터를 JSON으로 변환

    $.ajax({
      type: "post", // 어떤 방식으로 보낼지
      url: "http://127.0.0.1:8000/dobot", // 보낼 주소
      contentType: "application/json", // 서버에 JSON 형식임을 알려줌
      data: JSON.stringify({ data: inputData }), // 데이터를 JSON 문자열로 변환

      // 성공적인 전송시 서버에서 반환된 response 받음
      success: function (response) {
        // 서버 응답을 성공하면 실행

        text.append(
          '<div class = "message-bubble" id = "bot">' +
            "<div class='bot-message'>" +
            response.processed_data +
            "</div>" +
            "</div>" +
            "<div class = 'message-sender'>" +
            "DOBOT" +
            "</div>" +
            "<div class ='message-time' id = 'time'>" +
            getTime() +
            "</div>"
        );
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
      text.append(
        '<div class = "message-bubble" id = "user" >' +
          "<div class='user-message'>" +
          inputData +
          "</div>" +
          "</div>" +
          "<div class = 'message-sender'id = 'u2'>" +
          "나" +
          "</div>" +
          "<div class ='message-time' id = 'u' >" +
          getTime() +
          "</div>"
      );

      // fastapi의 BaseModel은 JSON 형식을 받는데 그냥 data로 보내면 오류남
      // contentType으로 JSON임을 알려주고 JSON.stringify로 데이터를 JSON으로 변환

      $.ajax({
        type: "post", // 어떤 방식으로 보낼지
        url: "http://127.0.0.1:8000/dobot", // 보낼 주소
        contentType: "application/json", // 서버에 JSON 형식임을 알려줌
        data: JSON.stringify({ data: inputData }), // 데이터를 JSON 문자열로 변환

        // 성공적인 전송시 서버에서 반환된 response 받음
        success: function (response) {
          // 서버 응답을 성공하면 실행

          text.append(
            '<div class = "message-bubble" id = "bot">' +
              "<div class='bot-message'>" +
              response.processed_data +
              "</div>" +
              "</div>" +
              "<div class = 'message-sender'>" +
              "DOBOT" +
              "</div>" +
              "<div class ='message-time' id = 'time'>" +
              getTime() +
              "</div>"
          );
        },

        error: function () {
          alert("실패");
        },
      });

      $("#message-input").val(""); // 입력 필드 새로고침
    }
  }
});
