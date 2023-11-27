                                       

$("#id_check-form-submit").click(function () {
  // 입력된 데이터 가져오기

  let id = $("#username-field").val(); // message-input의 값만 가져오기

  if (id !== "") {
    $.ajax({
      type: "post", // 어떤 방식으로 보낼지
      url: "http://127.0.0.1:8000/check", // 보낼 주소
      contentType: "application/json", // 서버에 JSON 형식임을 알려줌
      data: JSON.stringify({ id: id }), // 데이터를 JSON 문자열로 변환
      success: function (response) {
        $("#id_check").text("사용 가능 한 아이디 입니다").css("color", "green");
      },
      error: function () {
        $("#id_check").text("중복된 아이디 입니다").css("color", "red");
        $("#userId").val("");
      },
    });
  }
});

$(document).ready(function () {
  $("#check_password, #password-field").on("input", function () {
    let check_pw = $("#check_password").val();
    let pw = $("#password-field").val();

    if (check_pw !== "" && pw !== "") {
      if (check_pw !== pw) {
        $("#pw_check").text("비밀번호가 일치하지 않습니다").css("color", "red");
      } else {
        $("#pw_check").text("비밀번호가 일치합니다").css("color", "green");
      }
    }
  });
});
