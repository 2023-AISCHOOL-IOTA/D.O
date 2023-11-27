// 페이지 로드 시 챗봇의 첫 메시지를 추가합니다.
document.addEventListener("DOMContentLoaded", function () {
  addChatMessage("Bot", "무엇을 도와드릴까요?", getTime());
  toggleSpinner(false); // 스피너 비활성화
});



// 이미지를 생성하고 설정하는 함수
function addImage(imgPath, altText) {
  var img = document.createElement("img"); // 새 이미지 요소 생성
  img.src = imgPath; // 이미지 경로 설정
  img.alt = "Bot Avatar"; // 대체 텍스트 설정
  img.classList.add("avatar"); // CSS 클래스 추가

  return img; // 생성된 이미지 요소 반환
}

// 이미지를 생성하고 설정하는 함수
function addImage(imgPath, altText) {
  var img = document.createElement("img"); // 새 이미지 요소 생성
  img.src = imgPath;  
  img.alt = altText;
  img.classList.add("avatar"); // CSS 클래스 추가
  console.log(imgPath);

  return img; // 생성된 이미지 요소 반환
}
// 스피너 토글 함수입니다.
function toggleSpinner(show) {
  var spinner = document.querySelector(".spinner-container");
  spinner.style.display = show ? "flex" : "none"; // 스피너 표시 상태 설정
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

// 사용자가 메시지를 보낼 때 실행됩니다.
function sendUserMessage() {
  var input = document.getElementById("chat-input");
  var message = input.value.trim();
  if (message !== "") {
    addChatMessage("User", message, getTime());
    input.value = "";
    toggleSpinner(true); // 사용자가 메시지를 보낼 때 스피너 활성화
    // 챗봇의 답변을 시뮬레이션합니다.
  
  }
}


// 채팅창에 메시지 요소를 추가하는 함수입니다.
function addChatMessage(sender, text, time) {
  var chatBox = document.getElementById("chat-box");
  var messageWrapper = document.createElement("div");
  messageWrapper.classList.add(
    "chat-message",
    sender.toLowerCase() + "-message"
  );

  // var avatarImg = document.createElement('img');
  // avatarImg.classList.add('avatar');
  // avatarImg.src = sender === "Bot" ? "chatbot.png" : "user.png";

   // 이미지 요소를 생성하는 함수 호출
  var imgPath =
    sender === "Bot" ? "/static/images/chatbot.png" : "/static/images/user.png"; // 이미지 파일 경로와 대체 텍스트
  var altText = sender === "Bot" ? "Bot Avatar" : "User Avatar";
  var avatarImg = addImage(imgPath, altText);

  var senderName = document.createElement("div");
  senderName.classList.add("sender-name");
  senderName.textContent = sender;

  var chatBubble = document.createElement("div");
  chatBubble.classList.add("chat-bubble");
  chatBubble.textContent = text;

  var timestamp = document.createElement("div");
  timestamp.classList.add("timestamp");
  timestamp.textContent = time;

  if (sender === "User") {
    messageWrapper.appendChild(timestamp);
    messageWrapper.appendChild(chatBubble);
    messageWrapper.appendChild(senderName);
    messageWrapper.appendChild(avatarImg);
  } else {
    messageWrapper.appendChild(avatarImg);
    messageWrapper.appendChild(senderName);
    messageWrapper.appendChild(chatBubble);
    messageWrapper.appendChild(timestamp);
  }

  chatBox.appendChild(messageWrapper);
 // chatBox.scrollTop = chatBox.scrollHeight;
}
  $("#send-btn").click(function () {
    // 입력된 데이터 가져오기

    let inputData = $("#chat-input").val(); // message-input의 값만 가져오기
    if (inputData !== "") {
      //  text 변수에 저장

      let text = $(".message-container");

      // text에 append해 요소 추가
      sendUserMessage();
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

          addChatMessage("Bot", response.processed_data, getTime());
          

          var chatBody = document.getElementById("chat-body");
          chatBody.scrollTop = chatBody.scrollHeight;
          
        },
        
          

        error: function () {
          alert("실패");
          
        },
      });

      $("#chat-input").val(""); // 입력 필드 새로고침
    }
  });

  // 엔터시 작동
  $("#chat-input").keyup(function (event) {
    if (event.key === "Enter") {
      // 입력된 데이터 가져오기

      let inputData = $("#chat-input").val(); // message-input의 값만 가져오기
      if (inputData !== "") {
        //  text 변수에 저장

        let text = $(".message-container");

        // text에 append해 요소 추가
        sendUserMessage();
        var chatBody = document.getElementById("chat-body");
        //chatBody.scrollTop = chatBody.scrollHeight;

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

            addChatMessage("Bot", response.processed_data, getTime());
            var chatBody = document.getElementById("chat-body");
            chatBody.scrollTop = chatBody.scrollHeight;
            
          },
          beforeSend: function () {
           
          },

          error: function () {
            alert("실패");
            
          },
        });

        $("#chat-input").val(""); // 입력 필드 새로고침
      }
    }
  });