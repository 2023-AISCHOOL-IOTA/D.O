$("#toyou").click(function () {
  // 입력된 데이터 가져오기

  let inputData = $("#login").val(); // message-input의 값만 가져오기
  let inputpassword = $("#password").val();
  if (inputData !== "" && inputpassword !== "") {
    $.ajax({
      type: "post", // 어떤 방식으로 보낼지
      url: "http://127.0.0.1:8000/login", // 보낼 주소
      contentType: "application/json", // 서버에 JSON 형식임을 알려줌
      data: JSON.stringify({ login: [inputData, inputpassword] }), // 데이터를 JSON 문자열로 변환
      success: function (response) {
        alert(response.message);       
        window.location.href = "/dobot";
      },
      error: function () {
        alert("다시 시도해주세요");
        $("#login").val("");
        $("#password").val("");
      },
    });
  }
});
                    