function login() {
    var userId = document.getElementById("userId").value;

    if (userId === "") {
        alert("Please enter your ID.");
    } else {
        // 여기에 로그인 처리 로직을 추가하세요.
        // 예를 들면, 서버에 AJAX 요청을 보내서 로그인 여부를 확인할 수 있습니다.
        console.log("Login successful for user ID: " + userId);
    }
}

function signup() {
    // 여기에 회원가입 처리 로직을 추가하세요.
    console.log("Redirect to signup page.");
}


