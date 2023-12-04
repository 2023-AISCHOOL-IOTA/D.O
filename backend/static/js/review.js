// 글쓰기 버튼 이벤트 리스너
document.getElementById('writeBtn').addEventListener('click', function() {
    // 글쓰기 모달 표시
    document.getElementById('writeModal').style.display = 'block';
  });
  
  // 모달 닫기 버튼 이벤트 리스너
  document.getElementsByClassName('close')[0].addEventListener('click', function() {
    // 글쓰기 모달 숨기기
    document.getElementById('writeModal').style.display = 'none';
  });
  
 // 현재 시간 함수
function getTime() {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();

    // 시간 형식을 맞추기 위해 0을 추가
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;

    return hours + ':' + minutes;
}

  // 등록하기 버튼 이벤트 리스너
$("#submitBtn").click(function () {
  // 입력 값 가져오기
  var title = document.getElementById("titleInput").value.trim();
  var content = document.getElementById("contentInput").value.trim();
  // 제목과 내용이 있는 경우에만 처리
  if (title && content) {
    var indexNumber = inquiryList.rows.length;
    $.ajax({
      type: "post", // 어떤 방식으로 보낼지
      url: "http:/54.180.129.196/review", // 보낼 주소
      contentType: "application/json", // 서버에 JSON 형식임을 알려줌
      data: JSON.stringify({
        title: title,
        content: content,
        time: getTime(),
        number: indexNumber,
      }), // 데이터를 JSON 문자열로 변환
      // 성공적인 전송시 서버에서 반환된 response 받음
      success: function (response) {
        // 문의 목록 테이블에 행 추가
        var inquiryList = document.getElementById("inquiryList");
        var currentTime = new Date().toLocaleString();
        // 테이블의 현재 행 수를 인덱스 번호로 사용
        var row = inquiryList.insertRow();
        row.insertCell().textContent = indexNumber; // 인덱스 번호 셀 추가
        row.insertCell().textContent = title;
        row.insertCell().textContent = content;
        row.insertCell().textContent = currentTime;
        row.insertCell().textContent = response.user_name; // 기본값으로 '회원' 설정

        // 입력 필드 초기화
        document.getElementById("titleInput").value = "";
        document.getElementById("contentInput").value = "";
        // 모달 닫기
        document.getElementById("writeModal").style.display = "none";
      },
      error: function () {
        alert("다시 시도해주세요");
      },
    });
  }
});
  
  
  // 모달 바깥 영역 클릭 시 모달 닫기
  window.onclick = function(event) {
    if (event.target == document.getElementById('writeModal')) {
      document.getElementById('writeModal').style.display = 'none';
    }
  };
