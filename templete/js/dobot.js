function sendMessage() {
    var userInput = document.getElementById("userInput").value;
    if (userInput.trim() === "") {
      return;
    }

    var chatContainer = document.getElementById("chat-container");

    var userMessage = document.createElement("div");
    userMessage.className = "chat-container";
    userMessage.innerHTML = `
      <div class="user-message">
        <img src="user-image.jpg" alt="User Image" style="width: 30px; height: 30px; border-radius: 50%; margin-right: 10px;">
        <span>사용자 이름</span>
        <p>${userInput}</p>
        <span>보낸 시간</span>
      </div>
    `;
    chatContainer.appendChild(userMessage);

    // 여기에 실제 챗봇에게 메시지를 전송하고 응답을 받는 로직을 추가

    // 응답이 오면 아래의 코드를 사용하여 spinner를 숨깁니다.
    var spinner = document.getElementById("spinner");
    spinner.style.display = "none";

    // 입력창 비우기
    document.getElementById("userInput").value = "";
  }