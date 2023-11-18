$("#toyou").click(function () {
  // 입력된 데이터 가져오기

  let id = $("#login").val(); // message-input의 값만 가져오기
  let password = $("#password").val();
  let name = $("#name").val();
  if (id !== "" && password !== "" && name !== "") {
    $.ajax({
      type: "post", // 어떤 방식으로 보낼지
      url: "http://127.0.0.1:8000/join", // 보낼 주소
      contentType: "application/json", // 서버에 JSON 형식임을 알려줌
      data: JSON.stringify({ id: id, password: password, name: name }), // 데이터를 JSON 문자열로 변환
      success: function (response) {
        alert("회원가입이 완료 되었습니다");
        window.location.href = "/login";
      },
      error: function () {
        alert("다시 시도해 주세요");
        $("#login").val("");
        $("#password").val("");
        $("#name").val("");
      },
    });
  }
});
