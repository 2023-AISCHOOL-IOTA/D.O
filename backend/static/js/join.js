

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
        $("#id_check").text("사용 가능한 아이디입니다").css("color", "green");
      },
      error: function () {
        $("#id_check").text("중복된 아이디입니다").css("color", "red");
        $("#username-field").val("");
      },
    });
  }
});

$(document).ready(function () {
  $("#password-field_check, #password-field").on("input", function () {
    let check_pw = $("#password-field_check").val();
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

$("#signup-btn").click(function () {

  let id = $("#username-field").val();
  let password = $("#password-field").val();
  let name = $("#name-field").val();
  let id_check = $("#id_check").text();
  let pww = $("#pw_check").text();

    if (id !== "" && password !== "" && name !== "") {
      if (
        id_check === "사용 가능한 아이디입니다" &&
        pww === "비밀번호가 일치합니다"
      ) {
        $.ajax({
          type: "post",
          url: "http://127.0.0.1:8000/join",
          contentType: "application/json",
          data: JSON.stringify({ id: id, password: password, name: name }),
          success: function (response) {
            window.location.href = "/login";
          },
          error: function () {
            alert("다시 시도해주세요");
            $("#username-field").val("");
            $("#password-field").val("");
            $("#name-field").val("");
            $("#id_check").text("");
            $("#pw_check").text("");
            $("#password-field_check").val("");
          },
        });
      }
      else {
        alert(
          "회원가입 중 오류가 발생했습니다. 아이디 중복 여부와 비밀번호 일치 여부를 확인해주세요."
        );
        $("#username-field").val("");
        $("#password-field").val("");
        $("#name-field").val("");
        $("#id_check").text("");
        $("#pw_check").text("");
        $("#password-field_check").val("");
      }
    }
    else {
      alert("아이디, 비밀번호, 이름을 모두 입력해주세요");
    }
  }
);

$("#name-field").keyup(function (event) {
  if (event.key === "Enter") {
    let id = $("#username-field").val();
    let password = $("#password-field").val();
    let name = $("#name-field").val();
    let id_check = $("#id_check").text();
    let pww = $("#pw_check").text();

    if (id !== "" && password !== "" && name !== "" ) {
      if (
        id_check === "사용 가능한 아이디입니다" &&
        pww === "비밀번호가 일치합니다"
      ) {
        $.ajax({
          type: "post",
          url: "http://127.0.0.1:8000/join",
          contentType: "application/json",
          data: JSON.stringify({ id: id, password: password, name: name }),
          success: function (response) {
            window.location.href = "/login";
          },
          error: function () {
            alert("다시 시도해주세요");
            $("#username-field").val("");
            $("#password-field").val("");
            $("#name-field").val("");
            $("#id_check").text("");
            $("#pw_check").text("");
            $("#password-field_check").val("");
          },
        });
      }
      else {
        alert(
          "회원가입 중 오류가 발생했습니다. 아이디 중복 여부와 비밀번호 일치 여부를 확인해주세요."
        );
        $("#username-field").val("");
        $("#password-field").val("");
        $("#name-field").val("");
        $("#id_check").text("");
        $("#pw_check").text("");
        $("#password-field_check").val("");
      }
    }
    else {
      alert("아이디, 비밀번호, 이름을 모두 입력해주세요");
    }
  }
});