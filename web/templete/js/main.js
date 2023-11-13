function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    displayMessage("user", userInput);

    // 서버로 userInput을 전송하고 챗봇의 응답을 받아오는 로직을 추가하세요.
    // 예: fetch('/api/chat', { method: 'POST', body: JSON.stringify({ message: userInput }) })

    // 챗봇의 응답을 표시하는 예제 (임시로 하드코딩)
    var botResponse = "챗봇 응답 예제";
    displayMessage("bot", botResponse);

    // 입력창 초기화
    document.getElementById("user-input").value = "";
}

function displayMessage(sender, message) {
    var chatOutput = document.getElementById("chat-output");
    var newMessage = document.createElement("div");
    newMessage.className = sender;
    newMessage.textContent = message;
    chatOutput.appendChild(newMessage);

    // 스크롤을 항상 아래로 유지
    chatOutput.scrollTop = chatOutput.scrollHeight;
}
