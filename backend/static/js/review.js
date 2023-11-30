document.addEventListener('DOMContentLoaded', function() {
  const chatWindow = document.getElementById('chat-output');
  const inputField = document.getElementById('chat-input');
  const sendMessageButton = document.getElementById('send-message');
  const endChatButton = document.getElementById('end-chat');
  const loadHistoryButton = document.getElementById('load-history');

  // Send a message when the "Send" button is clicked
  sendMessageButton.addEventListener('click', function() {
    const message = inputField.value;
    chatWindow.innerHTML += `<p>${message}</p>`;
    inputField.value = '';
  });

  // End the chat and save to MongoDB when the "End Chat" button is clicked
  endChatButton.addEventListener('click', function() {
     endChatButton.addEventListener('click', function() {
    const chatContent = chatWindow.innerHTML;
    // AJAX 요청을 통해 채팅 내용을 서버로 보내 저장합니다.
    fetch('/save-chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ chat: chatContent })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Chat saved:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  });

  // Load the chat history when the "Load History" button is clicked
  loadHistoryButton.addEventListener('click', function() {
    // AJAX 요청을 통해 서버로부터 채팅 기록을 불러옵니다.
    fetch('/load-chat-history')
    .then(response => response.json())
    .then(data => {
      chatWindow.innerHTML = ''; // Clear current chat
      data.forEach(chat => {
        chatWindow.innerHTML += `<p>${chat.message}</p>`; // Load each message
      });
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  });
})});